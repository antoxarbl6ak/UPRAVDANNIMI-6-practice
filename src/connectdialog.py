from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class ConnectDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi(r"ui\connectdialog.ui", self)

        self.pushButtonconnect.clicked.connect(self.connectToDB)
    def connectToDB(self):
        db = QSqlDatabase.addDatabase("QODBC")
        connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={self.lineEditaddress.text().strip()};"
        f"DATABASE={self.lineEditdbname.text().strip()};"
        f"UID={self.lineEditlogin.text().strip()};"
        f"PWD={self.lineEditpassword.text()};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;")
        db.setDatabaseName(connection_string)
        if not db.open():
            error = db.lastError().text()
            QMessageBox.critical(None, "Ошибка подключения", 
                                 f"Не удалось подключиться к SQL Server:\n{error}")
        else:
            self.done(QDialog.Accepted)
            

