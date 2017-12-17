# 只要一启动先执行这个
from app01 import models
from oomph6.service import vv1


vv1.site.register(models.UserInfo)
vv1.site.register(models.Role)