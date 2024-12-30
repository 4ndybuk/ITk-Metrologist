from PySide6.QtWidgets import (QDialog,QWidget,QSizePolicy,QHBoxLayout,
                               QVBoxLayout,QPushButton,
                               QApplication)
from PySide6.QtGui import (QColor, QBrush, QPen,QFont,QPainter)
from PySide6.QtCore import Qt,QRectF

class ChipOrientation(QDialog):
    """
    Display window for the paintEvent
    """
    def __init__(self,serial_number: str,hex_list: list):
        super().__init__()
        self.serial_number = serial_number
        self.hex_list = hex_list
        self.setWindowTitle(f"{serial_number} - Front-End Chip Orientation")
        self.resize(500,500)

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
        layout.addStretch(1)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def paintEvent(self,event):
        """
        Drawing the FE chip orientation for display in QDialog
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QPen(Qt.black,2))
        painter.setBrush(QBrush(QColor(212, 231, 250)))

        # Add the chip rectangles
        painter.drawRect(85,84,160,160)
        painter.drawRect(255,84,160,160)
        painter.drawRect(85,254,160,160)
        painter.drawRect(255,254,160,160)
        # Add GAx notations to each rectangle
            # Draw the circles
        painter.drawEllipse(139,104,50,50)
        painter.drawEllipse(310,104,50,50)
        painter.drawEllipse(139,334,50,50)
        painter.drawEllipse(310,334,50,50)
            # Insert the text
        painter.drawText(QRectF(139,104,50,50),Qt.AlignCenter,"GA1")
        painter.drawText(QRectF(310,104,50,50),Qt.AlignCenter,"GA4")
        painter.drawText(QRectF(139,334,50,50),Qt.AlignCenter,"GA2")
        painter.drawText(QRectF(310,334,50,50),Qt.AlignCenter,"GA3")
            # Assign FE hexadecimal values per chip
        font = QFont(".AppleSystemUIFont",25)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(QRectF(139,169,50,50),Qt.AlignCenter,self.hex_list[0])
        painter.drawText(QRectF(310,169,50,50),Qt.AlignCenter,self.hex_list[3])
        painter.drawText(QRectF(139,274,50,50),Qt.AlignCenter,self.hex_list[1])
        painter.drawText(QRectF(310,274,50,50),Qt.AlignCenter,self.hex_list[2])
            # Set a title at the top
        title_font = QFont(".AppleSystemUIFont",19)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(QRectF(102,10,300,60),Qt.AlignCenter,self.serial_number)