def method(call):
    def wrapper(*args, **kwargs):
        return call(*args, **kwargs)
    return wrapper
class cached_data(object):
    def __init__(self,function):
        self._function = function
        self._lock = False
        self._value = None
    def __call__(self,*args,**kwargs):
        if not self._lock:
            self._value = self._function(*args,**kwargs)
            self._lock = True
            print("NoLock")
        return self._value
 
import time
class A():
    def __init__(self):
        self.abc = "world"
    @method
    @cached_data
    def fun(self):
        time.sleep(3)
        return "hello" + self.abc
 
if __name__ == "__main__1":
    a = A()
    begin = time.time()
    print(a.fun())
    print(time.time() - begin)
    begin = time.time()
    print(a.fun())
    print(time.time() - begin)
    
class PureData():
    def __init__(self):
        self.name = "Bob"
        self.id = "1127"

class Interface():
    def __init__(self,data):
        self.data = data
    def __getattr__(self,item):
        return self.data.__dict__[item]
            
    
if __name__ == "__main__":
    my_data = PureData()
    my_data.name = "BobFeng"
    my_data.id = "11271395"
    my_in = Interface(my_data)
    print(my_in.name)
    print(my_in.id)
    my_data2 = PureData()
    my_data2.name = "bfeng1"
    my_data2.id = "none"
    my_in2 = Interface(my_data2)
    print(my_in2.name)
    print(my_in2.id)
    print(my_data2.age)
