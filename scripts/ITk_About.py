from PySide6.QtWidgets import (QDialog,QLabel,QWidget,QSizePolicy,
                               QHBoxLayout,QVBoxLayout,QPushButton,
                               QApplication)
from PySide6.QtCore import Qt
import sys

infotext = """
<p style="text-align: center; font-size: 22px;">
<b>ITk METROLOGIST</b><br>v2.0
</p>
<p style="text-align: center;"> <i>Author: Andy Bukowski</i> <br>
<i>University of Liverpool</i></p>


<p style="text-align: left;"> <b>Purpose</b><br>This program has been designed to automate the pixel metrology analysis and its<br>subsequent
upload to the production database. It ensures swift processing, provides<br>advanced analytics through
data visualisation tools and spreadsheets for personal component<br>organisation. The 
program also allows data processing for wirebonding pull tests<br>and their upload to the database.<br><br>
<b>What do I need?</b><br>
Make sure you have your .DAT, .STA, and .CSV files ready and that each file is not missing<br>any data
points. The program is <b>data-order sensitive</b> and any discrepancies will not allow<br>you to
make database uploads. Ensure that the order is correct and no lines are missing. Best<br>practice is to compare
other files and see if they have a matching data order.<br><br>

<b>For .CSV files:</b> Make sure that the Object ID has a full serial number and not just a section.<br>
The component ID gets send to the production database for recongintion hence full length <br>is required.<br><br><br>

<i>Powered by</i><br>
<i>Plotly v2.32.0 - Graphical Analytics<br>
Qt Framework PySide6 v6.7.2 - Graphical User Interface<br>
itkdb v0.6.8 - Production Database<br><br>
Icons - www.flaticon.com<br>
gear icon made by Pixel perfect<br>
webApp icon made by zafdesign<br>
information and gsheets icons made by Freepik<br>
database icon made by Stockio</i>
"""

class CustomInfoWindow(QDialog):
    """
    Pop-up window for the program information (About) with an HTML coded text above and a close button
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About ITk Metrologist")
        self.setFixedSize(600,656)

        # Main information text widget
        text = QLabel()
        text.setText(infotext)
        text.setAlignment(Qt.AlignTop)

        # Defining the close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Defining the window layout
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_layout = QHBoxLayout()
        button_layout.addWidget(spacer)
        button_layout.addWidget(close_button)
        button_layout.addWidget(spacer)

        # Applying the layout to the widget
        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addLayout(button_layout)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    widget = CustomInfoWindow()
    widget.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()