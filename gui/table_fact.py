from tkinter import *
from tkinter import ttk
from pathlib import Path
from pathlib import Path
from tkinter import messagebox 
import os
from sqlite3 import *

ASSETS_PATH = Path(__file__).resolve().parent / "assets"

class tb:
    def __init__(self):

        self.window2 = Toplevel()
        self.window2.grab_set()
        w = 620
        h = 370 
        ws = self.window2.winfo_screenwidth()
        hs = self.window2.winfo_screenheight() 
        x = (ws/2) - (w/2)
        y = (hs/3) - (h/3)
        self.window2.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.window2.title("Facturas editadas")
        self.window2.iconbitmap(str(ASSETS_PATH / "iconbitmap1.ico"))
        self.frame = Frame(self.window2)
        self.frame.pack()
        self.table = ttk.Treeview(self.frame, height=15, columns=('#0', '#1', '#2', '#3', '#4'))
        self.table.grid(row=2, column=0, columnspan=5)
    def search(self):
        query = self.search_entry.get()
        if query:
            selections = []
            for child in self.table.get_children():
                ls =str(self.table.item(child)['values'])
                if query.lower() in ls.lower():
                    data = self.table.item(child)['values']
                    print(data)
                    selections.append(child)
            print('search completed')
            self.table.selection_set(selections)
        else:
            messagebox.showerror(title='Busqueda Vacía', message='¡Ingrese algo para buscar!')
            self.window2.after(1, lambda: self.window2.focus_force())
    def tblib(self):
        lb1 = Label(self.frame, text="Buscar:")
        lb1.grid(row=1, column=1, padx=125, pady=2, sticky=E)
        self.search_entry = Entry(self.frame, width=20)
        self.search_entry.grid(row=1, column=1, padx=0,
                               pady=10, sticky=E, rowspan=1)
        btn = Button(self.frame, text="Ir", width=5, command=self.search)
        btn.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")
        btn2 = Button(self.frame, text="ABRIR", width=10, command=lambda:self.open_file())
        btn2.grid(row=1, column=4, padx=10, pady=5, sticky="nsew")
        boton1 = Button(self.frame, text="ACTUALIZAR", command=lambda: self.window2.destroy(
        ) or self.window2.after(0, tb().tblib()))
        boton1.grid(row=1, column=3, padx=10, pady=5, sticky="nsew")
        self.table.heading("#0", text="ID")
        self.table.heading("#1", text="NIT")
        self.table.heading("#2", text="SERIE")
        self.table.heading("#3", text="FECHA")
        self.table.heading("#4", text="HORA")
        self.table.heading("#5", text="NOMBRE ARCHIVO")
        self.table.column("#0", width=40)
        self.table.column("#1", width=150)
        self.table.column("#2", width=90)
        self.table.column("#3", width=100)
        self.table.column("#4", width=70)
        self.table.column("#5", width=150)
        cn = connect("./db/FACTURAS")
        miCursor=cn.cursor()
        miCursor.execute("SELECT * FROM Facturas")
        facturas = miCursor.fetchall()
        for pr in facturas:
            self.table.insert('', END, text=pr[0], values=(pr[1],
                pr[2], pr[3], pr[4], pr[5]))
        cn.commit()
        cn.close()
        style = ttk.Style()
        style.theme_use("xpnative")
        style.map("Treeview")
        style.map("Button")
        if __name__ == '__main__':        
            self.window2.mainloop()
    def open_file(self):
        query = self.search_entry.get()
        data = []
        try:
            if query: 
                for child in self.table.get_children():
                    ls =str(self.table.item(child)['values'])
                    if query.lower() in ls.lower():
                        data = self.table.item(child)['values']
            else:
                curItem = self.table.focus()
                data = self.table.item(curItem)["values"]
            if data:
                path = Path(__file__).resolve().parent / "pdf"
                os.system('"'+str(path) + "/"+data[4]+'.pdf'+'"')
            else:
                messagebox.Message(master=self.window2)
                messagebox.showerror(title='Selección Vacía', message='¡No ha seleccionado ningun registro!')
                self.window2.after(1, lambda: self.window2.focus_force())
        except:
            messagebox.showerror(title='Error.', message='El archivo no fue encontrado.')