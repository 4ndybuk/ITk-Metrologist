from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import Qt
import re
from itkdb import Client

def iref_values(client: Client,bare_id: str):
        
    serial_list = []
    hex_list = []

    # Security check to ensure that the serial number corresponds to the bare module
    if re.match(r"^20UPGB[0-9]+",bare_id):
        # Retrieving component information from the database
        try:
            component = client.get('getComponent',
                                json={"component":bare_id,
                                    "alternativeIdentifier":False})
        except:
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Error", "Component not found!",
                                QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
            return

        try:
            # Iterating over all children components for the bare module to extract the serial numbers
            for child in component['children']:
                if child['componentType']['code'] == "FE_CHIP":
                    serial_number = child['component']['serialNumber']
                    serial_list.append(serial_number)
                    decimal = int(serial_number[9:])
                    # Converting serial IDs in decimal to hexadecimal to obtain chip ID
                    hex_number = hex(decimal)[5:]
                    hex_list.append(hex_number.upper())

            # Processing JSON structure with list comprehensions to obtain testRun identifiers
            fe_chip = [client.get('getComponent',
                                    json={"component":serial_id,
                                          "alternativeIdentifier":False}) for serial_id in serial_list]
            fe_chip_tests = [entry['tests'] for entry in fe_chip]
            test_ids = [
                item['id']
                for test in fe_chip_tests
                for element in test[0:]
                for item in element['testRuns'][0:]
                if element['code'] == "FECHIP_TEST"
            ]

            # Obtaining test results and IREF trim bit values
            testRun_array = [client.get('getTestRun',
                                       json={"testRun": test_id}) for test_id in test_ids]
            iref_trim_bits = [
                item['value']
                for entry in testRun_array
                for item in entry['results'][0:]
                if item['code'] == "IREF_TRIM"
            ]
            return hex_list, iref_trim_bits, bare_id

        except Exception as e:
            print(e)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Error", "An error has occured in processing data\n\nPlease try again",
                                QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)           

    else:
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
        QMessageBox.critical(None,"Error", "The serial number does not correspond to a bare module\n\nPlease try again",
                            QMessageBox.Ok)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
    