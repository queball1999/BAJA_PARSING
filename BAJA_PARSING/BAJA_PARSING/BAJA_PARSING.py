#
#   Program: BAJA Parsing Program
#
#   Software: Microsoft Visual Studios 16.8.3
#
#   GUI: PyQt5
#
#   Date: 26th of March 2022
#
#   Author: Quynn Bell
#

# importing operating system libraries
import os
#importing Sysytem-specefic parameters and functions
import sys
# importing regular expressions library
import re
# importing time libraries for python
import datetime
import time
# import shutil library for copying files
import shutil
# importing PyQt5 GUI
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

ua_logo = os.path.join(__location__ + '/photos/ua_logo.png')
minimize = os.path.join(__location__ + '/photos/minimize_button.png')
maximize = os.path.join(__location__ + '/photos/maximize_button.png')
close_button = os.path.join(__location__ + '/photos/close_button.png')

css_dark = """
QMainWindow { background-color : #202020; color : white; }
QWidget { background-color : #202020; border : None; }
QMenuBar { background-color : #383838; color : white; font-family : Arial, sans-serif; font-size : 12; }
QMenuBar::item { background-color : #383838; color : white; font-family : Arial, sans-serif; font-size : 12; }
QMenuBar::item:selected { background-color : #202020; color : white; }
QMenuBar::item:pressed { background-color : #202020; color : white; }
QMenu {  background-color : #383838; color : white; font-family : Arial, sans-serif; font-size : 12; }
QMenu::item { background-color : #383838; color : white; }
QMenu::item:selected { background-color : #2d2d30; color : white; }
QMenu::item:pressed { background-color : #2d2d30; color : white; }
QToolBar { background-color : #383838; color : white; }
QToolButton { background-color : #383838; color : white; font-family : Arial, sans-serif; font-size : 12; font-weight : bold; }
QToolButton::hover { background-color : #2d2d30; color : white; }
QToolButton::pressed { background-color : #202020; color : white; }
QLabel { background-color : #202020; color : white; font-family : Arial, sans-serif; font-weight : bold; font-size : 18; }
QLineEdit { background-color : #2d2d30; color : white; border-color : white; border-width : 1px; border-style : solid; padding : 4px 4px 4px 4px; font-family : Arial, sans-serif; font-weight : bold; font-size : 18; }
QListWidget { background-color : #2d2d30; color : white; border-color : white; border-width : 1px; border-style : solid; padding : 10px 10px; font-family : Arial, sans-serif; font-weight : bold; font-size : 18; }
QPushButton { background-color : #2d2d30; color : white; border-color : white; border-width : 1px; border-style : solid; padding : 4px 10px 4px 10px; font-family : Arial, sans-serif; font-weight : bold; font-size : 18; }
QPushButton:hover {background-color : #202020; color : white; border-color : white; border-width : 1px; border-style : solid; padding : 4px 10px 4px 10px; }
QPushButton:pressed {background-color : #2d2d30; color : white; border-color : white; border-width : 1px; border-style : solid; padding : 4px 10px 4px 10px; }
QProgressBar { color : white; background-color : #2d2d30; border : 1px solid white; text-align : center; }
QProgressBar::chunk { background-color: #0c234b; }
QScrollArea { background-color : #2d2d30; border-color : white; border-width : 1px; border-style : solid; padding-top : 10px; padding-bottom : 10px; }
QScrollBar::vertical { background-color : #2d2d30; width : 15px; margin: 15px 3px 15px 3px; border : 1px transparent #2d2d30; border-radius : 4px;  }
QScrollBar::handle:vertical { background-color : #ab0520; border-radius: 4px; min-height: 20px; }
QScrollBar::sub-line:vertical { height : 0px }
QScrollBar::add-line:vertical { height : 0px }
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { background : none; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background : none; height : 0px }
QStatusBar { background-color : #383838; color : white; font-family : Arial, sans-serif; font-weight : bold; font-size : 18;}
QTabWidget::pane { background-color : #383838; color : white; }
QTabBar::tab { background-color : #383838; color : white; min-width : 35ex; padding : 4px 10px 4px 10px; font-family : Arial, sans-serif; font-weight : bold; font-size : 18; }
QTabBar::tab:hover { background-color : #2d2d30; color : white; }
QTabBar::tab:selected { border-color : #005dac; border-width : 1px; border-style : solid; }
QTabBar::close-button { image : url(photos/close_button.png); }
QTextEdit { background-color : #2d2d30; color : white; border-color : white; border-width : 1px; border-style : solid; padding : 4px 4px 4px 4px; font-family : Arial, sans-serif; font-weight : bold; font-size : 18; }
"""

