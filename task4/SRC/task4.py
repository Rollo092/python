import sys
text_orig = sys.argv[1]     #Оригинал текста
text_serch = sys.argv[2]    #Текст №2
y = 0           #Начальная позиция индексов       
if text_orig == text_serch:
     print (text_orig, text_serch, '- OK')
elif text_serch.find('*') != -1: # Есть в тексте №2 "*"? Если есть то присваиваем n
    n = text_serch.find('*')     # Вычислили позицию *
    while text_orig[y] == text_serch[y]:
	    y=y+1           # Сравниваем, пока не упремся в разные символы
    if n == y:              # Если позиция * в строке b совпадает "разными символами"
        print (text_orig, text_serch , "- OK")        # то значит все последующее = оригининалу
    else:
        print(text_orig, text_serch , '- KO')     # Если позиция отличается от *, то значит стр2 != стр1
