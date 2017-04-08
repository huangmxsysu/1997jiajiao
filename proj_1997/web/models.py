from django.db import models

# Create your models here.
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.translation import ugettext_lazy as _

import json

import ast
 
class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"
 
    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)
 
    def to_python(self, value):
        if not value:
            value = []
 
        if isinstance(value, list):
            return value
 
        return ast.literal_eval(value)
 
    def get_prep_value(self, value):
        if value is None:
            return value
 
        return str(value) # use str(value) in Python 3
 
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class about_us(models.Model):
    class Meta:
        verbose_name = '关于我们'
        verbose_name_plural = '关于我们'

    content = RichTextUploadingField(verbose_name = '富文本编辑')

    def __str__(self):
        return '点击修改'


class index_info(models.Model):
    class Meta:
        verbose_name = '首页信息'
        verbose_name_plural = '首页信息'

    image = models.ImageField(verbose_name = '首页logo', upload_to='index/', max_length=256)

    def image_tag(self):
        return u'<img src="%s" width="200px" />' % self.image.url

    image_tag.short_description = 'logo 预览'
    image_tag.allow_tags = True

    subtitle = models.TextField(verbose_name = 'logo下文字', max_length=4096)

    slider_delay = models.IntegerField(verbose_name = '滚动间隔时间(单位为毫秒)')

    def __str__(self):
        return "首页信息 <id: %d>" % self.id


class slider(models.Model):
    class Meta:
        verbose_name = '首页滚动图'
        verbose_name_plural = '首页滚动图'

    image = models.ImageField(verbose_name = '轮播图片', upload_to='slider/', max_length=256)

    def image_tag(self):
        return u'<img src="%s" width="200px" />' % self.image.url

    image_tag.short_description = '轮播图片预览'
    image_tag.allow_tags = True

    description = models.TextField(verbose_name = '相关描述', max_length=4096)

    order = models.PositiveIntegerField(verbose_name = '轮播顺序(由0开始)')

    def __str__(self):
        return "首页滚动图 <id: %d>" % self.id


class teacher(models.Model):
    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'


    name = models.CharField(verbose_name = '姓名', max_length=265)

    MALE = False
    FEMALE = True
    gender = models.BooleanField(verbose_name = '性别', choices=((MALE,'Male'), (FEMALE,'Female')), default=MALE)

    subject = models.CharField(verbose_name = '科目（空格分隔）', max_length=1024)

    school = models.CharField(verbose_name = '学校', max_length=512)
    college = models.CharField(verbose_name = '专业', max_length=512)
    grade = models.CharField(verbose_name = '年级', max_length=265)
    order = models.PositiveIntegerField(verbose_name = '顺序(由0开始)', default=0)

    avatar = models.ImageField(verbose_name = '头像图片', upload_to='avatar/', max_length=256)
    def avatar_tag(self):
        return u'<img src="%s" width="200px" />' % self.avatar.url
    avatar_tag.short_description = '头像图片预览'
    avatar_tag.allow_tags = True

    card = models.ImageField(verbose_name = '校园卡图片', upload_to='card/', max_length=256)
    def card_tag(self):
        return u'<img src="%s" width="200px" />' % self.card.url
    card_tag.short_description = '校园卡图片预览'
    card_tag.allow_tags = True

    description = RichTextUploadingField(verbose_name = '个人简介')

    time_slot = models.TextField(verbose_name = '时段（不在这里修改）', max_length=4096, default='[]')

    def set_time_slot(self, x):
        self.time_slot = json.dumps(x)

    def get_time_slot(self):
        return json.loads(self.time_slot)

    def __str__(self):
        return self.name


class reservation(models.Model):
    class Meta:
        verbose_name = '家教预约'
        verbose_name_plural = '家教预约'

    name = models.CharField(verbose_name = '预约人', max_length=265)
    phone_num = models.CharField(verbose_name = '预约人电话', max_length=32)
    address = models.TextField(verbose_name = '预约人地址', max_length=2048)

    teacher = models.ForeignKey(teacher, models.CASCADE, verbose_name = '预约教师', 
                related_name="reservations");

    ctime = models.DateTimeField(verbose_name = '修改时间', auto_now=True)

    time_slot = models.TextField(verbose_name = '预约时段', max_length=4096, default='[]')

    def set_time_slot(self, x):
        self.time_slot = json.dumps(x)

    def get_time_slot(self):
        return json.loads(self.time_slot)

    UNPROCESSED = 0
    SUCCEED = 1
    EXPIRED = 2
    status = models.IntegerField(verbose_name = '状态', choices=((UNPROCESSED, '未处理'), 
                                        (SUCCEED, '成功'),
                                        (EXPIRED, '失效')),
                                default=UNPROCESSED)

    def __str__(self):
        return "家教预约 <预约人：%s 预约教师：%s>" % (self.name, self.teacher.name)


class system_setting(models.Model):
    class Meta:
        verbose_name = '系统设置（谨慎操作）'
        verbose_name_plural = '系统设置（谨慎操作）'

    msg_account = models.CharField(verbose_name = '信息平台账号', max_length=64)
    msg_pwd = models.CharField(verbose_name = '信息平台密码', max_length=32)

    def __str__(self):
        return '相关设置详情 (只能有一条)'
