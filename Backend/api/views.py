# views.py - Nơi tiếp nhận các yêu cầu (Requests) từ React
# Kiểm tra ai có quyền vào
# Xử lý Logic (Lọc task, gán tên người dùng)
# Quyết định dữ liệu trả về

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
# AllowAny - Mở cửa hoàn toàn, ai cũng vào được (dùng cho Đăng ký/Đăng nhập).
# IsAuthenticated - Chỉ những ai có Token hợp lên trên Header mới được phép truy cập
from django.contrib.auth.models import User
from .models import Todo
from .serializers import UserSerializer, TodoSerializer

# Xử lý đăng ký
class CreateUserView(generics.CreateAPIView):
    # generics.CreateAPIView - Tiếp nhận request POST để tạo mới một đối tượng (ở đây là tạo User).
    queryset = User.objects.all() # chỉ cho DRF biết no sẽ thao tác trên bảng dữ liệu User
    serializer_class = UserSerializer # chỉ định Serializer kiểm tra dữ liệu đầu vào và băm mật khẩu
    permission_classes = [AllowAny] # chức năng đang ký tài khoản cần phải cho phép tất cả mọi người gọi API

# CRUD
# kế thừa lớp viewsets.ModelViewSet cho các hành động xem danh sách, xem chi tiết, thêm, sửa
# thay vì viết 4, 5 class riêng biệt
class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer 
    permission_classes = [IsAuthenticated] 
    # bất kỳ ai gọi vào các API thuộc ViewSet này (đọc, thêm, sửa, xóa)
    # đều phải chia ra một access_token hợp lệ

    # Hàm phân tách dữ liệu và đọc trạng thái
    def get_queryset(self):
        user = self.request.user # nhờ Token gửi lên, Django giải mã và biết chính xác ai đang gọi API và
                                 # gán vào biến User
        queryset = Todo.objects.filter(user=user) # đảm bảo chỉ nhìn thấy task do chính mình tạo ra
        
        status = self.request.query_params.get('status')
        # bắt các tham số truyền trên thanh URL từ React gửi lên
        if status == 'completed': # nếu status == 'completed' -> Lọc các task đã hoàn thành
            queryset = queryset.filter(completed=True)
        elif status == 'pending': # nếu status == 'pending' -> Lọc các task chưa hoàn thành
            queryset = queryset.filter(completed=False)
            
        return queryset.order_by('-created_at') # sắp xếp ngược, việc gì mới tạo sẽ được đẩy lên trên cùng

    # Hàm tự động gán chủ sở hữu
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)