class Main(QMainWindow):

    def __init__(self):
         # setting up window parameters
        super().__init__()
        self.w = None
        self.clicked = False
        self.file_list = []
        self.current_time = {'short' : '', 'long' : '', 'utc' : '', 'reg' : '', 'date' : ''}
        self.update_time()

        self.file_regex = '^([A-Z]{1})+([:])+([\\/])+([a-zA-Z0-9.,\[\]+=~`!@#$%^&\(\)\-\s\\/_]+)+[.]+([\w]{2,6})$'

        self.statusTimer = QTimer()
        self.statusTimer.timeout.connect(self.clear_status_label)

        screen = app.primaryScreen()
        size = screen.size()
        self.width = 1000
        self.height = 800
        self.left = (size.width() / 2) - (self.width / 2)
        self.top = (size.height() / 2) - (self.height / 2)
        
        self.supportedFileTypes = ("Data Files (*.txt);;")

        self.setStyleSheet(css_dark)
        self.setFont(QFont('Arial', 14))
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)
        self.labels()


    def labels(self):
        # declaring grid layout for widget organization
        widget = QWidget()
        gridLayout = QGridLayout()

        self.buttonFrame = QFrame()
        button_frame_grid = QGridLayout()
        self.buttonFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.clearFrame = QFrame()
        clear_frame_grid = QGridLayout()
        self.clearFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.clearFrame.hide()

        # labels, buttons, and entry fields
        self.prompt = QLabel('QParse: BAJA Parsing Program')
        self.prompt.setStyleSheet(" QLabel { border-bottom : 5px solid #ab0520; padding : 5px 0px; } ")
        self.prompt.setFont(QFont('Arial', 18))
        self.spacer = QLabel('')

        self.inputPrompt = QLabel('Input File Location:', self)
        self.inputFile = QLineEdit(self)
        self.inputFile.setReadOnly(True)
        self.browseFiles = QPushButton('Browse Files', self)
        self.browseFiles.clicked.connect(self.browseInputFiles)
        self.clearInput = QPushButton('Clear', self)
        self.clearInput.clicked.connect(self.clearInputEntry)

        self.outputPrompt = QLabel('Output Folder Location:', self)
        self.outputFolder = QLineEdit(self)
        self.outputFolder.setReadOnly(True)
        self.browseFolder = QPushButton('Browse Folder', self)
        self.browseFolder.clicked.connect(self.browseOutputFolder)
        self.clearOutput = QPushButton('Clear', self)
        self.clearOutput.clicked.connect(self.clearOutputEntry)

        self.processPrompt = QLabel('Process Output:', self)
        self.processBox = QTextEdit(self)
        self.processBox.setAcceptDrops(False)
        self.processBox.insertPlainText('>> Program Started: {}'.format(self.current_time['long']))

        self.statusLabel = QLabel('')
        self.statusLabel.setFont(QFont('Arial', 12))
        self.statusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.openButton = QPushButton('Open File', self)
        self.openButton.clicked.connect(self.openPushed)
        self.parseButton = QPushButton('Parse File', self)
        self.parseButton.clicked.connect(self.parsePushed)

        self.exportLogButton = QPushButton('Export Output', self)
        self.exportLogButton.clicked.connect(self.exportProcessBox)
        self.clearOutputButton = QPushButton('Clear Output', self)
        self.clearOutputButton.clicked.connect(self.clearProcessBox)
        
        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)

        button_frame_grid.addWidget(self.openButton, 0, 0, 1, 1)
        button_frame_grid.addWidget(self.parseButton, 0, 1, 1, 1)
        self.buttonFrame.setLayout(button_frame_grid)

        clear_frame_grid.addWidget(self.exportLogButton, 0, 0, 1, 1)
        clear_frame_grid.addWidget(self.clearOutputButton, 0, 1, 1, 1)
        self.clearFrame.setLayout(clear_frame_grid)

        #gridLayout.addWidget(self, QWidget, row, column, rowSpan, columnSpan, Qt.Alignment alignment = 0)
        gridLayout.addWidget(self.prompt, 0, 0, 1, 3)
        gridLayout.addWidget(self.spacer, 1, 0, 1, 3)
        gridLayout.addWidget(self.inputPrompt, 2, 0, 1, 1)
        gridLayout.addWidget(self.inputFile, 3, 0, 1, 1)
        gridLayout.addWidget(self.browseFiles, 3, 1, 1, 1)
        gridLayout.addWidget(self.clearInput, 3, 2, 1, 1)
        gridLayout.addWidget(self.outputPrompt, 4, 0, 1, 1)
        gridLayout.addWidget(self.outputFolder, 5, 0, 1, 1)
        gridLayout.addWidget(self.browseFolder, 5, 1, 1, 1)
        gridLayout.addWidget(self.clearOutput, 5, 2, 1, 1)
        gridLayout.addWidget(self.processPrompt, 6, 0, 1, 1)
        gridLayout.addWidget(self.processBox, 7, 0, 1, 3)
        gridLayout.addWidget(self.statusLabel, 8, 0, 1, 3, Qt.AlignCenter)
        gridLayout.addWidget(self.buttonFrame, 9, 0, 1, 3, Qt.AlignCenter)
        gridLayout.addWidget(self.clearFrame, 10, 0, 1, 3, Qt.AlignCenter)
        gridLayout.addWidget(self.progressBar, 11, 0, 1, 3)

        
        tb = QToolBar(self)
        tb.setMovable(False)
        tb.setContextMenuPolicy(Qt.PreventContextMenu)
        tb.mouseMoveEvent = self.mouseMove
        tb.mousePressEvent = self.mousePress

         #Tool Bar
        icon = QLabel(self)
        pixmap = QPixmap(ua_logo)
        pixmap = pixmap.scaled(25, 25)
        icon.setPixmap(pixmap)
        icon.setStyleSheet(" QLabel { background-color : #383838; } ")

        title = QLabel(' QParse: UofA BAJA Parsing Program')
        title.setStyleSheet(" QLabel { background-color : #383838; } ")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer.setStyleSheet(" QWidget { background-color : #383838; } ")

        minButton = QAction(self)
        minButton.setIcon(QIcon(minimize))
        minButton.setToolTip('Minimize')
        minButton.triggered.connect(self.minWindow)

        maxButton = QAction(self)
        maxButton.setIcon(QIcon(maximize))
        maxButton.setToolTip('Maximize')
        maxButton.triggered.connect(self.maxWindow)

        closeButton = QAction(self)
        closeButton.setIcon(QIcon(close_button))
        closeButton.setToolTip('Close')
        closeButton.triggered.connect(self.closeWindow)

        tb.addWidget(icon)
        tb.addWidget(title)
        tb.addWidget(spacer)
        tb.addAction(minButton)
        tb.addAction(maxButton)
        tb.addAction(closeButton)

        self.addToolBar(tb)
        widget.setLayout(gridLayout)
        self.setCentralWidget(widget)
        self.initUI()


    def browseInputFiles(self):
        options = QFileDialog.Options()

        self.filename , check = QFileDialog.getOpenFileName(self, "Select File to Parse", "", self.supportedFileTypes, options=options)

        if len(self.filename) != 0:
            self.inputFile.setText(self.filename)
            self.update_time()
            if any(self.processBox.toPlainText()):
                self.processBox.insertPlainText('\n>> [{}] File Imported: [{}]'.format(self.current_time['short'], self.filename))
            else:
                self.processBox.insertPlainText('>> [{}] File Imported: [{}]'.format(self.current_time['short'], self.filename))
    

    def browseOutputFolder(self):
        options = QFileDialog.Options()
       
        self.foldername = QFileDialog.getExistingDirectory(self, "Select Output Folder Loctation", "", options=options)
        
        if len(self.foldername) != 0:
            self.outputFolder.setText(self.foldername)
            self.update_time()
            if any(self.processBox.toPlainText()):
                self.processBox.insertPlainText('\n>> [{}] Folder Imported: [{}]'.format(self.current_time['short'], self.foldername))
            else:
                self.processBox.insertPlainText('>> [{}] Folder Imported: [{}]'.format(self.current_time['short'], self.foldername))
    

    def clearInputEntry(self):
        self.update_time()
        self.inputFile.clear()

        if any(self.filename):
            if any(self.processBox.toPlainText()):
                self.processBox.insertPlainText('\n>> [{}] File Removed: [{}]'.format(self.current_time['short'], self.filename))
            else:
                self.processBox.insertPlainText('>> [{}] File Removed: [{}]'.format(self.current_time['short'], self.filename))

        self.filename = ''


    def clearOutputEntry(self):
        self.update_time()
        self.outputFolder.clear()

        if any(self.foldername):
            if any(self.processBox.toPlainText()):
                self.processBox.insertPlainText('\n>> [{}] Folder Removed: [{}]'.format(self.current_time['short'], self.foldername))
            else:
                self.processBox.insertPlainText('>> [{}] Folder Removed: [{}]'.format(self.current_time['short'], self.foldername))

        self.foldername = ''
    

    def openPushed(self):
        if any(self.inputFile.text()):
            if re.search(self.file_regex, self.filename):
                position = self.pos()
                size = self.size()
                self.w = viewContents(size, position, self.filename)
            else:
                self.statusLabel.setText('Incorrect input file format!')
                self.statusTimer.start(5000)
        else:
            self.statusLabel.setText('No input file imported!')
            self.statusTimer.start(5000)
            self.browseInputFiles()


    def parsePushed(self):
        if any(self.inputFile.text()) and any(self.outputFolder.text()):
            if re.search(self.file_regex, self.filename) and self.filename.split('.')[-1].lower() == 'txt':
                self.statusLabel.setText('Parsing file...')
                self.statusTimer.start(5000)
                self.parseFile(self.filename, self.foldername)
            else:
                self.statusLabel.setText('Incorrect input file format!')
                self.statusTimer.start(5000)
        elif not any(self.inputFile.text()):
            self.statusLabel.setText('No input file imported!')
            self.statusTimer.start(5000)
            self.browseInputFiles()
        elif not any(self.outputFolder.text()):
            self.statusLabel.setText('No output folder imported!')
            self.statusTimer.start(5000)
            self.browseOutputFolder()


    def exportProcessBox(self):
        self.progressBar.setValue(0)
        if any(self.processBox.toPlainText()):
            if any(self.opened_folder):
                try:
                    self.progressBar.setValue(20)
                    foldername = self.opened_folder + '/output'
                    self.update_time()
                    self.progressBar.setValue(40)
                    self.processBox.insertPlainText('\n>> [{}] {} File Exported!'.format(self.current_time['short'], foldername + '/output.txt'))
                    self.processBox.ensureCursorVisible()
                    self.progressBar.setValue(60)
                    os.mkdir(os.path.join(foldername))
                    self.progressBar.setValue(80)
                    with open(os.path.join(foldername + '/output.txt'), 'a+') as file:
                        file.write(self.processBox.toPlainText())
                        file.close()
                    self.progressBar.setValue(100)
                    self.statusLabel.setText('Output successfully exported!')
                    self.statusTimer.start(5000)
                    self.clearProcessBox()
                except:
                    self.statusLabel.setText('Could not export output!')
                    self.statusTimer.start(5000)
                    self.progressBar.setValue(0)
            else:
                self.statusLabel.setText('File has not been parsed!')
                self.statusTimer.start(5000)
                self.progressBar.setValue(0)
        else:
            self.statusLabel.setText('Process box has been cleared!')
            self.statusTimer.start(5000)
            self.progressBar.setValue(0)


    def clearProcessBox(self):
        self.processBox.clear()
        self.progressBar.setValue(0)
        self.clearFrame.hide()
        self.buttonFrame.show()
        self.openButton.setEnabled(True)
        self.parseButton.setEnabled(True)
        self.update_time()
        self.processBox.insertPlainText('>> [{}] Output Cleared!'.format(self.current_time['short']))
        self.processBox.insertPlainText('\n>> Program Started {}'.format(self.current_time['long']))


    def parseFile(self, filename = '', foldername = ''):
        self.browseFiles.setEnabled(False)
        self.clearInput.setEnabled(False)
        self.browseFolder.setEnabled(False)
        self.clearOutput.setEnabled(False)
        self.openButton.setEnabled(False)
        self.parseButton.setEnabled(False)
        self.setFocus(False)
        self.update_time()
        foldername += '/QParse{}'.format(self.current_time['date'])

        self.timer = QElapsedTimer()
        self.timer.start()

        os.mkdir(os.path.join(foldername))
        self.opened_folder = foldername

        self.thread = parseFile(filename, foldername)
        self.thread.start()
        self.thread.progress.connect(self.update)
        self.thread.finished.connect(self.finished)


    def update(self, count, interval):
        runtime = (self.timer.elapsed() / 1000)
        self.progressBar.setValue(interval)
        self.update_time()
        self.processBox.insertPlainText('\n>> [{}] Parsing Line {}...'.format(self.current_time['short'], count))
        self.processBox.ensureCursorVisible()
        self.statusLabel.setText('Time Elapsed: {} seconds'.format(runtime))
        

    def finished(self, text):
        self.file_list.append(text)

        if 'formatted.txt' in text:
            self.browseFiles.setEnabled(True)
            self.clearInput.setEnabled(True)
            self.browseFolder.setEnabled(True)
            self.clearOutput.setEnabled(True)

            for file in self.file_list:
                self.update_time()
                self.processBox.insertPlainText('\n>> [{}] {} successfully saved!'.format(self.current_time['short'], file))
                self.processBox.ensureCursorVisible()

            runtime = (self.timer.elapsed() / 1000)
            self.parseButton.setEnabled(True)
            self.progressBar.setValue(100)
            self.update_time()
            self.processBox.insertPlainText('\n>> [{}] File Parsing Finished in {} seconds!'.format(self.current_time['short'], runtime))
            self.processBox.ensureCursorVisible()
            self.statusLabel.setText('File Parsing Finished in {} seconds!'.format(runtime))
            self.statusTimer.start(5000)
            self.buttonFrame.hide()
            self.clearFrame.show()


    def clear_status_label(self):
        self.statusLabel.clear()


    def dragEnterEvent( self, event ):
        data = event.mimeData()
        urls = data.urls()
        if ( urls and urls[0].scheme() == 'file' ):
            event.acceptProposedAction()


    def dragMoveEvent( self, event ):
        data = event.mimeData()
        urls = data.urls()
        if ( urls and urls[0].scheme() == 'file' ):
            event.acceptProposedAction()


    def dropEvent( self, event ):
        data = event.mimeData()
        urls = data.urls()
        if ( urls and urls[0].scheme() == 'file' ):
            self.dropData = [urls[0].path()[1:]]
            self.filename = urls[0].path()[1:]
            self.inputFile.setText(str(self.filename))
            if not any(self.processBox.toPlainText()):
                self.processBox.insertPlainText('>> [{}] File Imported: {}'.format(self.current_time['short'], str(self.filename)))
            else:
                self.processBox.insertPlainText('\n>> [{}] File Imported: {}'.format(self.current_time['short'], str(self.filename)))
                    

    def mousePress(self, event):
        self.old_pos = event.screenPos()


    def mouseMove(self, event):
        if self.isMaximized():
            self.showNormal()
        if self.clicked:
            dx = self.old_pos.x() - event.screenPos().x()
            dy = self.old_pos.y() - event.screenPos().y()     
            self.move(self.pos().x() - dx, self.pos().y() - dy)
        self.old_pos = event.screenPos()
        self.clicked = True


    def minWindow(self):
        self.setWindowState(Qt.WindowMinimized)


    def maxWindow(self):
        if self.isMaximized():
            self.showNormal()
        elif not self.isMaximized():
            self.showMaximized()


    def closeWindow(self):
        app.quit()

    
    def update_time(self):
        self.current_time['short'] = datetime.datetime.now().strftime('%H:%M:%S:%f')
        self.current_time['long'] = datetime.datetime.now().strftime('%a %b %d %Y %H:%M:%S')
        self.current_time['utc'] = datetime.datetime.utcnow()
        self.current_time['reg'] = datetime.datetime.now()
        self.current_time['date'] = datetime.datetime.now().strftime('%m-%d-%y %H.%M.%S')


    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.show()


