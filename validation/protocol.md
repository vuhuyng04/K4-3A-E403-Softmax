# Kịch bản vòng validation — 10 phút / người (guide §4.2)

**Mục tiêu:** xem học viên thật có *tự* tìm được chỗ mình hiểu sai và *tự* mở căn cứ trong bài giảng bằng prototype không — **không** hỏi "bạn thấy hay không".
**Cần:** 5 người ngoài nhóm, trong đó **2 willing user đã khai ở CP1** (Lương Quang Huy, Hà Mạnh Tuân). Làm trước **CP5 13:00 · 18/9**.
**Vai:** 1 người dẫn (đọc kịch bản, giao task), 1 người ghi (chỉ ghi, không nói). Đổi vai giữa các phiên để ai cũng có tên trong log.

## Chuẩn bị (2 phút trước mỗi phiên)

- [ ] `python codebase/server/app.py` đang chạy, mở `http://localhost:8000`, `/api/health` báo `has_key: true`.
- [ ] Trình duyệt ở **câu 2** (top-p), **chưa chọn đáp án**. Không mở sẵn khung tutor.
- [ ] Người ghi mở `validation/note-sheet.md` (copy một bản cho mỗi người thử), ghi giờ bắt đầu.
- [ ] Máy tính đưa cho người thử — **người thử tự cầm chuột** từ đầu đến cuối.

## 5 nhịp

| # | Nhịp | Người dẫn nói (đọc nguyên văn) | Người ghi ghi |
|---|---|---|---|
| 1 | **Comfort** ~1' | "Tụi mình đang đánh giá *sản phẩm*, không đánh giá bạn. Không có câu trả lời đúng/sai. Bạn cứ **nói to suy nghĩ** trong lúc dùng nhé." | — |
| 2 | **Context** ~1' | "Kể mình nghe **lần gần nhất** bạn làm quiz trên VLearn mà bị sai một câu — lúc đó bạn làm gì để hiểu vì sao sai? Mất bao lâu?" | Câu chuyện thật, nguyên văn (đây là evidence bổ sung cho §1) |
| 3 | **Task** ~1' | "Trên màn hình là một câu trắc nghiệm của khoá. Hãy **làm câu này, và nếu sai thì tìm hiểu mình hiểu sai ở đâu, rồi mở được đoạn bài giảng làm căn cứ để kiểm lại**. Xong thì nói mình biết." | Giờ bắt đầu task |
| 4 | **Observe** ~5' | **Im lặng.** Chỉ được dùng 3 câu cứu hộ khi người thử kẹt >20 giây: "Cứ nói to suy nghĩ nhé" · "Bạn sẽ làm gì tiếp?" · "Bạn nghĩ nó nên hoạt động thế nào?" **Cấm:** thuyết minh màn hình, giải thích nút/icon, hỏi "bạn có thích không". | **Hành động đầu tiên** · chỗ **do dự** (nhìn quanh, rê chuột không bấm) · chỗ **hiểu sai** (bấm nhầm, đọc sai nhãn) · chỗ **phải gợi ý** · có bấm **mã trích dẫn** không · có gõ tự do không, gõ gì · giờ xong task |
| 5 | **Hỏi sau khi dùng** ~2' | Đọc đúng 4 câu, ghi **nguyên văn** câu trả lời: ① "Điều gì **khó hiểu hoặc khó chịu nhất**?" ② "Kết quả AI đưa ra, bạn **có tin không — vì sao**?" ③ "Bạn **có dùng thật** không — vì sao / vì sao chưa?" ④ "Nếu từ mai không được dùng cái này nữa, bạn thấy: **rất tiếc / hơi tiếc / không sao**?" | 4 câu trả lời nguyên văn, kể cả nói tắt, nói sai |

Sau đó cảm ơn, **không** giải thích thêm về sản phẩm cho tới khi đã ghi xong.

## Đọc log — thang bằng chứng 4 tầng (mạnh → yếu)

1. **Hành vi quan sát được** (bấm gì, kẹt ở đâu, bỏ qua gì) — mạnh nhất
2. **Lời nói trong lúc dùng** ("ơ cái này là gì", "sao không thấy…")
3. **Giải thích khi được hỏi** (4 câu sau dùng)
4. **Dự đoán tương lai** ("mình sẽ dùng") — yếu nhất, chỉ là gợi ý

Mỗi hành động có **hai nghĩa** (PAIR 5.1) — ghi cả ngữ cảnh: bấm gợi ý lần 2 là *khám phá* hay *chưa hài lòng*? Gõ lại câu hỏi là *đào sâu* hay *bị hiểu sai*? **Bỏ qua** (không bấm mã trích dẫn, không đọc khung "ngoài bài giảng") gần như luôn là tiêu cực → ghi rõ.

## Mức nghiêm trọng

| Mức | Nghĩa |
|---|---|
| **3 · chặn** | Không hoàn thành task nếu không được gợi ý |
| **2 · vướng** | Hoàn thành nhưng do dự/nhầm >20 giây hoặc phải thử lại |
| **1 · nhỏ** | Nhận xét, không ảnh hưởng hoàn thành |
| **0 · trơn** | Làm được ngay |

## Sau 5 phiên

1. Chép 5 phiếu vào `validation/log.md` (mỗi người 1 dòng + 4 câu trả lời).
2. Viết **4 dòng tổng hợp** ở cuối `log.md`.
3. **≥1 thay đổi** → làm, ghi vào `spec.md` §9 Changelog kèm mã người thử (P1…P5). Giữ nguyên gì thì nói rõ vì sao.
4. Quote cho slide 5: chọn 2 quote **nói lúc đang làm việc** (tầng 1–2), không chọn lời khen.

> Nếu cả 5 phiên chỉ toàn lời khen → phiên chưa đạt: giao lại task khó hơn (câu 9 — đề lỗi, hoặc câu 7) hoặc đổi người.
