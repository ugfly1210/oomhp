from django.shortcuts import render

# Create your views here.

#
# HOST_LIST = []
#
# for i in range(101):
#     HOST_LIST.append('第%s次,我爱你❄️❄'%i)
#
# def hosts(request):
#     '''查看用户请求的当前页'''
#     current_page = int(request.GET.get('page'))
#     # 每页要显示的个数
#     show_page_count = 10
#     # 计算数据库中的数据
#     start = (current_page-1) * show_page_count # 当前页起始数据数
#     end = current_page * show_page_count       # 当前页结束数数
#     host = HOST_LIST[start:end]
#     # 当前数据库中所有数据
#     totle_count = len(HOST_LIST)
#     # 当前数据能显示的最大页
#     max_page_num,div = divmod(totle_count,show_page_count)
#     if div > 0 :
#         max_page_num += 1
#
#     for i in range(1,max_page_num+1): # 先拿到从头到尾
#         if i == current_page :
#             "<a class='avtive' href=''>"

from utils.fy import Pagination
HOST_LIST = []
for i in range(1,199):
    HOST_LIST.append('%s 加入到修理赵贱明团队中...'%i)

def hosts(request):
    pager_obj = Pagination(request.GET.get('page',1),len(HOST_LIST),request.path_info)
    host_list = HOST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render(request,'hosts,html',{'host_list':host_list,'page_html':html})

USER_LIST = []

for i in range(1,305):
    USER_LIST.append('%s 修理完赵贱明了已经...'%i)
def users(request):
    pager_obj = Pagination(request.GET.get('page',1),len(USER_LIST),request.path_info)
    user_list = HOST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render(request,'users.html',{'user_list':user_list,'page_html':html})
