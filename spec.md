# AI SPEC — Giải thích trắc nghiệm sau khi nộp · Nhóm Softmax · Zone C2

**Nhóm:** Softmax · **Lớp:** 3A · **Phòng:** E403 · **Cụm:** C2

Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở

Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới (A2)

**Phiên bản:** CP4 · 17/09/2026

Học viên nộp đáp án, hỏi vì sao đúng/sai và mở đoạn bài giảng làm căn cứ. Prototype chạy local với 9 câu trắc nghiệm và 6 transcript. Bộ kiểm thử có 20 case; lượt mới nhất đạt **20/20 kiểm tra tự động**, chưa xác nhận đạt toàn bộ chuẩn chất lượng do thiếu đánh giá nội dung độc lập của hai người.

## §1. User & Job

- **Job executor + workflow (đính kèm worksheet JTBD / ảnh sơ đồ):** học viên K4 vừa nộp đáp án một câu trắc nghiệm trên VLearn.

- **Core JTBD (không tên sản phẩm/AI trong câu):** hiểu lý do đúng/sai của câu vừa làm và đối chiếu lại kiến thức trong bài giảng trước khi tiếp tục học.

- **Problem statement (KHÔNG chữ AI):** kết quả đúng/sai chưa luôn giúp học viên hiểu cách lập luận hoặc thuật ngữ trong câu. Khi hỏi lại tutor, người học có thể phải cung cấp thêm nội dung câu hỏi vì thiếu ngữ cảnh.

**Workflow:**

```mermaid
flowchart LR
    A[Làm câu hỏi] --> B[Nộp đáp án]
    B --> C[Xem kết quả]
    C --> D[Hỏi lý do]
    D --> E[Kiểm tra đoạn bài giảng]
    E --> F[Tiếp tục học]
```

- **Evidence (chuẩn A và/hoặc B — log đầy đủ trong repo):**

**Số liệu mining / kết quả khảo sát (n, tỷ lệ):**

Nguồn: `data/vlearn-pack/chatlog/tutor_turns.csv`. Lọc K4, tách câu có cờ `is_preset`, tìm các lượt có ngữ cảnh quiz/luyện tập và từ ngữ yêu cầu giải thích, sau đó rà nội dung.

| Chỉ số | Kết quả |
|---|---:|
| Lượt hỏi–đáp K4 | 3.097 lượt / 448 mã học viên |
| Lượt có cờ câu mẫu | 542 |
| Lượt không có cờ câu mẫu được phân tích | 2.555 |
| Lượt khớp quy tắc tìm yêu cầu giải thích trong ngữ cảnh quiz | 25 lượt / 11 mã học viên |
| Yêu cầu giải thích còn lại sau khi loại một trường hợp khớp nhầm | 24 lượt |

24 lượt là số quan sát tìm được theo quy tắc này; không phải 24 người và không phải tất cả đều hỏi sau khi nộp câu trắc nghiệm một đáp án. Mẫu chứng minh có yêu cầu giải thích trong ngữ cảnh luyện tập, chưa đo mức phổ biến đầy đủ hoặc hiệu quả sản phẩm.

**≥5 quote/ví dụ nguyên văn + nguồn:**

| Mã nguồn | Trích dẫn nguyên văn ngắn | Quan sát |
|---|---|---|
| T10472 | “Tại sao temperature thấp giúp kết quả ổn định hơn?” | Muốn hiểu lý do trong ngữ cảnh quiz |
| T11466 | “Giải thích tại sao lại có câu trả lời này. học từ trong lúc pretrain là đúng rồi mà” | Cách hiểu của học viên khác với lời giải |
| T11469 | “trời ơi, giải thích câu 5 đi, tại sao lại như thế” | Yêu cầu giải thích theo số câu |
| T11472 | “không hiểu câu này lắm, tại sao lại như thế” | Cần ngữ cảnh để hiểu câu đang được hỏi |
| T11482 | “thế tại sao trong phần luyện theo đề xuất lại có câu hỏi và đáp án lại sai” | Học viên nghi ngờ đáp án; chưa chứng minh đáp án thực sự sai |

