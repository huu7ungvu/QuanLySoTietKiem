from django.contrib import admin
from .models import Khachhang, Loaitietkiem, Phieutietkiem, Phieuruttien, Baocaongay, Baocaothang

# Register your models here.
class KhanghangAdmin (admin.ModelAdmin):
    list_display = ["makh", "tenkh", "diachi", "cccd"]
    search_fields = ["makh", "tenkh"]

class LoaitietkiemAdmin (admin.ModelAdmin):
    list_display = ["maltk", "ltk", "kyhan", "sotiengoitoithieu", "thoigiangoitoithieu", "laisuat"]
    search_fields = ["maltk", "ltk", "kyhan"]

class PhieutietkiemAdmin (admin.ModelAdmin):
    list_display = ["maptk", "makh", "maltk", "sotiengoi", "ngaydongphieu", "ngaymophieu", "sodu", "tinhtrang"]
    search_fields = ["maptk", "makh"]
    list_filter = ["ngaymophieu"]

class PhieuruttienAdmin (admin.ModelAdmin):
    list_display = ["maprt", "makh", "maptk", "ngayrut", "sotienrut"]
    search_fields = ["maprt", "makh_id", "ngayrut"]
    list_filter = ["ngayrut"]

class BaocaongayAdmin (admin.ModelAdmin):
    list_display = ["ngay", "tongthu", "tongchi", "chechlechthuchi"]
    search_fields = ["ngay"]
    list_filter = ["ngay"]

class BaocaothangAdmin (admin.ModelAdmin):
    list_display = ["ngaythang", "phieugoi", "phieudong", "chenhlechdonggoi"]
    list_filter = ["ngaythang"]


# Register your models here.
admin.site.register(Khachhang, KhanghangAdmin)
admin.site.register(Loaitietkiem, LoaitietkiemAdmin)
admin.site.register(Phieutietkiem, PhieutietkiemAdmin)
admin.site.register(Phieuruttien, PhieuruttienAdmin)
admin.site.register(Baocaongay, BaocaongayAdmin)
admin.site.register(Baocaothang, BaocaothangAdmin)
