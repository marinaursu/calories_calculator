from tkinter import *
from tkinter import messagebox

import csv
from os.path import exists
if not exists("calories.csv"): #проверка на наличие файла calorie.csv возле скрипта, в случае отсутсвия выход из программы
    print("\033[91mБаза с таблицей каллорийности отсутствует!\033[0m")
    messagebox.showerror("Ошибка", "База с таблицей каллорийности отсутствует!")
    quit()
with open("calories.csv", encoding='utf-8') as r_file:
    file_reader = csv.DictReader(r_file, delimiter=";")
    rows = list(file_reader)

def calculate_calories_button(): # Функция реакции на нажатие кнопки
    calculate_calories(wg.get(),search(pn.get())) #Передаем на подсчёт wg - съеденные граммы, search(pn) - результат поиска в базе

# Tkinter объекты:
bg_color = '#0FCAF4' # цвет заднего фона
buttons_color = '#0F99F4' # цвет кнопок
tk = Tk()
pn = StringVar() # tkinter переменная для хранения названия продукта которое вводит пользователь
wg = StringVar() # tkinter переменная для хранения съеденных граммов продукта
tip_var = StringVar() # tkinter переменная для заполнения подсказки из имеющихся продуктов в базе
cal_calc = StringVar() # tkinter переменная для вывода подсчёта каллорийности в Label

tk.title('Подсчёт потребленных каллорий') #заголовок окна
tk.geometry('800x640') #размер окна 800 пикселей на 600 пикселей
tk.option_add('*font', ('verdana', 12, 'bold')) # утсанавливаем шрифт (verdana), размер шрифта (12), начертание шрифта (жирный)
tk.resizable(width=False, height=False) # отключаем изменение размера/растягивание окна

frame = Frame(tk, bg=bg_color) # создаем рамку в главном окне с именем frame
frame.place(relwidth=1, relheight=1) # Относительная ширина/высота фрейма 1 (100%), на весь размер окна
pn.trace("w", lambda name, index, mode, pn=pn: callback(pn))
product_name = Entry(frame,width=30, textvariable=pn,bg='white').grid(row=1, column=0,padx=(20, 10))
weight_gramm = Entry(frame, textvariable=wg,bg='white',width=10).grid(row=1, column=1,padx=(1, 10))
Label(frame, text='Продукт', bg=bg_color, font=24).grid(row=0, column=0)
Label(frame, text='Кол-во (грамм)', bg=bg_color, font=24).grid(row=0, column=1)
btn=Button(frame, text='Подсчитать', bg=buttons_color, command=calculate_calories_button,font = ('calibre',10,'bold')).grid(row=1, column=3)
if tip_var != None and tip_var != "":
    tips=Label(frame, textvariable=tip_var, relief=RAISED, bg='white', font=18).grid(row=3, column=0,padx=(20, 10))

def search(product):
    tmp = ""
    y = [i for i in rows if i['Наименование'].upper().startswith(product.upper())]
    if len(y) >= 1 and product != "":
        for k in y:
            tmp += k['Наименование'] + "" if k == y[-1] else k['Наименование'] + "\n"
            tip_var.set(tmp)
        return y[0]

def callback(entered_text):
    search(entered_text.get())

def calculate_calories(current_weight, current_product):
    current_weight = 1 if current_weight == '' else current_weight  # если переменная пустая то присваиваем 1
    if float(current_weight) > 0 and current_product != None:
        c = round(float(current_weight)*(float(current_product['Калорийность'])/100),2)
        p = round(float(current_weight)*(float(current_product['Белков'])/100),2)
        f = round(float(current_weight)*(float(current_product['Жиров'])/100),2)
        ch = round(float(current_weight)*(float(current_product['Углеводов'])/100),2)
        tmp_calc = f"-----------------------------------\nПродукт: {current_product['Наименование']}    - {current_weight} г."
        tmp_calc += f"\nБелков: {p}\nЖиров: {f}\nУглеводов: {ch}\n--------------------\nЭнергитическая ценность: {c} Ккал."
        cal_calc.set(tmp_calc)
        Label(frame, textvariable=cal_calc,  bg=bg_color, font=18,anchor="w").grid(row=4, column=0,padx=(10, 10))
    else:
        add_product_msg_box = messagebox.askquestion('Продукт отсутствует!', 'Хотите добавить свой продукт?',icon='info')
        if add_product_msg_box == 'yes':
            add_new_product(pn.get())
def add_new_product(new_product_name):
    frame2 = Frame(tk, bg=bg_color) # Создаем второй фрэйм который перекроет первый чтоб разместить новые объекты
    frame2.place(relwidth=1, relheight=1)  # Относительная ширина/высота фрейма2 =  1 (100%), на весь размер окна
    new_name = StringVar()
    new_name.set(new_product_name)
    new_proteins = StringVar()
    new_proteins.set(0)
    new_fat = StringVar()
    new_fat.set(0)
    new_carbohydrates = StringVar()
    new_carbohydrates.set(0)
    new_calories = StringVar()
    new_calories.set(0)
    Label(frame2, text='Продукт', bg=bg_color, font=24).grid(row=0, column=1)
    Label(frame2, text='Белков на 100г', bg=bg_color, font=24).grid(row=2, column=0)
    Label(frame2, text='Жиров на 100г', bg=bg_color, font=24).grid(row=2, column=1)
    Label(frame2, text='Углеводов на 100г', bg=bg_color, font=24).grid(row=5, column=0)
    Label(frame2, text='Каллорийность на 100г', bg=bg_color, font=24).grid(row=5, column=1)
    Entry(frame2, width=20, textvariable=new_name, bg='white').grid(row=1, column=1, padx=(20, 10),pady=(10, 10))
    Entry(frame2, textvariable=new_proteins, bg='white', width=10).grid(row=4, column=0, padx=(1, 10),pady=(1, 10))
    Entry(frame2, textvariable=new_fat, bg='white', width=10).grid(row=4, column=1, padx=(1, 10),pady=(1, 10))
    Entry(frame2, textvariable=new_carbohydrates, bg='white', width=10).grid(row=6, column=0, padx=(1, 10),pady=(1, 10))
    Entry(frame2, textvariable=new_calories, bg='white', width=10).grid(row=6, column=1, padx=(1, 10),pady=(1, 10))
    def get_latest_data_entered_by_user(): # служебная функция чтоб получать последние данные введённые пользователем
        new_product_dict = {'Наименование': new_name.get(), 'Белков': new_proteins.get(), 'Жиров': new_fat.get(),
                            'Углеводов': new_carbohydrates.get(), 'Калорийность': new_calories.get()}
        return new_product_dict
    # Без лямбды кнопка выполняла команду без нажатия, как временное решение нашла lambda, потом разберусь в чем причина
    Button(frame2, text='Сохранить', bg=buttons_color, command=lambda: save_new_product(get_latest_data_entered_by_user()), font=('calibre', 10, 'bold')).grid(row=1, column=3)

    def save_new_product(new_product_data):
        save_product_msg_box = messagebox.askquestion('Сохранение...!', 'Вы уверены что хотите сохранить?', icon='info')
        if save_product_msg_box == 'yes':
            with open("calories.csv", mode="a", encoding='utf-8') as w_file:
                file_writer = csv.DictWriter(w_file, delimiter=";", lineterminator="\r", fieldnames=(
                "Наименование", "Белков", "Жиров", "Углеводов", "Калорийность"))
                file_writer.writerow(new_product_data)
            frame2.destroy() # Разрушаем второй фрэйм (frame2) чтобы опять увидеть первый (frame)


tk.mainloop()
