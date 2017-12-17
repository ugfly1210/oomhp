# 只要一启动先执行这个

from app01 import models
from oomph6.service import vv1
from django.utils.safestring import mark_safe

class UserInfoConfig(vv1.Oomph6Config):
    def edit(self,obj):  # 这个obj对应for row in data_list 中的row
        return mark_safe('<a href="/edit/%s">编辑</a>'%obj.id)
    def checkbox(self,obj):
        return mark_safe('<input type="checkbox" name="pk" value="%s" />'%obj.id)

    list_display = [checkbox,'id','name',edit]

vv1.site.register(models.UserInfo,UserInfoConfig)

class RoleConfig(vv1.Oomph6Config):
    list_display = ['id','name']
vv1.site.register(models.Role,RoleConfig)