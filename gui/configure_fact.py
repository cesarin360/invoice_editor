from tkinter import *
import tkinter.messagebox as messagebox
import tkinter.filedialog
import tkinter.font as tkfont
from pathlib import Path
import configparser as cp
from tkinter import colorchooser


ASSETS_PATH = Path(__file__).resolve().parent / "assets"

class configure:
	def __init__(self):
		self.window1 = Toplevel()
		self.window1.grab_set()
		w = 250
		h = 280 
		ws = self.window1.winfo_screenwidth()
		hs = self.window1.winfo_screenheight() 
		x = (ws/2) - (w/2)
		y = (hs/3) - (h/3)
		self.window1.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.window1.iconbitmap(str(ASSETS_PATH / "iconbitmap1.ico"))
		self.window1.title("Configuración")
		self.window1.configure(bg="#FCFCFC")
		canvas = Canvas(
            self.window1, bg="#FCFCFC", height=280, width=250,
            bd=0, highlightthickness=0, relief="ridge")
		canvas.place(x=0, y=0)
		text_box_bg = PhotoImage(file=ASSETS_PATH / "TextBox_Bg1.png")
		color_entry_img = canvas.create_image(193, 180, image=text_box_bg)
		size_entry_img = canvas.create_image(193, 100, image=text_box_bg)

		config = cp.ConfigParser()
		config.read('config.ini')
		color_ini = config['DEFAULT']['COLOR_CODE']
		size_ini = config['DEFAULT']['SIZE_CODE']
		color = StringVar(value = str(color_ini))
		size = StringVar(value = str(size_ini))

		self.color_entry = Entry(self.window1, bd=0, bg="#F6F7F9", highlightthickness=0, textvariable=color)
		self.color_entry.place(x=33, y=175, width=180.0, height=35)
		
		self.size_entry = Entry(self.window1, bd=0, bg="#F6F7F9", highlightthickness=0, text="20", textvariable=size)
		self.size_entry.place(x=33, y=92, width=180.0, height=35)
		self.size_entry.focus()

		color_picker_img = PhotoImage(file = ASSETS_PATH / "color-picker.png")
		color_picker_button = Button(
			self.window1,
            image = color_picker_img,
            text = '',
            compound = 'center',
            fg = 'white',
            borderwidth = 0,
            highlightthickness = 0,
            command = self.color_picker,
            relief = 'flat')

		color_picker_button.place(
            x = 190, y = 170,
            width = 24,
            height = 22)

		bold_font = tkfont.Font(family="Verdana", size=13, weight="bold")
		canvas.create_text(
            32.0, 85.0, text="Tamaño", fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")

		canvas.create_text(
            32.0, 165.0, text="Color (HEX)", fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")

		canvas.create_text(
            123, 33.0, text="Configuración",
            fill="#515486", font=bold_font)

		aceptar_btn_img = PhotoImage(file=ASSETS_PATH / "Aceptar.png")
		aceptar_btn = Button(self.window1, image = aceptar_btn_img,
			borderwidth=0, highlightthickness=0,
            command=lambda:self.btn_clicked(), relief="flat")
		aceptar_btn.place(x=70, y=230, width=110, height=34)
		self.window1.resizable(False, False)
		self.window1.mainloop()
	def btn_clicked(self):
		e_color = self.color_entry.get()
		e_size = self.size_entry.get()
		if e_size.isdigit():
			if len(e_color) == 7:
				print(len(e_color))
				config = cp.ConfigParser()
				config.read('config.ini')
				config.set('DEFAULT', 'COLOR_CODE', e_color)
				config.set('DEFAULT', 'SIZE_CODE', e_size)
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				self.window1.destroy()
			else:
				messagebox.showerror(title='Error', message='Código de color hexadecimal incorrecto.')
		else:
			messagebox.showerror(title='Error', message='El campo Tamaño solo acepta números.')
	def color_picker(self):
		try:
			color_code = colorchooser.askcolor()
			self.color_entry.delete(0, END)
			self.color_entry.insert(0, color_code[1])
			self.window1.after(1, lambda: self.window1.focus_force())
		except:
			pass
		