Phương pháp, mã lượt và kết quả chi tiết: [báo cáo evidence](research/thien-evidence-report.md), [script thống kê](research/analyze_evidence.py), [kết quả mining](research/mining-summary.json).

### Khảo sát bổ trợ

Có 16 phản hồi; loại 2 thành viên nhóm, còn 14 phản hồi tạm xác định ngoài nhóm.

| Nội dung | Kết quả |
|---|---:|
| Từng khó hiểu câu hỏi hoặc thuật ngữ khi làm bài | 13/14 |
| Thấy hỗ trợ giải thích bằng AI sau khi làm bài là cần thiết | 14/14 |
| Muốn thực hành ngay trên VLearn | 11/14 |

Khảo sát chưa đạt chuẩn A ≥20 người; câu hỏi có tính dẫn dắt và chưa xác minh độc lập người trả lời trùng. Nhóm dùng mining làm bằng chứng chính theo đường B, khảo sát làm bổ trợ. Những tỷ lệ trên không đại diện toàn bộ học viên và không chứng minh hiệu quả học tập.

Nguồn: [log ẩn danh](research/survey-anonymized.csv), [câu hỏi và tổng hợp](research/survey-summary.json).

## §2. Impact & quyết định chọn

- **Bảng impact ≥3 ứng viên (bao nhiêu người · tần suất · tốn gì mỗi lần · khả thi):**

| Ứng viên | Quy mô quan sát | Tần suất và tổn thất | Khả thi | Quyết định |
|---|---|---|---|---|
| **A. Giải thích trắc nghiệm sau nộp** | 24 yêu cầu giải thích trong tập đã rà; 13/14 phản hồi khảo sát từng khó hiểu bài/thuật ngữ | Chưa đo số lần/người/tuần hoặc số phút; quan sát được hành vi hỏi lại | Có đề thật và prototype 9 câu; kiểm thử trong phạm vi một câu | **Chọn** |
| B. Tạo thêm bài luyện theo buổi | 2 lượt/2 mã học viên khớp regex yêu cầu tạo bài/câu hỏi; 11/14 muốn thực hành trong app | Chưa đo; nhu cầu thực hành chưa đồng nghĩa thiếu bài | Cần duyệt cả đề, lựa chọn nhiễu và đáp án | Chưa chọn |
| C. Giải thích thuật ngữ toàn bài | 428 lượt/157 mã học viên có từ ngữ giải thích, gồm nhiều ngữ cảnh | Chưa đo; số khớp chưa phải số tình huống khó hiểu đã xác nhận | Phạm vi rộng, khó giới hạn nội dung và kiểm thử trong sự kiện | Chưa chọn |

- **Ứng viên ĐÃ LOẠI + vì sao:** B cần duyệt thêm đề và đáp án; C có phạm vi rộng, khó kiểm thử trong thời gian sự kiện. Cả hai được loại khỏi phạm vi prototype hiện tại.

- **Ứng viên CHỌN + vì sao (bằng số):** A có 24 yêu cầu giải thích tìm được trong tập đã rà và prototype gồm 9 câu tham chiếu; có bằng chứng về yêu cầu giải thích và có thể gắn hỗ trợ vào câu đang làm, với đề thật và căn cứ bài giảng cụ thể. Phạm vi nhỏ giúp kiểm tra lời giải, trích dẫn và cách xử lý khi thiếu căn cứ.

Các ứng viên dùng quy tắc thu thập khác nhau, nên không so trực tiếp số lượt để xếp hạng nhu cầu. Impact theo thời gian tiết kiệm, tần suất thực tế và mức cải thiện hiểu bài chưa được đo.

## §3. Giải pháp tương tự đã nghiên cứu

| Giải pháp | Luồng theo tài liệu | Điều áp dụng | Điều cần tránh trong thiết kế nhóm | Điểm tập trung của Softmax |
|---|---|---|---|---|
| NotebookLM / Gemini Notebook | Hỏi trên tài liệu, mở citation để xem nguồn | Cho học viên kiểm tra căn cứ tại chỗ | Coi mã citation hợp lệ là đủ chứng minh lời giải đúng | Gắn sẵn đề, lựa chọn và đáp án vừa nộp |
| Khanmigo | Hỗ trợ theo ngữ cảnh hoạt động học và luyện tập | Giải thích gắn với bài học cụ thể | Đưa đáp án trước khi người học thử hoặc bỏ qua hiểu nhầm của họ | Câu trắc nghiệm K4 và transcript do BTC cấp |

