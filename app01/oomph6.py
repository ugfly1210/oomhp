# 只要一启动先执行这个

from app01 import models
from oomph6.service import vv1
from django.utils.safestring import mark_safe

class UserInfoConfig(vv1.Oomph6Config):


    list_display = ['id','name'] # 需要自定义页面显示内容时,写函数.

vv1.site.register(models.UserInfo,UserInfoConfig)


class RoleConfig(vv1.Oomph6Config):
    list_display = ['id','name']
vv1.site.register(models.Role,RoleConfig)