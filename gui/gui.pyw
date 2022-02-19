import re
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.font as tkfont
import configure_fact as cf
import configparser as cp
import table_fact as table
import pyperclip
from pathlib import Path
import program_get_pdf as pgd

ASSETS_PATH = Path(__file__).resolve().parent / "assets"

app_path = Path(__file__).resolve().parent

output_path = ""

class main:
    def __init__(self):
        self.ini()
        self.window = tk.Tk()
        w = 450
        h = 480 
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight() 
        x = (ws/2) - (w/2)
        y = (hs/3) - (h/3)
        self.window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        logo = tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
        self.window.call('wm', 'iconphoto', self.window._w, logo)
        self.window.title("")
        self.window.configure(bg="#FCFCFC")
        canvas = tk.Canvas(
            self.window, bg="#FCFCFC", height=519, width=862,
            bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=-430, y=0)
        text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
        token_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
        URL_entry_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
        filePath_entry_img = canvas.create_image(650.5, 329.5, image=text_box_bg)

        self.token_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
        self.token_entry.place(x=60, y=137+25, width=290.0, height=35)
        self.token_entry.focus()

        self.URL_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
        self.URL_entry.place(x=60, y=218+25, width=290.0, height=35)

        self.path_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
        self.path_entry.place(x=60, y=299+25, width=290.0, height=35)

        table_picker_img = tk.PhotoImage(file = ASSETS_PATH / "table.png")
        table_picker_button = tk.Button(
            image = table_picker_img,
            text = '',
            compound = 'center',
            fg = 'white',
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda:table.tb().tblib(),
            relief = 'flat')

        table_picker_button.place(
            x = 337, y = 75,
            width = 24,
            height = 22)

        setting_picker_img = tk.PhotoImage(file = ASSETS_PATH / "setting.png")
        setting_picker_button = tk.Button(
            image = setting_picker_img,
            text = '',
            compound = 'center',
            fg = 'white',
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda:cf.configure(),
            relief = 'flat')

        setting_picker_button.place(
            x = 370, y = 75,
            width = 24,
            height = 22)

        path_picker_img = tk.PhotoImage(file = ASSETS_PATH / "path_picker.png")
        path_picker_button = tk.Button(
            image = path_picker_img,
            text = '',
            compound = 'center',
            fg = 'white',
            borderwidth = 0,
            highlightthickness = 0,
            command = self.select_path,
            relief = 'flat')

        path_picker_button.place(
            x = 360, y = 319,
            width = 24,
            height = 22)
        code_picker_img = tk.PhotoImage(file = ASSETS_PATH / "key.png")
        code_picker_button = tk.Button(
            image = code_picker_img,
            text = '',
            compound = 'center',
            fg = 'white',
            borderwidth = 0,
            highlightthickness = 0,
            relief = 'flat')

        code_picker_button.place(
            x = 360, y = 160,
            width = 24,
            height = 22)
        link_picker_img = tk.PhotoImage(file = ASSETS_PATH / "enlace.png")
        link_picker_button = tk.Button(
            image = link_picker_img,
            text = '',
            compound = 'center',
            fg = 'white',
            borderwidth = 0,
            highlightthickness = 0,
            relief = 'flat')

        link_picker_button.place(
            x = 360, y = 240,
            width = 24,
            height = 22)
        canvas.create_text(
            490.0, 153.0, text="No. Autoriación", fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")
        canvas.create_text(
            490.0, 233.5, text="URL", fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")
        canvas.create_text(
            490.0, 314.5, text="Dirección de Carpeta",
            fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
        canvas.create_text(
            646.5, 428.5, text="Generate",
            fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
        bold_font = tkfont.Font(family="Verdana", size=20, weight="bold")
        canvas.create_text(
            600, 70.0, text="Ingresé\nla información.",
            fill="#515486", font=bold_font)
        generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
        generate_btn = tk.Button(
            image=generate_btn_img, borderwidth=0, highlightthickness=0,
            command=lambda:self.btn_clicked(), relief="flat")
        generate_btn.place(x=130, y=390, width=180, height=55)
        m = tk.Menu(self.window, tearoff = 0)
        m.add_command(label ="Pegar", command=lambda:self.paste())
        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()
        self.URL_entry.bind("<Button-3>", do_popup)
        self.token_entry.bind("<Button-3>", do_popup)
        self.window.resizable(False, False)
        self.window.mainloop()
    def btn_clicked(self):
        token = self.token_entry.get()
        URL = self.URL_entry.get()
        output_path = self.path_entry.get()
        output_path = output_path.strip()
        if not token:
            tk.messagebox.showerror(
                title="¡Campo Vacio!", message="Por favor ingrese el código.")
            return
        if not URL:
            tk.messagebox.showerror(
                title="¡Campo Vacio!", message="Por favor ingrese la URL.")
            return
        cs = self.read_ini()
        result = pgd.get_pdf(URL, token, cs[1], cs[0], str(output_path)).get()
        if not result:
            tk.messagebox.showerror(
                title="¡Error!", message="Por favor verifica si los campos estan correctamente.")
            return
        self.token_entry.delete(0, 'end')
        self.URL_entry.delete(0, 'end')
        self.path_entry.delete(0, 'end')
    def select_path(self):
        global output_path
        output_path = tk.filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, output_path)
    def ini(self):
        if not os.path.exists('./config.ini'):
            ini_file = open('config.ini', 'a+')
            ini_file.write('; config.ini\n[DEFAULT]\nCOLOR_CODE = #000000\nSIZE_CODE = 20') 
    def read_ini(self):
        config = cp.ConfigParser()
        config.read('config.ini')
        color_ini = config['DEFAULT']['COLOR_CODE']
        size_ini = config['DEFAULT']['SIZE_CODE']
        color = str(color_ini)
        size = str(size_ini)
        return [color, size]
    def paste(self):
        if str(self.window.focus_get()) == '.!entry2':
            self.URL_entry.insert(0,pyperclip.paste())
        if str(self.window.focus_get()) == '.!entry':
            self.token_entry.insert(0,pyperclip.paste())
def app():
    mi_app = main()
    return 0
if __name__ == '__main__':
    app() 