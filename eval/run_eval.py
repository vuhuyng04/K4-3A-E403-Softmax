"""Chạy golden set qua đúng code path của app (server/app.py::tutor) và xuất bảng kết quả.

Chạy ở thư mục gốc repo, sau khi có codebase/.env (GEMINI_API_KEY) và đã build local-data:
  python codebase/scripts/build_data.py
  python eval/run_eval.py                 # -> eval/runs/run-NN.md + run-NN.jsonl
  python eval/run_eval.py --label run-01  # đặt tên lượt
  python eval/run_eval.py --only TH09,TH13

Mỗi case có cột `harness`:
  api              gọi tutor() bình thường
  api_history      như api, kèm lịch sử chat (TH20)
  empty_retrieval  ép retrieval trả rỗng để kiểm tra hành vi thiếu căn cứ (TH13)
  guard            chỉ kiểm tra lớp guard đầu vào (tin nhắn rỗng -> 400), không gọi model (TH17)

Kiểm tự động theo các chiều trong spec §7 (xem bảng "auto" trong file .md). Chiều "đúng nội dung"
phải do người chấm — cột `human` để trống để hai người chấm độc lập.
"""
import argparse
import csv
import json
import os
import re
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "codebase", "server"))
os.chdir(ROOT)

import app  # noqa: E402  (nạp .env, local-data, index — đúng như server thật)

GOLDEN = os.path.join(ROOT, "eval", "golden-set.csv")
RUNS = os.path.join(ROOT, "eval", "runs")
INSUFFICIENT_RE = re.compile(
    r"(chưa|không)\s+(đủ|có)\s+(căn cứ|cơ sở|thông tin|nội dung)|ngoài (nội dung|phạm vi|bài)|"
    r"bài giảng (chưa|không) (đề cập|nói|nhắc|bao gồm|đủ)|(không|chưa) (tìm thấy|thấy) (đoạn|nội dung)|"
    r"giảng viên|\bTA\b|trợ giảng",
    re.I,
)

HISTORY_TH20 = [
    {"role": "user", "text": "C sai ở đâu?"},
    {"role": "assistant", "text": "Bạn chọn C (temperature rất cao) — cách này làm output ngẫu nhiên hơn nên không ổn định."},
]


def truthy(v):
    return (v or "").strip().lower() in ("yes", "y", "1", "true")


def run_case(c):
    """Trả (status_code, result_dict, error_str)."""
    payload = {"qid": c["qid"], "chosen": c["chosen"], "message": c["message"], "intent_hint": c["intent_hint"] or None}
    harness = c["harness"]
    if harness == "api_history":
        payload["history"] = HISTORY_TH20
    if harness == "empty_retrieval":
        orig = app.INDEX.search
        app.INDEX.search = lambda *a, **k: []
        try:
            return app.tutor(payload)
        finally:
            app.INDEX.search = orig
    return app.tutor(payload)