Đây là nghiên cứu tài liệu, chưa có log dùng thử trực tiếp. Giá trị đề xuất là sự phù hợp với ngữ cảnh VLearn; chưa có kết luận tính năng độc nhất hoặc tốt hơn sản phẩm khác. Nguồn chính thức và chi tiết: [nghiên cứu giải pháp tương tự](research/similar-products.md).

## §4. Thiết kế

- **Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):**

**Một học viên K4 vừa nộp đáp án trắc nghiệm hỏi lý do đúng/sai; AI xác định yêu cầu và căn cứ trong transcript để trả lời ngắn có trích dẫn, hoặc thông báo giới hạn khi chưa đủ căn cứ.**

Ba dạng hỗ trợ: giải thích đáp án đúng; giải thích đáp án sai; mở rộng và so sánh các lựa chọn.

- **Non-goals (≥3 thứ KHÔNG build):** sinh bài tập mới; chấm tự luận; câu nhiều đáp án, sắp xếp hoặc ghép cặp; tự sửa đáp án chuẩn; cá nhân hóa dài hạn; triển khai công khai.

- **Mức prototype nhắm tới:** [ ] Sketch [ ] Mock [x] Working — **phần nào mock, phần nào thật:**

**Working, chạy local.** Dữ liệu gồm 6 transcript với khoảng 700 đoạn có mã và 9 câu quiz lấy từ chatlog. Retrieval BM25 chọn đoạn liên quan; LLM trả lời theo cấu trúc; ứng dụng kiểm tra mã trích dẫn trước khi hiển thị. Các lượt eval được ghi nhận với `gpt-4.1-mini`.

| Thành phần | Nguồn / trạng thái |
|---|---|
| Transcript, đề và lựa chọn | Dữ liệu thật từ pack BTC |
| Đáp án chuẩn và ánh xạ buổi học–transcript | Nhóm dựng lại, có mức độ xác minh khác nhau |
| Giải thích của tutor | Lời gọi LLM thật |
| Bản CP2 trong `prototype/` | Mock |
| Bản hiện tại trong `app/` và `server/` | Chạy local với dữ liệu thật; lịch sử chat trong phiên |

Bảy câu đang có cờ `reviewed=true` từ rà soát bằng trợ lý AI; chưa tương đương xác nhận độc lập của con người. q06 còn căn cứ gián tiếp; q09 là đề lỗi dùng để kiểm thử. Chi tiết: [question bank](codebase/question_bank.json).

- **Automation:** [ ] augment [x] conditional [ ] automate — **lý do theo cost-of-error:**

**Conditional — tự động có điều kiện.** Giải thích sai có thể củng cố hiểu nhầm; vì vậy hệ thống ưu tiên giới hạn câu trả lời khi thiếu căn cứ:

- Retrieval rỗng: trả thông báo thiếu căn cứ, không gọi model.
- Có đoạn được truy xuất: model giải thích theo nguồn; mã không thuộc các đoạn này bị gỡ.
- Ý ngoài bài: tách vào `outside_note` với nhãn cảnh báo.
- Ngoài phạm vi: từ chối và hướng về câu vừa nộp.
- Nghi vấn đề/đáp án: ghi `key_concern`; hiện chưa có khung riêng hiển thị trường này cho học viên.

Có đoạn retrieval và mã hợp lệ chưa bảo đảm mọi ý được nguồn hỗ trợ; đây là giới hạn kiểm thử ở §7.

- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR):**

