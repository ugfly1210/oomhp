# 只要一启动先执行这个

from app01 import models
from oomph6.service import vv1
from django.utils.safestring import mark_safe

class UserInfoConfig(vv1.Oomph6Config):

    def edit(self,obj=None,is_header=False):
        # 这个obj对应for row in data_list 中的row
        # 写obj=None,是因为 表头中不需要obj,所以为了避免报错,默认为None
        if is_header:
            return '编辑'
        return mark_safe('<a href="/edit/%s">编辑</a>'%obj.id)

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'  # 表头
        return mark_safe('<input type="checkbox" name="pk" value="%s" />'%obj.id) # 表中数据

    def delete(self,obj=None,is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="/delete/%s">删除</a>'%obj.id)
    list_display = [checkbox,'id','name',edit,delete] # 需要自定义页面显示内容时,写函数.

vv1.site.register(models.UserInfo,UserInfoConfig)


class RoleConfig(vv1.Oomph6Config):
    list_display = ['id','name']
vv1.site.register(models.Role,RoleConfig)