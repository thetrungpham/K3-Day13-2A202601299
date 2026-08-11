
## Alert 1

- Tên: High latency P95
- Severity: warning
- SLI/SLO liên quan: Latency P95 <= 3000 ms, mục tiêu 99.5%.
- Điều kiện và thời gian duy trì: latency_p95_ms > 3000 trong 5 phút.
- Ảnh hưởng tới người dùng: Phản hồi chat chậm, dễ gây timeout hoặc người dùng bỏ phiên.
- Ba bước kiểm tra đầu tiên:
  1. Kiểm tra panel latency, traffic và thời điểm P95 bắt đầu tăng.
  2. Mở trace chậm trong cùng khoảng thời gian để xác định span chiếm nhiều thời gian.
  3. Dùng correlation ID của trace để tìm log liên quan và xác nhận nguyên nhân.
- Mitigation tạm thời: Nếu incident practice đang bật, tắt incident; nếu không, chuyển tạm sang luồng fallback hoặc giảm tải request.
- Owner: on-call-engineer


## Alert 2

- Tên: Elevated error rate
- Severity: critical
- SLI/SLO liên quan: Error rate <= 2%, mục tiêu 99.0%.
- Điều kiện và thời gian duy trì: error_rate_pct > 5 trong 3 phút.
- Ảnh hưởng tới người dùng: Người dùng nhận lỗi hoặc không nhận được câu trả lời.
- Ba bước kiểm tra đầu tiên:
  1. Xem error-rate panel và breakdown theo error_type.
  2. Mở trace lỗi gần nhất để xác định span bị lỗi.
  3. Tìm log có correlation ID tương ứng để đọc error detail.
- Mitigation tạm thời: Tắt incident practice nếu đang bật; chuyển request sang fallback an toàn hoặc tạm giới hạn feature bị ảnh hưởng.
- Owner: on-call-engineer


## Alert 3

- Tên: Cost budget exceeded
- Severity: warning
- SLI/SLO liên quan: Daily cost <= 2.5 USD.
- Điều kiện và thời gian duy trì: daily_cost_usd > 2.5.
- Ảnh hưởng tới người dùng: Ngân sách vận hành tăng bất thường, có thể ảnh hưởng tính sẵn sàng lâu dài.
- Ba bước kiểm tra đầu tiên:
  1. So sánh traffic với tổng cost và token input/output trong cùng time range.
  2. Mở các trace có cost hoặc output token cao bất thường.
  3. Dùng log/correlation ID để kiểm tra model, feature và incident liên quan.
- Mitigation tạm thời: Tắt incident practice nếu đang bật; giới hạn output token hoặc chuyển tạm sang luồng/model chi phí thấp hơn.
- Owner: team-lead
