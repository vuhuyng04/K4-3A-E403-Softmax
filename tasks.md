# Phân công công việc — Nhóm Softmax · K4-3A-E403 · Track A2

Lát cắt: *Học viên nộp câu trả lời bài tập buổi N → AI chấm đúng / một phần / sai kèm trích dẫn transcript → học viên biết chỗ hiểu sai.*

| Thành viên | Vai trò | Khối điểm chịu trách nhiệm chính |
|---|---|---|
| **Huy** (đội trưởng) | Spec & Product Lead · Demo | R2 (15) · R3 (11) · R6 (8) · R7 (3) · 25 điểm nộp CP |
| **Thiên** | Evidence & Research | R1 (15) |
| **Phong** | Prompt & Eval | R4 (15) |
| **Sơn** | Build & Prototype | R5 (8) |

Nguyên tắc: **ai có tên ở đâu phải giải thích được phần đó** (giám khảo hỏi bất kỳ ai). Mọi người đọc `spec.md` bản cuối trước CP6.

---

## Lịch & việc theo checkpoint

### 16/9 — CP1 19:30 · Canvas + repo ✅ đã xong

| Ai | Việc | Trạng thái |
|---|---|---|
| Huy | Repo, README, TEAMMATES, canvas.md, nộp form CP1 | ✅ |
| Huy | Điền email/Discord/SĐT vào `TEAMMATES.md` | ⬜ |

### 16/9 — CP2 21:00 · Cho thấy luồng hoạt động

| Ai | Việc | Output |
|---|---|---|
| **Sơn** | Dựng khung app: chọn buổi → hiện 1 bài tập → ô nhập câu trả lời → nút "Chấm" → khung kết quả (verdict · giải thích · trích dẫn). Chưa cần AI thật, trả kết quả cứng | `codebase/` chạy được local, flow bấm hết được |
| **Huy** | Vẽ sơ đồ luồng 1 trang (user → app → AI → kết quả, nhánh "không đủ căn cứ") + chốt stack với Sơn; nộp form CP2 | `codebase/flow.png` hoặc mermaid trong `codebase/README.md` |
| **Thiên** | Đọc `data/README.md` + `DATA_DICTIONARY.md`; đọc 30–50 mẫu chatlog K4 để nhận diện pattern "xin bài tập / nhờ kiểm tra / hỏi có hiểu đúng không"; định nghĩa tiêu chí đếm | Ghi chú tiêu chí đếm vào `eval/evidence-method.md` |
| **Phong** | Chọn 1 buổi học (transcript có mã đoạn) làm buổi demo; soạn 5–8 bài tập tự luận ngắn từ transcript, mỗi bài kèm đáp án mẫu + mã đoạn căn cứ | `codebase/data/exercises.json` |
| **Cả nhóm** | Mỗi người 15': dùng thử 1 sản phẩm tương tự (ChatGPT study mode · Khanmigo · Quizlet AI · NotebookLM) — trả lời 4 câu guide §2.2 | Gửi Huy để ghi spec §3 |

### 17/9 — CP3 16:00 · AI thật + đo lượt đầu (làm trong LEC + tự làm)

| Ai | Việc | Output |
|---|---|---|
| **Phong** | Viết prompt chấm bài: input = câu hỏi + đáp án mẫu + đoạn transcript liên quan + câu trả lời học viên; output JSON `{verdict, explanation, citations[], confidence}`; luật "không có căn cứ → verdict = `insufficient_evidence`" | `codebase/prompts/grader.md` |
| **Phong** | Golden set ≥20 case trong `eval/golden-set.csv`: cột `id · exercise_id · student_answer · expected_verdict · difficulty_class(①②③④/normal/rare) · source(chatlog id / tự viết)`. Cơ cấu: 8–10 thường · ≥2 mỗi lớp ①②③④ · 2–4 hiếm · ≥10 lấy/phát triển từ chatlog thật | `eval/golden-set.csv` |
| **Sơn** | Nối AI thật vào nút "Chấm" (API key qua `.env`, không commit); lưu trace log mỗi lượt (input, prompt, output, thời gian) vào `codebase/logs/`; script chạy golden set tự động | `codebase/` Working ở quyết định trung tâm · `eval/run_eval.py` |
| **Sơn** | Quay video 30s: bấm thật, AI trả kết quả thật | `eval/cp3-demo.mp4` (hoặc link) |
| **Phong + Sơn** | Chạy lượt đo 1 trên golden set; bảng `case · input · output · đạt?` | `eval/run-01.md` với % |
| **Thiên** | Đếm trên 3.097 lượt K4 theo tiêu chí đã định; trích ≥5 quote nguyên văn (ghi mã hội thoại, không dán dài); khảo sát ≥20 học viên giờ nghỉ với câu Mom Test, log từng câu trả lời | `eval/evidence-mining.md` · `eval/survey-log.md` |
| **Huy** | Viết spec §1 (từ Thiên) · §4 lát cắt, non-goals, automation, §4b ≥4 nguyên tắc HAX/PAIR · §5 kịch bản lỗi ≥8 (chạy HAX Playbook) · §6 bốn đường đi; nộp form CP3 | `spec.md` §1, §4–§6 |

