# Necessary modules
import itkdb
import logging
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QApplication
##########################################################

def validate_login(db_passcode1: str, db_passcode2: str):

    """
    validate_login() - valdiates the login credentials in order to access the ITk database.
    Uses itkdb library to retrieve correct user inforamtion and provides accesss
    """

    global client

    if db_passcode1 and db_passcode2:
        try:
            u = itkdb.core.User(access_code1=db_passcode1, access_code2=db_passcode2)
            client = itkdb.Client(user=u)
            client.user.authenticate()
            user = client.get('getUser', json={'userIdentity': client.user.identity})
            print("Accessing ITk Database...\nHello {} {}, \nWelcome to the ITk Database".format(user["firstName"], user["lastName"]))
            logging.info("""
                            Accessing ITk Database...
                            
                            Hello {} {}
                            Welcome to the ITk Database
                            """.format(user["firstName"], user["lastName"]))
            return True, client, user
        
        except Exception as e:
            print(e)
            logging.error(f"{e}")
            return False, None, None

    # Allows faster logging in to the database by storing both passwords in an .env file within the same directory
    elif "ITKDB_ACCESS_CODE1" in os.environ and "ITKDB_ACCESS_CODE2" in os.environ:
        try: 
            client = itkdb.Client()
            client.user.authenticate()
            user = client.get('getUser', json={'userIdentity': client.user.identity})
            print("Accessing ITk Database...\nHello {} {}, \nWelcome to the ITk Database".format(user["firstName"], user["lastName"]))
            logging.info("""
                            Accessing ITk Database...
                            
                            Hello {} {}
                            Welcome to the ITk Database
                            """.format(user["firstName"], user["lastName"]))
            return True, client, user
        
        except Exception as e:
            print(e)
            logging.error(f"{e}")
            return False, None, None

    else:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
        messagebox = QMessageBox()
        messagebox.setWindowTitle("Error")
        messagebox.setText("No Passwords Detected")
        messagebox.setInformativeText("Please Enter Passwords")
        messagebox.setIcon(QMessageBox.Critical)
        messagebox.setStandardButtons(QMessageBox.Ok)
        messagebox.setDefaultButton(QMessageBox.Ok)
        messagebox.exec()
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)

        return False, None, None 
