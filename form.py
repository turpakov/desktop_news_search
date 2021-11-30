# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2
from PyQt5.QtWidgets import QGridLayout, QLabel

conn = psycopg2.connect(dbname='lenta', user='postgres', password='101010', host='localhost', port='1234')
conn.autocommit = True
cur = conn.cursor()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("LENTA")
        MainWindow.resize(900, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        MainWindow.setMaximumSize(QtCore.QSize(900, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 50, 831, 471))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        self.tableWidget.itemDoubleClicked.connect(self.on_cell_item_clicked)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(120, 10, 551, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.lineEdit.setPlaceholderText('Поиск по тексту')

        self.loadData = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.loadData)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("LENTA", "LENTA"))
        MainWindow.setWindowIcon(QtGui.QIcon("icons\\main.jpg"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "url"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "title"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "topic"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "tags"))
        self.tableWidget.horizontalHeader().setSectionResizeMode(1)
        self.loadData.setText("Загрузить")

    def on_cell_item_clicked(self):
        try:
            col = self.tableWidget.currentColumn()
            row = self.tableWidget.currentRow()
            title = self.tableWidget.item(row, col).text()
            cur.execute(f"select text from lenta where title = '{title}'")
            text = cur.fetchone()[0]
            d = Info(title, text)
            d.exec()
        except:
            pass

        
class Info(QtWidgets.QDialog):
    def __init__(self, title, text, parent=None):
        super(Info, self).__init__(parent)
        self.setWindowTitle(f'{title}')
        self.resize(800, 500)
        self.setWindowIcon(QtGui.QIcon("icons\\info.png"))
        layout = QGridLayout()
        text_box = QtWidgets.QTextEdit()
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        text_box.setFont(font)
        text_box.setReadOnly(True)
        layout.addWidget(text_box, 0, 0, 4, 4)
        text_box.append(text)
        self.setLayout(layout)

class ClassDialogFalse(QtWidgets.QDialog):
    def __init__(self, text, parent=None):
        super(ClassDialogFalse, self).__init__(parent)
        self.setGeometry(710, 400, 500, 100)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btnClosed)
        self.verticalLayout.addWidget(self.pushButton)
        self.setWindowTitle(text)
        self.pushButton.setText("Ok")
        self.setWindowIcon(QtGui.QIcon("icons\\false.jpg"))
        self.setWhatsThis('')

    def btnClosed(self):
        self.close()


class ClassDialogTrue(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ClassDialogTrue, self).__init__(parent)
        self.setGeometry(710, 400, 500, 100)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.btnClosed)
        self.verticalLayout.addWidget(self.pushButton)
        self.setWindowTitle("Load completed successfully!")
        self.pushButton.setText("Ok")
        self.setWindowIcon(QtGui.QIcon("icons\\true.jpg"))
        self.setWhatsThis('')

    def btnClosed(self):
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

