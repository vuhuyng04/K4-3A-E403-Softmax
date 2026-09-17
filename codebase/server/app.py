"""Server local cho VLearn AI Tutor (dữ liệu thật + Gemini).

Chạy:
  python codebase/scripts/build_data.py   # một lần, sau khi có data/
  python codebase/server/app.py           # mở http://localhost:8000
"""
import json
import os
import re
import sys
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODEBASE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from llm import LLMError, generate_json  # noqa: E402
from prompts import RESPONSE_SCHEMA, SYSTEM, build_user_prompt  # noqa: E402
from retrieval import Index  # noqa: E402

CITE_RE = re.compile(r"\[(T\d{2}-\d{3})\]")


def load_env(path):
    env = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    keys = ("GEMINI_API_KEY", "GEMINI_MODEL", "OPENAI_API_KEY", "OPENAI_MODEL", "PORT", "TOP_K")
    return {**{k: os.environ[k] for k in keys if k in os.environ}, **env}  # .env ưu tiên hơn biến môi trường


ENV = load_env(os.path.join(CODEBASE, ".env"))
# Có OPENAI_API_KEY thì dùng OpenAI, không thì Gemini.
PROVIDER = "openai" if ENV.get("OPENAI_API_KEY") else "gemini"
API_KEY = ENV.get("OPENAI_API_KEY") or ENV.get("GEMINI_API_KEY", "")
MODEL = ENV.get("OPENAI_MODEL", "gpt-4.1-mini") if PROVIDER == "openai" else ENV.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
PORT = int(ENV.get("PORT", "8000"))
TOP_K = int(ENV.get("TOP_K", "8"))

LOCAL = os.path.join(CODEBASE, "local-data")
try:
    SEGMENTS = json.load(open(os.path.join(LOCAL, "segments.json"), encoding="utf-8"))
    QUESTIONS = {q["id"]: q for q in json.load(open(os.path.join(LOCAL, "questions.json"), encoding="utf-8"))}
except FileNotFoundError:
    sys.exit("Chưa có codebase/local-data/. Chạy trước: python codebase/scripts/build_data.py")
BANK = json.load(open(os.path.join(CODEBASE, "question_bank.json"), encoding="utf-8"))
INDEX = Index(SEGMENTS)
LOG_DIR = os.path.join(CODEBASE, "logs")
os.makedirs(LOG_DIR, exist_ok=True)


def trace(record):
    with open(os.path.join(LOG_DIR, "trace.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def public_question(q):
    return {k: q[k] for k in ("id", "turn_id", "lecture", "lecture_title", "section", "stem", "options", "reviewed")} | {
        "hard_case": q.get("hard_case")}


def tutor(payload):
    q = QUESTIONS.get(payload.get("qid"))
    chosen = payload.get("chosen")
    message = (payload.get("message") or "").strip()[:1000]
    if not q or chosen not in q["options"] or not message:
        return 400, {"error": "Thiếu câu hỏi, đáp án đã chọn hoặc tin nhắn."}
    if not API_KEY:
        return 500, {"error": "Chưa có OPENAI_API_KEY hoặc GEMINI_API_KEY trong codebase/.env."}

    transcripts = BANK["lecture_transcripts"].get(q["lecture"])
    query = " ".join([q["stem"], *q["options"].values(), q["options"][chosen], message])
    segs = INDEX.search(query, transcripts, k=TOP_K)
    allowed = {s["id"] for s in segs}

    user = build_user_prompt(q, chosen, segs, message, payload.get("intent_hint"), payload.get("history") or [])
    t0 = time.time()
    try:
        out, usage = generate_json(API_KEY, MODEL, SYSTEM, user, RESPONSE_SCHEMA, provider=PROVIDER)
    except LLMError as e:
        trace({"at": datetime.now().isoformat(timespec="seconds"), "qid": q["id"], "chosen": chosen,
               "message": message, "error": str(e)})
        return 502, {"error": str(e)}
    latency = int((time.time() - t0) * 1000)

    answer = out.get("answer", "")
    cited = list(dict.fromkeys(CITE_RE.findall(answer)))
    invalid = [c for c in cited if c not in allowed]
    for c in invalid:
        answer = answer.replace(f"[{c}]", "")
    valid = [c for c in cited if c in allowed]
    by_id = {s["id"]: s for s in segs}
    result = {
        "intent": out.get("intent"),
        "answer": answer,
        "outside_note": out.get("outside_note", ""),
        "key_concern": out.get("key_concern", ""),
        "severity": out.get("severity", []),
        "citations": [{k: by_id[c][k] for k in ("id", "section", "text", "lecture_title")} for c in valid],
        "invalid_citations": invalid,
        "grounded": bool(valid),
        "anchor_hit": bool(set(valid) & set(q.get("anchors", []))),
        "retrieved": [{"id": s["id"], "score": s["score"], "section": s["section"]} for s in segs],
        "latency_ms": latency,
        "model": MODEL,
        "tokens": {"in": usage.get("promptTokenCount"), "out": usage.get("candidatesTokenCount")},
    }
    trace({"at": datetime.now().isoformat(timespec="seconds"), "qid": q["id"], "turn_id": q["turn_id"],
           "chosen": chosen, "key": q["key"], "intent_hint": payload.get("intent_hint"), "message": message,
           **{k: result[k] for k in ("intent", "answer", "outside_note", "key_concern", "severity", "invalid_citations",
                                     "grounded", "anchor_hit", "latency_ms", "model", "tokens")},
           "cited": valid, "retrieved": [s["id"] for s in segs]})
    return 200, result


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self):
        n = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(n).decode("utf-8") or "{}")
        except ValueError:
            return {}

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            with open(os.path.join(CODEBASE, "app", "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if path == "/api/health":
            return self._send(200, {"provider": PROVIDER, "model": MODEL, "has_key": bool(API_KEY), "segments": len(SEGMENTS),
                                    "questions": len(QUESTIONS), "top_k": TOP_K})
        if path == "/api/questions":
            return self._send(200, [public_question(q) for q in QUESTIONS.values()])
        return self._send(404, {"error": "Không tìm thấy"})

    def do_POST(self):
        payload = self._json()
        if self.path == "/api/submit":
            q = QUESTIONS.get(payload.get("qid"))
            if not q or payload.get("chosen") not in q["options"]:
                return self._send(400, {"error": "Câu hỏi hoặc đáp án không hợp lệ."})
            return self._send(200, {"key": q["key"], "correct": payload["chosen"] == q["key"],
                                    "key_source": q["key_source"]})
        if self.path == "/api/tutor":
            return self._send(*tutor(payload))
        return self._send(404, {"error": "Không tìm thấy"})

    def log_message(self, fmt, *args):
        if "/api/" in (args[0] if args else ""):
            print(f"[{datetime.now():%H:%M:%S}] {args[0]} -> {args[1]}")


if __name__ == "__main__":
    print(f"VLearn AI Tutor · {PROVIDER} · model={MODEL} · key={'OK' if API_KEY else 'THIẾU — điền vào codebase/.env'}")
    print(f"{len(SEGMENTS)} đoạn transcript · {len(QUESTIONS)} câu hỏi · top_k={TOP_K}")
    print(f"Mở http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
