# Định nghĩa cấu trúc cơ sở dữ liệu bằng code

from django.db import models # module cốt lõi của Django
from django.contrib.auth.models import User
# Django cung cấp sẵn một hệ thống quản lý người dùng (Authentication System) cực kỳ mạnh mẽ. 
# Lệnh này gọi ra bảng User mặc định của Django (bảng này đã chứa sẵn các cột như username, password, email...).

class Todo(models.Model):
    
    # 1. Liên kết người dùng
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    # Khai báo khóa ngoại: Quan hệ One-to-many (một user có thể có nhiều Todo)
        # models.ForeignKey(User, ...) - trỏ tới bảng User đã import
        # on_delete=models.CASCADE - Nếu User bị xóa thì xóa toàn bộ các Todo thuộc về User đó
        # related_name="todos" - cho phép User tra cứu ngược các Todo của mình
        # có thể gọi my_user.todos.all() để lấy danh sách toàn bộ task của người dùng đó.
       
    # 2. Cột tiêu đề công việc
    title = models.CharField(max_length=200)
    # Định nghĩa một cột lưu trữ văn bản độ dài tối đa 200 ký tự
    
    # 3. Cột trạng thái hoàn thành
    completed = models.BooleanField(default=False)
    # Định nghĩa cột lưu giá trị Đúng/Sai (Hoàn thành/Chưa hoàn thành)
    # Mặc định là False
    
    # 4. Thời gian tạo
    created_at = models.DateTimeField(auto_now_add=True)
    # models.DateTimeField - Cột lưu trữ ngày và giờ.
    # (auto_now_add=True) - Tự động lấy giờ hiện tại của hệ thống và điền vào

    # Định nghĩa cách hiển thị (String Representation)
    def __str__(self):
        return self.title
    # Yêu cầu hiện thị nội dung của cột title