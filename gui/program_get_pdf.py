import requests
import urllib3
import pdfkit as pdf
import os
import sqlite3
import re
from get_tag import MyHTMLParser as My
from datetime import datetime, date
from tkinter import messagebox 
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from pathlib import Path

class get_pdf:
	def __init__(self, url, code='', font_size_code='', font_color_code='', path=''):
		urllib3.disable_warnings()
		self.url = url
		self.code = code
		self.font_size_code = font_size_code if font_size_code else '20'
		self.font_color_code = font_color_code if font_color_code else 'black'
		self.path = path
	def get(self):
		try:
			page = requests.get(self.url, verify=False)
			soup = BeautifulSoup(page.content.decode("utf-8"), 'html.parser')
			h1 = soup.new_tag('h1')
			h1.string = 'NO. AUTORIZACIÓN: '+self.code if self.code else ''
			style = soup.new_tag('style')
			style.string = 'h1{ font-family: Arial; font-weight: normal; font-size: %spx; color: %s; }' % (self.font_size_code, self.font_color_code)
			hr = soup.new_tag('hr')
			meta = soup.new_tag('meta', charset="utf-8")
			soup.div.append(style)
			soup.div.append(h1)
			soup.div.append(hr)
			soup.head.append(meta)
			soup.style.append('.page { display: block; margin-left: auto; margin-right: auto; }')
			nameFile = 'htmlFile'
			address = nameFile+'.html'
			html = self.replace_tildes(str(soup.prettify()))
			f = open(address,'w')
			f.write(html)
			f.close()
			o = urlparse(self.url)
			query = parse_qs(o.query)
			var = query['DATA'][0].split('|', 2)
			var1 = var[1]
			var2 = var1.split('-')[0]
			var3 = My.get(str(soup.div))
			if not self.path:
				options = {
					'page-size': 'Letter',
				    'margin-top': '0.75in',
				    'margin-right': '0.75in',
				    'margin-bottom': '0.75in',
				    'margin-left': '0.75in',
				    'encoding': "utf-8",
				    'custom-header': [
				        ('Accept-Encoding', 'gzip')
				    ],
				}
				if not self.path:
					self.create_db(NOMBRE = var1, SERIE = var2, NIT = var3)
					print('save')
				pdf.from_file(address, 'pdf/'+var1+'.pdf', options=options)
				path = Path(__file__).resolve().parent / "pdf"
				os.system('"'+str(path) + "/"+var1+'.pdf'+'"')
			else:
				pdf.from_file(address, self.path+"/"+var1+'.pdf')
				path = self.path + "/"+var1+'.pdf'
				os.system('"' + path + '"')
			return True
		except:
			print("error")
			return False
	def create_db(self, **kwargs):
		now = datetime.now()
		hora_actual = now.strftime("%H:%M:%S")
		dia_actual = date.today()
		cn = sqlite3.connect("./db/FACTURAS")
		miCursor=cn.cursor()
		factura = [
			(kwargs['NIT'], kwargs['SERIE'], str(dia_actual), str(hora_actual), kwargs['NOMBRE']),
		]
		miCursor.executemany("INSERT INTO FACTURAS VALUES (NULL,?,?,?,?,?)", factura)
		cn.commit()
		cn.close()
	def replace_tildes(self, strg=''):
		str_1 = strg
		tildes_min = {
					  'normal':['á','é','í','ó','ú'],
					  'code': ['&aacute;','&eacute;','&iacute;','&oacute;','&uacute;']
					 }

		tildes_may = {
					  'normal':['Á','É','Í','Ó','Ú'],
					  'code': ['&Aacute;','&Eacute;','&Iacute;','&Oacute;','&Uacute;']
					 }
		for k, i in enumerate(tildes_min['normal']):
			str_1 = re.sub(i, tildes_min['code'][k], str_1)
		for k, i in enumerate(tildes_may['normal']):
			str_1 = re.sub(i, tildes_may['code'][k], str_1)
		str_1 = re.sub('ñ', '&ntilde;', str_1)
		str_1 = re.sub('Ñ', '&Ntilde;', str_1)
		return str_1