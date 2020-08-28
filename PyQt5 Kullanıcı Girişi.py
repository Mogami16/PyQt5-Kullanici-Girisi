import sys
from PyQt5 import QtWidgets, QtGui
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import time

class Pencere(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()

		self.baglanti_olustur()
		self.init_ui()

	def init_ui(self):
		self.setWindowTitle("133 - Kullanıcı Girişi Projesi Arayüzü Tasarlama")
		self.setGeometry(100,100,480,400)


		self.eposta = QtWidgets.QLineEdit()
		self.parola = QtWidgets.QLineEdit()
		self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
		self.parola_durum = False
		self.aktivasyon_durum = False
		self.parola_goster = QtWidgets.QPushButton(self)

		self.aktivasyon_alani = QtWidgets.QLineEdit()
		self.aktivasyon_buton = QtWidgets.QPushButton(self)
		self.aktivasyon_buton.setText("Onayla")
		self.aktivasyon_buton.setGeometry(1000000,10000000, 1, 1)


		self.yazi1 = QtWidgets.QLabel("E-Posta")
		self.yazi2 = QtWidgets.QLabel("Parola")
		self.yazi3 = QtWidgets.QLabel(self)
		self.yazi4 = QtWidgets.QLabel("Aktivasyon Kodu")
		
		self.giris = QtWidgets.QPushButton(self)
		self.kayit = QtWidgets.QPushButton(self)

		self.v_box = QtWidgets.QVBoxLayout()

		self.v_box.addWidget(self.yazi1)
		self.v_box.addWidget(self.eposta)
		
		self.v_box.addWidget(self.yazi2)
		self.v_box.addWidget(self.parola)
		self.v_box.addStretch()

		h_box = QtWidgets.QHBoxLayout()

		h_box.addLayout(self.v_box)
		h_box.addStretch()

		self.kayit.setText("Kayıt Ol")
		self.kayit.setGeometry(10,130,100,50)

		self.giris.setText("Giriş Yap")
		self.giris.setGeometry(130,130,100,50)

		self.parola_goster.setText("Parolayı Göster / Sakla")
		self.parola_goster.setGeometry(250,75,120,20)


		self.giris.clicked.connect(self.giris_yap)
		self.kayit.clicked.connect(self.mail_gonder)
		self.parola_goster.clicked.connect(self.goster)




		self.setLayout(h_box)
		self.show()

	def giris_yap(self):
		ad = self.eposta.text()
		par = self.parola.text()

		self.cur.execute("SELECT * FROM Üyeler WHERE EPosta = ? AND Parola = ?",(ad,par))
		data = self.cur.fetchall()

		if len(data) == 0:
			self.yazi3.setText("Hatalı Giriş !")
			self.yazi3.setFont(QtGui.QFont("Sanserif", 12))
			self.yazi3.move(70,95)


		else:
			self.yazi3.setText("Hoş Geldiniz...")
			self.yazi3.move(70,95)

	def baglanti_olustur(self):
		self.conn = sqlite3.connect("database.db")
		self.cur = self.conn.cursor()

		self.cur.execute("CREATE TABLE IF NOT EXISTS Üyeler (EPosta TEXT, Parola TEXT)")
		self.conn.commit()

	def kayit_ol(self):
		if int(self.aktivasyon_alani.text()) == self.aktivasyon:
			self.yazi3.setText("Aktivasyon Doğru")
			time.sleep(2)

			eposta = self.eposta.text()
			parola = self.parola.text()

			self.cur.execute("INSERT INTO Üyeler VALUES (?,?)", (eposta, parola))
			self.conn.commit()

			self.yazi3.setText("İşlem Başarılı.")
			self.yazi3.setFont(QtGui.QFont("Sanserif", 12))
			self.yazi3.move(70,95)
			time.sleep(2)

		else:
			self.yazi3.setText("Hatalı Aktivasyon")

	def goster(self):
		if self.parola_durum == True:
			self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
			self.parola_durum = False
		else:
			self.parola.setEchoMode(QtWidgets.QLineEdit.Normal)
			self.parola_durum = True

	def mail_gonder(self):
		self.aktivasyon_durum = True
		eposta = self.eposta.text()
		parola = self.parola.text()
		self.aktivasyon = random.randint(1000,9999)

		mesaj = MIMEMultipart()

		mesaj["From"] = "eposta"
		mesaj["To"] = eposta
		mesaj["Subject"] = "Aktivasyon Kodu"

		yazi = f"""
	Aktivasyon Kodunuz:

	{self.aktivasyon}

		"""

		govde = MIMEText(yazi, "plain")
		mesaj.attach(govde)

		try:
			mail = smtplib.SMTP("smtp.gmail.com",587)
			
			mail.ehlo()
			mail.starttls()

			mail.login("eposta","Şifre")

			mail.sendmail(mesaj["From"], mesaj["To"], mesaj.as_string())

			self.yazi3.setText("Aktivasyon Gönderildi.")
			self.yazi3.move(70,95)
			mail.close()

			self.v_box.addWidget(self.yazi4)
			self.v_box.addWidget(self.aktivasyon_alani)

			self.aktivasyon_durum = True

			self.aktivasyon_buton.setText("Onayla")
			self.aktivasyon_buton.setGeometry(260,367, 150, 22)
			self.aktivasyon_buton.clicked.connect(self.kayit_ol)

		except:
			self.yazi3.setText("Bir Hata Oluştu !")
			self.yazi3.move(70,95)




app = QtWidgets.QApplication(sys.argv)

Pencere = Pencere()



sys.exit(app.exec())