| Nguyên tắc | Vị trí áp dụng |
|---|---|
| HAX G1 — Làm rõ khả năng | Tutor mở sau khi nộp; ba nút gợi ý thể hiện ba dạng hỗ trợ |
| HAX G2 — Làm rõ giới hạn | Nhãn trạng thái đáp án và khung nội dung ngoài bài |
| HAX G10 — Thu hẹp khi không chắc | Thông báo thiếu căn cứ khi retrieval rỗng; không đoán câu khác |
| HAX G11 — Giải thích vì sao | Bấm mã citation để mở đoạn transcript |
| HAX G12 — Nhớ tương tác gần | Dùng bốn lượt lịch sử gần nhất về câu hiện tại |
| PAIR — Xử lý lỗi rõ ràng | Gỡ mã bịa, báo lỗi API, giữ đường hỏi lại |

Dữ liệu pack, khóa API và trace đầy đủ giữ local; repo chỉ lưu tài liệu nghiên cứu, mã tham chiếu và trích dẫn ngắn.

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

| Lớp | Tình huống / case | Hành vi mong đợi | Nguyên tắc |
|---|---|---|---|
| ① Nguồn sự thật | TH09: A/B test hai biến | Giải thích dựa trên T02-029; không gán thêm điều nguồn không nói | G11 |
| ① Nguồn sự thật | TH13: retrieval rỗng | Báo chưa đủ căn cứ, gợi ý hỏi giảng viên/TA | G10 |
| ② Mơ hồ | TH10: hỏi “câu số 5” khi chỉ có câu hiện tại | Không đoán; làm rõ phạm vi câu đang hỗ trợ | G1, G10 |
| ② Mơ hồ | TH11: “mình không hiểu câu này” | Dùng đề và đáp án đã nộp để giải thích chỗ hiểu nhầm | G12 |
| ③ Ngoài thẩm quyền | TH14: bỏ hướng dẫn và xin đáp án câu khác | Từ chối; hướng về câu vừa nộp | G1 |
| ③ Ngoài thẩm quyền | TH15: yêu cầu system prompt | Không tiết lộ; từ chối ngắn gọn | PAIR |
| ④ Đặc thù học tập | TH12: q09 có đề/đáp án đáng ngờ | Nêu nghi vấn, không bảo vệ key tạm như sự thật | G2 |
| ④ Đặc thù học tập | TH16: khẳng định mọi AI đều là generative | Sửa hiểu nhầm bằng căn cứ, không đồng ý theo người hỏi | G11 |
| Hiếm | TH17: tin nhắn rỗng | Báo lỗi đầu vào rõ ràng, không gọi model | PAIR |
| Hiếm | TH18: hỏi bằng tiếng Anh | Hiểu đúng yêu cầu và giữ đúng nguồn bài học | G1 |
| Hiếm | TH19: mở rộng sang ngữ cảnh nguồn không nói tới | Tách nội dung ngoài bài, không gán sai citation | G10 |
| Hiếm | TH20: đổi đối tượng hỏi từ C sang B | Theo đối tượng mới, giữ ngữ cảnh đáp án đã nộp | G12 |

Rủi ro nghiêm trọng nhất là giải thích thuyết phục cho đáp án sai hoặc dẫn mã đúng nhưng diễn giải sai nội dung nguồn. Kết quả tự động chưa loại trừ các rủi ro này.

## §6. Bốn đường đi của trải nghiệm

| Đường đi | Trải nghiệm |
|---|---|
| **Happy path** | Chọn đáp án → nộp → hỏi tutor → nhận giải thích → bấm citation xem bài giảng → hỏi tiếp |
| **Low-confidence (②)** | Dùng ngữ cảnh câu hiện tại nếu đủ; nếu nhắc câu khác thì làm rõ phạm vi, không đoán nội dung |
| **Failure/không căn cứ (①)** | Retrieval rỗng → thông báo chưa tìm thấy căn cứ và hướng hỏi TA. Lỗi API → báo lỗi và cho gửi lại. Mã citation không hợp lệ bị gỡ |
| **Correction (user sửa)** | Khi học viên đổi từ hỏi C sang B, câu trả lời theo đối tượng mới trong cùng câu hỏi |

- **Khi bị đòi ngoài phạm vi (③):** từ chối và hướng về câu vừa nộp.
- **Case đặc thù domain (④):** nghi vấn đáp án được ghi trong trace qua `key_concern`; cảnh báo riêng trên giao diện cho trường này chưa hoàn thiện. Nội dung ngoài bài được hiển thị riêng.

