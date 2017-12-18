# 只要一启动先执行这个

from app01 import models
from oomph6.service import vv1
from django.utils.safestring import mark_safe

class UserInfoConfig(vv1.Oomph6Config):

    list_display = ['id','name'] # 需要自定义页面显示内容时,写函数.
    show_add_btn = False
    # def get_add_btn(self):
    #     # 去session中查看是否有添加权限
    #     show_add_btn = True

vv1.site.register(models.UserInfo,UserInfoConfig)


class RoleConfig(vv1.Oomph6Config):
    list_display = ['id','name']
vv1.site.register(models.Role,RoleConfig)