class viewContents(QMainWindow):
    def __init__(self, size, position, filename):
        super().__init__()
        self.w = None
        self.clicked = False
        self.filename = filename
        self.main_size = size
        self.position = position
        self.width = self.main_size.width()
        self.height = self.main_size.height()
        self.left = self.position.x()
        self.top = self.position.y()
        
        self.thread = ''
        self.statusTimer = QTimer()
        self.statusTimer.timeout.connect(self.clear_status_label)

        self.setStyleSheet(css_dark)
        self.setFont(QFont('Arial', 14))
        self.labels()

        
    def labels(self):
        # declaring grid layout for widget organization
        widget = QWidget()
        grid_layout = QGridLayout()

        # labels, buttons, and entry fields
        self.prompt = QLabel('View File: {}'.format(self.filename))
        self.prompt.setStyleSheet(" QLabel { border-bottom : 5px solid #ab0520; padding : 5px 0px; } ")

        self.fileContents = QTextEdit(self)
        self.fileContents.setReadOnly(True)
        self.fileContents.setAcceptDrops(False)

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)

        self.statusLabel = QLabel('Loading File...')
        self.statusLabel.setFont(QFont('Arial', 12))
        self.statusLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.close = QPushButton('Close', self)
        self.close.clicked.connect(self.close_window)

        #grid_layout.addWidget(self, QWidget, row, column, rowSpan, columnSpan, Qt.Alignment alignment = 0)
        grid_layout.addWidget(self.prompt, 0, 0, 1, 1, Qt.AlignLeft)
        grid_layout.addWidget(self.fileContents, 1, 0, 1, 1)
        grid_layout.addWidget(self.statusLabel, 2, 0, 1, 1, Qt.AlignCenter)
        grid_layout.addWidget(self.progressBar, 3, 0, 1, 1,)
        grid_layout.addWidget(self.close, 4, 0, 1, 1, Qt.AlignCenter)

        tb = QToolBar(self)
        tb.setMovable(False)
        tb.setContextMenuPolicy(Qt.PreventContextMenu)
        tb.mouseMoveEvent = self.mouseMove
        tb.mousePressEvent = self.mousePress

         #Tool Bar
        icon = QLabel(self)
        pixmap = QPixmap(ua_logo)
        pixmap = pixmap.scaled(25, 25)
        icon.setPixmap(pixmap)
        icon.setStyleSheet(" QLabel { background-color : #383838; } ")

        title = QLabel(' QParse: UofA BAJA Parsing Program')
        title.setStyleSheet(" QLabel { background-color : #383838; } ")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer.setStyleSheet(" QWidget { background-color : #383838; } ")

        minButton = QAction(self)
        minButton.setIcon(QIcon(minimize))
        minButton.setToolTip('Minimize')
        minButton.triggered.connect(self.minWindow)

        maxButton = QAction(self)
        maxButton.setIcon(QIcon(maximize))
        maxButton.setToolTip('Maximize')
        maxButton.triggered.connect(self.maxWindow)

        closeButton = QAction(self)
        closeButton.setIcon(QIcon(close_button))
        closeButton.setToolTip('Close')
        closeButton.triggered.connect(self.close_window)

        tb.addWidget(icon)
        tb.addWidget(title)
        tb.addWidget(spacer)
        tb.addAction(minButton)
        tb.addAction(maxButton)
        tb.addAction(closeButton)

        self.addToolBar(tb)
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)
        self.printFileContents(self.filename)
        self.initUI()


    def printFileContents(self, filename):
        try:
            self.timer = QElapsedTimer()
            self.timer.start()
            self.thread = viewClass(filename)
            self.thread.start()
            self.thread.progress.connect(self.update)
            self.thread.finished.connect(self.finished)
        except:
            self.statusLabel.setText('[ERROR] Could not parse file!')
            self.statusTimer.start(5000)


    def update(self, line, interval):
        runtime = (self.timer.elapsed() / 1000)
        self.fileContents.insertPlainText(line)
        self.progressBar.setValue(interval)
        self.statusLabel.setText('Time Elapsed: {} seconds'.format(runtime))


    def finished(self):
        runtime = (self.timer.elapsed() / 1000)
        self.fileContents.moveCursor(QTextCursor.Start)
        self.progressBar.setValue(100)
        self.statusLabel.setText('File loaded in {} seconds!'.format(runtime))
        self.statusTimer.start(5000)
        #self.close.setEnabled(True)


    def clear_status_label(self):
        self.statusLabel.clear()
        

    def mousePress(self, event):
        self.old_pos = event.screenPos()


    def mouseMove(self, event):
        if self.isMaximized():
            self.showNormal()
        if self.clicked:
            dx = self.old_pos.x() - event.screenPos().x()
            dy = self.old_pos.y() - event.screenPos().y()     
            self.move(self.pos().x() - dx, self.pos().y() - dy)
        self.old_pos = event.screenPos()
        self.clicked = True


    def minWindow(self):
        self.setWindowState(Qt.WindowMinimized)


    def maxWindow(self):
        if self.isMaximized():
            self.showNormal()
        elif not self.isMaximized():
            self.showMaximized()


    def close_window(self):
        self.thread.terminate = True
        viewContents.close(self)


    def initUI(self):
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


