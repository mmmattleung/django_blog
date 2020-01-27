class Foo:
    def __init__(self, name):
        self.name = name

    #给对象设置属性，就会触发setattr
    def __setattr__(self, key, value):
        if not isinstance(value, str):
            raise TypeError('must be str')
        print('setattr----key: %s, %s' % (key, value))
        print(type(key))
        #不能使用setattr()设置，会造成递归报错
        self.__dict__[key] = value

    def __delattr__(self, item):
        print('delattr: %s' % item)
        self.__dict__.pop(item)

    def __getattr__(self, item):
        #属性不存在就会触发
        print('getattr: %s %s' % (item, type(item)))


f1 = Foo('a')
# f1.age = '18'
# del f1.age
# print(f1.age)
print(f1.xxxxxxx)