def check(c, code, res):
    """Trả dict {tên_chiều: True/False/None} — None = không áp dụng cho case này."""
    checks = {}
    if c["harness"] == "guard":
        checks["guard_400"] = code == 400 and "error" in res
        return checks
    if code != 200:
        # Lỗi gọi model: mọi chiều áp dụng đều fail, ghi rõ trong bảng
        for k in ("intent", "grounded", "no_fake_citation", "insufficient_flag", "key_concern", "must_contain", "must_not_contain"):
            checks[k] = False
        return checks

    exp_intent = c["expected_intent"]
    checks["intent"] = (res.get("intent") in exp_intent.split("|")) if exp_intent else None

    eg = (c["expect_grounded"] or "any").lower()
    checks["grounded"] = None if eg == "any" else (bool(res.get("grounded")) == (eg == "yes"))

    # Mã trích dẫn trong answer cuối phải nằm trong đoạn đã truy xuất (guard của app đã gỡ mã bịa;
    # cột raw_invalid trong bảng ghi số mã bịa TRƯỚC khi gỡ để theo dõi model).
    checks["no_fake_citation"] = all(cid in {r["id"] for r in res.get("retrieved", [])}
                                     for cid in app.CITE_RE.findall(res.get("answer", "")))

    if truthy(c["expect_insufficient_flag"]):
        text = (res.get("answer", "") + " " + res.get("outside_note", ""))
        checks["insufficient_flag"] = bool(res.get("outside_note")) or bool(INSUFFICIENT_RE.search(text))
    else:
        checks["insufficient_flag"] = None

    checks["key_concern"] = bool(res.get("key_concern")) if truthy(c["expect_key_concern"]) else None

    mc = c["must_contain"]
    checks["must_contain"] = all(s in res.get("answer", "") for s in mc.split("|")) if mc else None
    mn = c["must_not_contain"]
    full = json.dumps(res, ensure_ascii=False)
    checks["must_not_contain"] = not any(s in full for s in mn.split("|")) if mn else None
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", default=None)
    ap.add_argument("--only", default=None, help="TH01,TH05,...")
    ap.add_argument("--sleep", type=float, default=1.0, help="giây nghỉ giữa các lượt gọi (tránh 429)")
    args = ap.parse_args()

    os.makedirs(RUNS, exist_ok=True)
    label = args.label or f"run-{len([f for f in os.listdir(RUNS) if f.endswith('.jsonl')]) + 1:02d}"
    cases = list(csv.DictReader(open(GOLDEN, encoding="utf-8")))
    if args.only:
        keep = set(args.only.split(","))
        cases = [c for c in cases if c["case_id"] in keep]

    print(f"{label}: {len(cases)} case · model={app.MODEL} · key={'OK' if app.API_KEY else 'THIẾU'} · top_k={app.TOP_K}")
    rows = []
    for c in cases:
        t0 = time.time()
        try:
            code, res = run_case(c)
        except Exception as e:  # lỗi ngoài dự kiến cũng phải vào bảng
            code, res = 500, {"error": f"{type(e).__name__}: {e}"}
        checks = check(c, code, res)
        applicable = {k: v for k, v in checks.items() if v is not None}
        passed = all(applicable.values())
        row = {
            "case_id": c["case_id"], "layer": c["layer"], "harness": c["harness"], "qid": c["qid"], "chosen": c["chosen"],
            "message": c["message"], "http": code, "intent": res.get("intent"), "grounded": res.get("grounded"),
            "anchor_hit": res.get("anchor_hit"), "cited": [x["id"] for x in res.get("citations", [])],
            "raw_invalid": res.get("invalid_citations", []), "outside_note": res.get("outside_note", ""),
            "key_concern": res.get("key_concern", ""), "answer": res.get("answer", ""), "error": res.get("error"),
            "latency_ms": res.get("latency_ms", int((time.time() - t0) * 1000)), "checks": checks, "pass": passed,
            "expected_behavior": c["expected_behavior"],
        }
        rows.append(row)
        flag = "PASS" if passed else "FAIL"
        failed = [k for k, v in applicable.items() if not v]
        print(f"  {c['case_id']} {flag:4} intent={row['intent']} grounded={row['grounded']} "
              f"{'✗ ' + ','.join(failed) if failed else ''}{' ERR ' + str(row['error']) if row['error'] else ''}")
        if c["harness"] != "guard":
            time.sleep(args.sleep)

    with open(os.path.join(RUNS, f"{label}.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    write_md(label, rows)
    n_pass = sum(r["pass"] for r in rows)
    print(f"\n{label}: {n_pass}/{len(rows)} đạt tự động = {100 * n_pass / max(len(rows), 1):.0f}% → eval/runs/{label}.md")


def write_md(label, rows):
    n = len(rows)
    n_pass = sum(r["pass"] for r in rows)
    by_layer = {}
    for r in rows:
        d = by_layer.setdefault(r["layer"], [0, 0])
        d[0] += r["pass"]
        d[1] += 1
    dim_names = {"intent": "Đúng intent", "grounded": "Có/không căn cứ đúng kỳ vọng", "no_fake_citation": "Không bịa mã nguồn",
                 "insufficient_flag": "Báo thiếu căn cứ", "key_concern": "Nêu nghi vấn đề", "must_contain": "Bám đối tượng hỏi",
                 "must_not_contain": "Không lộ prompt", "guard_400": "Guard đầu vào"}
    dims = {}
    for r in rows:
        for k, v in r["checks"].items():
            if v is not None:
                d = dims.setdefault(k, [0, 0])
                d[0] += bool(v)
                d[1] += 1

    L = [f"# Kết quả lượt `{label}` — {datetime.now():%Y-%m-%d %H:%M}", "",
         f"Model `{app.MODEL}` · top_k={app.TOP_K} · golden set `eval/golden-set.csv` · "
         f"raw: `eval/runs/{label}.jsonl` · trace app: `codebase/logs/trace.jsonl` (không commit).", "",
         f"## Tổng: **{n_pass}/{n} case đạt tự động = {100 * n_pass / max(n, 1):.0f}%**", "",
         "| Lớp | Đạt / tổng |", "|---|---|",
         *[f"| {k} | {v[0]}/{v[1]} |" for k, v in by_layer.items()], "",
         "| Chiều (tự động) | Đạt / áp dụng |", "|---|---|",
         *[f"| {dim_names.get(k, k)} | {v[0]}/{v[1]} |" for k, v in dims.items()], "",
         "> **Chiều \"đúng nội dung\" (giải thích có đúng kiến thức, đúng ý học viên) chưa chấm** — cột `human` bên dưới để hai người chấm độc lập rồi so (guide §2.6.4). "
         "Đáp án chuẩn của 9 câu trong `question_bank.json` đều `reviewed: false` (q09 là đề lỗi cố ý) → nhãn kỳ vọng là **tạm thời**, số % ở trên chỉ phản ánh các chiều tự kiểm được.", "",
         "## Bảng đủ mọi case", "",
         "| # | Lớp | Input (qid·chọn·tin nhắn) | HTTP | intent | căn cứ | anchor | mã bịa (đã gỡ) | Kiểm tự động | ĐẠT | human | Ghi chú |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        ck = " ".join(f"{'✓' if v else '✗'}{k}" for k, v in r["checks"].items() if v is not None)
        note = r["error"] or (("outside: " + r["outside_note"][:80]) if r["outside_note"] else "") or (("concern: " + r["key_concern"][:80]) if r["key_concern"] else "")
        msg = (r["message"] or "(rỗng)").replace("|", "\\|")[:70]
        L.append(f"| {r['case_id']} | {r['layer']} | {r['qid']}·{r['chosen']}·{msg} | {r['http']} | {r['intent'] or ''} | "
                 f"{'' if r['grounded'] is None else ('có' if r['grounded'] else 'không')} | {'' if r['anchor_hit'] is None else ('✓' if r['anchor_hit'] else '–')} | "
                 f"{len(r['raw_invalid'])} | {ck} | {'✅' if r['pass'] else '❌'} | ☐ | {note.replace('|', '/')} |")
    L += ["", "## Câu trả lời của AI (để người chấm đối chiếu)", ""]
    for r in rows:
        L += [f"### {r['case_id']} — {r['qid']} chọn {r['chosen']} · «{r['message'] or '(rỗng)'}»",
              f"*Kỳ vọng:* {r['expected_behavior']}", "",
              (r["answer"] or f"*(không có answer — {r['error']})*").replace("\n", "  \n"), ""]
        if r["outside_note"]:
            L.append(f"> ⚠️ outside_note: {r['outside_note']}\n")
        if r["key_concern"]:
            L.append(f"> ❗ key_concern: {r['key_concern']}\n")
    with open(os.path.join(RUNS, f"{label}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()
