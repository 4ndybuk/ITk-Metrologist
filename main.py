#!/usr/bin/env python3

import sys
import os
import webbrowser
import logging
import multiprocessing
import subprocess

# Include the nested folders with modules and assets for importing
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'assets'))

# GUI modules - Qt Framework
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon, QPalette, QColor, QClipboard
# User Interface made with Qt Designer
from ui_mainwindow import Ui_MainWindow

# Personal modules specific for the program's purpose
from ITk_DB_Login import validate_login
from ITk_Importers import *
from ITk_Measurements import *
from ITk_GraphPlotter import graph_plot
from ITk_Logger import *
from ITk_DB_Upload import *
from ITk_Spreadsheet import upload_sh
from ITk_IREF_Fetcher import iref_values
from ITk_About import CustomInfoWindow
from ITk_ChipOrientation import ChipOrientation
from ITk_ScanComponent import *

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp,self).__init__()

        # Create an instance of the Ui_Mainwindow class
        self.ui = Ui_MainWindow()

        # Set up the UI for this window
        self.ui.setupUi(self)

        # Setting empty global variables for each file type and the database client
        self.dat_path = self.sta_path = self.csv_path = ""
        self.iref_trim_bits = self.hex_list = ""
        self.client = None
        self.user = None
        self.bare_id = None

        ##################################################################
        # Page 1 Configurations

        # Hide the progress bar
        self.ui.progressBar.hide()

        # Set Access Codes 1 and 2 to be masked with * markers
        self.ui.acc1input.setEchoMode(QLineEdit.Password)
        self.ui.acc2input.setEchoMode(QLineEdit.Password)

        # Adding widgets to the status bar
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer.setStyleSheet("background: none")
        self.ui.statusbar.addWidget(spacer)
        self.status_user = QLabel()
        self.ui.statusbar.addWidget(self.status_user)

        # Setting up a toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16,16))
        toolbar.setStyleSheet("""
                        QToolBar {
                            background: none
                        }
                        QToolButton {
                            background-color: lightgray;
                            border: 1px lightgray;
                            padding: 5px;
                            background: none;
                            border-radius: 8px
                        }
                        QToolButton:hover {
                            background-color: darkgray;
                        }
                    """)
        toolbar.setAllowedAreas(Qt.TopToolBarArea | Qt.BottomToolBarArea)
        self.addToolBar(toolbar)

        # Adding easy access icons for the database, spreadsheets, webapp and about window
        db_action = QAction(QIcon("assets/icons/database.png"),"ITk Database",self)
        db_action.setStatusTip("Open ITk Database")
        db_action.triggered.connect(self.open_database)
        toolbar.addAction(db_action)

        sheets_action = QAction(QIcon("assets/icons/gsheets.png"),"Google Sheets",self)
        sheets_action.setStatusTip("Open Google Sheets")
        sheets_action.triggered.connect(self.open_sheets)
        toolbar.addAction(sheets_action)

        webapp_action = QAction(QIcon("assets/icons/webApp.png"),"WebApp",self)
        webapp_action.setStatusTip("Open WebApp")
        webapp_action.triggered.connect(self.open_webapp)
        toolbar.addAction(webapp_action)
        toolbar.addSeparator()

        about_action = QAction(QIcon("assets/icons/information.png"),"About",self)
        about_action.setStatusTip("About")
        about_action.triggered.connect(self.open_about)
        toolbar.addAction(about_action)

        mod_action = QAction(QIcon("assets/icons/gear.png"),"Modify",self)
        mod_action.setStatusTip("Modify Passcodes")
        mod_action.triggered.connect(self.open_env)
        toolbar.addAction(mod_action)
        
        # Button signals
        self.ui.loginButton.clicked.connect(self.db_login)
        self.ui.acc2input.returnPressed.connect(self.db_login)
        self.ui.quitButton.clicked.connect(quit)

        ###############################################################
        # Page 2 Configurations

        # Metrology Tab
        self.ui.importButton.clicked.connect(self.import_files)
        self.ui.measureButton.clicked.connect(self.metro_measurements)
        self.ui.logoutButton.clicked.connect(self.logout)
        self.ui.plotButton.clicked.connect(self.plot_graph)

        # Wirebonding Tab
        self.ui.import_csv_Button.clicked.connect(self.import_csv_file)
        self.ui.measure_csv_Button.clicked.connect(self.csv_measurements)
        self.ui.logoutButton_2.clicked.connect(self.logout)

        # IREF Tab
        self.ui.serial_input.textChanged.connect(self.hide_label)
        self.ui.serial_input.returnPressed.connect(self.iref_trim_values)
        self.ui.copy_Button.clicked.connect(self.copy_to_clipboard)
        self.ui.chip_Button.clicked.connect(self.display_chip_orientation)

        # Scan Tab
        self.ui.scanTab.scan_input.textChanged.connect(lambda: hide_scan_label(self.ui.scanTab.scan_input,
                                                                               self.ui.scan_label))
        self.ui.scanTab.scan_input.returnPressed.connect(lambda: table_allocate(self.ui.tableWidget,
                                                                                self.client,
                                                                                self.ui.scanTab.scan_input))
        self.ui.clear_button.clicked.connect(lambda: clear_table(self.ui.tableWidget))
        self.ui.copytable_button.clicked.connect(lambda: copy_table(self.ui.tableWidget,
                                                                    self.ui.tablecopied_Label))

        ###############################################################
        # Page 3 Configurations

        # Basic configuration for logging format by setting time, level name and the text message for display
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO)
        self.text_handler = TextHandler(self.ui.textLog, format="%(asctime)s - %(levelname)s - %(message)s")
        logger = logging.getLogger()
        logger.addHandler(self.text_handler)
        logger.info("\nWelcome to the Metrologist\n")

        self.queue = multiprocessing.Queue()
        self.ui.progressBar.setMaximum(100)

        self.ui.gobackButton.clicked.connect(self.go_back)
        self.ui.itkButton.clicked.connect(lambda: upload_itk(self.component,self.results,self.client,self.csv_path))
        self.ui.sheetButton.clicked.connect(self.upload_sheets)

    def custom_messagebox(self,title,maintext,info_text,icon,button):
        """
        Creating a template messagebox for customisation with dictionaries
        """
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
        messagebox = QMessageBox()
        messagebox.setWindowTitle(title)
        messagebox.setText(maintext)
        messagebox.setInformativeText(info_text)
        messagebox.setIcon(icon)
        messagebox.setStandardButtons(button)
        messagebox.setDefaultButton(QMessageBox.Ok)
        verify = messagebox.exec()
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)

        return verify

    def db_login(self):
        """
        Function which applies an imported def validate_login() from ITk_DB_Login.py
        it sets the passcode entries from Page 1 class and returns Pass/Fail on the login
        attempt
        """

        # Retrieve input passwords from Page 1
        db_passcode1 = self.ui.acc1input.text()
        db_passcode2 = self.ui.acc2input.text()

        valid, client, user = validate_login(db_passcode1,db_passcode2)

        if valid:
            self.user = user
            self.client = client
            dict = {"title":"Welcome",
                    "maintext":"Login Successful",
                    "info":f"Signed User: {self.user["firstName"]} {self.user["lastName"]}",
                    "icon":QMessageBox.Information,
                    "button":QMessageBox.Ok}
            verify = self.custom_messagebox(dict["title"],dict["maintext"],dict["info"],dict["icon"],dict["button"])

            if verify == QMessageBox.Ok:
                # Move to Page 2
                self.ui.stackedWidget.setCurrentIndex(1)
                self.status_user.setText(f"<b>Current User:  {self.user["firstName"]} {self.user["lastName"]}</b>")
                self.ui.scanTab.scan_input.setFocus()
        else:
            dict = {"title":"Error",
                    "maintext":"Login Failed",
                    "info":"Incorrect credentials",
                    "icon":QMessageBox.Critical,
                    "button":QMessageBox.Ok}
            verify = self.custom_messagebox(dict["title"],dict["maintext"],dict["info"],dict["icon"],dict["button"])

            if verify == QMessageBox.Ok:
                self.user = None
                self.client = None
                self.ui.acc1input.setText("")
                self.ui.acc2input.setText("")
                db_passcode1 = ""
                db_passcode2 = ""

    @staticmethod
    def open_webapp():
        webbrowser.open("https://itk-pdb-webapps-pixels.web.cern.ch",new=2)

    @staticmethod
    def open_about():
        dialog = CustomInfoWindow()
        dialog.exec()
    
    @staticmethod
    def open_env():
        file_path = ".env"
        subprocess.run(["open","-a","TextEdit",file_path])
    
    @staticmethod
    def open_sheets():
        webbrowser.open("https://docs.google.com/spreadsheets/d/1O54CRUXG36WApvoALbAuL7MGo8sgtVgdQhKCYmQvUXY/edit?gid=0#gid=0",new=2)

    @staticmethod
    def open_database():
        webbrowser.open("https://itkpd-test.unicorncollege.cz/componentView?code=2c6c1865a91d71e2ee5f21f69c0b9512",new=2)

    def import_files(self):
        try:
            self.dat_path, self.sta_path = import_file(self.ui.dat_text,self.ui.sta_text,
                                                       self.ui.dat_label,self.ui.sta_label)
        except Exception as e:
            print(e)
    
    def import_csv_file(self):
        try:
            self.csv_list, self.csv_basename, self.csv_path = csv_import(self.ui.csv_text,self.ui.csv_label)
        except Exception as e:
            print(e)

    def metro_measurements(self):
        """
        Calls met_measurements() module from ITk_Measurements.py to take metrology measurements
        for each stage in pixel assembly (bare flex -> bare module -> assembled module).
        Returns all results to be assigned in Page 3 database upload
        """

        # Error checking that the file has been actually imported first
        if self.dat_path == "" and self.sta_path == "":
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Error", "No files have been imported\n\nPlease try again",
                                     QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
            return
        else:
            dat_basename = os.path.basename(self.dat_path[0])
            sta_basename = os.path.basename(self.sta_path[0])

            success, results = met_measurements(self.dat_path[0],
                                                self.sta_path[0],
                                                dat_basename,
                                                sta_basename,
                                                self.client)
            if success:
                # Clear pre-loaded csv files
                self.csv_path = ""
                
                # Metrology results
                self.results = results
                
                # Component information
                self.component_id = results["component_id"]
                self.component = results["component"]

                # Direct to the next page after obtaining measurements
                self.ui.stackedWidget.setCurrentIndex(2)
            else:
                # If the serial numbers do not match print and display the error
                print("The files are not matching, please choose the corresponding file")
                QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
                QMessageBox.critical(None,"Error", "Files not matching the same component ID\n\nPlease try again",
                                     QMessageBox.Ok)
                QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
    
    def csv_measurements(self):
        """
        Calls csv_measurements() module from ITk_Measurements.py to take pulltest  measurements
        for the assembled module stage.
        Returns all results to be assigned in Page 3 database for upload
        """

        # Error checking that the file has been actually imported first
        if self.csv_path == "":
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Error", "No files have been imported\n\nPlease try again",
                                     QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
            return
        else:
            results = csv_measurements(self.csv_list,self.csv_basename[0],self.client)
            self.results = results
            self.component_id = results["component_id"]
            self.component = results["component"]
            self.ui.sheetButton.setEnabled(False)
            self.ui.stackedWidget.setCurrentIndex(2)
    
    def logout(self):
        """
        Function which logs out the current user by clearing the database client,
        emptying the passcodes and returning to starting Page 1.
        """

        # Clear the global client
        self.client = None

        # Clear the logger and files
        clear_logger(self.text_handler)

        logging.info("You have been logged out. To come back please log in again")
        dict = {"title":"Logged Out",
                "maintext":"You have been logged out",
                "info":"Going back to the main page",
                "icon":QMessageBox.Information,
                "button":QMessageBox.Ok}
        verify = self.custom_messagebox(dict["title"],dict["maintext"],dict["info"],dict["icon"],dict["button"])

        if verify == QMessageBox.Ok:
            # Move to Page 1
            self.ui.acc1input.clear()
            self.ui.acc2input.clear()
            self.clear_text_met()
            self.clear_text_csv()
            self.clear_text_iref()
            clear_table(self.ui.tableWidget)
            self.dat_path = self.sta_path = self.csv_path = ""
            self.ui.stackedWidget.setCurrentIndex(0)
    
    def clear_text_met(self):
        self.ui.dat_text.clear()
        self.ui.sta_text.clear()
        self.ui.dat_label.show()
        self.ui.sta_label.show()
    
    def clear_text_csv(self):
        self.ui.csv_text.clear()
        self.ui.csv_label.show()
    
    def clear_text_iref(self):
        self.iref_trim_bits = self.hex_list = ""
        self.ui.serial_input.clear()
        self.ui.iref1_output.clear()
        self.ui.iref2_output.clear()
        self.ui.iref3_output.clear()
        self.ui.iref4_output.clear()
    
    def plot_graph(self):
        if self.dat_path == "":
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Error", "No .DAT file for plotting\n\nPlease try again",
                             QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
        else:
            graph_plot(self.dat_path[0])
    
    def go_back(self):
        """
        Go back to the previous frame depending on what file type has been imported
        Additionaly, clears all file text entries and pathways. 
        """

        clear_logger(self.text_handler)
        self.ui.sheetButton.setEnabled(True)

        if self.dat_path != "" and self.sta_path != "" and self.csv_path == "":
            # Set files paths to empty
            self.dat_path = self.sta_path = ""
            self.clear_text_met()
            self.clear_text_iref()
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.tabWidget.setCurrentIndex(0)
            
        elif self.dat_path == "" and self.sta_path == "" and self.csv_path != "":
            self.csv_path = ""
            self.clear_text_csv()
            self.clear_text_iref()
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.tabWidget.setCurrentIndex(1)
        
        else: 
            self.dat_path = self.sta_path = self.csv_path = ""
            self.clear_text_csv()
            self.clear_text_met()
            self.clear_text_iref()
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.tabWidget.setCurrentIndex(0)
    
    def upload_sheets(self):
        """
        Start the upload process using threading method to retrieve incriments for the progressbar
        """

        process = multiprocessing.Process(target=upload_sh, args=(self.results,
                                                                  self.queue))
        process.start()
        self.check_queue(self.queue)
    
    def check_queue(self,queue):

        """
        Check the queue for progress updates and update the progress bar
        """

        try:
            progress = queue.get_nowait()
            self.ui.progressBar.show()
            self.ui.progressBar.setTextVisible(False)
            self.ui.progressBar.setRange(0,100)
            self.ui.progressBar.setValue(progress)
            if progress < 100:
                # Scheduling the next queue check
                QTimer.singleShot(100, lambda: self.check_queue(queue))
            elif progress == 100:
                self.ui.progressBar.setValue(0)
                self.ui.progressBar.hide()
        except multiprocessing.queues.Empty:
            QTimer.singleShot(100, lambda: self.check_queue(queue))
    
    def hide_label(self):
        """
        Hides the text behind the input when typing in characters
        and shows the text when the input is empty
        """
        if self.ui.serial_input.text() != "":
            self.ui.serial_label.hide()
        else:
            self.ui.serial_label.show()
            self.ui.iref1_output.clear()
            self.ui.iref2_output.clear()
            self.ui.iref3_output.clear()
            self.ui.iref4_output.clear()
            # Additionally clears the saved parameters
            self.iref_trim_bits = ""
            self.hex_list = ""
    
    def iref_trim_values(self):
        """
        Obtains IREF trim bits and hexadecimal identificators for each FE chip
        """
        hex_list, iref_trim_bits, bare_id = iref_values(self.client,self.ui.serial_input.text())
        self.hex_list = hex_list
        self.iref_trim_bits = iref_trim_bits
        self.bare_id = bare_id

        # Allocating each trim bit value to the GUI rows
        self.ui.iref1_output.setText(f"{self.iref_trim_bits[0]}  ")
        self.ui.iref2_output.setText(f"{self.iref_trim_bits[1]}  ")
        self.ui.iref3_output.setText(f"{self.iref_trim_bits[2]}  ")
        self.ui.iref4_output.setText(f"{self.iref_trim_bits[3]}  ")

        if self.ui.serial_input.text() == "":
            self.ui.iref1_output.clear()
            self.ui.iref2_output.clear()
            self.ui.iref3_output.clear()
            self.ui.iref4_output.clear()

    def copy_to_clipboard(self):
        """
        Copies the output list to the clipbaord
        """
        if self.ui.serial_input.text() == "" or self.iref_trim_bits == "" or self.bare_id == None:
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Info", "Please type in the serial ID and press Enter",
                             QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
        else:
            clipboard = QClipboard()
            try:
                clipboard.setText(", ".join(map(str,self.iref_trim_bits)))
                self.ui.valuescopied_Label.show()
            except Exception as e:
                print(e)
    
    def display_chip_orientation(self):
        if self.hex_list != "" and self.iref_trim_bits != "":
            chip_orientation = ChipOrientation(self.bare_id,self.hex_list)
            chip_orientation.exec()
        elif self.bare_id == None or self.ui.serial_input.text() == "" or self.hex_list == "":
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Info", "Please type in the serial ID and press Enter",
                             QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)

def main():
    app = QApplication(sys.argv)

    # Setting custom app palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255,255,255))
    palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    app.setPalette(palette)

    window = MyApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()