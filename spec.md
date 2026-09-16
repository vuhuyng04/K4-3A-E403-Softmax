# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 17/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

# AI SPEC — Giải thích trắc nghiệm sau khi nộp · Nhóm Softmax · Cụm C2
Hướng: [x] A — VLearn Tutor  [ ] B — Trợ lý Discord  [ ] C — Lesson Studio  [ ] D — Học tập thích ứng & tương tác  [ ] E — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới (A2)

## §1. User & Job
- Job executor: học viên K4 vừa nộp đáp án một câu trắc nghiệm trên VLearn, muốn hiểu lý do đúng/sai trước khi tiếp tục.
- Core JTBD: xác định chỗ hiểu sai sau khi trả lời một câu trắc nghiệm và đối chiếu lại nội dung bài học.
- Problem statement: khi xem kết quả bài tập, một số học viên chưa hiểu lý do của đáp án hoặc thuật ngữ trong câu, phải hỏi lại và có thể thiếu ngữ cảnh câu đang làm; nguy cơ giữ hiểu nhầm chưa được đo định lượng.
- Workflow quan sát/đề xuất: làm câu hỏi → nộp đáp án → xem kết quả → hỏi vì sao → đối chiếu bài giảng → tiếp tục học. Chatlog có hành vi hỏi lại; toàn luồng tích hợp là thiết kế nhóm, chưa được validation.
- Evidence mining (đường B): 3.097 lượt K4/448 mã học viên; tách 542 preset, phân tích 2.555 lượt còn lại. Quy tắc tìm thấy 25 lượt vừa có ngữ cảnh quiz vừa có từ giải thích, từ 11 mã học viên. Rà loại T11544 (từ khóa nằm trong đề), giữ 24 yêu cầu giải thích rộng; không phải tất cả là câu một đáp án hoặc sau nộp.
- ≥5 quote nguyên văn, nguồn, quy tắc đếm, giới hạn và mã lượt: [báo cáo evidence](research/thien-evidence-report.md); [script chạy lại](research/analyze_evidence.py); [kết quả mining](research/mining-summary.json).
- Khảo sát bổ trợ: 16 phản hồi, loại 2 thành viên nhóm, còn 14 phản hồi tạm xác định ngoài nhóm; 13/14 từng khó hiểu câu hỏi/thuật ngữ, 14/14 thấy hỗ trợ giải thích bằng AI cần thiết, 11/14 muốn thực hành trong app. Chưa đạt đường A ≥20; câu hỏi dẫn dắt, chưa xác minh người trùng và chưa đo hiệu quả.
- Log câu trả lời ẩn danh: [survey-anonymized.csv](research/survey-anonymized.csv); câu hỏi nguyên văn và tổng hợp: [survey-summary.json](research/survey-summary.json). Bỏ qua thu khảo sát bổ sung theo phạm vi Thiên yêu cầu ở đợt này.

## §2. Impact & quyết định chọn
- [Bảng impact 3 ứng viên và giới hạn](research/thien-evidence-report.md): A giải thích sau nộp; B tạo thêm bài luyện; C giải thích thuật ngữ toàn bài.
- Chọn A theo xác nhận của Thiên: có 24 yêu cầu giải thích trong tập ứng viên đã rà và prototype có 9 câu tham chiếu; luồng giới hạn một câu giúp kiểm chứng nội dung/citation. Không tuyên bố A có impact lớn nhất.
- B chưa chọn: 2 lượt khớp regex tạo câu/bài, tín hiệu chưa đầy đủ; thêm gánh nặng duyệt đề và đáp án. C chưa chọn: 428 tín hiệu giải thích rộng, intent nhiễu và khó giới hạn scope trong sự kiện.
- Chưa đo số phút/tổn thất mỗi lần hoặc tần suất theo người/tuần; không tự gán số hay nhân proxy để tạo ROI. Phần impact định lượng còn thiếu và phải khai ở CP4.

## §3. Giải pháp tương tự đã nghiên cứu
- [Bảng nghiên cứu và nguồn chính thức](research/similar-products.md): NotebookLM/Gemini Notebook và Khanmigo.
- Học cách mở citation tại đoạn nguồn và hỗ trợ theo ngữ cảnh bài tập. Khác biệt đề xuất: tích hợp câu K4 vừa nộp cùng transcript BTC; không tuyên bố độc nhất.
- Đây là nghiên cứu tài liệu, chưa phải log dùng thử sản phẩm của thành viên. Các điều cần tránh là suy luận thiết kế, không phải lỗi đối thủ đã quan sát.

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
