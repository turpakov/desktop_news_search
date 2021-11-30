import csv
import sys

import psycopg2
import threading
from PyQt5 import QtWidgets
import form

conn = psycopg2.connect(dbname='lenta', user='postgres', password='101010', host='localhost', port='1234')
conn.autocommit = True
cur = conn.cursor()

Ui_MainWindow = form.Ui_MainWindow

class appCorrectData(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # init data
        data = self.select_all_data()
        self.load_data(data)
        # events
        self.loadData.clicked.connect(self.loadFile)
        self.lineEdit.textChanged.connect(self.updateTable)


    def updateTable(self):
        self.search()


    def select_all_data(self):
        select = 'select url, title, topic, tags from lenta limit 1000'
        cur.execute(select)
        data = cur.fetchall()
        return data


    def select_by_query(self, query):
        text = query.split(" ")
        for i in text:
            if i == "":
                text.remove(i)
        if len(text) == 1:
            query = text[0]
        else:
            query = ""
            for word in text:
                query += (word + " & ")
            query = query[: -2]
        select = "select url, title, topic, tags" \
                 " from lenta" \
                 f" where lenta_index @@ to_tsquery('russian', '{query}')" \
                 f" order by ts_rank(lenta_index, to_tsquery('russian', '{query}')) desc"
        cur.execute(select)
        data = cur.fetchall()
        return data


    def thread(my_func):
        def wrapper(*args, **kwargs):
            my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
            my_thread.start()
        return wrapper


    def load_data(self, data):
        self.tableWidget.setRowCount(0)
        try:
            for i, row in enumerate(data):
                self.tableWidget.insertRow(i)
                for j, cell in enumerate(row):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(cell)))
        except:
            pass
        return 0


    @thread
    def search(self):
        try:
            query = self.lineEdit.text()
            buff = query.strip(" ")
            if buff:
                data = self.select_by_query(buff)
            else:
                data = 0
            if data != 0:
                self.load_data(data)
            if not query:
                data = self.select_all_data()
                self.load_data(data)
            return data
        except:
            d = form.ClassDialogFalse("Incorrect execute!")
            d.exec()


    def loadFile(self):
        F = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', '')[0]
        try:
            if F:
                with open(F, 'r') as f:
                    reader = csv.reader(f)
                    next(reader)
                    for row in reader:
                        cur.execute(
                            f"INSERT INTO lenta VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', '{row[4]}')")
                        select = "UPDATE lenta " \
                                 "SET lenta_index = to_tsvector('russian', coalesce(title,'') || ' ' || coalesce(text,'')) " \
                                 f"WHERE text = '{row[2]}'"
                        cur.execute(select)
                    d = form.ClassDialogTrue()
                    d.exec()
        except:
            d = form.ClassDialogFalse("Incorrect file!")
            d.exec()


def show_form():
    app = QtWidgets.QApplication(sys.argv)
    a = appCorrectData()
    a.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    show_form()