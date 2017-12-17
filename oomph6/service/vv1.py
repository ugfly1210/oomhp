from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect

class Oomph6Config:
    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        print('site===',site)  # site=== <oomph6.service.vv1.Oomph6Site object at 0x103e3ca20>

    list_display = []

    def get_urls(self):
        app_model_name = self.model_class._meta.app_label,self.model_class._meta.model_name
        url_patterns = [
            url(r'^$',self.changelist_view,name='%s_%s_changelist'%(app_model_name)),
            url(r'^add/$',self.add_view,name='%s_%s_add'%(app_model_name)),
            url(r'^delete/(\d+)/$',self.delete_view,name='%s_%s_delete'%(app_model_name)),
            url(r'^edit/(\d+)/$',self.edit_view,name='%s_%s_edit'%(app_model_name)),
        ]
        return url_patterns


    @property
    def urls(self):
        return self.get_urls()

    ################'''处理请求的方法'''###################
    def changelist_view(self,request,*args,**kwargs):
        '''
        /oomph6/app01/userinfo/           self.model_class : models.UserInfo
        /oomph6/app01/role/               self.model_class : models.Role

        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        '''处理表头'''
        head_list = []
        for field_name in self.list_display:
            if isinstance(field_name,str):
                '''根据类和字段名称来获取字段对象的verbose_name'''
                # verborse_name = self.model_class._meta.get_field(field_name) # 可拿到对象
                verborse_name = self.model_class._meta.get_field(field_name).verbose_name
            else:
                verborse_name=field_name(self,is_header=True)
            head_list.append(verborse_name)

        '''处理表中数据'''
        data_list = self.model_class.objects.all()
        new_data_list = []
        # list_display = ['id','name']  # 每一个元素都是表里面的字段名
        for row in data_list:   # 每一个row是一个对象
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name,str):  # 如果是字符串
                      # temp.append(getattr(field_name,row))   # 这步很骚哦.  !!反射!!
                    val = getattr(row,field_name)   # 这步很骚哦.  !!反射!!
                else: # 如果是函数
                      # temp.append(field_name(self,row))      # 第一个参数是本身自己的,第二个参数代指对象,是从41行拿的
                    val = field_name(self,row)      # 第一个参数是本身自己的,第二个参数代指对象,是从41行拿的
                temp.append(val)
            new_data_list.append(temp)
        return render(request,'oomph6/changelist.html',{'data_list':new_data_list,'head_list':head_list})

    def add_view(self,request,*args,**kwargs):
        return HttpResponse('add_view')
    def edit_view(self,request,nid,*args,**kwargs):
        return HttpResponse('edit_view')
    def delete_view(self,request,nid,*args,**kwargs):
        return HttpResponse('delete_view')



class Oomph6Site:
    def __init__(self):
        self._registry={}

    def register(self,model_class,oomph6_config_class=None):
        '''oomph6_config_class这么一长串指的还是类名(命名失误)'''
        if not oomph6_config_class:
            oomph6_config_class = Oomph6Config
        self._registry[model_class] = oomph6_config_class(model_class,self) #这个self就是site
        '''
        {models.UserInfo : Oomph6Config(models.UserInfo,site)}   这个value和oomph6_config_obj 什么关系
                                                   是如何转换的
        '''

    def get_urls(self):
        url_pattern = []

        for model_class,oomph6_config_obj in self._registry.items():
            '''
            为每一个类,创建4个url
            /oomph6/app01/userinfo/
            /oomph6/app01/userinfo/add/
            /oomph6/app01/userinfo/(\d+)/delete
            '''
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name
            '''oomph6_config_obj : 同一个类生成的不同对象'''
            cur_path = url(r'^%s/%s/'%(app_name,model_name,),(oomph6_config_obj.urls,None,None))

            url_pattern.append(cur_path)
        return url_pattern

    @property
    def urls(self):
        # return ([],None,'oomph6')
        return (self.get_urls(),None,None)

site = Oomph6Site()