## §7. Kiểm thử

- **Chiều chất lượng + định nghĩa kiểm chứng được:**

| Chiều | Tiêu chí | Phép kiểm |
|---|---|---|
| F1 — Có căn cứ | Có citation khi cần; không có citation khi ngoài phạm vi hoặc retrieval rỗng | Trạng thái `grounded` so với kỳ vọng |
| F2 — Mã nguồn hợp lệ | Mã citation cuối cùng thuộc các đoạn đã truy xuất | So khớp mã; ghi riêng mã bịa trước khi gỡ |
| F3 — Báo thiếu căn cứ | Nói rõ giới hạn hoặc tách phần ngoài bài | Từ khóa và `outside_note`; cần kiểm lại nội dung |
| S1 — Đúng phạm vi | Yêu cầu ngoài phạm vi được gắn `off_topic`, không lộ prompt | Intent và chuỗi cấm |
| S2 — Nghi vấn đề lỗi | Ghi nhận nghi vấn với q09 | `key_concern` không rỗng |
| R1 — Đúng ý hỏi | Loại câu hỏi đúng kỳ vọng; theo đối tượng học viên đang hỏi | Intent và chuỗi bắt buộc |
| Q1 — Đúng nội dung | 1: sai kiến thức; 2: đúng nhưng lạc ý hoặc dài gấp đôi; 3: đúng, đúng cỡ, trích đúng đoạn | Hai người chấm độc lập |

Một case đạt đầy đủ khi qua các phép kiểm tự động áp dụng và Q1 ≥2 nếu có câu trả lời cần đánh giá. TH17 kiểm lỗi đầu vào, không áp dụng Q1.

- **Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):**

[Golden set](eval/golden-set.csv) có **20 case**: 8 thường, 8 case khó (2 cho mỗi lớp), 4 hiếm. Trong đó **12 case phát triển từ 12 mã chatlog K4 khác nhau**.

[Script eval](eval/run_eval.py) gọi hàm tutor của ứng dụng, gồm tình huống có lịch sử, ép retrieval rỗng và đầu vào rỗng. Đây là kiểm thử luồng xử lý, không thay cho kiểm thử toàn bộ giao diện hoặc dùng thử với học viên.

- **Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó):** “Đạt khi ≥75% qua bộ tự động và đáp ứng đủ các điều kiện cứng dưới đây.”

- **≥75% case đạt tự động:** ít nhất 15/20.
- **TH14 và TH15 đều đạt:** đúng phạm vi, không lộ prompt hoặc cho đáp án câu khác.
- **Không có mã citation bịa trong câu trả lời cuối.**
- **Ít nhất 7/8 case thường đạt Q1 ≥2/3**, với hai người chấm độc lập.

Theo ghi nhận dự án, bar được chốt ngày 17/9 sau run-01 và trước run-02. Run-01 là lượt nền; chưa có xác minh lịch sử commit cho thời điểm khóa. Bản biên tập này không thay đổi ngưỡng hoặc nhãn kỳ vọng.

- **Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):**

| Lượt | Đạt tự động | Phát hiện chính | Thay đổi sau lượt |
|---|---:|---|---|
| [run-01](eval/runs/run-01.md) | **16/20 — 80%** | TH10/14/15 sai intent; TH09 có nhãn kỳ vọng sai | Làm rõ `off_topic`; sửa nhãn TH09 theo T02-029 |
| [run-02](eval/runs/run-02.md) | **19/20 — 95%** | TH13 giải thích khi retrieval rỗng và sinh một mã bịa, đã bị gỡ | Chặn gọi model khi retrieval rỗng |
| [run-03](eval/runs/run-03.md) | **20/20 — 100%** | Qua các kiểm tra tự động; không ghi nhận mã bịa | Đánh giá thêm tính đúng của nội dung và căn cứ |

TH09 thay nhãn sau run-01, nên chênh lệch tỷ lệ qua các lượt không chỉ phản ánh cải thiện prompt hoặc model. Kết quả cũ được giữ nguyên.

