# eval/

Golden set + kết quả các lượt chạy. Định nghĩa "đạt" từng chiều và quality bar: `spec.md` §7.

| File | Nội dung |
|---|---|
| `thien-case-seeds.csv` | 20 seed case do Thiên phát triển từ chatlog K4 (mô tả hành vi kỳ vọng, chưa chạy được) |
| `golden-set.csv` | 20 case chạy được: input cụ thể (`qid`, `chosen`, `message`, `harness`) + nhãn kỳ vọng tự kiểm (`expected_*`) |
| `run_eval.py` | Chạy golden set qua đúng code path của app (`codebase/server/app.py::tutor`), kiểm tự động, xuất bảng |
| `runs/run-NN.md` | Bảng kết quả **đủ mọi case** của từng lượt (kể cả fail/lỗi) + câu trả lời AI để người chấm đối chiếu |
| `runs/run-NN.jsonl` | Output thô của lượt đó |

## Chạy một lượt đo

```bash
# ở thư mục gốc repo; cần data/ của BTC và codebase/.env có GEMINI_API_KEY
python codebase/scripts/build_data.py
python eval/run_eval.py --label run-01
```

Sau khi chạy: hai người chấm độc lập cột `human` (chiều Q1, thang 1–3) trên `runs/run-NN.md`, so kết quả, rồi ghi tổng hợp % vào `spec.md` §7 và failure đau nhất → sửa → chạy lại **trọn bộ**.

Case trích từ data pack chỉ ghi **mã hội thoại** (`source_turn_id`), không dán nguyên văn dài.
