from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument

def export_to_pdf_html(table_widget, filename="table.pdf"):
    html = "<html><body><table border='1' style='border-collapse: collapse;'>"

    html += "<tr style='background-color: #f0f0f0;'>"
    for col in range(table_widget.columnCount()):
        header = table_widget.horizontalHeaderItem(col)
        text = header.text() if header else f"Col {col+1}"
        html += f"<th style='padding: 5px;'>{text}</th>"
    html += "</tr>"

    for row in range(table_widget.rowCount()):
        html += "<tr>"
        for col in range(table_widget.columnCount()):
            item = table_widget.item(row, col)
            text = item.text() if item else ""
            html += f"<td style='padding: 5px;'>{text}</td>"
        html += "</tr>"
    
    html += "</table></body></html>"

    printer = QPrinter(QPrinter.HighResolution)
    printer.setOutputFormat(QPrinter.PdfFormat)
    printer.setOutputFileName(filename)
    
    doc = QTextDocument()
    doc.setHtml(html)
    doc.print_(printer)
    
    return True