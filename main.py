from time import sleep
from tkinter.ttk import Treeview
from DB import DB
from tkinter import *
from tkinter import messagebox

class Table:
    def __init__(self):
        self.cur_displayed = []
        table_frame = Frame(main_window)
        table_frame.grid(row=0, column=0, pady=30)

        col = ('ID', 'Тип', 'Грузопобъёмность', 'Длина', 'Ширина', 'Высота', 'Свободен')

        self.table = Treeview(table_frame, columns=col, show='headings')
        self.table.column('ID', width=38, anchor=CENTER)
        self.table.column('Тип', width=120, anchor=CENTER)
        self.table.column('Грузопобъёмность', width=160, anchor=CENTER)
        self.table.column('Длина', width=80, anchor=CENTER)
        self.table.column('Ширина', width=80, anchor=CENTER)
        self.table.column('Высота', width=80, anchor=CENTER)
        self.table.column('Свободен', width=80, anchor=CENTER)

        for c in col:
            self.table.heading(c, text=c)
        self.table.pack()

    def add(self, a):
        self.table.insert('', END, values=a)
        self.table.pack()

    def clear(self):
        for i in self.table.get_children():
            self.table.delete(i)

    def display_all(self):
        self.clear()
        self.all = db.all()
        self.cur_displayed = self.all.copy()
        if disp_op.get() == 1:
            self.display_free()
        elif disp_op.get() == 2:
            self.display_booked()
        else:
            self.display_cur()

    def display_selected(self, values):
        self.clear()
        self.all = db.size(values[0], values[1], values[2], values[3])
        self.cur_displayed = self.all.copy()
        if len(self.all) == 0:
            messagebox.showwarning(title='Предупреждение', message='Ни одной машины подходящий под заданные параметры не найдено.')
        if disp_op.get() == 1:
            self.display_free()
        elif disp_op.get() == 2:
            self.display_booked()
        else:
            self.display_cur()

    def update(self):
        if disp_op.get() == 1:
            self.display_free()
        elif disp_op.get() == 2:
            self.display_booked()
        else:
            self.display_cur()

    def display_free(self):
        self.clear()
        self.cur_displayed = []
        for q in self.all:
            if q[-1] == 1:
                self.cur_displayed.append(q)
        if sort_op.get() == 1:
            self.sort_by_id()
        else:
            self.sort_by_cap()

    def display_booked(self):
        self.clear()
        self.cur_displayed = []
        for q in self.all:
            if q[-1] == 0:
                self.cur_displayed.append(q)
        if sort_op.get() == 1:
            self.sort_by_id()
        else:
            self.sort_by_cap()

    def display_cur(self):
        self.clear()
        self.cur_displayed = self.all
        if sort_op.get() == 1:
            self.sort_by_id()
        else:
            self.sort_by_cap()

    def sort_by_cap(self):
        self.clear()
        transport_all = self.cur_displayed
        for i in range(len(transport_all)):
            transport_all[i] = list(transport_all[i])
            transport_all[i][0], transport_all[i][2] = transport_all[i][2], transport_all[i][0]
        transport_all = sorted(transport_all)
        for i in range(len(transport_all)):
            transport_all[i][0], transport_all[i][2] = transport_all[i][2], transport_all[i][0]
            transport_all[i] = tuple(transport_all[i])
        for q in transport_all:
            self.add(q)

    def sort_by_id(self):
        self.clear()
        cur = sorted(self.cur_displayed)
        for q in cur:
            self.add(q)

    def book_unbook(self):
        q = self.table.focus()
        if q == '':
            messagebox.showerror(title='Ошибка', message='Ничего не выбрано')
            return
        q = self.table.item(q)
        q = q['values'].copy()
        for i in range(2, 6):
            q[i] = float(q[i])
        q_t = tuple(q)
        if q[-1] == 1:
            q[-1] = 0
            db.book(q[0])
        else:
            q[-1] = 1
            db.unbook(q[0])
        for i in range(len(self.all)):
            if self.all[i] == q_t:
                self.all[i] = tuple(q)
        self.update()

    def delete(self):
        q = self.table.focus()
        if q == '':
            messagebox.showerror(title='Ошибка', message='Ничего не выбрано')
            return
        q = self.table.item(q)
        q = q['values'].copy()
        for i in range(2, 6):
            q[i] = float(q[i])
        q_t = tuple(q)
        db.delete(q[0])
        self.all.remove(q_t)
        self.update()

