from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo # import Todo từ models

# Serializer đóng vai trò là
# "Người phiên dịch" và "Nhân viên đóng gói" giữa Django (Python Object) và React (JSON).

# class xử lý đăng ký người dùng
# tiếp nhận dữ liệu đăng ký từ React (username, password), kiểm tra tính hợp lệ và tạo tài khoản mới
class UserSerializer(serializers.ModelSerializer): #kế thừa lớp này để Django REST Framework (DRF) tự động xây dựng các logic xử lý dựa trên Model User

    # Lớp cấu hình class Meta
    class Meta:
        model = User # chỉ định Serializer này sẽ làm việc vói bảng dữ liệu User của Django
        fields = ["id", "username", "password"]
        # định nghĩa các trường dữ liệu và React và Django sẽ trao đổi với nhau
        # Khi React gửi dữ liệu đăng ký lên, nó phải gửi đủ username và password.
        # Khi Django tạo xong, nó sẽ trả về id và username.
        extra_kwargs = {"password": {"write_only": True}}
        # code bảo mật write_only": True nghĩa là trường password này chỉ được phép gửi lên (Ghi) lúc đăng ký.

    # Hàm khởi tạo User nâng cao
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # User.objects.create_user: Đây là hàm đặc biệt của Django.
        # Nó sẽ tự động kích hoạt thuật toán băm mật khẩu (Password Hashing) (ví dụ: PBKDF2).
        # Chuỗi 123456 sẽ biến thành một chuỗi loằng ngoằng không thể giải mã trước khi lưu vào SQLite.
        return user

# Xử lý công việc CRUD
# Serializer này đơn giản hơn rất nhiều, dùng để đóng gói dữ liệu của các Task Todo để gửi
# cho React hiển thị, hoặc tiếp nhận dữ liệu sửa/xóa từ React gửi lên.
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo # liên kết trực tiếp với model = Todo trong models.py
        fields = ["id", "title", "completed", "created_at"] 
        # Quy định các thông tin sẽ lộ ra cho Frontend thấy và chỉnh sửa.