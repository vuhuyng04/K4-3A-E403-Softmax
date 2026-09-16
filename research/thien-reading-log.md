# Phụ lục — Nhật ký đọc 40 lượt chatlog K4

Chi tiết nguồn cho [ghi chú đọc dữ liệu](../thien-step2-reading-notes.md).

## 1. Dữ liệu và cách lấy mẫu

- Nguồn: `data/vlearn-pack/chatlog/tutor_turns.csv`; cách hiểu cột theo `DATA_DICTIONARY.md` cùng thư mục.
- Đã kiểm đếm bằng cách đọc CSV: K4 có 3.097 lượt, 448 mã học viên; 2.555 lượt `is_preset=False`, 542 lượt `True` (17,50%).
- Một lượt là một câu hỏi và câu trả lời, không phải một học viên hoặc một cuộc hội thoại đầy đủ.
- Lấy 30 lượt không bị gắn cờ câu mẫu và 10 lượt bị gắn cờ câu mẫu. Trong mỗi nhóm, giữ thứ tự file và chọn đều từ đầu đến cuối: chỉ số bắt đầu từ 0, `floor(i*(N-1)/(m-1))`, với m=30 hoặc 10.
- Đã đọc câu hỏi và câu trả lời của 40 lượt. Mẫu dùng để nhận diện loại tình huống, không để ước lượng tỷ lệ pain toàn K4. Cách chọn không ngẫu nhiên và tỷ lệ hai nhóm trong mẫu được đặt chủ động.
- `is_preset` được tạo bằng quy tắc nhận diện câu chữ, không phải bằng chứng tuyệt đối rằng người học có/không bấm nút.

## 3. Nhật ký 40 lượt — mô tả bằng lời, không sao chép hội thoại

