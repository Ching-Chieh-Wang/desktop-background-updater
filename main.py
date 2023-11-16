import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QToolBar,QMessageBox, QMainWindow,QSystemTrayIcon,QAction,QMenu,qApp,QMessageBox,QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication ,QRect,pyqtSignal,QTimer
from PyQt5 import QtCore
import ctypes
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import random as rd
import os
import json

class WallpaperUpdateModel:
    def __init__(self):
        self.timer=QTimer()
        self.timer.timeout.connect(self.nextImg)
        self.imgs=[]
        self.nowImgIdx=-1
        try:
            with open('params.json','r') as f:
                paramsParser=json.load(f)
                self.hoursInterval=paramsParser['hoursInterval']
                self.minutesInterval=paramsParser['minutesInterval']
        except:
            self.adjustIntervalOK(1,0)
    def adjustIntervalOK(self,hoursInterval,minutesInterval):
        self.terminate()
        self.hoursInterval=hoursInterval
        self.minutesInterval=minutesInterval
        params={"hoursInterval":hoursInterval,"minutesInterval":minutesInterval}
        with open('params.json','w') as f:

            json.dump(params,f)
        self.startCountDown()
    def nextImg(self):
        if self.nowImgIdx==len(self.imgs)-1:
            try:
               url = "https://github.com/ameizi/bing-wallpaper/blob/main/bing-wallpaper.md"  
               response = requests.get(url)
               soup = BeautifulSoup(response.text, 'html.parser')
               download_links = soup.find_all('a')
               image=rd.choice(download_links)
               self.imgs.append([image['href'][2:-2],image.text])
            except:
                return False
        self.nowImgIdx+=1 
        success= self.setImg()
        if not success:
            self.nowImgIdx-=1
            return False
        return True
    def previousImg(self):
        self.nowImgIdx-=1
        success =self.setImg()
        if not success :
            self.nowImgId+=1
            return False
        return True
    def setImg(self):
        path = os.getcwd()+'/wallpaper.jpg'
        self.terminate()
        response = requests.get(self.imgs[self.nowImgIdx][0], cookies={'over18':'1'})
        try:
            with open(path, 'wb') as file:
                file.write(response.content)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
            self.startCountDown()
            return True
        except:
            return False
    def imgInfo(self):
        import webbrowser 
        try:
            for infoUrl in search(self.imgs[self.nowImgIdx][1]+" site:peapix.com", stop=1,pause=0):
                pass
            webbrowser.get('windows-default').open_new(infoUrl)
        except:
            return False
        return True
    def startCountDown(self):
        self.timer.start(self.hoursInterval*3600000+self.minutesInterval*60000)
    def terminate(self):
        self.timer.stop()
        
            
            
            
            
