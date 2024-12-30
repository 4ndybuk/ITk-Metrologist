# Allocates the component information to the table widget QTableWidget
from PySide6.QtWidgets import (QTableWidget, QTableWidgetItem, QPushButton, 
                               QLineEdit, QLabel, QAbstractItemView, QApplication, 
                               QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard
import itkdb
import webbrowser

def table_allocate(table: QTableWidget, client: itkdb.Client, input: QLineEdit):
    try:
        component = client.get('getComponent',json={"component":input.text(),"alternativeIdentifier":False})
    except:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
        QMessageBox.critical(None,"Error", "Component not found!",
                             QMessageBox.Ok)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
        input.clear()
        return

    open_page_button = QPushButton("Open Page")
    open_page_button.clicked.connect(lambda: webbrowser.open(f"https://itkpd-test.unicorncollege.cz/componentView?code={component['code']}",new = 2))
    open_page_button.setStyleSheet("""
                                    QPushButton {
                                            background-color: white;
                                            border: 1px solid #c0c0c0;
                                            border-radius: 15px;
                                            padding: 1px 3px;
                                            font-size: 11px;
                                            font-weight: bold;
                                            color: #000000;
                                            text-align: center;
                                            }
                                    QPushButton:hover {
                                            background-color: #d4e7fa;
                                            }
                                    QPushButton:pressed {
                                            background-color: #bfd0e0;
                                            border: 1px solid #717171;
                                            }
                                            """)

    # Add a new row at the end of the table
    row_position = table.rowCount()
    table.insertRow(row_position)

    # Disable sorting when filling in the rows
    table.setSortingEnabled(False)
    # Disable editing
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # Align location and type cell to the centre
    location_cell = QTableWidgetItem(component['currentLocation']['code'])
    type_cell = QTableWidgetItem(component['componentType']['code'])
    location_cell.setTextAlignment(Qt.AlignCenter)
    type_cell.setTextAlignment(Qt.AlignCenter)

    table.setItem(row_position, 0, QTableWidgetItem(input.text()))
    table.setItem(row_position, 1, type_cell)
    table.setItem(row_position, 2, location_cell)
    table.setItem(row_position, 3, QTableWidgetItem(component['currentStage']['code']))
    table.setCellWidget(row_position, 4, open_page_button)

    # Enable sorting after filling in the rows
    table.setSortingEnabled(True)

    # Clear the input for another serial number
    input.clear()

def hide_scan_label(input: QLineEdit, label: QLabel):
    """
    Hides the text behind the input when typing in characters
    and shows the text when the input is empty
    """
    if input.text() != "":
        label.hide()
    else:
        label.show()

def clear_table(table: QTableWidget):
    """
    Clear the table contents
    """
    # Clear the table and set the row count to 0
    table.clearContents()
    table.setRowCount(0)

def copy_table(table: QTableWidget, label: QLabel):
    """
    Copy table contents to a clipboard
    """
    clipboard = QClipboard()
    contents = ""
    # Iterate over the rows and columns to get the info
    for row in range(table.rowCount()):
        row_data = []
        for col in range(4):
            item = table.item(row,col)
            row_data.append(item.text() if item else "")
        # Format and add the info to a string variable
        contents += "  ".join(row_data) + "\n"
    # Store the info in clipboard
    clipboard.setText(contents.strip())
    if contents != "":
        label.show()
    
    
            