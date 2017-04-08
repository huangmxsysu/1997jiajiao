from django.contrib import admin

# Register your models here.
from . import models

admin.site.site_header = "1997 站点管理"
admin.site.site_title = "1997 站点管理"


admin.site.register(models.about_us)

class index_info_admin(admin.ModelAdmin):
    list_display= ('image_tag', 'subtitle', 'slider_delay')
    readonly_fields = ('image_tag',)
    fields = ('image', 'image_tag', 'subtitle', 'slider_delay')

admin.site.register(models.index_info, index_info_admin)

class slider_admin(admin.ModelAdmin):
    list_display= ('image_tag', 'order', 'description',)
    readonly_fields = ('image_tag',)
    fields = ('image', 'image_tag', 'description', 'order')
    ordering = ('order', )

admin.site.register(models.slider, slider_admin)

class teacher_admin(admin.ModelAdmin):
    search_fields = ('name', 'subject', 'school', 'college', 'grade', 'order')
    list_display= ('name', 'avatar_tag', 'subject', 'school', 'college', 'grade', 'order')
    readonly_fields = ('avatar_tag', 'card_tag')
    # fields = ('image', 'avatar_tag', 'card_tag' 'description', 'order')
    ordering = ('order', )
    readonly_fields = ('time_slot', )

admin.site.register(models.teacher, teacher_admin)

class reservation_admin(admin.ModelAdmin):
    readonly_fields = ('time_slot', )

admin.site.register(models.reservation, reservation_admin)


admin.site.register(models.system_setting)