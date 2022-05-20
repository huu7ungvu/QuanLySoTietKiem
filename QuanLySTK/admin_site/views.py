from django.shortcuts import render
import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required # add login and permission required decorator
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,AccessMixin # add login and permission mixin 
from braces.views import GroupRequiredMixin # add GroupRequiredMixin to the class 
import email
from email import message
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from admin_site import models


# Create group_required decorator
def group_required(*group_names, login_url=None, raise_exception=False):
    def check_permission(user):
        if isinstance(group_names, six.string_types):
            group_names = (group_names, )
        else:
            group_names = group_names
        # fist check if user has the permission (even anon users)
    
        if user.groups.filter(name__in=group_names).exists():
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_permission, login_url=login_url)

# from django.contrib.auth.decorators import group_required
# Create your views here.

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        position = request.POST.get('position', False)

        # Xử lý mã nhân viên
        manv = 'NV' + str(int(models.Thamso.objects.get(tenthamso='SLNguoiDung').giatri)+1)

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username already exists")
                return redirect('adsite:signup')
            else:
                user = User.objects.create_user(username=username,password=password1,first_name=name,email=email)
                user.first_name = name # first name equal full name
                user.save()

                user_extend= models.UsersExtendClass.objects.create(user=user,manv=manv)
                user_extend.save()

                if position == "NhanVien":
                    group = Group.objects.get(name='NhanVien')
                    user.groups.add(group)

                if position == "NhanVienPhanTichDuLieu":
                    group = Group.objects.get(name='NhanVienPhanTichDuLieu')
                    user.groups.add(group)

                if position == "GiamDoc":
                    group = Group.objects.get(name='GiamDoc')
                    user.groups.add(group)
                    user.is_staff = True

                messages.success(request,"You are registered successfully")
                return redirect('accounts:signin')
        else:
            messages.error(request,"Password not matched")
            return redirect('adsite:signup')

    return render(request,"admin_site/Register/register.html")

def home (request):
    return HttpResponse("Hello, This is admin Site")