class filter_search_window:
    def __init__(self, mode=0):
        self.mode = mode
        all['state'] = DISABLED
        choise['state'] = DISABLED
        add['state'] = DISABLED

        self.entry_window = Toplevel()
        self.entry_window.title('Окно ввода')
        self.entry_window.geometry('370x140')
        self.entry_window.resizable(0, 0)
        self.l_weight = Label(self.entry_window, text='Введите массу перевозимого груза')
        self.l_length = Label(self.entry_window, text='Ввведите длинну перевозимого груза')
        self.l_width = Label(self.entry_window, text='Ввведите ширину перевозимого груза')
        self.l_height = Label(self.entry_window, text='Ввведите высоту перевозимого груза')
        k = 0

        if self.mode == 1:
            self.l_weight.configure(text='Введите грузопобъёмность машины')
            self.l_length.configure(text='Ввведите максимальную длинну перевозимого грза')
            self.l_width.configure(text='Ввведите максимальную ширину перевозимого грза')
            self.l_height.configure(text='Ввведите максимальную высоту перевозимого грза')
            self.entry_window.geometry('450x180')
            self.l_id = Label(self.entry_window, text='Введите уникальный id транспорта')
            self.l_type = Label(self.entry_window, text='Введите название марки машины')
            self.l_id.grid(row=0, column=0, sticky=W, padx=10)
            self.l_type.grid(row=1, column=0, sticky=W, padx=10)
            k = 2

        self.l_weight.grid(row=k, column=0, sticky=W, padx=10)
        self.l_length.grid(row=k+1, column=0, sticky=W, padx=10)
        self.l_width.grid(row=k+2, column=0, sticky=W, padx=10)
        self.l_height.grid(row=k+3, column=0, sticky=W, padx=10)

        self.entries = []
        self.id = StringVar()
        self.type = StringVar()
        for i in range(4):
            self.entries.append(StringVar())
#            self.entries[i].set('')

        if self.mode == 1:
            self.e_id = Entry(self.entry_window, textvariable=self.id)
            self.e_type = Entry(self.entry_window, textvariable=self.type)
            self.e_id.grid(row=0, column=1, sticky=W)
            self.e_type.grid(row=1, column=1, sticky=W)
        self.e_weight = Entry(self.entry_window, textvariable=self.entries[0])
        self.e_length = Entry(self.entry_window, textvariable=self.entries[1])
        self.e_width = Entry(self.entry_window, textvariable=self.entries[2])
        self.e_height = Entry(self.entry_window, textvariable=self.entries[3])
        self.e_weight.grid(row=k, column=1, sticky=W)
        self.e_length.grid(row=k+1, column=1, sticky=W)
        self.e_width.grid(row=k+2, column=1, sticky=W)
        self.e_height.grid(row=k+3, column=1, sticky=W)

        if self.mode == 0:
            self.submit_b = Button(self.entry_window, text='Подобрать машину по заданным параметрам', command=lambda: self.submit())
        else:
            self.submit_b = Button(self.entry_window, text='Добавить машину', command=lambda: self.add())
        self.submit_b.grid(row=6, column=0, columnspan=2, pady=15)

        self.entry_window.protocol("WM_DELETE_WINDOW", self.unblock)
        self.entry_window.mainloop()

    def unblock(self):
        all['state'] = NORMAL
        choise['state'] = NORMAL
        add['state'] = NORMAL
        self.entry_window.destroy()

    def clear_entries(self):
        for i in range(4):
            self.entries[i].set('')
        self.e_weight.delete(0, 'end')
        self.e_length.delete(0, 'end')
        self.e_width.delete(0, 'end')
        self.e_height.delete(0, 'end')
        if self.mode == 1:
            self.id.set('')
            self.type.set('')
            self.e_id.delete(0, 'end')
            self.e_type.delete(0, 'end')

    def input_error(self, s):
        messagebox.showerror(title='Ошибка', message=s)
        self.clear_entries()

    def add(self):
        id = self.id.get()
        type = self.type.get()
        param = [self.entries[i].get() for i in range(4)]
        print(id, type, *param)
        try:
            id = int(id)
            for i in range(4):
                param[i] = param[i].replace(',', '.')
                param[i] = float(param[i])
        except:
            self.input_error('Некоректный ввод одного или нескольких параметров.\nПопробуйте снова.')
            return
        ok = True
        if id <= 0:
            ok = False
        if type == '':
            ok = False
        for i in range(4):
            if param[i] <= 0:
                ok = False
        if not db.unique(id):
            ok = False
        if not ok: 
            self.input_error('Некоректный ввод одного или нескольких параметров.\nПопробуйте снова.')
            return
        db.insert_new(id, type, param[0], param[1], param[2], param[3])
        table.display_all()
        self.unblock()

    def submit(self):
        emp = 0
        values = ['' for i in range(4)]
        for i in range(4):
            values[i] = self.entries[i].get()
            values[i] = values[i].replace(',', '.')
            if values[i] == '':
                values[i] = '0'
                emp += 1
            if values[i][0] == '-':
                values[i] = 'qqq'
        try:
            for i in range(4):
                values[i] = float(values[i])
        except:
            self.input_error('Некоректный ввод одного или нескольких параметров.\nПопробуйте снова.')
            return
        if emp >= 4:
            self.input_error('Ничего не введено.')
            return
        if 1 <= emp <= 3:
            messagebox.showwarning(title='Предупреждение', message='Введены не все значения\nПустые ячейки не будут учитываться при поиске')
        self.unblock()
        choose_a_car_finish(values)
        

