# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainGUI.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFocusEvent,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeyEvent, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton, QSizePolicy, QStackedWidget, QStatusBar,
    QTabWidget, QTextEdit, QWidget, QTableWidget,QHeaderView)

from ITk_OpacityWidget import OpacityEffect

# Stylesheet for the interface buttons
buttonstyle = """
        QPushButton {
                background-color: white;
                border: 1px solid #c0c0c0;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 13px;
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
                """

# Stylesheet for the interface text displays
lineedit_style = """
                QLineEdit {
                    background-color: rgba(255, 255, 255, 0.8);
                    border-radius: 15px;
                    border: 1px solid #c0c0c0;
                }
                QMenu {
                    background-color: #F0F0F0;   
                    border: 1px solid #C0C0C0;   
                    border-radius: 6px;
                    padding: 3px;         
                }
                QMenu::item {
                    background-color: transparent; 
                }
                QMenu::item:selected { 
                    background-color: #bfd0e0;    
                    color: white;                
                    border-radius: 4px;
                }
                QMenu::separator {
                    height: 1px;                  
                    background: #F0F0F0;          
                    margin-left: 10px;
                    margin-right: 10px;
                }
                QMenu::indicator {
                    width: 16px;                  
                    height: 16px;
                }
                QMenu::indicator:checked {
                    background-color: #bfd0e0;    
                }
                QMenu::item:disabled {
                    color: #A0A0A0;                
                }
                """

# Creating a bold font for universal use
bold_font = QFont()
bold_font.setBold(True)

