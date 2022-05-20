from pyexpat import model # ???
from django.http import HttpResponse
from django.shortcuts import render, redirect
import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required # add login and permission required decorator
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,AccessMixin # add login and permission mixin 
from braces.views import GroupRequiredMixin # add GroupRequiredMixin to the class 
from django.views.generic.base import View
from django.db.models import Q
from admin_site import models 
from . import forms 
import random
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import *

# # Create group_required decorator
# def group_required(*group_names, login_url=None, raise_exception=False):
#     def check_permission(user):
#         if isinstance(group_names, six.string_types):
#             group_names = (group_names, )
#         else:
#             group_names = group_names
#         # fist check if user has the permission (even anon users)
    
#         if user.groups.filter(name__in=group_names).exists():
#             return True
#         # In case the 403 handler should be called raise the exception
#         if raise_exception:
#             raise PermissionDenied
#         # As the last resort, show the login form
#         return False
#     return user_passes_test(check_permission, login_url=login_url)

# Create your views here.

@login_required()
#@group_required('NhanVien',)
def home(request):
    return render(request,"normal_site/Home/home.html")

# class LapPhieuTietKiem(View):
#     model = models.Phieutietkiem
#     template_name = 'normal_site/lap_phieu_tiet_kiem.html'
#     form_class = forms.PhieuTietKiemForm

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         context = {'form': form}
#         return render(request,self.template_name,context)
    
#     def post(self, request, *args, **kwargs):
#         # lấy thông tin từ request
#         tenkh = request.POST.get('tenkh')
#         CMND = request.POST.get('CMND')
#         diachi = request.POST.get('diachi')
#         sotiengoi = request.POST.get('sotiengoi')
#         loaitietkiem = request.POST.get('loaitietkiem',False)

#         # check từng thông tin một
#         if (len(CMND)!=9 or len(CMND)!=12):
#             form = self.form_class(request.POST)
#             context = {'form': form}
#             messages.error(request,"CMND không hợp lệ")
#             return render(request,self.template_name,context)
#         else:
#             khachhang = models.Khachhang.objects.get(cccd=CMND)
#             if khachhang.exists():
#                 if khachhang.tenkh.lower() != tenkh.lower():
#                     form = self.form_class(request.POST)
#                     context = {'form': form}
#                     messages.error(request,"Tên khách hàng và CMND không khớp với thông tin khách hàng trong hệ thống")
#                     return render(request,self.template_name,context)
#                 else:
#                     flag_khachhangdatontai = True

#         sotiengoitoithieu = models.Loaitietkiem.objects.get(ltk=loaitietkiem).sotiengoitoithieu # có thể điều kiện get thay đổi tuy thuộc vào database
#         if (float(sotiengoi) < sotiengoitoithieu):
#                 form = self.form_class(request.POST)
#                 context = {'form': form}
#                 messages.error(request,"Số tiền gởi phải lớn hơn hoặc bằng {}".format(sotiengoitoithieu))
                
#                 return render(request,self.template_name,context)
#         # oke thì lưu lại -> 2 hướng (1: nếu khách hàng có thông tin rồi thì chỉ lưu vào bảng phieutietkiem; 2: ngược lại)
#         if flag_khachhangdatontai:
#             phieutietkiem = models.Phieutietkiem.objects.create(maptk=random.randint(1000,10000), # random là sai nha
#             makh=models.Khachhang.objects.get(cccd=CMND).makh,
#             maltk=models.Loaitietkiem.objects.get(ltk=loaitietkiem).maltk,
#             sotiengoi=sotiengoi,ngaymophieu=str(date.today()),
#             ngaydongphieu='',sodu=sotiengoi,tinhtrang=1)
#             phieutietkiem.save()

#             # chuyen trang
#             return redirect('/normal_site/phieutietkiem/')
#         else:
#             khachhang_save = models.Khachhang.objects.create(makh=random.randint(1000,10000),tenkh=tenkh,diachi=diachi,cccd=CMND) # random cũng là sai nha
#             khachhang_save.save()

#             phieutietkiem = models.Phieutietkiem.objects.create(maptk=random.randint(1000,10000), # random là sai nha
#             makh=models.Khachhang.objects.get(cccd=CMND).makh,
#             maltk=models.Loaitietkiem.objects.get(ltk=loaitietkiem).maltk,
#             sotiengoi=sotiengoi,ngaymophieu=str(date.today()),
#             ngaydongphieu='',sodu=sotiengoi,tinhtrang=1)
#             phieutietkiem.save()
#             # chuyen trang
#             return redirect('/normal_site/phieutietkiem/')

