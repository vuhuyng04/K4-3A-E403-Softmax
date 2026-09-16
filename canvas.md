# Canvas CP1 — Nhóm Softmax · K4-3A-E403 · Track A (A2)

> Theo `02-guide.md` §1.5 (Canvas 7 dòng). Nộp qua form CP1 trước **19:30 · 16/9**. Nội dung sẽ chuyển vào `spec.md` §1 / §4 / §8 và hoàn thiện dần đến CP4.

| # | Mục | Nội dung |
|---|---|---|
| 1 | **Hướng** | Track A — VLearn Tutor · đề **A2 · Tính năng AI mới trên VLearn** · Loại: tính năng mới |
| 2 | **Job executor** | **Học viên K4 vừa học xong một buổi trên VLearn**, muốn tự luyện để kiểm tra mình đã hiểu nội dung buổi đó chưa — trước khi sang buổi tiếp theo hoặc trước quiz |
| 3 | **Pain một câu** | Học viên **học xong buổi N, muốn luyện tập** → VLearn **không có bài tập bám theo nội dung từng buổi**, học viên tự tìm hoặc bỏ qua → khi tự làm xong **không có ai chấm và chỉ ra chỗ hiểu sai ngay lúc đó** → hiểu sai bị bỏ qua, mang sang buổi sau và vào quiz |
| 4 | **Bằng chứng đầu** | *(từ `data/vlearn-pack/chatlog/DATA_DICTIONARY.md`, BTC đã đếm)* ① Nền tảng hiện **không có tín hiệu nào cho biết học viên hiểu thật hay chưa**: chỉ **1,3%** lượt có rating, `understanding_level` **gần rỗng** · ② Tutor **không bao giờ kiểm tra người học**: `ask_probing_question` chỉ **28 / 13.494** lượt · ③ **3.097 lượt hỏi-đáp K4** trong ~1 tuần cho thấy học viên chủ động tự học sau giờ, nhưng chỉ có kênh "hỏi", không có kênh "luyện" · *(nhóm bổ sung đến CP4: đếm trong 3.097 lượt K4 số câu học viên xin bài tập / nhờ tutor kiểm tra câu trả lời của mình, ≥5 quote nguyên văn; khảo sát ≥20 học viên: "lần gần nhất sau buổi học bạn tự luyện thế nào, ai chấm?")* |
| 5 | **Lát cắt MỘT CÂU** | **Một học viên** vừa học xong buổi N · **nộp câu trả lời cho một bài tập tự luận ngắn của buổi đó** · **AI quyết định câu trả lời đúng / đúng một phần / sai, chỉ ra chỗ sai kèm trích dẫn đoạn transcript `[bài N · đoạn X]`** · học viên **biết mình hiểu sai ở đâu và xem lại đúng đoạn bài giảng** |
| 6 | **Automation + willing users** | **Conditional**: tìm được căn cứ trong transcript buổi đó → AI chấm và giải thích kèm trích dẫn; **không tìm được căn cứ** → AI **không phán đúng/sai**, trả "chưa đủ căn cứ trong bài — hỏi giảng viên/TA" và vẫn chỉ đoạn liên quan nhất. *Lý do (cost-of-error):* chấm sai = học viên học sai + mất niềm tin (đắt); nói "chưa chắc" = học viên mất 1 phút hỏi lại (rẻ). Bộ bài tập mỗi buổi do nhóm soạn sẵn từ transcript (phần mock, người duyệt) — AI chỉ làm phần chấm. · **Willing users (ngoài nhóm):** 1. Lương Quang Huy · 2. Hà Mạnh Tuân |
| 7 | **Phân công có tên** | **Nguyễn Vũ Huy** (đội trưởng) — spec, nộp form, slide + demo, điều phối validation · **Đào Ngọc Bình Thiên** — evidence: mining chatlog K4 + khảo sát ≥20 người + bảng impact · **Nguyễn Nguyên Phong** — prompt chấm bài + golden set ≥20 câu trả lời có nhãn + đo % · **Đỗ Thái Sơn** — code prototype (UI nộp bài → gọi AI thật → hiển thị kết quả + trích dẫn, trace log) + video CP3/CP5 |

## Ghi chú nội bộ (không cần nộp)

- **Vì sao chấm bài là quyết định trung tâm (không phải sinh bài tập):** một quyết định AI rõ ràng (đúng/một phần/sai) → golden set dễ xây và dễ đo: 20+ câu trả lời học viên với nhãn ground truth do nhóm gán, so với verdict AI. Sinh bài tập để mock (soạn sẵn 5–8 câu/buổi từ transcript, người duyệt).
- **4 lớp chỗ khó áp vào lát cắt:** ① *nguồn sự thật* — AI chấm dựa trên kiến thức ngoài bài, không trích được đoạn · ② *mơ hồ* — câu trả lời nửa vời, quá ngắn, sai chính tả thuật ngữ · ③ *ngoài phạm vi* — học viên hỏi xin đáp án luôn, dán code, "bỏ qua hướng dẫn trước đó" · ④ *domain* — chấm "đúng" cho câu sai khái niệm → học viên học sai ngay.
- **Golden set (eval/) dự kiến:** ≥20 câu trả lời: 8–10 thường (đúng rõ / sai rõ) · ≥2 mỗi lớp chỗ khó · 2–4 hiếm (bỏ trống, trả lời bằng tiếng Anh, trả lời đúng nhưng transcript thiếu). Chiều đo: verdict đúng nhãn? · có trích dẫn đúng đoạn? · không bịa nội dung ngoài transcript?
- **Ứng viên cho bảng impact §2 (≥3):** (a) *bài tập + chấm theo buổi* (chọn) · (b) *bản đồ lỗ hổng của lớp cho giảng viên* từ chatlog · (c) *tutor không bịa khi hỏi ngoài phạm vi* (28% không trích dẫn) — giữ lại làm ứng viên đã loại, ghi lý do.
- **Hard tests từ đề A2 phải cân nhắc:** data thưa (buổi ít câu hỏi) · câu mẫu chiếm đa số · hai đoạn transcript cùng nói một khái niệm · signal nhiễu.
- **Ràng buộc đạo đức (đề A):** không lộ ai hỏi gì · không đưa data ra ngoài pack · AI không "đoán chắc" khi không có căn cứ · giảng viên quyết nội dung dạy (bộ bài tập do người duyệt).
