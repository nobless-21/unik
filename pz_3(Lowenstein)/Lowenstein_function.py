from fuzzywuzzy import fuzz
from fuzzywuzzy import process

a = fuzz.ratio('Привет мир', 'Привет мир')
print(a)

a = fuzz.ratio('Привет мир', 'Привт кир')
print(a)

a = fuzz.partial_ratio('Привет мир', 'Привет мир!')
print(a)

a = fuzz.partial_ratio('Привет мир', 'Люблю колбасу, Привет мир')
print(a)

a = fuzz.partial_ratio('Привет мир', 'Люблю колбасу, привет мир')
print(a)

a = fuzz.token_sort_ratio('Привет наш мир', 'мир наш Привет')
print(a)

a = fuzz.token_sort_ratio('Привет наш мир', 'мир наш любимый Привет')
print(a)

a = fuzz.token_sort_ratio('1 2 Привет наш мир', '1 мир наш 2 ПриВЕт')
print(a)

a = fuzz.token_set_ratio('Привет наш мир', 'мир мир наш наш наш ПриВЕт')
print(a)

a = fuzz.WRatio('Привет наш мир', '!ПриВЕт наш мир!')
print(a)

a = fuzz.WRatio('Привет наш мир', '!ПриВЕт, наш мир!')
print(a)

city = ["Москва", "Санкт-Петербург", "Саратов", "Краснодар", "Воронеж", "Омск", "Екатеринбург", "Орск", "Красногорск", "Красноярск", "Самара"]
a = process.extract("Саратов", city, limit=2)
print(a)

city = ["Москва", "Санкт-Петербург", "Саратов", "Краснодар", "Воронеж", "Омск", "Екатеринбург", "Орск", "Красногорск", "Красноярск", "Самара"]
a = process.extractOne("Краногрск", city)
print(a)

#открытие файла на рабочем столе
#try:
#    files = os.listdir('C:\\Users\\hartp\\Desktop\\')
#    filestart = process.extractOne(namerec, files)
#    if filestart[1] >= 80:
#        os.startfile('C:\\Users\\hartp\\Desktop\\' + filestart[0])
#    else:
#        speak('Файл не найден')
#except FileNotFoundError:
 #   speak('Файл не найден')