class parseFile(QThread):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int, int)
    def __init__(self, filename = '', foldername = ''):
        super().__init__()
        self.filename = filename
        self.foldername = foldername


    def run(self):
        with open(self.filename, 'r+') as file:
            text = file.readlines()
            i = 0
            self.thread = {}

            shutil.copy(self.filename, self.foldername)

            self.thread[i] = formatted(text)
            self.thread[i].start()
            self.thread[i].progress.connect(self.progressFormat)
            self.thread[i].finished.connect(self.formatted)
            i += 1

            self.thread[i] = speed1Parse(text)
            self.thread[i].start()
            self.thread[i].finished.connect(self.speedDeg)
            i += 1

            self.thread[i] = speed2Parse(text)
            self.thread[i].start()
            self.thread[i].finished.connect(self.speedMPH)
            i += 1

            self.thread[i] = satParse(text)
            self.thread[i].start()
            self.thread[i].finished.connect(self.sat)
            i += 1

            self.thread[i] = altParse(text)
            self.thread[i].start()
            self.thread[i].finished.connect(self.alt)
            i += 1

            self.thread[i] = coordParse(text)
            self.thread[i].start()
            self.thread[i].finished.connect(self.coordinates)
            i += 1

    
    def progressFormat(self, count, interval):
        self.progress.emit(count, interval)


    def formatted(self, text):
        filename = os.path.join(self.foldername + '/formatted.txt')
        with open(filename, 'a+') as file:
            file.write(text)
            file.close()
        self.finished.emit(filename)


    def speedDeg(self, text):
        filename = os.path.join(self.foldername + '/speed_deg.txt')
        with open(filename, 'a+') as file:
            file.write(text)
            file.close()
        self.finished.emit(filename)


    def speedMPH(self, text):
        filename = os.path.join(self.foldername + '/speed_mph.txt')
        with open(filename, 'a+') as file:
            file.write(text)
            file.close()
        self.finished.emit(filename)


    def sat(self, text):
        filename = os.path.join(self.foldername + '/sattelites.txt')
        with open(filename, 'a+') as file:
            file.write(text)
            file.close()
        self.finished.emit(filename)


    def alt(self, text):
        filename = os.path.join(self.foldername + '/altitude.txt')
        with open(filename, 'a+') as file:
            file.write(text)
            file.close()
        self.finished.emit(filename)


    def coordinates(self, text):
        filename = os.path.join(self.foldername + '/coordinates.txt')
        with open(filename, 'a+') as file:
            file.write(text)
            file.close()
        self.finished.emit(filename)


