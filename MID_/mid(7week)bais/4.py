import re
res = re.findall(r'@\w+.(\w+)', 'abc.test@gmail.com, xyz@mail.ru, a.akshabayev@kbtu.kz')
print(res)