# Evidence & Research — Thiên · 16/09/2026

Phạm vi đã được Thiên xác nhận: **giải thích câu trắc nghiệm sau khi học viên nộp đáp án**. CP1 và CP2 đã hoàn thành theo thông tin của Thiên; CP3 chưa hoàn thành. Báo cáo này không xác nhận prototype đã chạy thành công hoặc có hiệu quả học tập.

## 1. Phương pháp mining có thể kiểm lại

Chạy tại gốc repo: `python -X utf8 research/analyze_evidence.py`.

Script đọc CSV bằng thư viện chuẩn, lọc `cohort_hint=K4`, tách `is_preset=False`, rồi áp regex không phân biệt hoa/thường trên toàn `student_question`, bao gồm tiền tố ngữ cảnh. Các regex, SHA-256 file nguồn và danh sách mã lượt khớp nằm trong `mining-summary.json`. Không xuất toàn văn hội thoại. Một dòng là một lượt hỏi–đáp, không phải một người hoặc một phiên học. Số người là số mã `student` duy nhất trong từng tập.

Đọc khám phá ban đầu: 40 lượt trong `../thien-step2-reading-notes.md`. Bước tiếp theo đọc các ứng viên có ngữ cảnh quiz và yêu cầu giải thích để phát hiện nhầm từ khóa. Đây là phân loại do trợ lý AI hỗ trợ; chưa được Thiên duyệt độc lập.

| Tập dữ liệu | Số lượng |
|---|---:|
| Toàn pack | 13.494 lượt |
| K4 | 3.097 lượt / 448 mã học viên |
| K4 có cờ câu mẫu | 542 lượt (17,50% K4) |
| K4 không có cờ câu mẫu — mẫu số chính | 2.555 lượt |

| Tín hiệu tự động trong 2.555 lượt | Lượt | Mã học viên | % lượt |
|---|---:|---:|---:|
| Ngữ cảnh quiz/trắc nghiệm/ôn câu hỏi/luyện đề xuất | 133 | 31 | 5,21% |
| Có chữ “đáp án” | 28 | 20 | 1,10% |
| Có “tại sao/vì sao/giải thích/không hiểu” | 428 | 157 | 16,75% |
| Vừa có ngữ cảnh quiz vừa có từ giải thích | 25 | 11 | 0,98% |
| Khớp mẫu yêu cầu tạo bài/câu hỏi | 2 | 2 | 0,08% |
| Khớp mẫu xác nhận/kiểm tra/chấm | 29 | 14 | 1,14% |

Các tập có thể chồng lấp, **không cộng các hàng**. 133 lượt không phải 133 trường hợp đau: có chào hỏi hoặc câu ngoài chủ đề dù đang ở màn hình quiz. 428 lượt gồm cả giải thích kiến thức chung. Hai hàng cuối là tín hiệu từ regex hẹp, không phải thống kê đầy đủ mọi yêu cầu luyện tập/kiểm tra. Không dùng tỷ lệ 0,98% làm tỷ lệ học viên cần sản phẩm.

### Rà nhóm 25 ứng viên

T11544 khớp vì đề ghép cặp chứa cụm “Soạn lời giải thích thân thiện”, không phải học viên yêu cầu giải thích. Loại lượt này khỏi nhóm yêu cầu giải thích đã rà. 24 lượt còn lại có yêu cầu làm rõ kiến thức/câu hỏi/đáp án trong ngữ cảnh luyện tập; không phải tất cả là trắc nghiệm một đáp án hoặc đã nộp bài.

Mã 24 lượt: T10472, T10477, T10524, T11200, T11466, T11469, T11472, T11482, T11560, T11569, T11623, T11648, T12013, T12193, T12235, T12577, T12711, T13001, T13004, T13005, T13196, T13199, T13200, T13201.

24/2.555 = 0,94% là **số quan sát tìm thấy bằng quy tắc này**, không phải ước lượng nhu cầu đầy đủ. Chưa đo recall hoặc rà toàn bộ 2.555 lượt. Có ví dụ nhiều đáp án/ghép cặp; chỉ dùng để chứng minh vấn đề rộng và tạo case ngoài phạm vi.

## 2. Quote ngắn nguyên văn và diễn giải

Trích từ `student_question`, bỏ tiền tố giao diện; mỗi đoạn dưới đây là chuỗi nguyên văn trong lượt nguồn. Không sao chép đề dài hoặc lời tutor làm đáp án chuẩn.

| turn_id | Trích dẫn | Điều có thể kết luận |
|---|---|---|
| T10472 | “Tại sao temperature thấp giúp kết quả ổn định hơn?” | Người học hỏi lý do trong ngữ cảnh quiz |
| T11466 | “Giải thích tại sao lại có câu trả lời này. học từ trong lúc pretrain là đúng rồi mà” | Có cách hiểu khác cần đối chiếu |
| T11469 | “trời ơi, giải thích câu 5 đi, tại sao lại như thế” | Hỏi bằng số câu; cần ngữ cảnh câu đang làm |
| T11472 | “không hiểu câu này lắm, tại sao lại như thế” | Yêu cầu mơ hồ nếu không có câu hỏi đi kèm |
| T11482 | “thế tại sao trong phần luyện theo đề xuất lại có câu hỏi và đáp án lại sai” | Người học nghi ngờ đáp án; chưa chứng minh đáp án thật sự sai |
| T11543 | “đáp án đúng của câu này là gì” | Hỏi đáp án, chưa rõ đã nộp hay chưa |
| T13004 | “tôi chọn {"order_id":"ORD-0042","limit":0} lại sai” | Ví dụ trực tiếp muốn hiểu vì sao lựa chọn bị đánh sai; câu nhiều đáp án ngoài phạm vi prototype hiện tại |

