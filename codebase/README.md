# codebase/

Prototype của nhóm Softmax. Ghi rõ phần nào **mock**, phần nào gọi AI thật. Không commit API key — dùng `.env` (đã ignore).

## `prototype/index.html` — mock luồng (CP2)

Mở trực tiếp bằng trình duyệt. Luồng: chọn đáp án trắc nghiệm → nộp → mở khóa AI Tutor → hỏi 3 loại câu (đáp án đúng · đáp án sai ở đâu · mở rộng/so sánh) → bấm trích dẫn `Buổi 5 · Đn` để xem đoạn transcript.

| Phần | Trạng thái |
|---|---|
| Transcript Buổi 5, 3 câu hỏi, đáp án chuẩn | **Mock** — nhóm tự soạn, không phải data thật |
| Câu trả lời của AI Tutor | **Mock** — soạn sẵn theo từng loại câu hỏi |
| Nhận diện loại câu hỏi khi tự gõ | **Mock** — bắt từ khóa đơn giản |
| Nhánh từ chối (prompt injection, xin đáp án câu khác) và nhánh "chưa đủ căn cứ" | **Mock** — minh họa hành vi mong muốn |
| Gọi LLM thật | Chưa có — làm ở CP3 |