### 17/9 — CP4 21:00 · Chốt spec + quality bar (không sửa sau mốc này)

| Ai | Việc | Output |
|---|---|---|
| **Phong** | Chốt định nghĩa "đạt" từng chiều (verdict đúng nhãn · trích dẫn đúng đoạn · không bịa ngoài transcript) và **quality bar bằng số** — chốt TRƯỚC khi xem kết quả lượt 2 | `spec.md` §7 |
| **Thiên** | Bảng impact ≥3 ứng viên (bao nhiêu người × tần suất × tốn gì) + ứng viên đã loại + lý do chọn bằng số | `spec.md` §2 |
| **Huy** | Ghép spec hoàn chỉnh §1–§9, tự khai phần chưa xong, review chéo với cả nhóm; nộp form CP4 | `spec.md` gần cuối |
| **Sơn** | Sửa prototype theo case fail lượt 1 (UI báo "chưa đủ căn cứ", loading, hiển thị trích dẫn bấm được) | `codebase/` |
| **Phong** | Lượt đo 2 sau khi sửa prompt; ghi changelog | `eval/run-02.md` · `spec.md` §9 |

### 18/9 sáng — CP5 13:00 · Slide + video dự phòng + validation

| Ai | Việc | Output |
|---|---|---|
| **Huy** | Slide 6 trang theo guide §5.1 (pain+evidence · lát cắt · demo · kết quả đo vs bar · user thật nói gì · backlog) → PDF; nộp form CP5 | `demo-slides.pdf` |
| **Sơn** | Quay video demo dự phòng đúng kịch bản sẽ demo trên sân khấu; dry run 1 lần | `validation/backup-demo.mp4` (hoặc link) |
| **Huy + Thiên** | Vòng validation: 5 người ngoài nhóm (gồm Lương Quang Huy, Hà Mạnh Tuân), giao task "làm bài tập buổi N và xem kết quả chấm", ngồi im quan sát, chép quote nguyên văn | `validation/log.md` (bảng: người thử · task · quan sát · quote · mức nghiêm trọng) + 4 dòng tổng hợp |
| **Sơn + Phong** | ≥1 thay đổi từ feedback validation → ghi §9 changelog; lượt đo cuối | `eval/run-final.md` · `spec.md` §9 |
| **Cả nhóm** | Mỗi người 1 file reflection | `reflection/<tên>.md` |

### 18/9 — CP6 17:30 · Thuyết trình (6' cụm / 10' chung kết)

| Ai | Phần nói |
|---|---|
| **Thiên** | Pain + bằng chứng (số đếm + quote) · bảng impact |
| **Huy** | Lát cắt · thiết kế · automation · kịch bản lỗi |
| **Sơn** | Demo live (video dự phòng sẵn sàng) · 1 case lỗi live |
| **Phong** | Kết quả đo vs quality bar · phân tích case fail · user thật nói gì |
| **Huy** | Backlog + kết luận · điều phối Q&A (giám khảo chạy 1 case lạ tại chỗ — Sơn thao tác, Phong giải thích verdict) |

---

## Việc xuyên suốt

| Ai | Việc |
|---|---|
| Huy | Nộp đúng hạn 5 form bằng MSSV 2A202602662; theo dõi giờ; ghi §9 changelog mỗi khi đổi gì |
| Sơn | Không commit `data/`, API key; giữ `codebase/README.md` ghi rõ mock/thật + cách chạy |
| Phong | Không sửa quality bar sau CP4; số đo ghi trung thực kể cả thấp |
| Thiên | Trích dẫn data: mã hội thoại thay vì dán nguyên văn dài; không suy ngược danh tính |
