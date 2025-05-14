from pydantic import BaseModel
from typing import Dict, Optional, Any # Any cho phép các giá trị bất kỳ trong dictionary đầu vào

# Model Pydantic này được thiết kế để đại diện cho cấu trúc dữ liệu
# mà hàm `filter_data` của bạn trả về.
class FilteredPetData(BaseModel):
    # Các trường này dựa trên các key trong dictionary được trả về
    # bởi hàm `filter_data` của bạn.

    id: int  # Tương ứng với 'ad_id', giả định rằng trường này luôn tồn tại và là số nguyên sau khi lọc.
             # Nếu `raw_data.get("id")` trả về None, Pydantic sẽ báo lỗi Validation khi khởi tạo.

    list_time: Optional[int] = None   # Timestamp (milliseconds), đã chuyển sang giờ Việt Nam
    list_time_sec: Optional[int] = None # Timestamp (seconds), đã chuyển sang giờ Việt Nam
    subject: Optional[str] = None     # Tiêu đề của tin đăng
    param_value: Optional[str] = None       # Giá trị từ 'param' đầu tiên (ví dụ: "Chó Poodle")
                                      # (Lưu ý: key trong dict là "param")
    price_string: Optional[str] = None # Giá dạng chuỗi (ví dụ: "4.000.000 đ")
    price: Optional[int] = None       # Giá dạng số (ví dụ: 4000000). Có thể là Optional[float] nếu giá có thể là số thập phân.
    area_name: Optional[str] = None   # Tên khu vực (ví dụ: "Quận 6")
    date_string: Optional[str] = None        # Chuỗi ngày tương đối (ví dụ: "8 phút trước")
                                      # (Lưu ý: key trong dict là "date")
    seller_name: Optional[str] = None # Tên người bán
    average_rating: Optional[float] = None # Đánh giá trung bình (ví dụ: 4.4)
    sold_ads: Optional[int] = None    # Số lượng tin đã bán
    image_url: Optional[str] = None       # URL của hình ảnh đầu tiên
                                      # (Lưu ý: key trong dict là "image")
    category_name: Optional[str] = None # Tên danh mục (ví dụ: "Chó")

    @classmethod
    def from_raw_data(cls, raw_data: Dict[str, Any]) -> 'FilteredPetData':
        """
        Tạo một instance của FilteredPetData từ một dictionary.
        Dictionary `raw_data` này được kỳ vọng là kết quả trả về
        từ hàm `filter_data` ban đầu của bạn.

        Pydantic sẽ tự động kiểm tra kiểu dữ liệu:
        - Nếu 'id' bị thiếu trong `raw_data` hoặc không phải là số nguyên, một lỗi ValidationError sẽ được nêu ra.
        - Đối với các trường Optional, nếu key tương ứng không có trong `raw_data`
          hoặc giá trị của nó là None, trường đó sẽ được gán giá trị mặc định là None.
        """
        # Cách tiếp cận này lấy giá trị cho từng trường một cách tường minh,
        # tương tự như ví dụ BookData bạn cung cấp.
        # Pydantic sẽ thực hiện việc kiểm tra kiểu khi cls(...) được gọi.
        return cls(
            id=raw_data.get("id"), # Nếu raw_data.get("id") là None, Pydantic sẽ báo lỗi vì `id: int` không phải Optional.
            list_time=raw_data.get("list_time"),
            list_time_sec=raw_data.get("list_time_sec"),
            subject=raw_data.get("subject"),
            param_value=raw_data.get("param_value"),
            price_string=raw_data.get("price_string"),
            price=raw_data.get("price"),
            area_name=raw_data.get("area_name"),
            date_string=raw_data.get("date_string"),
            seller_name=raw_data.get("seller_name"),
            average_rating=raw_data.get("average_rating"),
            sold_ads=raw_data.get("sold_ads"),
            image_url=raw_data.get("image_url"),
            category_name=raw_data.get("category_name"),
        )
