from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt5.QtSql import QSqlDatabase, QSql, QSqlQuery
from PyQt5.QtCore import Qt
from addrecorddialog import AddRecordDialog
from deleterecord import DeleteDialog
from editrecorddialog import EditRecordDialog
from exporttopdf import *


class MainWnndow(QMainWindow):
    def __init__(self, db):
        QMainWindow.__init__(self)
        uic.loadUi(r"ui\mainwindow.ui", self)

        self.db = db
        self.set_combobox_choosetable()
        self.pushButtonAdd.clicked.connect(self.addrecord)
        self.pushButtonDelete.clicked.connect(self.deleterecord)
        self.pushButtonEdit.clicked.connect(self.editrecord)
        self.action_pdf.triggered.connect(self.export_to_pdf)

        self.show()
    def export_to_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как PDF", "", "PDF Files (*.pdf)"
        )
        
        if filename:
            if not filename.endswith('.pdf'):
                filename += '.pdf'

            if export_to_pdf_html(self.tableWidget, filename):
                QMessageBox.information(self, "Успех", f"Таблица сохранена в:\n{filename}")
    def addrecord(self):
        table_name = self.comboBoxChooseTable.currentText()
        if table_name == "Выберете таблицу" or not table_name:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите таблицу из списка")
            return
        dialog = AddRecordDialog(self.db, table_name, self)
        if dialog.exec() == AddRecordDialog.Accepted:
            self.combobox_choosetable_index_changed(self.comboBoxChooseTable.currentIndex())
    def deleterecord(self):
        table_name = self.comboBoxChooseTable.currentText()
        dialog = DeleteDialog(self.db, table_name, self.tableWidget, self)
        if dialog.exec() == DeleteDialog.Accepted:
            self.combobox_choosetable_index_changed(self.comboBoxChooseTable.currentIndex())
    def editrecord(self):
        table_name = self.comboBoxChooseTable.currentText()
        dialog = EditRecordDialog(self.db, table_name, self.tableWidget, self)
        if dialog.exec() == EditRecordDialog.Accepted:
            self.combobox_choosetable_index_changed(self.comboBoxChooseTable.currentIndex())
    def set_combobox_choosetable(self):
        self.comboBoxChooseTable.addItem("Выберете таблицу")
        tables = [t for t in self.db.tables() if 'trace_xe_' not in t and 'sys.' not in t]
        self.comboBoxChooseTable.addItems(tables)
        self.comboBoxChooseTable.setCurrentIndex(0)
        self.comboBoxChooseTable.currentIndexChanged.connect(self.combobox_choosetable_index_changed)
    def combobox_choosetable_index_changed(self, index):
        if index == 0:
            return
        query = QSqlQuery(self.db)
    
        if not query.exec(f"SELECT * FROM [{self.comboBoxChooseTable.currentText()}];"):
            print(f"Ошибка запроса: {query.lastError().text()}")
            return False
        
        column_count = query.record().count()

        rows = []
        while query.next():
            row = []
            for i in range(column_count):
                value = query.value(i)
                row.append("" if value is None else str(value))
            rows.append(row)

        self.tableWidget.setColumnCount(column_count)
        self.tableWidget.setRowCount(len(rows))

        record = query.record()
        for i in range(column_count):
            header = record.fieldName(i)
            self.tableWidget.setHorizontalHeaderItem(i, QTableWidgetItem(header))

        for row_idx, row_data in enumerate(rows):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(cell_data)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_idx, col_idx, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        return True