class WallpaperUpdateView(QMainWindow):
    def __init__(self):
        super(WallpaperUpdateView,self).__init__()
        self.setWindowTitle("Desktop wallpaper updater")
        self.setWindowIcon(QIcon("desktop_wallpaper_update.ico"))
        self.resize(1031,154)
        self.splitter_2 = QtWidgets.QSplitter(self)
        self.splitter_2.setGeometry(QtCore.QRect(200, 30, 581, 31))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter_2.hide()
        self.hoursLbl = QtWidgets.QLabel(self.splitter_2)
        self.hoursLbl.setObjectName("hoursLbl")
        self.hoursSpin = QtWidgets.QSpinBox(self.splitter_2)
        self.hoursSpin.setMaximum(24)
        self.hoursSpin.setObjectName("hoursSpin")
        self.minutesLbl = QtWidgets.QLabel(self.splitter_2)
        self.minutesLbl.setObjectName("minutesLbl")
        self.minutesSpin = QtWidgets.QSpinBox(self.splitter_2)
        self.minutesSpin.setMaximum(60)
        self.minutesSpin.setObjectName("minutesSpin")
        self.updateIntervalOKBtn = QtWidgets.QPushButton(self.splitter_2)
        self.updateIntervalOKBtn.setObjectName("updateIntervalOKBtn")
        self.updateIntervalCancelBtn = QtWidgets.QPushButton(self.splitter_2)
        self.updateIntervalCancelBtn.setObjectName("updateIntervalCancelBtn")
        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setGeometry(QtCore.QRect(10, 70, 971, 61))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.exitBtn = QtWidgets.QPushButton(self.splitter)
        self.exitBtn.setObjectName("exitBtn")
        self.adjustIntervalBtn = QtWidgets.QPushButton(self.splitter)
        self.adjustIntervalBtn.setObjectName("adjustIntervalBtn")
        self.imgInfoBtn = QtWidgets.QPushButton(self.splitter)
        self.imgInfoBtn.setObjectName("imgInfoBtn")
        self.previousImgBtn = QtWidgets.QPushButton(self.splitter)
        self.previousImgBtn.setObjectName("previousImgBtn")
        self.previousImgBtn.setDisabled(True)
        self.nextImgBtn = QtWidgets.QPushButton(self.splitter)
        self.nextImgBtn.setObjectName("nextImgBtn")
        self.hoursLbl.setText( "Hours")
        self.minutesLbl.setText( "Minutes")
        self.minutesSpin.valueChanged.connect(self.adjustingInterval)
        self.updateIntervalOKBtn.setText( "OK")
        self.updateIntervalCancelBtn.setText( "Cancel")
        self.exitBtn.setText( "Exit")
        self.adjustIntervalBtn.setText( "Adjust Interval")
        self.imgInfoBtn.setText( "Image Info")
        self.imgInfoBtn.setDisabled(True)
        self.previousImgBtn.setText( "Previous Image")
        self.nextImgBtn.setText( "Next Image")
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon('desktop_wallpaper_update.ico'))
        self.showGUIAct = QAction('Settings')
        self.exitAct =  QAction('Exit')
        trayMenu = QMenu()
        trayMenu.addAction(self.showGUIAct)
        trayMenu.addAction(self.exitAct)
        self.tray.setContextMenu(trayMenu)
        self.tray.show()
    def terminate(self):
        self.hide()
        self.tray.setVisible(False)
    def adjustingInterval(self):
        if self.hoursSpin.value()==0:
            if self.minutesSpin.value()==0:
                self.minutesSpin.setValue(1)
            self.minutesSpin.setMinimum(1)
        else:
            self.minutesSpin.setMinimum(0)
        if self.minutesSpin.value()==0:
            if self.hoursSpin.value()==0:
                self.hoursSpin.setValue(1)
            self.hoursSpin.setMinimum(1)
        else:
            self.hoursSpin.setMinimum(0)
    def adjustInterval(self,initalHoursInterval,initalMinutesInterval):
        self.splitter_2.show()
        self.hoursSpin.setValue(initalHoursInterval)
        self.minutesSpin.setValue(initalMinutesInterval)
    def adjustIntervalOK(self):
        self.splitter_2.hide()
    def adjustIntervalCancel(self):
        self.splitter_2.hide()
    def loadImgError(self):
        if self.isVisible():
            QMessageBox.information(self,'Load image error','Check Internet connection')
        
        


        

class WallpaperUpdateController:
    def __init__(self):
        app = QApplication(sys.argv)
        QApplication.setQuitOnLastWindowClosed(False)
        self.model=WallpaperUpdateModel()
        self.model.timer.timeout.connect(self.nextImg)
        self.view=WallpaperUpdateView()
        self.view.nextImgBtn.clicked.connect(self.nextImg)
        self.view.previousImgBtn.clicked.connect(self.previousImg)
        self.view.showGUIAct.triggered.connect(self.view.show)
        self.view.exitAct.triggered.connect(self.terminate)
        self.view.exitBtn.clicked.connect(self.terminate)
        self.view.adjustIntervalBtn.clicked.connect(self.adjustInterval)
        self.view.updateIntervalOKBtn.clicked.connect(self.adjustIntervalOK)
        self.view.updateIntervalCancelBtn.clicked.connect(self.adjustIntervalCancel)
        self.view.imgInfoBtn.clicked.connect(self.imgInfo)
        self.nextImg()
        return sys.exit(app.exec_())    
    def imgInfo(self):
        success=self.model.imgInfo()
        if not success:
            self.view.loadImgError()
    def previousImg(self):
        success=self.model.previousImg()
        if not success:
            self.view.loadImgError()
        else:
            if self.model.nowImgId<=0:
                self.view.previousImgBtn.setDisabled(True)
        
    def nextImg(self):
        success=self.model.nextImg()
        if success:
            self.view.imgInfoBtn.setDisabled(False)
            if len(self.model.imgs)>1:
                self.view.previousImgBtn.setDisabled(False)
        else:
            self.view.loadImgError()


    def terminate(self):
        self.view.terminate()
        self.model.terminate()
        QCoreApplication.instance().quit()
    def adjustInterval(self):
        self.view.adjustInterval(self.model.hoursInterval,self.model.minutesInterval)
    def adjustIntervalOK(self):
        self.view.adjustIntervalOK()
        self.model.adjustIntervalOK(self.view.hoursSpin.value(),self.view.minutesSpin.value())
    def adjustIntervalCancel(self):
        self.view.adjustIntervalCancel()

        
        

if __name__ == '__main__':
    wallpaperUpdater=WallpaperUpdateController()