class formatted(QThread):
    finished = pyqtSignal(str)
    progress = pyqtSignal(int, int)
    def __init__(self, text = ''):
        super().__init__()
        self.text = text

    def run(self):
        self.formatted = ''
        interval = count = 0
        progressInterval = (100 / len(self.text))
        for line in self.text:
            line = re.sub(('\xFF\xFF\xFF'), '', line)
            line = re.sub(('\"'), '', line)

            if 'speedometer.val=' in line:
                line = re.sub(('speedometer.val='), 'Speed(deg):', line)
                self.formatted += line
            elif 'speedDigital.val=' in line:
                line = re.sub(('speedDigital.val='), 'Speed(mph):', line)
                self.formatted += line
            elif 'satDigital.txt=Sats:' in line:
                line = re.sub(('satDigital.txt=Sats:'), 'Satellites:', line)
                self.formatted += line
            elif 'altDigital.txt=Alt:' in line:
                line = re.sub(('altDigital.txt=Alt:'), 'Altitude:', line)
                self.formatted += line
            elif 'coordDigital.txt=' in line:
                line = re.sub(('coordDigital.txt='), 'Coordinates:', line)
                self.formatted += line
            else:
                self.formatted += line
            
            interval += progressInterval
            count += 1
            self.progress.emit(count, interval)
        self.finished.emit(self.formatted)


