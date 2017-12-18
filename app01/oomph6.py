# 只要一启动先执行这个
from app01 import models
from oomph6.service import vv1
from django.forms import ModelForm
from django.conf.urls import url
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse,render,redirect

class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        error_messages = {
            'name':{'required':'用户名不能为空!'}
        }



class UserInfoConfig(vv1.Oomph6Config):

    list_display = ['id','name'] # 需要自定义页面显示内容时,写函数.
    show_add_btn = False
    model_form_class = UserInfoModelForm
    # def get_add_btn(self):
    #     # 去session中查看是否有添加权限
    #     show_add_btn = True

vv1.site.register(models.UserInfo,UserInfoConfig)

class RoleConfig(vv1.Oomph6Config):
    list_display = ['id','name']
vv1.site.register(models.Role,RoleConfig)

class HostModelForm(ModelForm):
    class Meta:
        model = models.Host
        fields = ['id','hostname','ip','port']
        error_messages = {
            'hostname':{
                'required':'主机名不能为空',
            },
            'ip':{
                'required': 'IP不能为空',
                'invalid': 'IP格式错误',
            }
        }


class HostConfig(vv1.Oomph6Config):
    def ip_port(self,obj=None,is_header=False):
        if is_header:
            return '自定义列'
        return "%s:%s" %(obj.ip,obj.port,)

    list_display = ['id','hostname','ip','port',ip_port]
    # get_list_display

    show_add_btn = True
    # get_show_add_btn

    model_form_class = HostModelForm
    # get_model_form_class


    def extra_url(self):
        urls = [
            url('^report/$',self.report_view)
        ]
        return urls

    def report_view(self,request):
        return HttpResponse('自定义报表')

    def delete_view(self,request,nid,*args,**kwargs):
        if request.method == "GET":
            return render(request,'my_delete.html')
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())


vv1.site.register(models.Host,HostConfig)
