from django.test import TestCase

# Create your tests here.
class Base(object):
    def __init__(self,val):
        self.val = val
    def func(self):
        self.test()
        print(self.val)
    def test(self):
        print('Base.test')

class Foo(Base):
    def test(self):
        print('Foo.test')

class Bar(object):
    def __init__(self):
        self._registry = {}
    def register(self,a,b=None):
        if not b:
            b = Base
        self._registry[a] = b(a) # 函数、类、对象
# 执行 __init__，并获取到一个对象： b._registry; b.register
obj = Bar()
# obj._regitry[1] = Foo(1)
# { 1: Foo(1)  }
obj.register(1,Foo)
# obj._regitry[2] = Base(2)
# { 1: Foo(1), 2: Base(2) }
obj.register(2)
# 1. _registry中到底有什么？
# 2. 输出结果
obj._registry[1].func() # Foo的对象
obj._registry[2].func() # Base对象