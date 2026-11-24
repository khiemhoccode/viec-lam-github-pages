# Việc làm AI · IoT · Nhúng · TP.HCM

## Đưa lên github.io
1. Tạo repo mới trên GitHub (ví dụ `viec-lam`), tải toàn bộ file trong thư mục này lên (giữ nguyên thư mục `.github/workflows`).
2. Settings → Pages → Source: "Deploy from a branch" → Branch `main` / `(root)` → Save.
3. Sau 1–2 phút trang có tại `https://<tên-github>.github.io/viec-lam/`.

## Bật tự động cập nhật mỗi ngày (Tavily, miễn phí)
1. Vào https://app.tavily.com, đăng ký (Google/GitHub/email), copy **API key** (dạng `tvly-...`) trong trang Dashboard.
2. Repo → Settings → Secrets and variables → Actions → New repository secret: tên `TAVILY_API_KEY`, dán key vào.
3. Tab Actions → "Cập nhật tin tuyển dụng" → Run workflow để chạy thử. Từ đó nó tự chạy lúc 08:00 mỗi ngày.

Script dùng 8 truy vấn/ngày (~240/tháng), nằm trong gói miễn phí 1.000 credit/tháng. Nút "Cập nhật danh sách" trên trang tải lại `jobs.json`, mỗi ngày bấm 1 lần.
Tin do script thêm có thể thiếu tên công ty/lương, hãy mở link để xem chi tiết. Tin tự động cũ hơn 30 ngày bị xóa; 13 tin chọn tay ban đầu được giữ lại.
