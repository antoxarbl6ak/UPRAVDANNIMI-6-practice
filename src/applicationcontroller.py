import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtSql import QSqlDatabase
from connectdialog import ConnectDialog
from mainwindow import MainWnndow


class ApplicationController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.dialog = None
        self.mainwindow = None
        self.show_connect_dialog()
    def show_connect_dialog(self):
        self.dialog = ConnectDialog()
        self.dialog.lineEditaddress.setText("LAPTOP-BSD0NS03")
        self.dialog.lineEditdbname.setText("TEST")
        self.dialog.lineEditlogin.setText("sql_user")
        self.dialog.lineEditpassword.setText("password")
        if self.dialog.exec_() == QDialog.Accepted:
            db = QSqlDatabase.database()
            self.show_mainwindow(db)
        else:
            sys.exit(0)
    def show_mainwindow(self, db):
        self.mainwindow = MainWnndow(db)
        sys.exit(self.app.exec_())
