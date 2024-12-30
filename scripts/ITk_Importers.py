import logging
import os
import csv

from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication, QLineEdit, QLabel
from PySide6.QtCore import Qt

def import_file(dat_text: QLineEdit,sta_text: QLineEdit,dat_label: QLabel,sta_label: QLabel):

    global dat_path,sta_path

    dat_path = sta_path = ""

    """
    import_file(Your .DAT and .STA files) - a simple fucntion that imports your .DAT and .STA files respectively.
    Opens two consecutive open-file windows, safety checks the files for the right format and
    displays them on Page 2 in the desiganted text-widget for the user to see.

    """

    # Defining a file path for importing .DAT files and error checking if the file path is not in the wrong format
    choose_dat = QFileDialog.getOpenFileName(None, "Select a .DAT file", "", "DAT files (*.dat);;All files (*.*)")
    if choose_dat != ("", ""):
        dat_path = choose_dat
        if os.path.splitext(dat_path[0])[1] != ".DAT" and dat_path[1] != "":
            dat_path = ""
            logging.error("File is not in .DAT format")
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"File Format ", "File is not in .DAT format\n\nPlease try again",
                                     QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
            dat_path = QFileDialog.getOpenFileName(None, "Select a .DAT file", "", "DAT files (*.dat);;All files (*.*)")
        else:
            # Pastes the file path name in the text widget on Page 2
            dat_basename = os.path.basename(dat_path[0])
            dat_label.hide()
            dat_text.setReadOnly(False) 
            dat_text.clear()          
            dat_text.setText(dat_basename[:14])
            dat_font = dat_text.font()
            dat_font.setBold(True)
            dat_text.setFont(dat_font)
            dat_text.setReadOnly(True)
            logging.info(f"""
                    Selected .DAT file:
                    {os.path.basename(dat_path[0])}
                          """)
            
            choose_sta = QFileDialog.getOpenFileName(None, "Select a .STA file", "", "DAT files (*.sta);;All files (*.*)") 
            if choose_sta != ("", ""):
                sta_path = choose_sta
                if os.path.splitext(sta_path[0])[1] != ".STA" and sta_path[1] != "":
                    sta_path = ""
                    logging.error("File is not in .STA format")
                    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
                    QMessageBox.critical(None,"File Format ", "File is not in .STA format\n\nPlease try again",
                                        QMessageBox.Ok)
                    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
                    sta_path = QFileDialog.getOpenFileName(None, "Select a .STA file", "", "DAT files (*.sta);;All files (*.*)")
                else:
                    sta_basename = os.path.basename(sta_path[0])
                    sta_label.hide()
                    sta_text.setReadOnly(False) 
                    sta_text.clear()          
                    sta_text.setText(sta_basename[:14])
                    sta_font = sta_text.font()
                    sta_font.setBold(True)
                    sta_text.setFont(sta_font)
                    sta_text.setReadOnly(True)
                    logging.info(f"""
                            Selected .STA file:
                            {os.path.basename(sta_path[0])}
                                  """)
    
        if choose_dat != ("", "") and choose_sta == ("", ""):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Error", "Missing .STA file\n\nClearing all pathways",
                                QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
            dat_path = sta_path = ""
            choose_dat = choose_sta = ""

            dat_label.show()
            dat_text.setReadOnly(False)
            dat_text.clear()
            dat_text.setReadOnly(True)

            sta_text.setReadOnly(False)
            sta_text.clear()
            sta_text.setReadOnly(True)
                            
    return dat_path, sta_path
    
def csv_import(csv_text: QLineEdit,csv_label: QLabel):

    global csv_path

    csv_path = ""

    """
    Function that imports .CSV files for wirebond pull test analysis.
    Processes the file through a csv-reader, returns a seperate outfile 
    that is used for obtaining data, and appends data points to a list for
    better handling.
    """

    csv_basename = None

    # New processed list for data analysis
    csv_list = []
    # Processed file to read from for analsysis
    csv_new = "Processed ATLAS-Pixel Sample.csv"

    choose_csv = QFileDialog.getOpenFileName(None, "Select a .CSV file", "", "CSV files (*.csv);;All files (*.*)")

    if choose_csv != ("", ""):
        csv_path = choose_csv
        
        if os.path.splitext(csv_path[0])[1] != ".csv" and csv_path[1] != "":
            csv_path = ""
            logging.error("File is not in .CSV format")
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"File Format ", "File is not in .CSV format\n\nPlease try again",
                                QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
            csv_path = QFileDialog.getOpenFileName(None, "Select a .CSV file", "", "CSV files (*.csv);;All files (*.*)")
        else:
            # Reading the csv file and creating a new output csv with new filtering settings 
            with open(csv_path[0], 'r', newline='') as infile, open(csv_new, 'w', newline='') as outfile:
                reader = csv.reader(infile, quotechar='"')
                writer = csv.writer(outfile, quoting=csv.QUOTE_NONE, escapechar='\\')

                for row in reader:
                    writer.writerow(row)

            # Removing end of line characters and seperating elements by comma
            with open(csv_new) as file:
                for line in file:
                    line_list = line.rstrip().split(",")
                    # Appending filtered data to a new list above
                    csv_list.append(line_list)

            # Retriveting component ID and displaying it in the text widget on Page 2B

            try:
                csv_basename = [row[1] for row in csv_list[3:6] if row[0] == "Object ID"]
                csv_label.hide()
                csv_text.setReadOnly(False) 
                csv_text.clear()          
                csv_text.setText(csv_basename[0])
                font = csv_text.font()
                font.setBold(True)
                csv_text.setFont(font)
                csv_text.setReadOnly(True)

                logging.info(f"""
                        Selected .CSV file for:
                        {csv_basename[0]}
                        """)
                    
            except Exception as e:
                    print(f"{e}")
                    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
                    QMessageBox.critical(None,"Error", "An error occured while obtaining object ID from file",
                                        QMessageBox.Ok)
                    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
                    csv_path = ""
                    csv_list = ""
                    csv_basename = ""
                    csv_text.setReadOnly(False)     
                    csv_text.clear()           
                    csv_text.setReadOnly(True) 
            
            return csv_list, csv_basename, csv_path

def acquire_data(file_name):

    """
    acquire_data(imported file) - function designed to acquire filtered raw data by removing unecessary characters, empty lines and
    any lines that do not have all x, y and z components. The filtered data is then returned upon calling
    the function.

    """        
    acq_data = []

    with open(file_name, "r") as file:

        for line_number,line in enumerate(file):

            line_new = line.rstrip()    # removes all escape/end of line characters at end of line
            if line_new == "" :
                continue                # ignores all empty lines

            if os.path.splitext(file_name)[1] == ".DAT":

                line_list = line_new.split() # splits elements by empty white spaces
                if len(line_list) != 3: 
                    continue                 # ignores all lines which don't have 3 elements  

            elif os.path.splitext(file_name)[1] == ".STA":

                if line_number == 0:            # skip the first line that contains letter characters
                    continue

                line_list = line_new.split(',') # splits elements by comma
                while "" in line_list: 
                    line_list.remove("")        # ignores empty spaces at the end of each line as a result of file formatting
                
            else:
                print("File formatting error")

            # Appending a filtered list to a new list and return the data upon calling the fucntion
            line_list_numbered = [float(element) for element in line_list]
            acq_data.append(line_list_numbered) 
    
    return acq_data