# Ghi chú đọc chatlog K4 — Đào Ngọc Bình Thiên

**Vai trò:** Evidence & Research · **Nhóm:** Softmax · **Track:** A — VLearn Tutor.

**Hướng sản phẩm:** giải thích câu trắc nghiệm sau khi học viên nộp đáp án, kèm căn cứ từ transcript bài giảng.

## 1. Nguồn và phương pháp

Nguồn: `data/vlearn-pack/chatlog/tutor_turns.csv` và `DATA_DICTIONARY.md` cùng thư mục.

K4 có **3.097 lượt hỏi–đáp, 448 mã học viên**; gồm **542 lượt có cờ câu mẫu** và **2.555 lượt không có cờ câu mẫu**. Một lượt không tương đương một học viên.

Đọc khám phá 40 lượt: 30 lượt không có cờ câu mẫu và 10 lượt có cờ câu mẫu, chọn đều theo thứ tự file trong từng nhóm. Cách lấy mẫu và nhật ký đầy đủ nằm trong [phụ lục đọc dữ liệu](research/thien-reading-log.md). Mẫu dùng để nhận diện tình huống, không ước lượng tỷ lệ nhu cầu toàn K4.

## 2. Quan sát chính

| Mã lượt | Quan sát | Ý nghĩa với bài toán |
|---|---|---|
| T11543 | Học viên hỏi “đáp án đúng của câu này là gì”; tutor yêu cầu cung cấp nội dung câu hỏi | Cần giữ ngữ cảnh câu đang làm khi hỏi tutor |
| T12408 | Học viên trình bày cách hiểu rồi hỏi xác nhận | Có nhu cầu kiểm tra cách hiểu; chưa xác định liên quan trắc nghiệm |
| T12202 | Học viên yêu cầu “Đặt câu hỏi cho phần này” | Có nhu cầu tạo câu hỏi theo bài |
| T11745, T13072 | Học viên yêu cầu so sánh các khái niệm | Có nhu cầu phân biệt kiến thức dễ nhầm |
| T13173 | Cụm “đoán sai” nói về model, không phải đáp án học viên | Phải kiểm nội dung khi phân loại bằng từ khóa |

## 3. Kết luận và đề xuất

Mẫu đọc ghi nhận tình huống hỏi đáp án nhưng thiếu ngữ cảnh, cùng nhu cầu làm rõ và kiểm tra cách hiểu. Đề xuất cho prototype: chuyển sẵn đề, các lựa chọn và đáp án đã nộp vào tutor; giải thích gắn với đoạn bài giảng để học viên kiểm lại.

Đề xuất cần kiểm chứng bằng eval và dùng thử. Mẫu 40 lượt chưa chứng minh mức phổ biến, nhu cầu riêng sau nộp bài hoặc hiệu quả học tập của sản phẩm.

## 4. Tài liệu nghiên cứu liên quan

- [Báo cáo evidence và impact](research/thien-evidence-report.md): mining K4, 7 quote có nguồn, khảo sát hiện có và bảng 3 ứng viên.
- [Giải pháp tương tự](research/similar-products.md): nghiên cứu tài liệu chính thức và giới hạn.
- [Spec §1–§3](spec.md): người dùng, vấn đề, evidence và quyết định chọn.
- [Bàn giao CP3–CP6](research/thien-handoff.md): case cho eval và công việc còn lại.