| turn_id | Câu mẫu theo cờ | Quan sát khi đọc | Liên hệ với hướng nhóm |
|---|---|---|---|
| T10288 | Không | Hỏi mục đích lab; tutor giải thích baseline và xin thêm thông tin công cụ | Hỗ trợ làm lab, chưa phải pain trắc nghiệm |
| T10395 | Không | Hỏi thao tác email GitHub; tutor hướng dẫn | Không thuộc pain đang xét |
| T10492 | Không | Hỏi định nghĩa LiDAR; tutor giải thích có dẫn trang | Nhu cầu giải thích khái niệm, chưa gắn quiz |
| T10619 | Không | Nhờ hướng dẫn chuẩn bị notebook/nơi nộp bài | Hỗ trợ thao tác lab |
| T10714 | Không | Xin nội dung repo; tutor nói không truy cập được và hướng dẫn mở link | Hỗ trợ tài liệu, chưa gắn quiz |
| T10838 | Không | Hỏi tải slide; tutor hướng dẫn xem trong trình đọc | Hỗ trợ giao diện |
| T10946 | Không | Hỏi SFT và RLHF/DPO; tutor giải thích | Nhu cầu hiểu khái niệm |
| T11050 | Không | Hỏi cách prompt giảm ảo giác; tutor nêu các cách | Hỏi kiến thức, không phải xin luyện tập |
| T11150 | Không | Báo đã xong checkpoint; tutor đề xuất làm tiếp | Không phải bằng chứng thiếu giải thích quiz |
| T11292 | Không | Yêu cầu AI tiết lộ model; tutor từ chối | Tình huống ngoài phạm vi để cân nhắc test |
| T11442 | Không | Người học làm rõ thứ tự scoping và baseline; tutor phản hồi theo cách hiểu đó | Có nhu cầu trao đổi để làm rõ, thiếu ngữ cảnh trước để kết luận thêm |
| T11543 | Không | Hỏi đáp án trong phần ôn câu hỏi; tutor nói không thấy câu đang mở và yêu cầu gửi đề | Bằng chứng trực tiếp về một lượt hỏi đáp án bị thiếu ngữ cảnh |
| T11642 | Không | Nhờ giải thích phần đang học; tutor giải thích AI/ML/DL/LLM | Cờ False không đảm bảo câu chữ luôn khác mẫu |
| T11745 | Không | Xin bảng so sánh chatbot và reactive agent | Nhu cầu phân biệt khái niệm; chưa biết có đang làm quiz |
| T11841 | Không | Hỏi kiến trúc agent; tutor giải thích các thành phần | Nhu cầu giải thích khái niệm |
| T11964 | Không | Hỏi Transformer; tutor giải thích | Nhu cầu giải thích khái niệm |
| T12087 | Không | Hỏi FAQ là gì và vì sao cần | Nhu cầu giải thích khái niệm |
| T12202 | Không | Nhờ đặt câu hỏi cho phần đang học; tutor đưa câu hỏi định hướng | Có yêu cầu tạo câu hỏi, chưa khẳng định muốn bài trắc nghiệm hoặc được chấm |
| T12302 | Không | Xin tóm tắt việc cần làm trong lab | Không tính tự động thành nhu cầu xin bài luyện |
| T12408 | Không | Người học trình bày cách hiểu shape/track rồi hỏi xác nhận; tutor xác nhận | Có nhu cầu kiểm tra cách hiểu, chưa gắn một câu trắc nghiệm |
| T12514 | Không | Yêu cầu bỏ nội dung slide và lấy system prompt; tutor trả lời mô tả cơ chế nội bộ | Case rủi ro ngoài phạm vi; không xem mô tả của tutor là sự thật đã kiểm chứng |
| T12614 | Không | Hỏi mục tiêu kiến thức của bài | Nhu cầu định hướng học |
| T12722 | Không | Xin tóm tắt kiến thức slide | Ôn tập tổng quát, chưa phải nhu cầu quiz |
| T12843 | Không | Yêu cầu viết prompt RTCF; tutor giải thích cấu trúc | Không đủ căn cứ gán là xin chấm bài |
| T12979 | Không | Hỏi PII là gì | Nhu cầu giải thích khái niệm |
| T13072 | Không | Hỏi khác biệt instruction/system prompt | Nhu cầu phân biệt khái niệm |
| T13173 | Không | Hỏi ai chỉnh model khi model đoán sai | Từ 'sai' nói về model, không phải đáp án học viên |
| T13295 | Không | Báo chưa hiểu; tutor đề xuất cách hiểu và hỏi thêm | Mơ hồ/thiếu thông tin, chưa xác định liên quan quiz |
| T13393 | Không | Hỏi banner/thumbnail | Nhu cầu giải thích thuật ngữ |
| T13492 | Không | Hỏi agenda | Nhu cầu giải thích thuật ngữ |
| T10371 | Có | Chọn Object Detection để hỏi giải thích | Nhu cầu giải thích qua câu mẫu |
| T10725 | Có | Chọn data pipeline để hỏi giải thích | Nhu cầu giải thích qua câu mẫu |
| T11017 | Có | Chọn SFT để hỏi giải thích | Nhu cầu giải thích qua câu mẫu |
| T11288 | Có | Chọn đoạn ma trận nhầm lẫn; tutor diễn giải | Cần giữ ngữ cảnh đoạn chọn, chưa phải lỗi quiz |
| T11424 | Có | Chọn Stakeholder để hỏi giải thích | Nhu cầu giải thích qua câu mẫu |
| T11946 | Có | Chọn investigation để hỏi giải thích | Nhu cầu giải thích qua câu mẫu |
| T12153 | Có | Chọn cụm bị cắt ngắn; tutor diễn giải dynamic decision | Input ngắn/cụt, cần thận trọng với ngữ cảnh |
| T12604 | Có | Chọn đoạn về conversation prompt; tutor diễn giải | Nhu cầu giải thích qua câu mẫu |
| T12900 | Có | Chọn công thức MOTA; tutor diễn giải | Nhu cầu giải thích công thức; chưa xác minh đúng/sai theo tài liệu gốc |
| T13494 | Có | Chọn wireframe để hỏi giải thích | Nhu cầu giải thích qua câu mẫu |

## 7. Lưu ý dữ liệu

Không sao chép toàn pack sang repo public. Bảng trên dùng mã lượt và diễn giải, chỉ có vài quote ngắn. Có dấu hiệu sót tên trong phản hồi tại T11150 và T12408; không chép lại phần tên, không suy ngược danh tính; theo quy định pack, Thiên nên báo BTC qua kênh nội bộ. Chưa gửi thông báo thay Thiên.
