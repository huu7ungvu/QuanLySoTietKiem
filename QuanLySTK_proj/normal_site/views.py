from pyexpat import model # ???
from django.http import HttpResponse
from django.shortcuts import render, redirect
import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required # add login and permission required decorator
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,AccessMixin # add login and permission mixin 
from braces.views import GroupRequiredMixin # add GroupRequiredMixin to the class 
from django.views.generic.base import View
from django.db.models import Sum, Count
from admin_site import models 
from . import forms 
import random
from django.contrib import messages
from datetime import datetime, date
import calendar
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

#@login_required()
#@group_required('NhanVien',)
class Home(View):
    def get(self,request,username):
        try :
            user = models.User.objects.get(username=username)
        except :
            user = None
        
        if user is not None:
            position=user.groups.all().values()[0]['name']
            if position =='NhanVien':
                context = {'user': user,'position':'Nhân Viên'}
            elif position =='GiamDoc':
                context = {'user': user,'position':'Giám Đốc'}
            else:
                context = {'user': user,'position':'Nhân Viên Phân Tích Dữ Liệu'}
            return render(request,"normal_site/Home/home.html",context)
        else :
            return render(request,"normal_site/Home/home.html")
    # def get(self, request, *args, **kwargs): # Chưa hiểu đoạn này để làm gì luôn
        # return render(request, 'normal_site/Home/home.html')

def profile(request,username):
    user = models.User.objects.get(username=username)
    position=user.groups.all().values()[0]['name']
    if position=='NhanVien':
            context = {'user': user,'position':'Nhân Viên'}
    elif position=='GiamDoc':
            context = {'user': user,'position':'Giám Đốc'}
    else:
            context = {'user': user,'position':'Nhân Viên Phân Tích Dữ Liệu'}
    return render(request,"normal_site/Profile/profile.html",context)

