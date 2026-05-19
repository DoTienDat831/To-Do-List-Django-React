# Đóng vai trò là bản đồ của hệ thống Backend
# Khi Frontend React gửi một request lên Server, urls.py là nơi đầu tiên tiếp nhận thông tin, phân phối công việc

from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, TodoViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

# Tự động hóa URL bằng Router thay vì viết từng đường dẫn phức tạp cho các hành động
router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

# Các tuyến đường
urlpatterns = [
    path('admin/', admin.site.urls),
    # Đường dẫn trang quản trị, mở ra trang quản lý dữ liệu tối cao để quản lý User và các Task
    path('api/user/register/', CreateUserView.as_view(), name='register'),
    # Đường dẫn đăng ký Khi React gửi dữ liệu tài khoản mới qua phương thức POST tới api/user/register/
    # CreateUserView sẽ được kích hoạt để lưu User mới vào cơ sở dữ liệu.
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'), 
    # Đường dẫn đăng nhập (Login) - Khi người dùng nhập đúng Username và Password, nó sẽ tính toán và trả về 
    # access_token và refresh_token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    # Đường đãn đổi Refresh_token
    path('api/', include(router.urls)),
    # Nhúng toàn bộ Router vào hệ thống
]