# def TraCuu(request):
#     query = request.GET.get('q',None)
#     template_name = 'normal_site/tra_cuu.html'

#     if query is not None:
#         ptk = models.Phieutietkiem.objects.all()
#         ptk = ptk.filter(maptk__icontains=query) # có thêm cái Q search cũng khá hay
        
#         kh_list = []
#         for i in range(len(ptk)):
#             kh_list.append(models.Khachhang.objects.get(makh=ptk[i].makh).tenkh)
        
#         context = {'ptk':ptk,'kh_list':kh_list}
#         return render(request, template_name,context)
#     else:
#         return render(request,template_name)

# """ Tóm lại các bước lập phiếu rút tiền như sau nè: 
# (1) Template lấy thông tin để tìm kiếm phiếu
# (2) Phiếu được tìm kiếm kèm 2 nut submit là cancel và rút
# (3) 1 Popup hiện ra. 1 là sẽ báo phiếu này ko thể rút do chưa đến hạn. 2 là báo được rút tiền, 
# với ko kỳ hạn được phép chọn số tiền rút, với có kỳ hạn thì buộc phải xác nhận rút hết"""
# class TimKiemPhieuTietKiem(View):
#     model= models.Phieuruttien
#     template_name = 'normal_site/lap_phieu_rut_tien.html'
#     form_class = forms.TimKiemPhieuTietKiemForm

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         context = {'form': form}
#         return render(request,self.template_name,context)
    
#     def post(self, request, *args, **kwargs):
#         tenkh = request.POST.get('tenkh')
#         maptk = request.POST.get('maptk')

#         # check từng thông tin một
#         khachhang = models.Khachhang.objects.get(tenkh=tenkh)
#         phieutietkiem = models.Phieutietkiem.objects.get(maptk=maptk)

#         if phieutietkiem.exists() and khachhang.exists():
#             # get data from databases
#             phieutietkiem = models.Phieutietkiem.objects.get(maptk=maptk)
#             khachhang = models.Khachhang.objects.get(tenkh=tenkh)

#             context = {'ptk': phieutietkiem, 'kh': khachhang}
#             # render template
#             return render(request,"normal_site/thong_tin_phieu_tiet_kiem.html",context)

#         elif (phieutietkiem.exists() and khachhang.exists() == False):
#             form = self.form_class(request.POST)
#             context = {'form': form}
#             messages.error(request,"Tên khách hàng không tồn tại")
#             return render(request,self.template_name,context)

#         else :
#             form = self.form_class(request.POST)
#             context = {'form': form}
#             messages.error(request,"Mã phiếu không tồn tại")
#             return render(request,self.template_name,context)

# class RutPhieuTietKiem (View):
#     model = models.Phieuruttien
#     template_name = 'normal_site/confirm_rut_tien.html'

#     def get(self, request, *args, **kwargs):
#         phieutietkiem = models.Phieuruttien.objects.get(maptk=kwargs['maptk'])
#         # check phiếu còn hoạt động hay chưa
#         if phieutietkiem.tinhtrang==0:
#             context = {'tinhtrang': 'Phiếu đã đóng'}
#             return render(request,self.template_name,context)

#         # check phiếu đã đến hạn hay chưa
#         ngaymophieu = datetime.strptime(phieutietkiem.ngaymophieu, 'd/%m/%Y') # convert string to date
#         ngayhethan = ngaymophieu + relativedelta(months=+phieutietkiem.maltk.kyhan) # add kyhan to ngaymophieu
#         if datetime.today() < ngayhethan:
#             context = {'tinhtrang': 'Phiếu chưa đến kỳ hạn'}
#             return render(request,self.template_name,context)

#         # Render template rút tiền với 2 sự lựa chọn. 1 là sẽ báo rút hết, 2 là có thể lựa chọn số tiền.
    
#     def post(self, request, *args, **kwargs):
#         pass
# def ThongKe(request):
#     template_name = 'normal_site/thong_ke.html'
#     type = request.GET.get('t',None)
#     date = request.GET.get('d',None)

#     if type is None and date is None:
#         return render(request,template_name)
    
#     elif type is not None and date is None:
#         if type == "1":
#             context = {'t': "1"}
#             return render(request,template_name,context)
#         else :
#             context = {'t': "2"}
#             return render(request,template_name,context)

#     else :
#         if type == "1":
#             # get objects từ 3 bảng
#             # xử lý
#             # lưu xuống database
#             # đưa vào context
#             # render template
#             pass
#         else :
#             # get objects từ 3 bảng
#             # xử lý
#             # lưu xuống database
#             # đưa vào context
#             # render template
#             pass