class LapPhieuTietKiem(View):
    model = models.Phieutietkiem
    template_name = 'normal_site\PhieuTK\phieutk.html'

    def get(self, request, *args, **kwargs):
        ltk = models.Loaitietkiem.objects.all()
        ltk_list = []

        for i in range(len(ltk)):
            ltk_list.append(ltk[i].ltk)
        context = {'ltk': ltk_list}

        return render(request,self.template_name,context)
    
    def post(self, request, *args, **kwargs):
        # lấy thông tin từ request
        id = request.POST.get('id')
        tenkh = request.POST.get('tenkh')
        tenkh = tenkh.title()
        CMND = request.POST.get('CMND')
        diachi = request.POST.get('diachi')
        sotiengoi = request.POST.get('sotiengoi')
        loaitietkiem = request.POST.get('loaitietkiem',False)

        # check từng thông tin một (1: Thông tin khách hàng, 2: Số tiền tối thiểu)
        # (1)
        if id != '':
            khachhang = models.Khachhang.objects.filter(makh=id)
            if len(khachhang)!=0:
                if (tenkh != khachhang[0].tenkh or CMND != khachhang[0].cccd) :
                    messages.error(request, 'Thông tin khách hàng (Tên hoặc CCCD) không đúng với dữ liệu trong cơ sở dữ liệu')
                    return redirect('normal_site:lap_phieu_tiet_kiem')
            else: 
                messages.error(request, 'Khách hàng không tồn tại')
                return redirect('normal_site:lap_phieu_tiet_kiem')
        
        else :
            if (len(CMND)!=9 and len(CMND)!=12):
                messages.error(request,"CMND không hợp lệ" + str(len(CMND)))
                return redirect('normal_site:lap_phieu_tiet_kiem')
            else :
                khachhang = models.Khachhang.objects.filter(cccd=CMND)
                if len(khachhang)!=0:
                    if (tenkh != khachhang[0].tenkh) :
                        messages.error(request, 'CCCD đã tồn tại trong cơ sở dữ liệu và tên khách hàng đang nhập không khớp với CCCD đã tồn tại')
                        return redirect('normal_site:lap_phieu_tiet_kiem')
                    else:
                        messages.error(request, 'CCCD và tên khách hàng đã tồn tại trong cơ sở dữ liệu vui lòng nhập thêm ID khách hàng')
                        return redirect('normal_site:lap_phieu_tiet_kiem')

        # (2)
        sotiengoitoithieu = models.Loaitietkiem.objects.get(ltk=loaitietkiem).sotiengoitoithieu
        if (float(sotiengoi) < sotiengoitoithieu):
            messages.error(request,"Số tiền gởi phải lớn hơn hoặc bằng {}".format(sotiengoitoithieu))
            return redirect('normal_site:lap_phieu_tiet_kiem')


        # oke thì lưu lại -> 2 hướng (1: nếu khách hàng có thông tin rồi thì chỉ lưu vào bảng phieutietkiem; 2: ngược lại)
        if id != '': # đã có nhập id => Khách hàng đã đăng ký tài khoản
            phieutietkiem = models.Phieutietkiem.objects.create(maptk='PTK' + str(int(models.Thamso.objects.get(tenthamso='SLPhieuTietKiem').giatri)+1),
            makh=models.Khachhang.objects.get(makh=id),
            maltk=models.Loaitietkiem.objects.get(ltk=loaitietkiem),
            sotiengoi=sotiengoi,ngaymophieu=str(date.today()),
            ngaydongphieu=None,sodu=sotiengoi,tinhtrang=1)
            phieutietkiem.save()
        
            # cập nhật tham số SLPhieuTietKiem
            models.Thamso.objects.filter(tenthamso='SLPhieuTietKiem').update(giatri=str(int(models.Thamso.objects.get(tenthamso='SLPhieuTietKiem').giatri)+1))

            messages.success(request, 'Lập phiếu tiết kiệm thành công')
            return redirect('normal_site:lap_phieu_tiet_kiem')
        
        else:
            khachhang_save = models.Khachhang.objects.create(makh='KH' + str(int(models.Thamso.objects.get(tenthamso='SLKhachHang').giatri)+1),
            tenkh=tenkh,diachi=diachi,cccd=CMND)

            khachhang_save.save()

            phieutietkiem = models.Phieutietkiem.objects.create(maptk='PTK' + str(int(models.Thamso.objects.get(tenthamso='SLPhieuTietKiem').giatri)+1),
            makh=khachhang_save,
            maltk=models.Loaitietkiem.objects.get(ltk=loaitietkiem),
            sotiengoi=sotiengoi,ngaymophieu=str(date.today()),
            ngaydongphieu=None,sodu=sotiengoi,tinhtrang=1)
            phieutietkiem.save()

            # cập nhật tham số SLPhieuTietKiem và SLKhachHang
            models.Thamso.objects.filter(tenthamso='SLPhieuTietKiem').update(giatri=str(int(models.Thamso.objects.get(tenthamso='SLPhieuTietKiem').giatri)+1))
            models.Thamso.objects.filter(tenthamso='SLKhachHang').update(giatri=str(int(models.Thamso.objects.get(tenthamso='SLKhachHang').giatri)+1))

            messages.success(request, 'Lập phiếu tiết kiệm thành công')
            return redirect('normal_site:lap_phieu_tiet_kiem')

class TraCuu(View):
    template_name = 'normal_site/Tracuu/tra_cuu.html'

    def post(self, request, *args, **kwargs):
        query = request.POST.get('q')
        ptk = models.Phieutietkiem.objects.filter(makh=query)
        
        if len(ptk) == 0:
            messages.error(request, 'Không tìm thấy phiếu tiết kiệm nào hoặc thông tin không đúng')
            return redirect('normal_site:tra_cuu')
        else:
            context = {'ptk':ptk,'query':query}
            return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

