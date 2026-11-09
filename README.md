# SportBook - FastAPI Sample

Ứng dụng web API đơn giản bằng FastAPI minh họa các phương thức RESTful cơ bản (CRUD).

## 1. Cài đặt thư viện

Mở terminal và cài đặt các thư viện từ file `requirements.txt`:
```bash
pip install -r requirements.txt
```

## 2. Khởi chạy ứng dụng

Chạy ứng dụng với Uvicorn:
```bash
uvicorn main:app --reload
```

Server sẽ chạy mặc định tại: `http://127.0.0.1:8000`

## 3. Xem tài liệu Swagger UI & ReDoc

FastAPI tự động tạo tài liệu tương tác:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Cho phép test trực tiếp các API trên trình duyệt)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 4. Các phương thức đã triển khai

| Phương thức | Endpoint | Mô tả |
| :--- | :--- | :--- |
| **GET** | `/` | Trang chào mừng |
| **GET** | `/bookings` | Lấy danh sách (hỗ trợ lọc `?sport=Bóng đá`) |
| **GET** | `/bookings/{id}` | Lấy chi tiết lịch đặt theo ID |
| **POST** | `/bookings` | Tạo một lịch đặt mới (truyền Body JSON) |
| **PUT** | `/bookings/{id}` | Cập nhật thông tin lịch đặt |
| **DELETE** | `/bookings/{id}` | Xóa một lịch đặt |
