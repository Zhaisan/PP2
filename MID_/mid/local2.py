Задача 1: Вернуть первое слово из строки
* Сначала попробуем вытащить каждый символ (используя .)
result = re.findall(r'.', 'test programming technologies test')

* Для того, чтобы в конечный результат не попал пробел, используем вместо . \w.
result = re.findall(r'\w', 'test programming technologies test')

* Теперь попробуем достать каждое слово (используя * или +)
result = re.findall(r'\w*', 'test programming technologies test')
result = re.findall(r'\w+', 'test programming technologies test')

* Теперь вытащим первое слово, используя ^:
result = re.findall(r'^\w+', 'test programming technologies test')

* Если мы используем $ вместо ^, то мы получим последнее слово, а не первое:
result = re.findall(r'\w+$', 'test programming technologies test1')
------------------------------------------------
Задача 2: Вернуть первые два символа каждого слова
* Вариант 1: используя \w, вытащить два последовательных символа, кроме пробельных, из каждого слова:
result = re.findall(r'\w\w', 'hello world programming technologies')

* Вариант 2: вытащить два последовательных символа, используя символ границы слова (\b):
result = re.findall(r'\b\w\w', 'hello world programming technologies')


Задача 3: вернуть список доменов из списка адресов электронной почты
abc.test@gmail.com, xyz@mail.ru, a.akshabayev@kbtu.kz

* Сначала вернем все символы после «@»
re.findall(r'@\w+', 'abc.test@gmail.com, xyz@mail.ru, a.akshabayev@kbtu.kz')

* части «.com», «.in» и т. д. не попали в результат. Изменим наш код:
re.findall(r'@\w+.\w+', 'abc.test@gmail.com, xyz@mail.ru, a.akshabayev@kbtu.kz')

* Второй вариант — вытащить только домен верхнего уровня, используя группировку — ():
re.findall(r'@\w+.(\w+)', 'abc.test@gmail.com, xyz@mail.ru, a.akshabayev@kbtu.kz')
------------------------------------------------
Задача 4: Извлечь дату из строки
* Используем \d для извлечения цифр.
result = re.findall(r'\d{2}-\d{2}-\d{4}', 'Amit 34-3456 12-05-2007, XYZ 56-4532 11-11-2011, ABC 67-8945 12-01-2009')

* вывести только год (месяц, день)
result = re.findall(r'\d{2}-\d{2}-(\d{4})', 'Amit 34-3456 12-05-2007, XYZ 56-4532 11-11-2011, ABC 67-8945 12-01-2009')
------------------------------------------------
Задача 5: Извлечь все слова, начинающиеся на гласную (aeiouAEIOU)
* Найдем все слова
result = re.findall(r'\w+', 'abc tatt eia a bobb')

* А теперь — только те, которые начинаются на определенные буквы
result = re.findall(r'[aeiouAEIOU]\w+', "abc tatt eia a bobb")

* Выше мы видим обрезанные слова, Для того, чтобы убрать их, используем \b для обозначения границы слова
result = re.findall(r'\b[aeiouAEIOU]\w+', "abc tatt eia a bobb")

* Также мы можем использовать ^ внутри квадратных скобок для инвертирования группы:
result = re.findall(r'\b[^aeiouAEIOU]\w+', "abc tatt eia a bobb")

* В результат попали слова, «начинающиеся» с пробела. Уберем их, включив пробел в диапазон в квадратных скобках:
result = re.findall(r'\b[^aeiouAEIOU ]\w+', "abc tatt eia a bobb")
------------------------------------------------
* Задача 6: Проверить телефонный номер 
text = '+7-777-5673443, +7-772-2344343 abc'
result = re.findall(r'\+7-[0-9]{3}-[0-9]{5}', text)
------------------------------------------------
Задача 7: Разбить строку по нескольким разделителям
line = 'asdf fjdk;afed,fjek,asdf,foo'
# String has multiple delimiters (";",","," ").

result = re.split(r'[;, ]', line)

Также мы можем использовать метод re.sub() для замены всех разделителей пробелами:
result = re.sub(r'[;, ]', ' ', line)



Using comprehensions print all prime numbers between 1, 1000
import math
def f(x):
    if x == 1:
        return False
    for i in range(2, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True
res = list(range(1, 1000))
res_prime = [item for item in res if f(item)]
print(res_prime)