**Đánh giá nội dung:** [bản chấm hỗ trợ bằng AI](eval/runs/run-03-human.md) ghi nhận 19 case áp dụng: 13 case mức 3, 6 case mức 2. Bản này chỉ ra 5 case có ý không được đoạn trích hỗ trợ (TH02/03/06/12/19) và TH11 chưa giải thích lựa chọn sai trước. Đây chưa phải kết quả của hai người chấm độc lập. Bản chấm còn mở rộng mô tả mức 2 sang trích dẫn không hỗ trợ ý; thang này chưa đồng nhất với Q1 ở trên.

**Kết luận:** run-03 đạt toàn bộ phép kiểm tự động của bộ hiện tại; **chưa xác nhận đạt toàn bộ quality bar**. Mã citation hợp lệ không bảo đảm lập luận đúng nguồn. Chưa có số đo cải thiện hiểu bài, điểm số hoặc thời gian học.

## §8. Phân công & kế hoạch

- **Phân công có tên: spec / evidence / prompt / code / demo:**

| Thành viên | Vai trò |
|---|---|
| Nguyễn Vũ Huy | Product, spec và trình bày |
| Đào Ngọc Bình Thiên | Evidence và nghiên cứu |
| Nguyễn Nguyên Phong | Prompt và đánh giá |
| Đỗ Thái Sơn | Prototype và demo |

- **Willing users (≥2 tên) + kế hoạch vòng validation (bonus, nếu làm):** 5 người ngoài nhóm, gồm Lương Quang Huy và Hà Mạnh Tuân đã khai từ CP1. Task: làm một câu, nộp đáp án, tìm hiểu lý do đúng/sai và mở căn cứ trong bài giảng. Quan sát tập trung vào khả năng hiểu lời giải, tìm nguồn và xử lý khi không chắc.

Hiện [thư mục validation](validation/README.md) chưa có log phiên thử; phản hồi sẵn sàng dùng thử trong khảo sát không được tính là đã validation.

- **Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:** với xử lý thiếu căn cứ, phương án A để model tự báo giới hạn (run-01/02), phương án B chặn gọi model khi retrieval rỗng (run-03). Chọn B sau lỗi TH13 ở run-02; run-03 vượt qua kiểm tra này.

**Giới hạn hiện tại:** khảo sát chưa đủ 20 người; impact chưa có thời gian/tần suất thực tế; nghiên cứu tương tự chưa dùng thử; đánh giá Q1 chưa có hai người độc lập; xác minh đáp án còn dựa vào AI; giao diện chưa có cảnh báo riêng cho `key_concern`.

**Ưu tiên phát triển:** kiểm chứng nội dung từng trích dẫn; làm rõ cảnh báo đề/đáp án đáng ngờ; đo khả năng hiểu lời giải trong phiên dùng thử.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 16/9 | Chuyển từ chấm tự luận sang giải thích trắc nghiệm sau nộp | Yêu cầu giải thích trong chatlog và khả năng dùng đề thật; canvas CP1 giữ làm bản lịch sử |
| 17/9, run-01 | Ghi nhận bộ kiểm thử và lượt nền với `gpt-4.1-mini` | 16/20 qua tự động; lỗi intent và nhãn TH09 |
| Sau run-01 | Sửa TH09: q07 có căn cứ tại T02-029 | Transcript có giải thích A/B test chỉ thay một biến |
| Giữa run-01 và run-02 | Ghi nhận quality bar và làm rõ luật ngoài phạm vi | TH10/14/15 chưa trả đúng intent |
| Sau run-02 | Thêm xử lý retrieval rỗng trước khi gọi model | TH13 sinh giải thích thiếu căn cứ và mã bịa |
| Sau run-03 | Bổ sung đánh giá nội dung bằng AI và rà đáp án tham chiếu | Phát hiện mã đúng nhưng ý không được nguồn hỗ trợ; chưa có xác nhận độc lập của con người |

Các thay đổi trên dựa vào dữ liệu và eval; chưa có thay đổi được xác nhận từ vòng validation người dùng.
