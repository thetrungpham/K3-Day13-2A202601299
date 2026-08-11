
# Alert và Runbook

## Dashboard specification

- Công cụ: Dashboard specification dựa trên endpoint `/metrics`.
- Khoảng thời gian mặc định: 1 giờ.
- Auto-refresh đề xuất: 30 giây.
- Nguồn dữ liệu: `GET /metrics`.
- Lớp dashboard chính gồm 6 panel.

### 1. Latency P50/P95/P99

- Tên panel: `Request latency percentiles`.
- Loại: Line chart hoặc 3 single values.
- Dữ liệu: `latency_p50`, `latency_p95`, `latency_p99`.
- Đơn vị: milliseconds (ms).
- Khoảng thời gian: 1 giờ.
- SLO/threshold: `latency_p95 <= 3000 ms`; warning khi P95 > 3000 ms.

### 2. Traffic

- Tên panel: `Request traffic`.
- Loại: Counter hoặc time-series.
- Dữ liệu: `traffic`.
- Đơn vị: requests.
- Khoảng thời gian: 1 giờ.
- Threshold: theo dõi traffic giảm về 0 hoặc tăng đột biến so với baseline.

### 3. Error

- Tên panel: `Error rate and error breakdown`.
- Loại: Single value cho error rate và table cho breakdown.
- Dữ liệu: `error_rate_pct`, `error_breakdown`.
- Đơn vị: percent (%) và request count.
- Khoảng thời gian: 1 giờ.
- SLO/threshold: `error_rate_pct <= 2%`; critical khi > 5% trong 3 phút.

### 4. Cost

- Tên panel: `LLM cost`.
- Loại: Single values hoặc line chart.
- Dữ liệu: `total_cost_usd`, `avg_cost_usd`.
- Đơn vị: USD.
- Khoảng thời gian: 1 giờ, đồng thời theo dõi tổng chi phí ngày.
- SLO/threshold: `daily_cost_usd <= 2.5 USD`.

### 5. Tokens

- Tên panel: `Token consumption`.
- Loại: Counter hoặc stacked bar chart.
- Dữ liệu: `tokens_in_total`, `tokens_out_total`.
- Đơn vị: tokens.
- Khoảng thời gian: 1 giờ.
- Threshold: điều tra khi token output tăng bất thường so với traffic.

### 6. Quality

- Tên panel: `Average quality score`.
- Loại: Gauge hoặc line chart.
- Dữ liệu: `quality_avg`.
- Đơn vị: score từ 0 đến 1.
- Khoảng thời gian: 1 giờ.
- SLO/threshold: `quality_avg >= 0.75`; cảnh báo khi thấp hơn ngưỡng

# Yêu cầu dashboard

Contract có thể kiểm tra bằng máy nằm tại `config/dashboard.yaml`. Hướng dẫn dựng và kiểm tra runtime nằm tại [DASHBOARD_SETUP.md](DASHBOARD_SETUP.md).

Dashboard chính cần đủ 6 nhóm thông tin:

1. Latency P50/P95/P99.
2. Traffic: request count hoặc QPS.
3. Error rate và breakdown theo loại lỗi.
4. Cost theo thời gian.
5. Tổng token input/output.
6. Quality proxy.

Tiêu chuẩn trình bày:

- Khoảng thời gian mặc định: 1 giờ.
- Tự refresh mỗi 15–30 giây nếu công cụ hỗ trợ.
- Có threshold hoặc SLO line.
- Ghi rõ đơn vị.
- Chỉ giữ 6–8 panel quan trọng ở lớp chính.
- Screenshot phải nhìn được tên panel và khoảng thời gian.

Kiểm tra contract trước khi chụp evidence:

```bash
python scripts/validate_dashboard.py
```