class speed1Parse(QThread):
    finished = pyqtSignal(str)
    def __init__(self, text = ''):
        super().__init__()
        self.text = text

    def run(self):
        self.speed_deg = ''
        for line in self.text:
            line = re.sub(('\xFF\xFF\xFF'), '', line)
            line = re.sub(('\"'), '', line)

            if 'speedometer.val=' in line:
                line = re.sub(('speedometer.val='), '', line)
                self.speed_deg += line

        self.finished.emit(self.speed_deg)


class speed2Parse(QThread):
    finished = pyqtSignal(str)
    def __init__(self, text = ''):
        super().__init__()
        self.text = text

    def run(self):
        self.speed_mph = ''
        for line in self.text:
            line = re.sub(('\xFF\xFF\xFF'), '', line)
            line = re.sub(('\"'), '', line)

            if 'speedDigital.val=' in line:
                line = re.sub(('speedDigital.val='), '', line)
                self.speed_mph += line

        self.finished.emit(self.speed_mph)
        

class satParse(QThread):
    finished = pyqtSignal(str)
    def __init__(self, text = ''):
        super().__init__()
        self.text = text

    def run(self):
        self.sats = ''
        for line in self.text:
            line = re.sub(('\xFF\xFF\xFF'), '', line)
            line = re.sub(('\"'), '', line)

            if 'satDigital.txt=Sats:' in line:
                line = re.sub(('satDigital.txt=Sats:'), '', line)
                self.sats += line

        self.finished.emit(self.sats)