""" Tóm lại các bước lập phiếu rút tiền như sau nè: 
(1) Template lấy thông tin để tìm kiếm phiếu
(2) Phiếu được tìm kiếm kèm 2 nut submit là cancel và rút
(3) 1 Popup hiện ra. 1 là sẽ báo phiếu này ko thể rút do chưa đến hạn. 2 là báo được rút tiền, 
với ko kỳ hạn được phép chọn số tiền rút, với có kỳ hạn thì buộc phải xác nhận rút hết"""
class TimKiemPhieuTietKiem(View):
    model= models.Phieutietkiem
    template_name = 'normal_site\Lapphieurut\\tim_kiem_phieu_tiet_kiem.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    
    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        id = id.upper()
        tenkh = request.POST.get('tenkh')
        tenkh = tenkh.title()
        CCCD = request.POST.get('CCCD')
        maptk = request.POST.get('maptk')
        maptk = maptk.upper()


        # check từng thông tin một (1: thông tin khách hang; 2: Mã phiếu tiết kiệm)
        khachhang = models.Khachhang.objects.filter(makh=id)
        phieutietkiem = models.Phieutietkiem.objects.filter(maptk=maptk)

        # 1: thông tin khách hàng
        if len(khachhang) != 0 :
            if tenkh != khachhang[0].tenkh or CCCD != khachhang[0].cccd:
                messages.error(request, 'Thông tin khách hàng không chính xác')
                return redirect('normal_site:tim_kiem_phieu_tiet_kiem')
        else:
            messages.error(request, 'Không tìm thấy khách hàng')
            return redirect('normal_site:tim_kiem_phieu_tiet_kiem')

        # 2: Mã phiếu tiết kiệm
        if len(phieutietkiem) == 0:
            messages.error(request, 'Không tìm thấy phiếu tiết kiệm')
            return redirect('normal_site:tim_kiem_phieu_tiet_kiem')
        
        return redirect('normal_site:rut_phieu_tiet_kiem',maptk=maptk)

