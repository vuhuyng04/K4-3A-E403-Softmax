"""Dựng dữ liệu local cho app từ data pack (không commit kết quả).

Đọc:
  data/vlearn-pack/transcript/transcript-0*-clean.md  -> các đoạn [Txx-NNN]
  data/vlearn-pack/chatlog/tutor_turns.csv            -> đề + đáp án của câu quiz thật
  codebase/question_bank.json                         -> danh sách turn_id + đáp án chuẩn (nhóm duyệt)
Ghi:
  codebase/local-data/segments.json
  codebase/local-data/questions.json

Chạy:  python codebase/scripts/build_data.py
"""
import csv
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PACK = os.path.join(ROOT, "data", "vlearn-pack")
CODEBASE = os.path.join(ROOT, "codebase")
OUT = os.path.join(CODEBASE, "local-data")

SEG_RE = re.compile(r"\*\*\[(T\d{2}-\d{3})\]\*\*\s*(.+?)(?=\n\s*\n|\Z)", re.S)
HEAD_RE = re.compile(r"^(#{1,2})\s+(.+)$", re.M)
SECTION_PREFIX = re.compile(r"^\(Đang học phần “(.+?)” của buổi này\)\s*")


def build_segments():
    segments = []
    files = sorted(glob.glob(os.path.join(PACK, "transcript", "transcript-0*-clean.md")))
    if not files:
        sys.exit(f"Không thấy transcript trong {PACK}/transcript — kiểm tra lại thư mục data/")
    for path in files:
        text = open(path, encoding="utf-8").read()
        tid = "T" + re.search(r"transcript-(\d{2})", path).group(1)
        title = text.splitlines()[0].lstrip("# ").replace("Transcript bài giảng (bản sạch) — ", "")
        heads = [(m.start(), m.group(2).strip()) for m in HEAD_RE.finditer(text) if m.group(1) == "##"]
        for m in SEG_RE.finditer(text):
            section = ""
            for pos, h in heads:
                if pos < m.start():
                    section = h
                else:
                    break
            segments.append({
                "id": m.group(1),
                "transcript": tid,
                "lecture_title": title,
                "section": section,
                "text": " ".join(m.group(2).split()),
            })
    return segments


def parse_question(raw):
    """Tách đề và các lựa chọn từ câu học viên dán vào tutor.

    Mỗi lựa chọn là một khối bắt đầu bằng dòng chỉ có chữ cái (A, B, C...) theo đúng thứ tự.
    Chỉ lấy dòng đầu sau chữ cái — các dòng sau là nhãn của nền tảng ("Đáp án đúng",
    "Bạn đã chọn", gợi ý) hoặc câu học viên gõ thêm.
    """
    body = SECTION_PREFIX.sub("", raw).strip()
    blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", body) if b.strip()]
    stem, options, expected = [], {}, "A"
    for b in blocks:
        lines = b.split("\n")
        if lines[0].strip() == expected and len(lines) > 1:
            options[expected] = lines[1].strip()
            expected = chr(ord(expected) + 1)
        elif not options:
            stem.append(b)
        else:
            break
    return "\n\n".join(stem).strip(), options


def build_questions():
    bank = json.load(open(os.path.join(CODEBASE, "question_bank.json"), encoding="utf-8"))
    rows = {}
    with open(os.path.join(PACK, "chatlog", "tutor_turns.csv"), encoding="utf-8") as f:
        wanted = {q["turn_id"] for q in bank["questions"]}
        for r in csv.DictReader(f):
            if r["turn_id"] in wanted:
                rows[r["turn_id"]] = r
    questions = []
    for q in bank["questions"]:
        r = rows.get(q["turn_id"])
        if not r:
            print(f"  ! bỏ qua {q['id']}: không thấy {q['turn_id']} trong chatlog")
            continue
        stem, options = parse_question(r["student_question"])
        if q["key"] not in options:
            print(f"  ! {q['id']}: đáp án chuẩn {q['key']} không có trong các lựa chọn {list(options)}")
        questions.append({**q, "stem": stem, "options": options,
                          "section": SECTION_PREFIX.match(r["student_question"]).group(1),
                          "lecture_title": r["lecture_title"]})
    return questions


def main():
    os.makedirs(OUT, exist_ok=True)
    segments = build_segments()
    json.dump(segments, open(os.path.join(OUT, "segments.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    by_t = {}
    for s in segments:
        by_t[s["transcript"]] = by_t.get(s["transcript"], 0) + 1
    print(f"segments.json: {len(segments)} đoạn {by_t}")

    questions = build_questions()
    seg_ids = {s["id"] for s in segments}
    for q in questions:
        missing = [a for a in q.get("anchors", []) if a not in seg_ids]
        if missing:
            print(f"  ! {q['id']}: anchor không tồn tại {missing}")
    json.dump(questions, open(os.path.join(OUT, "questions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"questions.json: {len(questions)} câu")
    for q in questions:
        print(f"  {q['id']} {q['turn_id']} {q['lecture']} key={q['key']} options={''.join(q['options'])} | {q['stem'][:70]!r}")


if __name__ == "__main__":
    main()
