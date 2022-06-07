# __ĐỒ ÁN NHẬP MÔN CÔNG NGHỆ PHẦN MỀM - SE104.M23__ 
__QUẢN LÝ PHIẾU TIẾT KIỆM__

__NHÓM 17__

TÊN THÀNH VIÊN | MSSV 
 ------------ | ------------- 
BÙI THANH TRÀ ___(Nhóm trưởng)___ | 19522370
VŨ HỮU TÙNG | 19522497
NGUYỄN THỊ MAI PHƯƠNG | 19522063
NGUYỄN ĐẠI KỲ | 19521731
NGÔ ĐỨC THIỆN | 19522261

# __CÁC BƯỚC ĐỂ RUN SOURCE CODE__
## 1: Tạo môi trường ảo
## 2: Cài đặt các thư viện cần thiết trong file requirements 
```
pip install requirements.txt
```
## 3: Tạo database 
- Tạo database với các thông tin như sau:
  - Tên database: quan_ly_phieu_tiet_kiem
  - Username: banking_dev
  - Password: asdfghjkl01
  - Host: '127.0.0.1'
  - PORT: '3306'
- Run script sql trong forder database để tạo các bảng, ràng buộc, khóa và dữ liệu demo
## 4: Tạo ra các 3 Nhóm user cở bản sử dụng website
```
python manage.py group_permissions
```
## 5: Tạo một tài khoản để tiến hành đăng nhập vào hệ thống với quyền ADMIN
```
python manage.py createsuperuser
```
## 6: Runserver werbsite
```
python manage.py runserver
```
## 7: Tiến hành đăng nhập bằng tài khoản đã tạo ở bước 5 vào login site theo đường dẫn là http://127.0.0.1:8000/
## 8: Sau khi vào được admin site, ta chọn register để đăng ký tài khoản để sử dụng website
## 9: Sau khi đăng ký thành công tài khoản, ta đăng nhập tài khoản đã tạo và sử dụng các chức năng của website