class RutPhieuTietKiem (View):
    model = models.Phieuruttien
    template_name = 'normal_site/Lapphieurut/lap_phieu_rut_tien.html'

    def tinh_so_du(self,phieutietkiem,ngayhethan):
        sotien = int(phieutietkiem.sodu)
        laisuat = phieutietkiem.maltk.laisuat
        songaygoi = int((ngayhethan - phieutietkiem.ngaymophieu).days)
        songayquahan = int((date.today() - ngayhethan).days)
        laisuatquahan = models.Loaitietkiem.objects.get(maltk='LTK01').laisuat

        sodukhadung = sotien + int(sotien * (laisuat/100) * (songaygoi/365)) # lãi theo kỳ hạn
        sodukhadung = sodukhadung + + int(sodukhadung * (laisuatquahan/100) * (songayquahan/365)) # lãi theo quá hạn
        return sodukhadung

    def get(self, request, *args, **kwargs):
        phieutietkiem = models.Phieutietkiem.objects.get(maptk=kwargs['maptk'])

        # Check xem phiếu đủ điều kiện rút tiền hay không (1: Check trạng thái phiếu; 2: Check đến kỳ hạn rút tiền)

        # (1)
        if phieutietkiem.tinhtrang == 0:
            context = {'phieutietkiem':phieutietkiem,'closed':'closed'}
            return render(request, self.template_name,context)
        # (2)
        thoigiangoitoithieu = phieutietkiem.maltk.thoigiangoitoithieu
        ngayhethan = phieutietkiem.ngaymophieu + relativedelta(days=thoigiangoitoithieu)

        if date.today() < ngayhethan:
            context = {'phieutietkiem':phieutietkiem,'undue':'undue'}
            return render(request,self.template_name,context)
        
        # Kiểm tra loai tiet kiem
        if phieutietkiem.maltk.maltk == 'LTK01':
            is_ruthet = False
        else :
            is_ruthet = True

        context = {'phieutietkiem':phieutietkiem,'khachhang':phieutietkiem.makh,'ok':'ok',
        'sodukhadu': self.tinh_so_du(phieutietkiem,ngayhethan),
        'ngayhethan':ngayhethan, 
        'is_ruthet':is_ruthet}
        return render(request,self.template_name,context)
    
    def post(self, request, *args, **kwargs):
        huy = request.POST.get('huy')
        if huy == '1'  :
            return redirect('normal_site:tim_kiem_phieu_tiet_kiem')
        else :
            maptk = kwargs['maptk']
            phieutietkiem = models.Phieutietkiem.objects.get(maptk=maptk)
            ngayhethan = phieutietkiem.ngaymophieu + relativedelta(days=phieutietkiem.maltk.thoigiangoitoithieu)
            sodukhadu = self.tinh_so_du(phieutietkiem,ngayhethan)
            rut = request.POST.get('rut_1')
            if rut == "Rút Phiếu" :
                sotien = request.POST.get('sotien')
                sotien = int(sotien)
                if sotien > sodukhadu :
                    messages.error(request, 'Số tiền rút không được lớn hơn số dư khả dụng')
                    return redirect('normal_site:rut_phieu_tiet_kiem',maptk=maptk)
                elif sotien < 100000 :
                    messages.error(request, 'Số tiền rút không được nhỏ hơn 100.000 VND')
                    return redirect('normal_site:rut_phieu_tiet_kiem',maptk=maptk)
                elif (sodukhadu - sotien) < 100000:
                    messages.error(request, 'Số tiền khả dụng trong phiếu sau rút không được nhỏ hơn 100.000 VND')
                    return redirect('normal_site:rut_phieu_tiet_kiem',maptk=maptk)
                else :
                    # Tính tiền còn lại
                    sotienconlai = sodukhadu - sotien
                    # Kiểm tra số tiền còn lại để xử lý phiếu tiết kiệm (1: đóng phiểu, 2: tiếp tục)
                    if sotienconlai == 0:
                        phieutietkiem.tinhtrang = 0
                        phieutietkiem.sodu = 0
                        phieutietkiem.ngaydongphieu = str(date.today())
                        phieutietkiem.save()
                    else :
                        phieutietkiem.sodu = sotienconlai
                        phieutietkiem.save()

                    # Lưu phiếu rút tiền
                    maprt = 'PRT'+ str(int(models.Thamso.objects.get(tenthamso='SLPhieuRutTien').giatri) + 1)
                    models.Thamso.objects.filter(tenthamso='SLPhieuRutTien').update(giatri=int(models.Thamso.objects.get(tenthamso='SLPhieuRutTien').giatri) + 1)

                    phieuruttien = models.Phieuruttien.objects.create(maprt=maprt,maptk=phieutietkiem,sotienrut=sotien,ngayrut=str(date.today()),makh=phieutietkiem.makh)
                    phieuruttien.save()
                    
                messages.success(request, 'Rút tiền thành công')
                return redirect('normal_site:tim_kiem_phieu_tiet_kiem')

            else:
                # hủy phiếu tiết kiệm
                phieutietkiem.tinhtrang = 0
                phieutietkiem.sodu = 0
                phieutietkiem.ngaydongphieu = str(date.today())
                phieutietkiem.save()
                
                # Lưu phiếu rút tiền
                maprt = 'PRT'+ str(int(models.Thamso.objects.get(tenthamso='SLPhieuRutTien').giatri) + 1)
                models.Thamso.objects.filter(tenthamso='SLPhieuRutTien').update(giatri=int(models.Thamso.objects.get(tenthamso='SLPhieuRutTien').giatri) + 1)

                phieuruttien = models.Phieuruttien.objects.create(maprt=maprt,maptk=phieutietkiem,sotienrut=sodukhadu,ngayrut=str(date.today()),makh=phieutietkiem.makh)
                phieuruttien.save()
                    
                messages.success(request, 'Rút tiền thành công')
                return redirect('normal_site:tim_kiem_phieu_tiet_kiem')

