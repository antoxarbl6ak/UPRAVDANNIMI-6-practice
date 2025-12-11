from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel


class DeleteDialog(QDialog):
    def __init__(self, db, table_name, table_widget, parent=None):
        super().__init__(parent)
        self.db = db
        self.table_name = table_name
        self.table_widget = table_widget
        
        self.setWindowTitle(f"Удаление записи")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        message = QLabel(f"Удалить выбранную запись из таблицы '{table_name}'?")
        message.setStyleSheet("font-weight: bold;")
        layout.addWidget(message)
        
        warning = QLabel("Это действие нельзя отменить!")
        warning.setStyleSheet("color: red;")
        layout.addWidget(warning)

        button_layout = QHBoxLayout()
        btn_ok = QPushButton("Удалить")
        btn_cancel = QPushButton("Отмена")
        
        btn_ok.clicked.connect(self.delete_record_simple)
        btn_cancel.clicked.connect(self.reject)
        
        btn_ok.setStyleSheet("background-color: #ff4444; color: white;")
        
        button_layout.addWidget(btn_ok)
        button_layout.addWidget(btn_cancel)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def delete_record_simple(self):
        try:
            current_row = self.table_widget.currentRow()
            
            if current_row == -1:
                QMessageBox.warning(self, "Ошибка", "Не выбрана строка!")
                return

            model = QSqlTableModel(self, self.db)
            model.setTable(self.table_name)
            model.select()
            
            if model.rowCount() > current_row:
                if model.removeRow(current_row):
                    if model.submitAll():
                        QMessageBox.information(self, "Успех", "Запись удалена!")
                        self.accept()
                    else:
                        QMessageBox.critical(self, "Ошибка", "Не удалось сохранить изменения")
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось удалить строку")
            else:
                QMessageBox.warning(self, "Ошибка", "Строка не найдена в базе данных")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {str(e)}")