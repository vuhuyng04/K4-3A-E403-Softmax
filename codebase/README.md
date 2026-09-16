# codebase/

Prototype của nhóm Softmax — AI Tutor giải thích câu trắc nghiệm sau khi học viên nộp bài. Không commit API key — dùng `codebase/.env` (đã ignore).

## 1. Bản chạy thật — `app/` + `server/` (CP3)

Dữ liệu thật từ `data/vlearn-pack/` + gọi Gemini thật. **Chỉ chạy local** — không publish vì chứa transcript và đề quiz của khoá.

```bash
# 1. Dựng dữ liệu local (cần thư mục data/ ở gốc repo)
python codebase/scripts/build_data.py

# 2. Điền GEMINI_API_KEY vào codebase/.env (mẫu: codebase/.env.example)

# 3. Chạy server (chỉ dùng thư viện chuẩn Python 3.10+, không cần pip install)
python codebase/server/app.py
# mở http://localhost:8000
```

| Thành phần | File | Thật / Mock |
|---|---|---|
| Transcript bài giảng (700 đoạn `[Txx-NNN]`) | `scripts/build_data.py` → `local-data/segments.json` | **Thật** — 6 transcript sạch của BTC |
| Câu trắc nghiệm (9 câu) | `question_bank.json` (chỉ mã) → `local-data/questions.json` | **Thật** — đề + lựa chọn trích từ chatlog K4 (học viên dán vào tutor), mã nguồn `turn_id` |
| Đáp án chuẩn | `question_bank.json` → `key`, `key_source` | **Nhóm dựng lại** từ nhãn nền tảng / câu trả lời tutor VLearn — `reviewed: false` = chưa duyệt |
| Ghép buổi học ↔ transcript | `question_bank.json` → `lecture_transcripts` | **Nhóm tự đánh giá** (D01 → T04, T06 · D03 → T05, T01, T02, T03) |
| Truy xuất đoạn liên quan | `server/retrieval.py` (BM25, top-k) | Thật |
| Giải thích + phân loại intent | `server/prompts.py`, `server/llm.py` | **Gọi Gemini thật**, JSON có schema |
| Kiểm tra trích dẫn | `server/app.py` | Thật — trích dẫn không nằm trong đoạn đã truy xuất bị gỡ và ghi `invalid_citations` |
| Trace log | `logs/trace.jsonl` (ignored) | Thật — mỗi lượt: input, output, trích dẫn, anchor_hit, latency, tokens |

Case khó có sẵn: `q07` (có thể không có trong transcript), `q09` (đề lỗi: tập nucleus là {A,B,C} nhưng mỗi lựa chọn chỉ 1 token).

## 2. Bản mock — `prototype/index.html` (CP2)

Mở trực tiếp bằng trình duyệt. Toàn bộ transcript, câu hỏi, câu trả lời AI là dữ liệu nhóm tự soạn; có chế độ "Demo từng bước".
