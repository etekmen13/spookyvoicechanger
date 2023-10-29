import sys #for running and exiting the app
import math
# For GUI
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtSvgWidgets import *
import ctypes

#For Interpreting WAV Data and Plotting
from scipy.io.wavfile import read
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import sounddevice as sd

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.setWindowTitle("Spooky Voice Changer")
        width = 400
        height = 500
        self.setGeometry(screensize[0]//2 - width//2,screensize[1]//2 - height//2, width, height)
        self.setFixedSize(width, height)
        self.playIntro(width, height)


    def playIntro(self, width, height):
        labelWidth = 400
        labelHeight = 200
        child = QLabel(self)
        child.setText("HackNC2023")
        child.setFont(QFont('Impact', 50))
        child.setAlignment(Qt.AlignmentFlag.AlignCenter)
        child.resize(labelWidth, labelHeight)

        title = QLabel(self)
        title.setText("Spooky \nVoice Changer")
        title.setFont(QFont('Impact', 50))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setGeometry(-labelWidth,-labelHeight,labelWidth, labelHeight)
        
        author = QLabel(self)
        author.setText("By \nEmre Tekmen")
        author.setFont(QFont('Impact', 50))
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author.setGeometry(-labelWidth,-labelHeight,labelWidth, labelHeight)

        self.anim = QPropertyAnimation(child, b"pos")
        self.anim.setStartValue(QPoint(width//2 - labelWidth//2,height + labelHeight))
        self.anim.setEndValue(QPoint(width//2 - labelWidth//2, height//2 - labelHeight//2))
        self.anim.setDuration(1500)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.anim_2 = QPropertyAnimation(child, b"pos")
        self.anim_2.setStartValue(QPoint(width//2 - labelWidth//2,height//2 - labelHeight//2))
        self.anim_2.setEndValue(QPoint(width//2 - labelWidth//2, -labelHeight))
        self.anim_2.setDuration(1500)
        self.anim_2.setEasingCurve(QEasingCurve.Type.InOutCubic)


        self.anim7 = QPropertyAnimation(title, b"pos")
        self.anim7.setStartValue(QPoint(width//2 - labelWidth//2,height + labelHeight))
        self.anim7.setEndValue(QPoint(width//2 - labelWidth//2, height//2 - labelHeight//2))
        self.anim7.setDuration(1500)
        self.anim7.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.anim8 = QPropertyAnimation(title, b"pos")
        self.anim8.setStartValue(QPoint(width//2 - labelWidth//2,height//2 - labelHeight//2))
        self.anim8.setEndValue(QPoint(width//2 - labelWidth//2, -labelHeight))
        self.anim8.setDuration(1500)
        self.anim8.setEasingCurve(QEasingCurve.Type.InOutCubic)


        self.anim9 = QPropertyAnimation(author, b"pos")
        self.anim9.setStartValue(QPoint(width//2 - labelWidth//2,height + labelHeight))
        self.anim9.setEndValue(QPoint(width//2 - labelWidth//2, height//2 - labelHeight//2))
        self.anim9.setDuration(1500)
        self.anim9.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.anim10 = QPropertyAnimation(author, b"pos")
        self.anim10.setStartValue(QPoint(width//2 - labelWidth//2,height//2 - labelHeight//2))
        self.anim10.setEndValue(QPoint(width//2 - labelWidth//2, -labelHeight))
        self.anim10.setDuration(1500)
        self.anim10.setEasingCurve(QEasingCurve.Type.InOutCubic)


        self.demonFilter = DemonFilter(self, 10)
        self.demonFilter.clicked.connect(self.onDemonClicked)
        self.anim_3 = QPropertyAnimation(self.demonFilter, b"pos")
        self.anim_3.setStartValue(QPoint(10,height + self.demonFilter.height()))
        self.anim_3.setEndValue(QPoint(10, 10))
        self.anim_3.setDuration(1000)
        self.anim_3.setEasingCurve(QEasingCurve.Type.InOutCubic)
        

        self.chipmunkFilter = ChipmunkFilter(self, width-10)
        self.chipmunkFilter.clicked.connect(self.onChipmunkClicked)
        self.anim_4 = QPropertyAnimation(self.chipmunkFilter, b"pos")
        self.anim_4.setStartValue(QPoint(width-self.chipmunkFilter.width()-10,height + self.chipmunkFilter.height()))
        self.anim_4.setEndValue(QPoint(width-self.chipmunkFilter.width()-10, 10))
        self.anim_4.setDuration(1000)
        self.anim_4.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.audioWindow = DragNDrop()
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.audioWindow)
        self.container = QWidget(self)
        self.container.setLayout(self.mainLayout)
        self.container.setGeometry(0, height+self.container.height(),400,200)
        self.anim_5 = QPropertyAnimation(self.container, b"pos")
        self.anim_5.setStartValue(QPoint(width//2-self.container.width()//2,height + self.container.height()))
        self.anim_5.setEndValue(QPoint(width//2 - self.container.width()//2, self.container.height()+10))
        self.anim_5.setDuration(1000)
        self.anim_5.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.anim_group = QSequentialAnimationGroup()
        self.anim_group.addAnimation(self.anim)
        self.anim_group.addAnimation(self.anim_2)
        self.anim_group.addAnimation(self.anim7)
        self.anim_group.addAnimation(self.anim8)
        self.anim_group.addAnimation(self.anim9)
        self.anim_group.addAnimation(self.anim10)
        self.anim_group.addAnimation(self.anim_3)
        self.anim_group.addAnimation(self.anim_4)
        self.anim_group.addAnimation(self.anim_5)
        self.anim_group.start()

    def onDemonClicked(self):
        if self.audioWindow.canvasContainer == None:
            return
        if self.chipmunkFilter.isChecked():
            return
        if self.demonFilter.isChecked():
            print("on")
            self.demonFilter.setStyleSheet("background-color: rgb(250, 202, 142); margin:5px; border:1px solid black radius 2 pt; ")
            self.pitchDown()
        else:
            print("off")
            self.demonFilter.setStyleSheet("background-color: rgb(232, 177, 109); margin:5px; border:1px solid black radius 2 pt; ")
            self.pitchNeutral()
    
    def onChipmunkClicked(self):
        if self.audioWindow.canvasContainer == None:
            return
        if self.demonFilter.isChecked():
            return
        if self.chipmunkFilter.isChecked():
            print("on")
            self.chipmunkFilter.setStyleSheet("background-color: rgb(250, 202, 142); margin:5px; border:1px solid black radius 2 pt; ")
            self.pitchUp()
        else:
            print("off")
            self.chipmunkFilter.setStyleSheet("background-color: rgb(232, 177, 109); margin:5px; border:1px solid black radius 2 pt; ")
            self.pitchNeutral()
    def pitchDown(self):
        if self.audioWindow.canvasContainer == None:
            return
        self.audioWindow.canvasContainer.canvas.changePitch(-1200)
    def pitchNeutral(self):
        if self.audioWindow.canvasContainer == None:
            return
        self.audioWindow.canvasContainer.canvas.changePitch(0)
   
    def pitchUp(self):
        if self.audioWindow.canvasContainer == None:
            return
        self.audioWindow.canvasContainer.canvas.changePitch(1200)
        
            
class DemonFilter(QPushButton):
    def __init__(self, parent, x):
        super().__init__(parent=parent)
        self.setCheckable(True)
        width = 175
        height = 167
        label = QLabel(self)
        p = QPixmap('devil.png')
        pixmap = p.scaledToWidth(width)
        pixmap = p.scaledToHeight(height)
        label.setPixmap(pixmap)
        self.setGeometry(x,500 + height, width, height)
        self.setStyleSheet("background-color: rgb(232, 177, 109); margin:5px; border:1px solid black radius 2 pt; ")
    
class ChipmunkFilter(QPushButton):
    def __init__(self, parent, x):
        super().__init__(parent=parent)
        self.setCheckable(True)
        width = 175
        height = 167
        label = QLabel(self)
        p = QPixmap('chipmunk.png')
        pixmap = p.scaledToWidth(width)
        pixmap = p.scaledToHeight(height)
        label.setPixmap(pixmap)
        self.setGeometry(x,500 + height, width, height)
        self.setStyleSheet("background-color: rgb(232, 177, 109); margin:5px; border:1px solid black radius 2 pt; ")

class DragNDrop(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.canvasContainer = None
        self.lbl = QLabel("Drop Audio File Here (WAV ONLY)")
        self.setMaximumHeight(125)
        self.lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.l = QVBoxLayout()
        self.l.addWidget(self.lbl)
        self.setLayout(self.l)
        #Invisible Play Button
        self.playToggle= QPushButton("Play")
        self.l.addWidget(self.playToggle)
        self.playToggle.pressed.connect(self.play_audio)
        self.playToggle.hide()


    def dragEnterEvent(self, a0) -> None:
        if a0.mimeData().hasImage:
            a0.accept()
        else:
            a0.ignore()

    def dropEvent(self, a0) -> None:
        if a0.mimeData().hasImage:
            a0.setDropAction(Qt.DropAction.CopyAction)
            filePath = a0.mimeData().urls()[0].toLocalFile()
            if self.canvasContainer == None:
                self.setCanvas(filePath)
            else:
                self.updateCanvas(filePath)
            print(filePath)

    def dragMoveEvent(self, a0) -> None:
        if a0.mimeData().hasImage:
            a0.accept()
        else:
            a0.ignore()
    
    def setCanvas(self, filePath):
        self.canvasContainer = CanvasWidget(filePath)
        self.l.replaceWidget(self.lbl, self.canvasContainer)
        self.lbl.setParent(None)
        self.playToggle.show()
    
    def updateCanvas(self, filePath):
        self.canvasContainer.parent = None
        self.l.removeWidget(self.canvasContainer)

    def play_audio(self):
        if self.playToggle.text() == "Play":
            sd.play(self.canvasContainer.canvas.data, self.canvasContainer.canvas.Fs)  
            self.playToggle.setText("Stop") 
        elif self.playToggle.text() == "Stop":
            sd.stop()
            self.playToggle.setText("Play")


class CanvasWidget(QWidget):
    def __init__(self, filePath):
        super().__init__()
        self.canvas = Canvas(parent=self, width=5, height=4, dpi=100, wav=filePath)
        l = QVBoxLayout()
        l.addWidget(self.canvas)
        l.addSpacerItem(QSpacerItem(0, 20))
        self.setLayout(l)
        
class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, wav=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        self.fig.set_facecolor("none")
        self.axes = self.fig.add_subplot(111)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        super(Canvas, self).__init__(self.fig)
        self.fig.tight_layout()
        print("canvas created")
        
        if wav == None:
            return
    #EXTRACT DATA AND ORGANIZE

        self.Fs, self.data = read(wav) #sample rate and wave data
        #if stereo only use the left channel
        if len(self.data.shape) == 2:
            self.data = self.data[:,0]         
        print(self.data.size)
        Ts = 1/self.Fs
        N = self.data.size
        t = np.arange(N)*Ts 
        print(f"t = ", t)
        self.data = self.data[:]
        self.ogData = self.data[:]
        self.axes.set_ylim(ymin=-0.6, ymax=0.6)
        self.normalizedData = self.data/(2*np.max(abs(self.data))) # normalize between -0.5 and 0.5
        self.axes.plot(t,self.normalizedData, color=(0/255, 0/255, 0/255))
        self.axes.set_facecolor(color='None')
        self.axes.set_frame_on(False)
        self.draw()

    def scaleFrequency(self, pitch, window):
        fft = np.fft.rfft(window)
        scalar = 2**(pitch/1200)
        shiftedFFT = np.zeros(fft.size)
        for i in range (len(fft)):
            shift_index = int(i * scalar)
            if shift_index < len(shiftedFFT):
                shiftedFFT[shift_index] = fft[i]
        shiftedFFT = np.fft.irfft(shiftedFFT)
        return shiftedFFT
        
    def changePitch(self, pitch):
        windowLen = 5000
        hopLen = 2000
        signal = self.ogData
        signal_len = len(signal)

        if signal_len < signal_len - hopLen + windowLen:
            remainder = signal_len - hopLen + windowLen - signal_len
            print(remainder)
            signal = np.concatenate((signal,np.zeros(remainder)))
        signal_len = len(signal)
        windows = []
        shiftedWindows = []
        numWindows = (signal_len-windowLen)//hopLen+1

        for i in range(numWindows):
            start = i * hopLen
            end = start + windowLen
            window = signal[start:end]
            windows.append(window)

        hanning = np.hanning(windowLen)
        for window in windows:
            shiftedWindow = self.scaleFrequency(pitch, window)
            shiftedWindow = shiftedWindow * hanning
            shiftedWindows.append(shiftedWindow)
        
        output = np.zeros(signal_len)
        for i in range(numWindows):
            start = i * hopLen
            end = start + windowLen
            output[start:end] += shiftedWindows[i]
        #output = output/np.max(np.abs(output))
        output = output.astype('int16')
        self.data = output


app = QApplication(sys.argv)
app.setWindowIcon(QIcon('download.jfif'))
app.setStyle("fusion")
app.setStyleSheet(open('appStyle.css').read())
window = MainWindow()
window.show()
sys.exit(app.exec())