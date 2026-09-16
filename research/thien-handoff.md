# Bàn giao Thiên — CP3 đến CP6

## Đã làm trong lượt này

- Mining có script chạy lại, tách K4/preset, mã nguồn từng tín hiệu, 7 quote ngắn.
- Tổng hợp khảo sát hiện có và log ẩn danh; không thu thêm khảo sát theo yêu cầu.
- Bảng 3 ứng viên và giới hạn số liệu; nghiên cứu 2 giải pháp từ nguồn chính thức.
- Điền spec §1–§3 cho hướng trắc nghiệm sau nộp.
- 20 case seed cho Phong: 8 thường, 8 case khó (2/lớp), 4 hiếm; 12 mã chatlog thật khác nhau.

## Trước CP3 — 16:00 17/09

Phong nhận `eval/thien-case-seeds.csv`, mở nguồn local theo turn_id, duyệt input/đáp án/citation, xác định expected output chấm được rồi chạy đầy đủ. Không dùng trực tiếp seed làm nhãn vàng. TH10/11 cần harness thiếu context; TH13 cần mô phỏng retrieval rỗng. 9 đáp án trong question_bank chưa được người duyệt. Sơn phụ trách AI chạy thật + trace và video 30 giây; Huy nộp checkpoint.

Thiên cần đọc và hiểu phương pháp/giới hạn trong `thien-evidence-report.md`, rà lại quote và nhận định AI đã hỗ trợ viết. Không cần đợi đủ khảo sát mới bàn giao evidence.

## Trước CP4 — 21:00 17/09

Huy tích hợp thiết kế thực tế vào §4–§9 và khóa quality bar cùng Phong. Đề xuất ghi changelog: chuyển từ chấm tự luận sang giải thích trắc nghiệm theo xác nhận của Thiên ngày 16/09; không ghi là kết quả validation. Canvas CP1 giữ làm bản lịch sử; README phân công cũ còn cần đồng bộ khi nhóm chốt bản spec.

Các thiếu hụt khai thật: khảo sát n=14 ngoài nhóm, chưa đạt chuẩn A; chưa đo phút/tần suất để lượng hóa impact; nghiên cứu tương tự chưa dùng thử; chưa có eval hoặc validation trong lượt này.

## Trước CP5 — 13:00 18/09

Hỗ trợ Huy tổ chức 5 người ngoài nhóm theo README (gồm 2 willing users CP1). Giao task: “Bạn vừa trả lời một câu; hãy tìm hiểu chỗ mình hiểu sai và mở căn cứ để kiểm lại.” Quan sát im lặng; ghi task, điểm kẹt, quote, quyết định. Không coi câu trả lời sẵn sàng dùng thử trong khảo sát là validation.

Mẫu mỗi người: mã người/vai → task → hành vi quan sát → quote nguyên văn → mức nghiêm trọng → sửa/giữ và lý do. Tổng hợp 4 dòng: chủ đề lặp; sửa trước demo; giữ nguyên; để sau. Chuyển quyết định cho §9.

## Nội dung slide có thể dùng ngay

- Slide 1: 24 yêu cầu giải thích được rà từ nhóm ứng viên trong chatlog K4; ví dụ T11469. Nói rõ phương pháp không tìm hết nhu cầu.
- Slide 2: bảng A/B/C trong evidence report; lựa chọn dựa vào độ cụ thể và khả thi, chưa có ROI/phút tiết kiệm.
- Slide 5: chưa có quote validation; chỉ thay bằng kết quả golden set khi Phong đã đo theo hướng dẫn.
- Slide 6: ưu tiên duyệt đáp án/căn cứ, xử lý thiếu context, kiểm chứng khả năng hiểu sau giải thích; đây là đề xuất trước eval, cần cập nhật theo lỗi thật.

## Reflection và Q&A

Chưa tạo reflection hoàn chỉnh vì chưa có lời kể cá nhân và case fail của nhóm sau chạy. Dữ kiện có thể dùng: đã đọc khám phá chatlog; AI hỗ trợ script, thống kê, soạn nghiên cứu; phát hiện T11544 là false positive do từ “giải thích” nằm trong đề. Thiên tự xác nhận việc thực sự làm và bổ sung bài học từ eval/validation.

Câu hỏi luyện trả lời: Vì sao tách preset? Vì sao 25 lượt không có nghĩa 25 người? Vì sao khảo sát 100% “cần AI” chưa chứng minh hiệu quả? Vì sao chưa được coi lời tutor là đáp án chuẩn? Tại sao chọn A dù proxy C lớn hơn? Mã case nào cho thấy đã có kết quả bài làm?