class altParse(QThread):
    finished = pyqtSignal(str)
    def __init__(self, text = ''):
        super().__init__()
        self.text = text

    def run(self):
        self.alt = ''
        for line in self.text:
            line = re.sub(('\xFF\xFF\xFF'), '', line)
            line = re.sub(('\"'), '', line)

            if 'altDigital.txt=Alt:' in line:
                line = re.sub(('altDigital.txt=Alt:'), '', line)
                self.alt += line

        self.finished.emit(self.alt)


class coordParse(QThread):
    finished = pyqtSignal(str)
    def __init__(self, text = ''):
        super().__init__()
        self.text = text

    def run(self):
        self.coord = ''
        for line in self.text:
            line = re.sub(('\xFF\xFF\xFF'), '', line)
            line = re.sub(('\"'), '', line)

            if 'coordDigital.txt=' in line:
                line = re.sub(('coordDigital.txt='), '', line)
                self.coord += line

        self.finished.emit(self.coord)


class viewClass(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(str, int)
    def __init__(self, filename = ''):
        super().__init__()
        self.filename = filename
        self.terminate = False

    def run(self):
        try:
            with open(self.filename, 'r+') as file:
                text = file.readlines()
                progressInterval = (100 / len(text))
                interval = i = 0
                while i < len(text) and self.terminate == False:
                    interval += progressInterval
                    self.progress.emit(text[i], interval)
                    i += 1
            self.finished.emit()
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())