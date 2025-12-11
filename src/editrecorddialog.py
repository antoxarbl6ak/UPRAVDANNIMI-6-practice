from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtSql import QSqlQuery, QSqlTableModel
from PyQt5.QtCore import Qt

class EditRecordDialog(QDialog):
    def __init__(self, db, table_name, table_widget, parent=None):
        super().__init__(parent)
        self.db = db
        self.table_name = table_name
        self.table_widget = table_widget
        self.selected_row = table_widget.currentRow()
        
        if self.selected_row == -1:
            QMessageBox.warning(None, "Ошибка", "Не выбрана строка!")
            self.reject()
            return
        
        self.setWindowTitle(f"Изменить запись")
        self.setMinimumWidth(300)
        
        layout = QVBoxLayout(self)
        
        columns = []
        for col in range(table_widget.columnCount()):
            header_item = table_widget.horizontalHeaderItem(col)
            if header_item:
                columns.append(header_item.text())
        
        self.inputs = {}

        model = QSqlTableModel()
        model.setTable(table_name)
        pk_index = model.primaryKey()
        pk_columns = []
        if pk_index.count() > 0:
            for i in range(pk_index.count()):
                pk_column_name = pk_index.fieldName(i)
                pk_columns.append(pk_column_name.lower())
        self.pk_columns = pk_columns
        
        for col_idx, field_name in enumerate(columns):
            label = QLabel(field_name)
            line_edit = QLineEdit()
            
            item = table_widget.item(self.selected_row, col_idx)
            if item:
                line_edit.setText(item.text())
            
            if field_name.lower() in pk_columns:
                line_edit.setReadOnly(True)
                line_edit.setStyleSheet("background-color: #f0f0f0;")
            
            layout.addWidget(label)
            layout.addWidget(line_edit)
            self.inputs[field_name] = (line_edit, col_idx)
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("Сохранить")
        btn_cancel = QPushButton("Отмена")
        
        btn_ok.clicked.connect(self.edit_record_simple)
        btn_cancel.clicked.connect(self.reject)
        
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
    
    def edit_record_simple(self):
        try:
            where_parts = []
            where_values = []
            
            set_parts = []
            set_values = []
            
            for field_name, (line_edit, col_idx) in self.inputs.items():
                value = line_edit.text().strip()
                
                is_id_field = field_name.lower() in self.pk_columns
                
                if is_id_field:
                    where_parts.append(f"[{field_name}] = ?")
                    where_values.append(value)
                else:
                    set_parts.append(f"[{field_name}] = ?")
                    set_values.append(value if value else None)
            
            if not where_parts:
                QMessageBox.warning(self, "Ошибка", "Не найден ID для обновления!")
                return
            
            sql = f"UPDATE {self.table_name} SET {', '.join(set_parts)} WHERE {' AND '.join(where_parts)}"
            
            query = QSqlQuery(self.db)
            query.prepare(sql)
            
            for value in set_values + where_values:
                query.addBindValue(value)
            
            if query.exec():
                QMessageBox.information(self, "Успех", "Запись обновлена!")
                self.accept()
            else:
                error = query.lastError().text()
                QMessageBox.critical(self, "Ошибка", f"Ошибка: {error}")
        
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")