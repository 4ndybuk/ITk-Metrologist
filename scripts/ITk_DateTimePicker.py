from PySide6.QtWidgets import QMainWindow, QDateTimeEdit, QVBoxLayout, QWidget, QLabel, QPushButton, QApplication
from PySide6.QtCore import QDateTime, Qt, QDate, QTime
import sys
import datetime as dt

class DateTimePicker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Measurement Date")

        self.text = QLabel()
        self.text.setText("Set date and time of the measurement")

        self.date_time_picker = QDateTimeEdit()
        self.date_time_picker.setDateTime(QDateTime.currentDateTime())
        self.date_time_picker.setCalendarPopup(True)
        self.date_time_picker.dateTimeChanged.connect(self.date_time_changed)

        self.ok_button = QPushButton("Okay")
        self.ok_button.clicked.connect(self.date_time_changed)

        layout =  QVBoxLayout()
        layout.addWidget(self.text)
        layout.addWidget(self.date_time_picker)
        layout.addWidget(self.ok_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def date_time_changed(self,datetime:QDateTime):
        timeformat = datetime.toString(Qt.ISODate)
        parsed_time = dt.datetime.strptime(timeformat, "%Y-%m-%dT%H:%M:%S")

        today = dt.datetime.today().strftime('%d/%m/%Y')
        mydate = dt.datetime.strptime(today, '%d/%m/%Y')
        datetimeobject = dt.datetime.combine(mydate,dt.datetime.now(dt.timezone.utc).time())
        print(datetimeobject)

        return parsed_time.isoformat(timespec='milliseconds')

def main():
    app = QApplication(sys.argv)
    window = DateTimePicker()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()