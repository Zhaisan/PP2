import re
result = re.findall(r'\w*', 'test programming technologies test')
result = re.findall(r'\w+', 'test programming technologies test')
print(result)