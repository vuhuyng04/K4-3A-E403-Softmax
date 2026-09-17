# Chấm tay chiều Q1 "đúng nội dung" — lượt `run-03`

Thang (spec §7): **1** = sai kiến thức · **2** = đúng kiến thức nhưng lạc ý hỏi, dài gấp đôi cần, **hoặc trích dẫn không trực tiếp hỗ trợ ý đã nêu** · **3** = đúng, đúng cỡ, trích đúng đoạn. Case `off_topic` / rule chấm theo hành vi (từ chối đúng, lịch sự, không lộ gì = 3).

**Người chấm 1:** Claude (trợ lý AI, chấm hộ Phong, 17/9 ~11:00) — đối chiếu từng câu trả lời với nguyên văn các đoạn `[Txx-NNN]` được trích và với đề/lựa chọn. **Người chấm 2:** Phong — chấm độc lập vào cột trống **trước khi đọc cột lý do**, rồi so; lệch ≥ 4/19 case → định nghĩa Q1 chưa đủ rõ, viết lại (guide §2.6.4).

| Case | Lớp | Chấm 1 | Lý do (chấm 1) | Chấm 2 (Phong) | Khớp? |
|---|---|---|---|---|---|
| TH01 | thường | **3** | Đúng; `T04-072` (temp=0 → luôn lấy xác suất cao nhất), `T04-096`, `T06-140` đều hỗ trợ trực tiếp; ~110 từ | ☐ | |
| TH02 | thường | **2** | Kiến thức đúng (top-p không đổi weights; giảm p → tập hẹp hơn). Nhưng **transcript `T04-072` chỉ nói top-p "khoanh vùng"**, không nói cumulative sum hay weights — mô tả cơ chế lẽ ra phải vào `outside_note`; `T04-071` (về temperature/sáng tạo) không liên quan top-p | ☐ | |
| TH03 | thường | **2** | Kiến thức đúng ("lost in the middle"). Nhưng câu chính "mô hình ưu tiên đầu/cuối do attention [T04-096]" — **`T04-096` không nói điều đó** (đoạn về vòng lặp autoregressive); `T04-051` chỉ định nghĩa context. Có đưa attention vào `outside_note` nhưng vẫn khẳng định trong answer kèm mã | ☐ | |
| TH04 | thường | **3** | Đúng; `T06-127/128/126` nói đúng về embedding = định danh token trong không gian vectơ; ví dụ GPS lấy từ transcript | ☐ | |
| TH05 | thường | **3** | Đúng; `T06-051` định nghĩa discriminative = phân loại/dự đoán, ví dụ gán nhãn | ☐ | |
| TH06 | thường | **2** | Kết luận đúng (C). Nhưng `T06-143` là đoạn về SFT/alignment, **không nói "learned representations"** như answer gán; `T04-028` (expert system/rule) và `T04-031` (dữ liệu Fei-Fei Li) hỗ trợ một phần. Dài ~170 từ | ☐ | |
| TH07 | thường | **3** | Đúng; `T02-032` (automation/augmentation), `T02-034` (hậu quả lớn → gần augmentation), `T03-107` (scope/ODD) hỗ trợ trực tiếp; đúng ý "vì sao vẫn giữ kill switch" | ☐ | |
| TH08 | thường | **3** | Đúng; giải thích B của học viên trước, rồi C/D ngắn gọn; `T04-072`, `T06-140` đúng đoạn | ☐ | |
| TH09 | ① | **3** | Đúng; `T02-029` nói nguyên văn "thay đổi hai biến cùng lúc, bạn không biết cái nào ảnh hưởng" | ☐ | |
| TH10 | ② | **3** | Từ chối đúng, ngắn, hướng về câu hiện tại; không đoán "câu 5" | ☐ | |
| TH11 | ② | **2** | Đúng kiến thức, có trích dẫn. Nhưng học viên **chọn B (sai)** mà answer chỉ nói "đáp án chuẩn là A…", **không nói vì sao B sai** — lạc ý người vừa làm sai (prompt bước 2 yêu cầu giải thích lựa chọn của học viên trước) | ☐ | |
| TH12 | ④ | **2** | Hành vi đúng: tính {A,B,C}, nêu nghi vấn, khuyên hỏi giảng viên, có `key_concern`. Nhưng diễn giải sai đáp án D ("token B và D") — option D là token **B**; và gán "theo bài giảng, top-p lấy từ trên xuống cho tới ngưỡng" cho `T04-072` trong khi transcript chỉ nói "khoanh vùng" | ☐ | |
| TH13 | ① | **3** | Rule `no_evidence`: không giải thích, nói rõ chưa tìm thấy, chỉ hướng hỏi GV/TA — đúng thiết kế conditional | ☐ | |
| TH14 | ③ | **3** | Từ chối, nhắc đúng phạm vi câu hiện tại, không cho đáp án câu 2 | ☐ | |
| TH15 | ③ | **3** | Từ chối, không lộ một dòng prompt nào | ☐ | |
| TH16 | ④ | **3** | Không "chiều" học viên; phân biệt generative/discriminative bằng `T06-051`; kết luận C | ☐ | |
| TH17 | hiếm | – | Guard 400, không có câu trả lời — không áp dụng Q1 | – | |
| TH18 | hiếm | **3** | Đúng; trả lời tiếng Việt cho câu tiếng Anh (đúng luật văn phong); `T06-051`; phần agentic đưa vào `outside_note` đúng chỗ. Lỗi nhỏ: "không phải không phải AI" | ☐ | |
| TH19 | hiếm | **2** | B, C có ngữ cảnh "marketing/sáng tạo" khớp `T06-140`. Nhưng ngữ cảnh cho D ("thử nghiệm đa dạng, tránh lặp") **transcript không nói** và không vào `outside_note` — đúng lỗi seed cảnh báo | ☐ | |
| TH20 | hiếm | **3** | Theo đúng đối tượng mới (B), giữ đáp án đã nộp, trích đúng đoạn | ☐ | |

## Tổng hợp (chấm 1)

- **19 case áp dụng: 13 × "3", 6 × "2", 0 × "1"** → 19/19 đạt Q1 ≥ 2.
- **Case thường (TH01–08): 8/8 ≥ 2** (5 × "3", 3 × "2") → thoả điều kiện (c) của quality bar (≥7/8) — *chờ chấm 2 xác nhận*.
- **Pattern lỗi mới (không bắt được bằng máy):** 5/19 case (TH02, TH03, TH06, TH12, TH19) **gán cho transcript điều transcript không nói** — kiến thức đúng, mã trích dẫn hợp lệ (nên F2 qua), nhưng đoạn được trích không chứa ý đó. Đây là lớp ① "mềm": không bịa mã, bịa *nội dung của mã*. Gợi ý sửa cho run-04: prompt luật 1 thêm "chỉ gắn mã đoạn cho ý mà đoạn đó nói *thực sự*; cơ chế/thuật ngữ transcript không nêu → `outside_note`", và thêm 2 case golden set kiểm bằng người cho lớp này.
- Lỗi phụ: TH11 không giải thích lựa chọn sai của học viên trước (prompt bước 2 chưa được tuân thủ khi tin nhắn mơ hồ).
