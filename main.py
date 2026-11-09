from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(
    title="SportBook API",
    description="Ứng dụng FastAPI đơn giản quản lý đặt sân thể thao (SportBook) với đầy đủ CRUD và các phương thức cơ bản.",
    version="1.0.0"
)

# Model định nghĩa dữ liệu đầu vào / đầu ra
class BookingBase(BaseModel):
    customer_name: str = Field(..., example="Nguyễn Văn A", description="Tên khách hàng")
    sport_type: str = Field(..., example="Bóng đá", description="Môn thể thao: Bóng đá, Cầu lông, Tennis,...")
    court_number: int = Field(..., ge=1, example=1, description="Số sân")
    booking_hours: float = Field(..., gt=0, example=2.0, description="Số giờ đặt")

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    customer_name: Optional[str] = Field(None, example="Nguyễn Văn B")
    sport_type: Optional[str] = Field(None, example="Cầu lông")
    court_number: Optional[int] = Field(None, ge=1, example=2)
    booking_hours: Optional[float] = Field(None, gt=0, example=1.5)

class BookingResponse(BookingBase):
    id: int
    total_price: float

    class Config:
        from_attributes = True

# Bộ nhớ tạm (In-memory database)
fake_db = [
    {
        "id": 1,
        "customer_name": "Nguyễn Văn A",
        "sport_type": "Bóng đá",
        "court_number": 1,
        "booking_hours": 2.0,
        "total_price": 200000.0,
    },
    {
        "id": 2,
        "customer_name": "Trần Thị B",
        "sport_type": "Cầu lông",
        "court_number": 3,
        "booking_hours": 1.5,
        "total_price": 120000.0,
    }
]

HOUR_RATE = 100000.0  # 100,000 VNĐ / giờ

# 1. GET (Trang chủ / Root)
@app.get("/", tags=["General"])
def read_root():
    return {
        "message": "Chào mừng đến với SportBook API!",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# 2. GET (Lấy danh sách, hỗ trợ lọc theo môn thể thao qua Query Parameter)
@app.get("/bookings", response_model=List[BookingResponse], tags=["Bookings"])
def get_bookings(sport: Optional[str] = None):
    if sport:
        filtered = [b for b in fake_db if b["sport_type"].lower() == sport.lower()]
        return filtered
    return fake_db

# 3. GET (Lấy chi tiết một lượt đặt sân qua Path Parameter)
@app.get("/bookings/{booking_id}", response_model=BookingResponse, tags=["Bookings"])
def get_booking(booking_id: int):
    for item in fake_db:
        if item["id"] == booking_id:
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy lịch đặt với ID {booking_id}"
    )

# 4. POST (Tạo mới lượt đặt sân)
@app.post("/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, tags=["Bookings"])
def create_booking(payload: BookingCreate):
    new_id = (fake_db[-1]["id"] + 1) if fake_db else 1
    new_booking = {
        "id": new_id,
        "customer_name": payload.customer_name,
        "sport_type": payload.sport_type,
        "court_number": payload.court_number,
        "booking_hours": payload.booking_hours,
        "total_price": payload.booking_hours * HOUR_RATE,
    }
    fake_db.append(new_booking)
    return new_booking

# 5. PUT (Cập nhật toàn bộ hoặc một phần)
@app.put("/bookings/{booking_id}", response_model=BookingResponse, tags=["Bookings"])
def update_booking(booking_id: int, payload: BookingUpdate):
    for item in fake_db:
        if item["id"] == booking_id:
            update_data = payload.model_dump(exclude_unset=True)
            item.update(update_data)
            # Tính lại giá nếu có cập nhật số giờ
            if "booking_hours" in update_data:
                item["total_price"] = item["booking_hours"] * HOUR_RATE
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy lịch đặt với ID {booking_id}"
    )

# 6. DELETE (Xóa một lượt đặt sân)
@app.delete("/bookings/{booking_id}", status_code=status.HTTP_200_OK, tags=["Bookings"])
def delete_booking(booking_id: int):
    for index, item in enumerate(fake_db):
        if item["id"] == booking_id:
            deleted_item = fake_db.pop(index)
            return {"message": f"Đã xóa thành công lịch đặt ID {booking_id}", "data": deleted_item}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy lịch đặt với ID {booking_id}"
    )
