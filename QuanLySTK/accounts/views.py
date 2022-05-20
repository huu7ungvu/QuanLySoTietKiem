from urllib import response
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required # add login and permission required decorator
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin,AccessMixin # add login and permission mixin 
from braces.views import GroupRequiredMixin # add GroupRequiredMixin to the class 

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

#@login_required()
class MyPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = '/accounts/signin'

#class ResetPasswordView(ResetPasswordView)

# Create your views here.
def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            if user.is_active:
                if user.is_superuser==False:
                    login(request,user)
                    return redirect('normal_site:home') # điều hướng về trang admin
                else:
                    login(request,user)
                    return redirect('adsite:home') # điều hướng về trang chủ
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('accounts:signin')

    return render(request,"accounts/signin.html")