def choose_a_car():
    choise = filter_search_window()

def choose_a_car_finish(values):
    table.display_selected(values)

def add_an_element():
    adding = filter_search_window(1)

main_window = Tk()
main_window.title('Домашка')
main_window.geometry('640x440')
main_window.resizable(0, 0)

db = DB()
table = Table()

test_focuc = Button(main_window, text='Забронировать/разбронировать транспорт', height=1, width=35, anchor=W, command=lambda: table.book_unbook())
test_focuc.place(x=0, y=270)
deleting = Button(main_window, text='Удалить транспорт из базы', height=1, width=21, anchor=E, command=lambda: table.delete())
deleting.place(x=480, y=270)

ask_sort = Label(main_window, text='Сортировать по: ')
ask_sort.place(x=0, y=300)
sort_op = IntVar()
sort_op.set(1)
sort_op_1 = Radiobutton(main_window, text='по номеру', variable=sort_op, value=1, command=lambda: table.sort_by_id())
sort_op_2 = Radiobutton(main_window, text='по грузоподъёмности', variable=sort_op, value=2, command=lambda: table.sort_by_cap())
sort_op_1.place(x=100, y=300)
sort_op_2.place(x=200, y=300)

ask_disp = Label(main_window, text='Показывать: ')
disp_op = IntVar()
disp_op.set(3)
disp_op_1 = Radiobutton(main_window, text='только свободный транспорт', variable=disp_op, value=1, command=lambda: table.display_free())
disp_op_2 = Radiobutton(main_window, text='только занятый транспорт', variable=disp_op, value=2, command=lambda: table.display_booked())
disp_op_3 = Radiobutton(main_window, text='весь транспорт', variable=disp_op, value=3, command=lambda: table.display_cur())
ask_disp.place(x=0,y=320)
disp_op_1.place(x=100, y=320)
disp_op_2.place(x=300, y=320)
disp_op_3.place(x=480, y=320)

all = Button(main_window, text = 'Показать весь транспорт', width=40, height=1, anchor=CENTER, command=lambda: table.display_all(), fg='#000000')
all.place(x=180, y=350)
choise = Button(main_window, text='Подобрать грузовик', width=40, height=1, anchor=CENTER, command=lambda: choose_a_car(), fg='#000000')
choise.place(x=180, y=380)
add = Button(main_window, text='Добавить новый транспорт', width=40, height=1, anchor=CENTER, command=lambda: add_an_element(), fg='#000000')
add.place(x=180, y=410)

main_window.mainloop()