def ThongKe(request,t=None,d=None):
    template_name = 'normal_site/Thongke/thong_ke.html'
    type = request.GET.get('t',None)
    date = request.GET.get('d',None)

    if type is None and date is None:
        return render(request,template_name)
    
    elif type is not None and date is None:
        if type == "1":
            context = {'t': "1"}
            return render(request,template_name,context)
        else :
            context = {'t': "2"}
            return render(request,template_name,context)

    else:
        if type == "Thống kê theo ngày":
            date_split = date.split('-')
            y = date_split [0]
            m = date_split [1]
            d = date_split [2]
            
            # check đã có trong database hay chưa
            baocaongay_check = models.Baocaongay.objects.filter(ngay__year=y,ngay__month=m,ngay__day=d)
            if len(baocaongay_check) != 0:
                context = {'baocaongay': baocaongay_check,'t':"1",'date':date}
                return render(request,template_name,context)

            # get objects từ 2 bảng
            maltk = models.Loaitietkiem.objects.values_list('maltk',flat=True)
            maltk = list(maltk)
            phieuruttien = models.Phieuruttien.objects.filter(ngayrut__year=y,ngayrut__month=m,ngayrut__day=d)
            phieutietkiem = models.Phieutietkiem.objects.filter(ngaymophieu__year=y,ngaymophieu__month=m,ngaymophieu__day=d)

            # xử lý và lưu xuống database
            for i in maltk:
                try:
                    tong_thu = int(phieutietkiem.filter(maltk=i).aggregate(Sum('sotiengoi'))['sotiengoi__sum'])
                except:
                    tong_thu = 0
                    
                
                try:
                    tong_chi = int(phieuruttien.filter(maltk=i).aggregate(Sum('sotienrut'))['sotienrut__sum'])
                except:
                    tong_chi = 0

                chenhlech = abs(tong_thu - tong_chi)
                
                baocaongay = models.Baocaongay.objects.create(ngay=date,maltk=models.Loaitietkiem.objects.get(maltk=i),tongthu=tong_thu,tongchi=tong_chi,chechlechthuchi=chenhlech)

            # đưa vào context
            baocaongay = models.Baocaongay.objects.filter(ngay__year=y,ngay__month=m,ngay__day=d)
            context = {'baocaongay': baocaongay,'t':"1",'date':date}

            # render template
            return render(request,template_name,context)

        else :
            date_split = date.split('-')
            y = date_split [0]
            m = date_split [1]
            maltk = models.Loaitietkiem.objects.values_list('maltk',flat=True)
            maltk = list(maltk)
            
            # check đã có trong database hay chưa
            baocaothang_check = models.Baocaothang.objects.filter(ngaythang__year=y,ngaythang__month=m)
            if len(baocaothang_check) != 0:
                context = {'baocaothang': baocaothang_check,'t':"2", 'maltk':maltk, 'date':date}
                return render(request,template_name,context)

            # get objects bảng
            phieumo = models.Phieutietkiem.objects.filter(ngaymophieu__year=y,ngaymophieu__month=m)
            phieudong = models.Phieutietkiem.objects.filter(ngaydongphieu__year=y,ngaydongphieu__month=m)

            # xử lý # lưu xuống database
            songaytrongthang = calendar.monthrange(int(y),int(m))[1]
            for i in maltk:
                for j in range (1,songaytrongthang+1):
                    try:
                        somo = int(phieumo.filter(maltk=i,ngaymophieu__day=j).aggregate(Count('maptk'))['maptk__count'])
                    except:
                        somo = 0
                    
                    try:
                        sodong = int(phieudong.filter(maltk=i,ngaydongphieu__day=j).aggregate(Count('maptk'))['maptk__count'])
                    except:
                        sodong = 0

                    chenhlech = abs(somo-sodong)

                    if j<10:
                        date_temp = date + str('-0') + str(j) 
                    else :
                        date_temp = date + str('-') + str(j)

                    baocaothang = models.Baocaothang.objects.create(ngaythang=date_temp
                    ,maltk=models.Loaitietkiem.objects.get(maltk=i)
                    ,phieugoi=somo,phieudong=sodong,chenhlechdonggoi=chenhlech)
            
            # đưa vào context
            baocaothang = models.Baocaothang.objects.filter(ngaythang__year=y,ngaythang__month=m)
            context = {'baocaothang': baocaothang,'t':"2", 'maltk':maltk, 'date':date}

            # render template
            return render(request,template_name,context)