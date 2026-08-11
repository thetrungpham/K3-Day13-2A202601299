# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: 4aesieunhan
- Repository URL: (https://github.com/thetrungpham/K3-Day13-2A202601299)
- Commit SHA cuối: f23ae2f
- Thành viên và vai trò:
  - Vũ Thành Dương (2A202602007): CP1 (PII)
  - Lê Thành Nam (2A202601397): CP1 (Correlation ID, gán log metadata)
  - Chu Phú Thành (2A202601289): CP2 (Tích hợp Langfuse, đo đếm error_rate_pct, viết SLO, Alert rules và Runbook)
  - Phạm Thế Trung (2A202601299): CP3 (Điều tra Challenge)

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100
- Tổng số traces: 75 
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: https://cloud.langfuse.com/project/cmso2s1r203qhad0iir54fnmo/dashboards

## 3. Logging và tracing

- Evidence correlation ID: req-f592c8dd
- Evidence PII redaction: {"service": "api", "payload": {"message_preview": "What is the policy for PII and credit card [REDACTED_CREDIT_CARD]?"}, "event": "request_received", "correlation_id": "req-f592c8dd", "model": "claude-sonnet-4-5", "user_id_hash": "4d14d5d4f719", "env": "dev", "session_id": "s09", "feature": "qa", "level": "info", "ts": "2026-08-11T08:40:13.766069Z"}
- Evidence trace waterfall: ![trace-waterfall.png](trace-waterfall.png)
- Giải thích một span đáng chú ý: `retrieve_docs` mất thời gian bất thường

## 4. Prompt versioning

- Prompt name: day13-chat
- Version/label baseline: v1 / `baseline` 
- Version/label candidate: v2 / `candidate`
- Trace ID của mỗi version:  
  - Baseline v1: `00bd4bb6d28bcaa159ffb91c0fb5307`
  - Candidate v2: `8c8ca2186bfc9752c918f6b942e81d4`
- Bằng chứng đổi label hoặc rollback: Đã promote v2 lên label `production`, sau đó rollback label `production` về v1. Evidence: `submission/evidence/prompt-production-rollback-v1.png`.

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: ![validate_result.png]
- Evidence dashboard: https://cloud.langfuse.com/project/cmso2s1r203qhad0iir54fnmo/dashboards/langfuse-home-dashboard
- SLO đã chọn và lý do: Chọn latency_p95_ms (Objective: 3000ms, Target: 99.5%). Lý do: Với API tương tác trực tiếp (chat), thời gian phản hồi (latency) đặc biệt quan trọng cho trải nghiệm người dùng; việc duy trì 99.5% lượng request dưới 3 giây là tiêu chuẩn hợp lý.
- Alert rules và runbook: Cảnh báo high_latency_p95 (kích hoạt khi latency_p95_ms > 3000 liên tục trong 5 phút). Cách xử lý (Runbook) tham khảo tại docs/alerts.md#alert-1.

## 6. Điều tra challenge

- Challenge ID: `day13-k3-observability-v1`
- Triệu chứng từ metrics: P99 Latency của hệ thống tăng vọt lên trên 2500ms khi request các câu hỏi liên quan đến feature `refund`.
- Trace ID liên quan: `req-f592c8dd` (Trace trên Langfuse cho thấy Span `retrieve_docs` tốn thời gian bất thường).
- Log line/correlation ID liên quan: `req-f592c8dd`
- Root cause: Có sự cố xảy ra ở Component Retriever. Cụ thể trong file `app/mock_rag.py`, cờ sự kiện `rag_slow` đã được kích hoạt, dẫn đến hàm `retrieve()` bị delay cưỡng bức bằng `time.sleep(2.5)`. Điều này làm toàn bộ quy trình RAG bị nghẽn.
- Fix action: Tắt tính năng mô phỏng sự cố bằng cách đưa biến `rag_slow` về `False` trong hệ thống (hoặc khởi động lại/scale up dịch vụ vector database trong thực tế).
- Preventive measure: 
  - Đặt timeout tối đa (ví dụ 1000ms) cho bước gọi RAG/VectorDB, nếu quá thời gian sẽ ngắt và fallback.
  - Thiết lập Alert rules cảnh báo ngay khi P90 Latency của riêng Span Retrieval vượt mức 1.5 giây.
  - Cấu hình circuit breaker để bảo vệ hệ thống nếu RAG chậm kéo dài.

## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Vũ Thành Dương (2A202602007) | Làm phần CP1 về xử lý và bảo vệ PII (Redaction) | sercurity and compliance | Cách sử dụng RegEx để giấu dữ liệu nhạy cảm trong log. |
| Lê Thành Nam (2A202601397) | CP1: Sinh và truyền Correlation ID xuyên suốt request, gán log metadata. | A update | Hiểu được tầm quan trọng của Context Variables và Correlation ID trong việc truy vết. |
| Chu Phú Thành (2A202601289) | CP2: Tích hợp Langfuse, tạo dashboard đo error_rate_pct, thiết kế SLO, Alert rules & Runbook. | hoan thien cp2 | Cách xác định ngưỡng SLO hợp lý và quy trình xử lý sự cố qua Runbook. |
| Phạm Thế Trung (2A202601299) | CP3: Điều tra incident, trace span, phân tích log để tìm ra root cause (`rag_slow`), đề xuất giải pháp. | update: CP3, Update commit SHA in REPORT.md | Cách kết hợp Metrics -> Traces -> Logs để phân tích lỗi hệ thống thực tế. |
