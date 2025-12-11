from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5 import Qt

class AddRecordDialog(QDialog):
    def __init__(self, db, table_name, parent=None):
        super().__init__(parent)
        self.db = db
        self.table_name = table_name
        
        self.setWindowTitle(f"Добавить в {table_name}")
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout(self)
        
        model = QSqlTableModel()
        model.setTable(table_name)
        model.select()
        
        all_columns = []
        for i in range(model.columnCount()):
            column_name = model.headerData(i, 1)
            all_columns.append(column_name)
        
        pk_index = model.primaryKey()
        pk_columns = []
        if pk_index.count() > 0:
            for i in range(pk_index.count()):
                pk_column_name = pk_index.fieldName(i)
                pk_columns.append(pk_column_name)

        columns_without_pk = [col for col in all_columns if col not in pk_columns]
        
        self.inputs = {}
        
        for field_name in columns_without_pk:
            label = QLabel(field_name)
            line_edit = QLineEdit()
            
            layout.addWidget(label)
            layout.addWidget(line_edit)
            
            self.inputs[field_name] = line_edit
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Добавить")
        btn_cancel = QPushButton("Отмена")
        
        btn_ok.clicked.connect(self.add_record)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        
        layout.addLayout(btn_layout)
    
    def add_record(self):
        columns = []
        values = []
        
        for field_name, line_edit in self.inputs.items():
            value = line_edit.text().strip()
            if value:
                columns.append(field_name)
                escaped_value = value.replace("'", "''")
                values.append(f"'{escaped_value}'")
        
        if not columns:
            QMessageBox.warning(self, "Ошибка", "Введите данные")
            return
        
        sql = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({', '.join(values)})"
        
        query = QSqlQuery(self.db)
        if query.exec(sql):
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", query.lastError().text())