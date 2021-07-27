import sys
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
import time
import pytube
import re
import os

class downloader(QWidget):
    def __init__(self):
        super(downloader,self).__init__()
        loadUi('youtube.ui',self)
        self.tur = ""
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.mp3.setIcon(QIcon('img/cil-headphones.ico'))
        self.mp4.setIcon(QIcon('img/cil-airplay.ico'))
        self.indir.setIcon(QIcon('img/cil-download.ico'))
        self.setWindowTitle('Youtube Downloader')

        self.indir.clicked.connect(self.down)
        self.makemini.clicked.connect(lambda: self.showMinimized())
        self.makeclose.clicked.connect(lambda: self.close())
        self.setWindowIcon(QIcon('img/logo.ico'))
        
        
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:  
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        
        
        self.titlebar.mouseMoveEvent = moveWindow
        
    def mousePressEvent(self,event):
        self.clickPosition = event.globalPos()
        
    
    
    def geturl(self):
        try:
            url = self.url.text()
            playlist = pytube.Playlist(url)
            return playlist
        except:
            self.playlistbilgi.setText("Geçerli youtube URL'si giriniz url alamadık")

        
    @pyqtSlot()
    def down(self):
        print(self.mp3.isChecked())
        print(self.mp4.isChecked())
        
        try:
            print("buraya geldim... 1")

            playlist = self.geturl()
            print(playlist)
            print("buraya geldim... 2")
            if self.mp3.isChecked():
                print("buraya geldim... 3")
                for num,url in enumerate(playlist,1):
                    video = pytube.YouTube(url,on_progress_callback=self.progress_funcmp3)
                    self.mp3streams = video.streams.get_audio_only(subtype="webm")
                    self.mp3streams.download()
                    self.playlistbilgi.setText(f"{num}. dosya bitti.")
                dosyalar = os.listdir()
                for i in dosyalar:
                    if i.endswith(".webm"):
                        base, _ = os.path.splitext(i)
                        os.rename(i,base+".mp3")
                self.playlistbilgi.setText("İndirme İşlemi Tamamlandı")

            elif self.mp4.isChecked():
                print("buraya geldim... 4")
                for num,url in enumerate(playlist,1):
                    print("buraya geldim... 4.5")
                    self.video = pytube.YouTube(url,on_progress_callback=self.progress_funcmp4)
                    print("buraya geldim... 5")
                    print(self.video.streams)
                    print("buraya geldim 5.5")
                    self.mp4streams = self.video.streams.get_highest_resolution()
                    print("buraya geldim... 6")
                    self.mp4streams.download()
                    self.playlistbilgi.setText(f"{num}. dosya bitti.")
                self.playlistbilgi.setText("İndirme İşlemi Tamamlandı")
            else:
                self.playlistbilgi.setText("Lütfen indirme formatı seçiniz!!!")
        except:
            self.playlistbilgi.setText("Geçerli Playlist URL'si giriniz son kod")
            print("buraya geldim... 7")
            


    
    def progress_funcmp3(self, stream, chunk,bytes_remaining):
        size = self.mp3streams.filesize
        dosyaboyutu = size*10**-6
        self.videoboyutu.setText(f"{dosyaboyutu:.2f} mb")
        kalanboyut = bytes_remaining*10**-6
        self.kalanboyut.setText(f"{kalanboyut:.2f} mb")
        progress = (float(abs(bytes_remaining-size)/size))*float(100)
        self.pbar.setValue(progress)

    def progress_funcmp4(self, stream, chunk, bytes_remaining):
        size = self.mp4streams.filesize
        dosyaboyutu = size*10**-6
        self.videoboyutu.setText(f"{dosyaboyutu:.2f} mb")
        kalanboyut = bytes_remaining*10**-6
        self.kalanboyut.setText(f"{kalanboyut:.2f} mb")
        progress = (float(abs(bytes_remaining-size)/size))*float(100)
        self.pbar.setValue(progress)

    
        


app = QApplication(sys.argv)
pencere = downloader()
pencere.show()
sys.exit(app.exec_())
