import sqlite3
cn = sqlite3.connect("FACTURAS")
miCursor=cn.cursor()
miCursor.execute('''
	CREATE TABLE Facturas(
	ID_DTE INTEGER PRIMARY KEY AUTOINCREMENT,
	NIT_DTE TEXT,
	SERIE_DTE TEXT,
	FECHA_EDIT_DTE DATE,
	HORA_EDIT_DTE TIME,
	NOMBRE_ARCHIVO TEXT UNIQUE
)
''')
cn.commit()
cn.close()