class FocusTab(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.scan_input = QLineEdit(self)
        self.scan_input.setObjectName(u"scan_input")
        self.scan_input.setFont(bold_font)
        self.scan_input.setGeometry(QRect(200, 97, 261, 31))
        self.scan_input.setStyleSheet(lineedit_style)
        self.scan_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def focusInEvent(self, event: QFocusEvent):
        self.scan_input.setFocus()
        return QWidget.focusInEvent(self,event)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(702, 520)
        MainWindow.setMinimumSize(QSize(702, 520))
        MainWindow.setMaximumSize(QSize(702, 520))
        MainWindow.setBaseSize(QSize(591, 0))
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"background-image: url('assets/NewATLAS.jpg');\n"
                                "background-repeat: no-repeat;\n"
                                "background-position: center;\n"
                                "")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(20, 20, 661, 421))
        self.stackedWidget.setTabletTracking(False)
        self.stackedWidget.setToolTipDuration(1)
        self.stackedWidget.setStyleSheet(u"background: none;\n"
                                        "background-color: rgba(255, 255, 255, 0.4);\n"
                                        "border-radius: 20px;\n"
                                        "")
        self.stackedWidget.setFrameShadow(QFrame.Shadow.Raised)

        # Page 1 Setup #############################################################
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.appTitle = QLabel(self.page_1)
        self.appTitle.setObjectName(u"appTitle")
        self.appTitle.setGeometry(QRect(40, 30, 581, 91))
        font1 = QFont()
        font1.setFamilies([u"Open Sans"])
        font1.setPointSize(42)
        font1.setBold(True)
        self.appTitle.setFont(font1)
        self.appTitle.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.0);\n"
                                   "color: black")
        self.acc1input = QLineEdit(self.page_1)
        self.acc1input.setObjectName(u"acc1input")
        self.acc1input.setGeometry(QRect(220, 150, 231, 31))
        self.acc1input.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                    "border-radius: 15px;\n"
                                    "border: 1px solid #c0c0c0")
        self.acc1input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.access1label = QLabel(self.page_1)
        self.access1label.setObjectName(u"access1label")
        self.access1label.setGeometry(QRect(270, 120, 131, 21))
        self.access1label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.0)")
        self.access2label = QLabel(self.page_1)
        self.access2label.setObjectName(u"access2label")
        self.access2label.setGeometry(QRect(270, 220, 131, 31))
        self.access2label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.0)")
        self.loginButton = QPushButton(self.page_1)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setGeometry(QRect(280, 310, 111, 31))
        self.loginButton.setStyleSheet(buttonstyle)
        self.loginButton.setCheckable(True)
        self.loginButton.setChecked(False)
        self.loginButton.setAutoDefault(False)
        self.loginButton.setFlat(False)
        self.quitButton = QPushButton(self.page_1)
        self.quitButton.setObjectName(u"quitButton")
        self.quitButton.setGeometry(QRect(280, 350, 111, 31))
        self.quitButton.setStyleSheet(buttonstyle)
        self.quitButton.setAutoDefault(True)
        self.acc2input = QLineEdit(self.page_1)
        self.acc2input.setObjectName(u"acc2input")
        self.acc2input.setGeometry(QRect(220, 250, 231, 31))
        self.acc2input.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                    "border-radius: 15px;\n"
                                    "border: 1px solid #c0c0c0")
        self.acc2input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.acc2input.setClearButtonEnabled(False)
        self.stackedWidget.addWidget(self.page_1)

        # Page 2A Setup ###############################################################
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.tabWidget = QTabWidget(self.page_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 10, 661, 431))
        self.tabWidget.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.0)")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.metrologyTab = QWidget()
        self.metrologyTab.setObjectName(u"metrologyTab")
        self.importButton = QPushButton(self.metrologyTab)
        self.importButton.setObjectName(u"importButton")
        self.importButton.setGeometry(QRect(270, 110, 121, 30))
        self.importButton.setStyleSheet(buttonstyle)
        self.descriptLabel = QLabel(self.metrologyTab)
        self.descriptLabel.setObjectName(u"descriptLabel")
        self.descriptLabel.setGeometry(QRect(20, 20, 621, 81))
        self.descriptLabel.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                        "border-radius: 15px;\n"
                                        "border: 1px solid #c0c0c0")
        self.dat_text = QLineEdit(self.metrologyTab)
        self.dat_text.setObjectName(u"dat_text")
        self.dat_text.setGeometry(QRect(194, 160, 271, 31))
        self.dat_text.setStyleSheet(lineedit_style)
        self.dat_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dat_text.setReadOnly(True)
        self.sta_text = QLineEdit(self.metrologyTab)
        self.sta_text.setObjectName(u"sta_text")
        self.sta_text.setGeometry(QRect(194, 230, 271, 31))
        self.sta_text.setStyleSheet(lineedit_style)
        self.sta_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sta_text.setReadOnly(True)
        self.measureButton = QPushButton(self.metrologyTab)
        self.measureButton.setObjectName(u"measureButton")
        self.measureButton.setGeometry(QRect(270, 290, 121, 30))
        self.measureButton.setStyleSheet(buttonstyle)
        self.layoutWidget = QWidget(self.metrologyTab)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(80, 340, 501, 32))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.logoutButton = QPushButton(self.layoutWidget)
        self.logoutButton.setObjectName(u"logoutButton")
        self.logoutButton.setStyleSheet(buttonstyle)

        self.horizontalLayout.addWidget(self.logoutButton)

        self.plotButton = QPushButton(self.layoutWidget)
        self.plotButton.setObjectName(u"plotButton")
        self.plotButton.setStyleSheet(buttonstyle)

        self.horizontalLayout.addWidget(self.plotButton)

        self.dat_label = QLabel(self.metrologyTab)
        self.dat_label.setObjectName(u"dat_label")
        self.dat_label.setGeometry(QRect(290, 140, 89, 71))
        self.sta_label = QLabel(self.metrologyTab)
        self.sta_label.setObjectName(u"sta_label")
        self.sta_label.setGeometry(QRect(290, 180, 89, 131))
        self.tabWidget.addTab(self.metrologyTab, "")
        self.sta_label.raise_()
        self.dat_label.raise_()
        self.importButton.raise_()
        self.descriptLabel.raise_()
        self.dat_text.raise_()
        self.sta_text.raise_()
        self.measureButton.raise_()
        self.layoutWidget.raise_()

        # Page 2B Setup ###################################################
        self.wirebondTab = QWidget()
        self.wirebondTab.setObjectName(u"wirebondTab")
        self.import_csv_Button = QPushButton(self.wirebondTab)
        self.import_csv_Button.setObjectName(u"import_csv_Button")
        self.import_csv_Button.setGeometry(QRect(270, 110, 121, 30))
        self.import_csv_Button.setStyleSheet(buttonstyle)
        self.descriptLabel_wire = QLabel(self.wirebondTab)
        self.descriptLabel_wire.setObjectName(u"descriptLabel_wire")
        self.descriptLabel_wire.setGeometry(QRect(40, 20, 581, 81))
        self.descriptLabel_wire.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                             "border-radius: 15px;\n"
                                             "border: 1px solid #c0c0c0")
        self.csv_label = QLabel(self.wirebondTab)
        self.csv_label.setObjectName(u"csv_label")
        self.csv_label.setGeometry(QRect(280, 130, 101, 91))
        self.measure_csv_Button = QPushButton(self.wirebondTab)
        self.measure_csv_Button.setObjectName(u"measure_csv_Button")
        self.measure_csv_Button.setGeometry(QRect(270, 210, 121, 30))
        self.measure_csv_Button.setStyleSheet(buttonstyle)
        self.logoutButton_2 = QPushButton(self.wirebondTab)
        self.logoutButton_2.setObjectName(u"logoutButton_2")
        self.logoutButton_2.setGeometry(QRect(210, 260, 238, 30))
        self.logoutButton_2.setStyleSheet(buttonstyle)
        self.csv_text = QLineEdit(self.wirebondTab)
        self.csv_text.setObjectName(u"csv_text")
        self.csv_text.setGeometry(QRect(200, 160, 261, 31))
        self.csv_text.setStyleSheet(lineedit_style)
        self.csv_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.csv_text.setReadOnly(True)
        self.tabWidget.addTab(self.wirebondTab, "")

        # Page 2C Setup ###################################################
        # IREF Tab -----------------------------
        self.IREF_tab = QWidget()
        self.IREF_tab.setObjectName(u"IREF_tab")
        self.descriptLabel_iref = QLabel(self.IREF_tab)
        self.descriptLabel_iref.setObjectName(u"descriptLabel_iref")
        self.descriptLabel_iref.setGeometry(QRect(40, 20, 581, 81))
        self.descriptLabel_iref.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                            "border-radius: 15px;\n"
                                            "border: 1px solid #c0c0c0")
        self.serial_input = QLineEdit(self.IREF_tab)
        self.serial_input.setFont(bold_font)
        self.serial_input.setObjectName(u"serial_input")
        self.serial_input.setGeometry(QRect(200, 120, 261, 31))
        self.serial_input.setStyleSheet(lineedit_style)
        self.serial_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serial_label = QLabel(self.IREF_tab)
        self.serial_label.setObjectName(u"serial_label")
        self.serial_label.setGeometry(QRect(280, 90, 101, 91))
        self.iref1_output = QLineEdit(self.IREF_tab)
        self.iref1_output.setFont(bold_font)
        self.iref1_output.setObjectName(u"iref1_output")
        self.iref1_output.setGeometry(QRect(200, 160, 261, 31))
        self.iref1_output.setStyleSheet(lineedit_style)
        self.iref1_output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.iref1_output.setReadOnly(True)
        self.iref2_output = QLineEdit(self.IREF_tab)
        self.iref2_output.setFont(bold_font)
        self.iref2_output.setObjectName(u"iref2_output")
        self.iref2_output.setGeometry(QRect(200, 200, 261, 31))
        self.iref2_output.setStyleSheet(lineedit_style)
        self.iref2_output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.iref2_output.setReadOnly(True)
        self.iref3_output = QLineEdit(self.IREF_tab)
        self.iref3_output.setObjectName(u"iref3_output")
        self.iref3_output.setFont(bold_font)
        self.iref3_output.setGeometry(QRect(200, 240, 261, 31))
        self.iref3_output.setStyleSheet(lineedit_style)
        self.iref3_output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.iref3_output.setReadOnly(True)
        self.iref4_output = QLineEdit(self.IREF_tab)
        self.iref4_output.setFont(bold_font)
        self.iref4_output.setObjectName(u"iref4_output")
        self.iref4_output.setGeometry(QRect(200, 280, 261, 31))
        self.iref4_output.setStyleSheet(lineedit_style)
        self.iref4_output.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.iref4_output.setReadOnly(True)
        self.copy_Button = QPushButton(self.IREF_tab)
        self.copy_Button.setObjectName(u"copy_Button")
        self.copy_Button.setGeometry(QRect(340, 320, 121, 30))
        self.copy_Button.setStyleSheet(buttonstyle)
        self.iref1_label = QLineEdit(self.IREF_tab)
        self.iref1_label.setObjectName(u"iref1_label")
        self.iref1_label.setFont(bold_font)
        self.iref1_label.setGeometry(QRect(200, 160, 121, 31))
        self.iref1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iref1_label.setReadOnly(True)
        self.iref1_label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                        "border-radius: 15px;\n"
                                        "border: 1px solid #c0c0c0")
        self.iref2_label = QLineEdit(self.IREF_tab)
        self.iref2_label.setObjectName(u"iref2_label")
        self.iref2_label.setFont(bold_font)
        self.iref2_label.setGeometry(QRect(200, 200, 121, 31))
        self.iref2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iref2_label.setReadOnly(True)
        self.iref2_label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                        "border-radius: 15px;\n"
                                        "border: 1px solid #c0c0c0")
        self.iref3_label = QLineEdit(self.IREF_tab)
        self.iref3_label.setObjectName(u"iref3_label")
        self.iref3_label.setFont(bold_font)
        self.iref3_label.setGeometry(QRect(200, 240, 121, 31))
        self.iref3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iref3_label.setReadOnly(True)
        self.iref3_label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                        "border-radius: 15px;\n"
                                        "border: 1px solid #c0c0c0")
        self.iref4_label = QLineEdit(self.IREF_tab)
        self.iref4_label.setObjectName(u"iref4_label")
        self.iref4_label.setFont(bold_font)
        self.iref4_label.setGeometry(QRect(200, 280, 121, 31))
        self.iref4_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.iref4_label.setReadOnly(True)
        self.iref4_label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                        "border-radius: 15px;\n"
                                        "border: 1px solid #c0c0c0")
        self.valuescopied_Label = OpacityEffect(self.IREF_tab)
        self.valuescopied_Label.setObjectName(u"valuescopied_Label")
        self.valuescopied_Label.setGeometry(QRect(250, 360, 161, 21))
        self.valuescopied_Label.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                               "border-radius: 10px;")
        self.valuescopied_Label.hide()
        self.chip_Button = QPushButton(self.IREF_tab)
        self.chip_Button.setObjectName(u"chip_Button")
        self.chip_Button.setGeometry(QRect(200, 320, 121, 30))
        self.chip_Button.setStyleSheet(buttonstyle)
        self.tabWidget.addTab(self.IREF_tab, "")
        self.serial_label.raise_()
        self.descriptLabel_iref.raise_()
        self.serial_input.raise_()
        self.iref1_output.raise_()
        self.iref2_output.raise_()
        self.iref3_output.raise_()
        self.iref4_output.raise_()
        self.copy_Button.raise_()
        self.iref1_label.raise_()
        self.iref2_label.raise_()
        self.iref3_label.raise_()
        self.iref4_label.raise_()
        self.valuescopied_Label.raise_()
        self.chip_Button.raise_()
        # Scan Component Tab ---------------------------------------
        self.scanTab = FocusTab()
        self.scanTab.setObjectName(u"scanTab")
        self.descriptLabel_scan = QLabel(self.scanTab)
        self.descriptLabel_scan.setObjectName(u"descriptLabel_scan")
        self.descriptLabel_scan.setGeometry(QRect(40, 10, 581, 81))
        self.descriptLabel_scan.setStyleSheet(u"background-color: rgba(255, 255, 255, 0.8);\n"
                                                "border-radius: 15px;\n"
                                                "border: 1px solid #c0c0c0")
        self.scan_label = QLabel(self.scanTab)
        self.scan_label.setObjectName(u"scan_label")
        self.scan_label.setGeometry(QRect(280, 66, 101, 91))
        self.tableWidget = QTableWidget(self.scanTab)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(20, 136, 621, 244))
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setStyleSheet("""
                QTableWidget {
                    background-color: rgba(255, 255, 255, 0.8);
                    border-radius: 14px;
                    border: 1px solid #c0c0c0;
                    padding: 5px;
                }
                QScrollBar:vertical {
                    background: transparent;
                    width: 8px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: rgba(0, 0, 0, 0.5);
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical:hover {
                    background: rgba(0, 0, 0, 0.8);
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
                QMenu {
                    background-color: #F0F0F0;   
                    border: 1px solid #C0C0C0;   
                    border-radius: 6px;
                    padding: 3px;        
                }
                QMenu::item {
                    background-color: transparent; 
                }
                QMenu::item:selected { 
                    background-color: #bfd0e0;    
                    color: white;                
                    border-radius: 4px;
                }
                QMenu::separator {
                    height: 1px;                  
                    background: #F0F0F0;          
                    margin-left: 10px;
                    margin-right: 10px;
                }
                QMenu::indicator {
                    width: 16px;                  
                    height: 16px;
                }
                QMenu::indicator:checked {
                    background-color: #bfd0e0;    
                }
                QMenu::item:disabled {
                    color: #A0A0A0;                
                }
                """)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Serial ID","Type","Location","Stage","PDB Link"])
        self.tableWidget.horizontalHeader().resizeSection(0,136)
        self.tableWidget.horizontalHeader().resizeSection(1,110)
        self.tableWidget.horizontalHeader().resizeSection(2,76)
        self.tableWidget.horizontalHeader().resizeSection(3,122)
        self.tableWidget.horizontalHeader().resizeSection(4,132)
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.clear_button = QPushButton(self.scanTab)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setGeometry(QRect(60, 100, 121, 30))
        self.clear_button.setStyleSheet(buttonstyle)
        self.copytable_button = QPushButton(self.scanTab)
        self.copytable_button.setObjectName(u"copytable_button")
        self.copytable_button.setGeometry(QRect(480, 100, 121, 30))
        self.copytable_button.setStyleSheet(buttonstyle)
        self.tablecopied_Label = OpacityEffect(self.scanTab)
        self.tablecopied_Label.setObjectName(u"tablecopied_Label")
        self.tablecopied_Label.setGeometry(QRect(250, 350, 161, 21))
        self.tablecopied_Label.setStyleSheet(u"background-color: rgba(255, 255, 255, 1.0);\n"
                                               "border-radius: 10px;")
        self.tablecopied_Label.hide()
        self.valuescopied_Label.hide()
        self.tabWidget.addTab(self.scanTab, "")
        self.scan_label.raise_()
        self.descriptLabel_scan.raise_()
        self.scanTab.scan_input.raise_()
        self.clear_button.raise_()
        self.copytable_button.raise_()
        self.tablecopied_Label.raise_()
        self.stackedWidget.addWidget(self.page_2)

        # Page 3 Setup ###################################################
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.textLog = QTextEdit(self.page_3)
        self.textLog.setObjectName(u"textLog")
        self.textLog.setGeometry(QRect(13, 10, 631, 361))
        self.textLog.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #c0c0c0;
                border-radius: 10px;
                padding: 5px;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 0, 0, 0.5);
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 0, 0, 0.8);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QMenu {
                background-color: #F0F0F0;   
                border: 1px solid #C0C0C0;   
                border-radius: 6px;
                padding: 3px;        
            }
            QMenu::item {
                background-color: transparent; 
            }
            QMenu::item:selected { 
                background-color: #bfd0e0;    
                color: white;                
                border-radius: 4px;
            }
            QMenu::separator {
                height: 1px;                  
                background: #F0F0F0;          
                margin-left: 10px;
                margin-right: 10px;
            }
            QMenu::indicator {
                width: 16px;                  
                height: 16px;
            }
            QMenu::indicator:checked {
                background-color: #bfd0e0;    
            }
            QMenu::item:disabled {
                color: #A0A0A0;                
            }
        """)
        self.gobackButton = QPushButton(self.page_3)
        self.gobackButton.setObjectName(u"gobackButton")
        self.gobackButton.setGeometry(QRect(21, 376, 201, 30))
        self.gobackButton.setStyleSheet(buttonstyle)
        self.itkButton = QPushButton(self.page_3)
        self.itkButton.setObjectName(u"itkButton")
        self.itkButton.setGeometry(QRect(232, 376, 201, 30))
        self.itkButton.setStyleSheet(buttonstyle)
        self.sheetButton = QPushButton(self.page_3)
        self.sheetButton.setObjectName(u"sheetButton")
        self.sheetButton.setGeometry(QRect(443, 376, 191, 30))
        self.sheetButton.setStyleSheet(buttonstyle)
        self.stackedWidget.addWidget(self.page_3)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(33, 444, 637, 14))
        self.progressBar.setStyleSheet("""
                                        QProgressBar {
                                                border: 1px solid #c0c0c0;
                                                border-radius: 5px;
                                                background-color: #87fa9a;
                                                margin: 0px;
                                        }
                                        QProgressBar::chunk {
                                                background-color: #87fa9a;
                                                border-radius: 4px;
                                                margin: 0px;
                                        }
                                        """)
        self.progressBar.setValue(24)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"background: none")
        self.statusbar.setSizeGripEnabled(True)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"ITk Metrologist - Pixel Data Analysis", None))
        self.appTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:48pt;\">ITk METROLOGIST</span></p></body></html>", None))
        self.acc1input.setInputMask("")
        self.acc1input.setText("")
        self.access1label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:18pt; font-weight:700;\">Access Code 1:</span></p></body></html>", None))
        self.access2label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:18pt; font-weight:700;\">Access Code 2:</span></p></body></html>", None))
        self.loginButton.setText(QCoreApplication.translate("MainWindow", u"Log In", None))
        self.quitButton.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.acc2input.setText("")
        self.importButton.setText(QCoreApplication.translate("MainWindow", u"Import Files", None))
        self.descriptLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700; font-style:italic;\">Componet Metrology</span></p><p align=\"center\">\u2022 Choose your .DAT and .STA file to obtain metrology measurements </p><p align=\"center\">\u2022 Designed for <span style=\" font-weight:700;\">Hybrid Flex</span>, <span style=\" font-weight:700;\">Bare Module</span> and <span style=\" font-weight:700;\">Assembled Module</span> components</p><p><br/></p><p><br/></p></body></html>", None))
        self.dat_text.setText("")
        self.measureButton.setText(QCoreApplication.translate("MainWindow", u"Measure", None))
        self.logoutButton.setText(QCoreApplication.translate("MainWindow", u"Log Out", None))
        self.plotButton.setText(QCoreApplication.translate("MainWindow", u"Plot Graphs", None))
        self.dat_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">.DAT File:</span></p></body></html>", None))
        self.sta_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">.STA File:</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.metrologyTab), QCoreApplication.translate("MainWindow", u"Metrology", None))
        self.import_csv_Button.setText(QCoreApplication.translate("MainWindow", u"Import File", None))
        self.descriptLabel_wire.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700; font-style:italic;\">Pull Test Upload</span></p><p align=\"center\">\u2022 Choose your <span style=\" font-weight:700;\">.CSV</span> file to obtain pull test information</p><p align=\"center\">\u2022 Additional: Outputs a processed .CSV file in the same directory</p><p><br/></p><p><br/></p></body></html>", None))
        self.csv_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">.CSV File:</span></p></body></html>", None))
        self.measure_csv_Button.setText(QCoreApplication.translate("MainWindow", u"Measure", None))
        self.logoutButton_2.setText(QCoreApplication.translate("MainWindow", u"Log Out", None))
        self.csv_text.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.wirebondTab), QCoreApplication.translate("MainWindow", u"Wirebonding", None))
        self.descriptLabel_iref.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700; font-style:italic;\">IREF Trim Bit Values</span></p><p align=\"center\">\u2022 Type in the Bare Module serial ID, press <span style=\" font-weight:700;\">Enter</span> and retrieve the IREF trim bit values</p><p align=\"center\">\u2022 Press <span style=\" font-weight:700;\">Copy </span>to copy values to clipboard <span style=\" font-weight:700;\">| </span>Press <span style=\" font-weight:700;\">Chip Display </span>to display FE chip orientation</p><p><br/></p><p><br/></p></body></html>", None))
        self.serial_input.setText("")
        self.serial_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Serial ID</span></p></body></html>", None))
        self.iref1_output.setText("")
        self.iref2_output.setText("")
        self.iref3_output.setText("")
        self.iref4_output.setText("")
        self.copy_Button.setText(QCoreApplication.translate("MainWindow", u"Copy", None))
        self.iref1_label.setText("IREF bit 1")
        self.iref2_label.setText("IREF bit 2")
        self.iref3_label.setText("IREF bit 3")
        self.iref4_label.setText("IREF bit 4")
        self.valuescopied_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">IREF Values Copied</p></body></html>", None))
        self.chip_Button.setText(QCoreApplication.translate("MainWindow", u"Chip Display", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.IREF_tab), QCoreApplication.translate("MainWindow", u"IREF Fetcher", None))
        self.descriptLabel_scan.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700; font-style:italic;\">Scan Components</span></p><p align=\"center\">\u2022 Connect your barcode scanner via Bluetooth and scan the component's <span style=\" font-weight:700;\">QR code</span></p><p align=\"center\">\u2022 Organise your components in a list with <span style=\" font-weight:700;\">Open Page</span> links to the database</p><p><br/></p><p><br/></p></body></html>", None))
        self.scanTab.scan_input.setText("")
        self.scan_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Serial ID</span></p></body></html>", None))
        self.clear_button.setText(QCoreApplication.translate("MainWindow", u"Clear Table", None))
        self.copytable_button.setText(QCoreApplication.translate("MainWindow", u"Copy Contents", None))
        self.tablecopied_Label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Table Contents Copied</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.scanTab), QCoreApplication.translate("MainWindow", u"Scan Components", None))
        self.gobackButton.setText(QCoreApplication.translate("MainWindow", u"Go Back", None))
        self.itkButton.setText(QCoreApplication.translate("MainWindow", u"ITk Upload", None))
        self.sheetButton.setText(QCoreApplication.translate("MainWindow", u"Sheets Upload", None))
    # retranslateUi