T12578 còn chứa dấu “Bạn đã chọn”, “Đáp án đúng”, “Chưa đúng”; T12013/T12193 có dấu kết quả và câu hỏi “tại sao”. Đây là bằng chứng có hành vi hỏi trong ngữ cảnh kết quả, không chứng minh mọi lượt quiz đều diễn ra sau nộp.

## 3. Khảo sát hiện có

Nguồn local: `Thông tin liên hệ.csv`. Script loại đúng hai tên Thiên và Phong, giữ câu trả lời nguyên văn của bốn câu liên quan trong `survey-anonymized.csv`; câu hỏi đầy đủ nằm trong `survey-summary.json`. Không xuất tên, MSSV, timestamp hoặc thông tin liên hệ. Mã R01… theo thứ tự các phản hồi giữ lại. Cần kiểm tra người trả lời là người khác nhau; tên viết tắt/ẩn danh không đủ để xác thực độc lập.

| Câu hỏi | Có | Không | Có thể |
|---|---:|---:|---:|
| Nhu cầu thực hành trên VLearn sau buổi học | 11/14 (78,57%) | 3 | — |
| Từng khó khăn với câu hỏi/thuật ngữ | 13/14 (92,86%) | 1 | — |
| Thấy AI hỗ trợ hiểu bài sau khi làm là cần thiết | 14/14 (100%) | 0 | — |
| Sẵn sàng dùng thử 5–10 phút ngày mai | 9/14 | 2 | 3 |

Có 16 phản hồi tổng, loại 2 trong nhóm, còn 14 phản hồi ngoài nhóm theo thông tin tên. **Chưa đạt chuẩn A ≥20 người.** Theo yêu cầu của Thiên, không thu thêm khảo sát trong đợt làm này. Dùng mining làm cơ sở cho chuẩn B, khảo sát làm bằng chứng bổ trợ. Không gộp 14 người khảo sát với 448 mã học viên vì không có phép đối chiếu danh tính và không được suy ngược danh tính.

Câu hỏi về AI có tính dẫn dắt; câu hỏi về khó khăn gộp câu hỏi và thuật ngữ. Không suy ra 100% sẵn sàng dùng, cải thiện điểm số hay tiết kiệm thời gian. Chưa thu số lần gặp/tuần hoặc số phút mỗi lần. 9 “có” và 3 “có thể” chưa phải 12 người đã đặt lịch hoặc đã dùng thử.

## 4. Bảng impact và quyết định

| Ứng viên | Quy mô quan sát / chỉ báo | Tần suất quan sát | Tốn gì mỗi lần | Khả thi và quyết định |
|---|---|---|---|---|
| A. Giải thích trắc nghiệm sau khi nộp | 25 tín hiệu/11 mã học viên; rà còn 24 yêu cầu giải thích rộng. 13/14 khảo sát từng khó hiểu bài/thuật ngữ | 24 lượt trong kỳ K4 của pack; chưa đo theo người/tuần | Chưa đo phút; phải hỏi lại/đối chiếu, có nguy cơ giữ hiểu nhầm | Chọn theo xác nhận của Thiên. Có prototype và 9 câu tham chiếu; scope một câu, ba kiểu hỏi |
| B. Tạo thêm bài luyện theo buổi | 2 lượt/2 mã khớp regex hẹp; 11/14 muốn thực hành trên app | 2 lượt khớp, chưa đo nhu cầu sinh bài mới | Chưa đo; công sức tìm bài mới là giả thuyết | Chưa chọn. Cần duyệt cả đề, distractor và đáp án; nhu cầu thực hành không đồng nghĩa thiếu bài |
| C. Giải thích thuật ngữ toàn bài | 428 lượt/157 mã có từ giải thích, gồm nhiều ngữ cảnh; chưa phải số pain xác nhận | 428 tín hiệu; chưa đo số lần khó hiểu/tuần | Chưa đo phút; phải tra lại khái niệm | Chưa chọn cho lát cắt này. Phạm vi rộng, tập intent nhiễu; ưu tiên gắn câu đang làm để eval cụ thể |

Không nhân các proxy thành điểm impact giả. Bảng chưa đủ dữ liệu để xếp hạng lợi ích định lượng hoặc khẳng định A có impact lớn nhất. A là quyết định sản phẩm dựa trên bằng chứng có tồn tại vấn đề + phạm vi build hiện có; các số A/B/C không phải ba tập cùng định nghĩa để so trực tiếp. Phần tần suất thực tế và tổn thất thời gian còn thiếu, có thể ảnh hưởng điểm impact.

## 5. Bàn giao cho Huy / Phong

- §1–§3 đã được đưa vào `../spec.md`; Huy phụ trách hoàn thiện các phần thiết kế, quality bar và chốt spec.
- `../eval/thien-case-seeds.csv`: 20 case thiết kế, gồm 12 case từ 12 mã chatlog khác nhau và 8 biến thể tự soạn; đây là seed có hành vi mong đợi, chưa phải golden set đã duyệt/chạy.
- Rủi ro phải kiểm CP3: cả 9 câu trong question_bank hiện `reviewed=false`; đáp án do tutor trả không tự động là ground truth. q07 thiếu căn cứ; q09 có nghi vấn đề/đáp án. Người duyệt cần kiểm transcript và có hành vi hiển thị phù hợp khi không đủ căn cứ.
- Không dùng kết quả mining thay % pass eval; chưa có lượt chạy AI trong phần việc này.
