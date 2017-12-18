from django.conf.urls import url
from django.forms import ModelForm
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse

class Oomph6Config:
    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        print('site===',site)  # site=== <oomph6.service.vv1.Oomph6Site object at 0x103e3ca20>
    '''11-37 实现默认显示 编辑,选择,删除'''
    # 1. 定制表单列 row
    def edit(self,obj=None,is_header=False):
        # 这个obj对应for row in data_list 中的row
        # 写obj=None,是因为 表头中不需要obj,所以为了避免报错,默认为None
        if is_header:
            return '编辑'
        return mark_safe('<a href="%s">编辑</a>'%self.get_edit_url(obj.id,))

    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'  # 表头
        return mark_safe('<input type="checkbox" name="pk" value="%s" />'%obj.id) # 表中数据

    def delete(self,obj=None,is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="%s">删除</a>'%self.get_delete_url(obj.id,))

    list_display = []
    def get_list_display(self):
        data = [] # 为什么加data???   只能调用该方法才能拿.  你不加data,直接用list_display试一试
                  # 每次请求进来,都会新生成一个空列表
        if self.list_display:
            data.extend(self.list_display)
            data.append(Oomph6Config.edit)
            data.append(Oomph6Config.delete)       # 对象调函数是方法, 类调函数 是函数
            data.insert(0,Oomph6Config.checkbox)   # 这是函数哦,不是方法,记得要手动传self
        return data
    # 2. 是否显示添加按钮
    show_add_btn = True
    def get_add_btn(self):
        return self.show_add_btn


##################3'''url相关'''############################3

    def get_urls(self):
        app_model_name = self.model_class._meta.app_label,self.model_class._meta.model_name
        url_patterns = [
            url(r'^$',self.changelist_view,name='%s_%s_changelist'%(app_model_name)),
            url(r'^add/$',self.add_view,name='%s_%s_add'%(app_model_name)),
            url(r'^(\d+)/delete/$',self.delete_view,name='%s_%s_delete'%(app_model_name)),
            url(r'^(\d+)/edit/$',self.edit_view,name='%s_%s_edit'%(app_model_name)),
        ]
        return url_patterns

    @property
    def urls(self):
        return self.get_urls()

    def get_edit_url(self,nid):
        name = "oomph6:%s_%s_edit" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name, args=(nid,)) # 有正则,就要加args动态反向生成url
        return edit_url
    def get_list_url(self): # 列表页面
        name = "oomph6:%s_%s_changelist" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_add_url(self):
        name = "oomph6:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_delete_url(self,nid):
        name = "oomph6:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name,args=(nid,))
        return edit_url

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
        for field_name in self.get_list_display():
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
            for field_name in self.get_list_display():
                if isinstance(field_name,str):
                      # temp.append(getattr(field_name,row))
                    val = getattr(row,field_name)   # 这步很骚哦.!!反射!!
                else: # 如果是函数
                      # temp.append(field_name(self,row))
                    val = field_name(self,row)      # 第一个参数是本身自己的,第二个参数代指对象,是从41行拿的
                temp.append(val)
            new_data_list.append(temp)
        return render(request,'oomph6/changelist.html',{'data_list':new_data_list,'head_list':head_list,'add_url':self.get_add_url(),'show_add_btn':self.get_add_btn()})

    def add_view(self,request,*args,**kwargs):
        '''使用ModelForm来实现该视图函数'''
        class TestModelForm(ModelForm):
            class Meta:
                model = self.model_class
                fields = '__all__'
        if request.method == 'GET':
            form = TestModelForm()
            return render(request,'oomph6/add_view.html',{'form':form})
        else:
            form = TestModelForm(request.post)
            if form.is_valid():
                form.save()  # save()过后说明保存成功了,就需要跳转到列表页面,对不对,在不在理
                return redirect(self.get_list_url())
            return render(request,'oomph6/add_view.html',{'form':form})


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
        return (self.get_urls(),'oomph6',None)

site = Oomph6Site()