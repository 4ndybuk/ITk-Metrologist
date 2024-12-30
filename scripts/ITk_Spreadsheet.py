import gspread
from gspread import Worksheet
from google.oauth2.service_account import Credentials
import re
import tkinter.messagebox as box
from gspread_formatting import *
from tkinter import simpledialog
from ITk_SheetRules import *
from statistics import mean
import webbrowser
import multiprocessing

"""
ITk Pixel Module Assembly Google Spreadsheet Automation:
Code designed for updating spreadsheets with metrology data for each pixel assemlby stage.
Based on obtained and processed data from the Smartscope machine, it automatically updates the spreadsheet 
as the program is run. 
"""
# The scope of API operations
scopes = ['https://www.googleapis.com/auth/spreadsheets']

# Appending the credentials for editing sheets
creds = Credentials.from_service_account_file("assets/credentials.json", scopes = scopes)

# Authorising the client with given credentials
client = gspread.authorize(creds)

sheet_id = "1O54CRUXG36WApvoALbAuL7MGo8sgtVgdQhKCYmQvUXY"
workbook  = client.open_by_key(sheet_id)

def upload_sh(results: dict,queue: multiprocessing.Queue):

    queue.put(5)

    if re.match("PCB", results['component']['componentType']['code'], re.IGNORECASE):

        # Selecting worksheets
        sheet = workbook.worksheet("Hybrids")

        # Fidning if component name is already in the spreadsheet
        comp_name = sheet.find(results['component_id'])

        # New bottom row if the component is not in the spreadsheet
        new_row = len(sheet.col_values(1)) + 1

        queue.put(10)

        if not comp_name:
            hybrid_cells(sheet,new_row,results,queue)
        else:
            hybrid_cells(sheet,comp_name.row,results,queue)
        hybrid_rules(sheet,queue)

    if re.match("BARE_MODULE", results['component']['componentType']['code'], re.IGNORECASE):

        sheet = workbook.worksheet("Bare modules") 
        comp_name = sheet.find(results['component_id'])
        new_row = len(sheet.col_values(1)) + 1
        queue.put(10)

        if not comp_name:
            bare_cells(sheet,new_row,results,queue)
        else:
            bare_cells(sheet,comp_name.row,results,queue)
        bare_rules(sheet,queue)

    if re.match("MODULE", results['component']['componentType']['code'], re.IGNORECASE):

        sheet = workbook.worksheet("Assembled modules") 
        comp_name = sheet.find(results['component_id'])
        new_row = len(sheet.col_values(1)) + 1
        queue.put(10)

        if not comp_name:
            assem_cells(sheet,new_row,results,queue)
        else:
            assem_cells(sheet,comp_name.row,results,queue)
        assem_rules(sheet,queue)

    # Signal the process is complete
    queue.put(85)
    queue.put(95)
    queue.put(100)

    open_site = box.askquestion("Results", "Upload successful - Would you like to open the results in a browser?")
    if open_site == "yes":
        # Opening test web page
        webbrowser.open(f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit?gid=0#gid=0",new = 2)
    else:
        return

def hybrid_cells(sheet: gspread.Worksheet,row: int,results: dict,queue: multiprocessing.Queue):

    """
    Updating cells for the hybrid component using update_cell function
    """

    sheet.update_cell(row, 1, results['component_id'])
    sheet.update_cell(row, 3, f"https://itkpd-test.unicorncollege.cz/componentView?code={results['component']['code']}")
    sheet.update_cell(row, 4, results['component']['currentLocation']['name'])
    queue.put(15)
    assembly_call(sheet,row,results)
    sheet.update_cell(row, 6, results["flex_results"]["x_dimension"])
    sheet.update_cell(row, 7, results["flex_results"]["y_dimension"])
    queue.put(20)
    sheet.update_cell(row, 8, results["flex_results"]["quad_thickness"][0]*1000)
    sheet.update_cell(row, 9, results["flex_results"]["quad_thickness"][1]*1000)
    sheet.update_cell(row, 10, results["flex_results"]["quad_thickness"][2]*1000)
    queue.put(25)
    sheet.update_cell(row, 11, results["flex_results"]["quad_thickness"][3]*1000)
    sheet.update_cell(row, 12, results["flex_results"]["avg_thickness"]*1000)
    sheet.format(f"L{row}", {"backgroundColor": {"red": 0.85,"green": 0.85,"blue": 0.85}})
    queue.put(30)
    sheet.update_cell(row, 13, results["flex_results"]["avg_stdev"]*1000)
    sheet.update_cell(row, 16, results["flex_results"]["hv_thickness"])
    sheet.update_cell(row, 17, results["flex_results"]["ftm_flex_thickness"])

    queue.put(40)

def bare_cells(sheet: gspread.Worksheet,row: int,results: dict,queue: multiprocessing.Queue):

    sheet.update_cell(row, 1, results['component_id'])
    queue.put(15)
    assembly_call(sheet,row,results)
    sheet.update_cell(row, 7, results["bare_results"]["fe_x"])
    queue.put(20)
    sheet.update_cell(row, 8, results["bare_results"]["fe_y"])
    sheet.update_cell(row, 9, results["bare_results"]["sensor_x"])
    queue.put(25)
    sheet.update_cell(row, 10, results["bare_results"]["sensor_y"])
    sheet.update_cell(row, 11, results["bare_results"]["avg_fe_thickness"]*0.001)
    queue.put(30)
    sheet.update_cell(row, 12, results["bare_results"]["avg_stdev_fe"])
    sheet.update_cell(row, 13, results["bare_results"]["avg_bare_thickness"]*0.001)
    queue.put(35)
    sheet.update_cell(row, 14, results["bare_results"]["avg_stdev_bare"])
    sheet.update_cell(row, 18, f"https://itkpd-test.unicorncollege.cz/componentView?code={results['component']['code']}")

    queue.put(40)

def assem_cells(sheet: gspread.Worksheet,row: int,results: dict,queue: multiprocessing.Queue):

    sheet.update_cell(row, 1, results['component']['currentLocation']['name'])
    queue.put(15)
    sheet.update_cell(row, 2, simpledialog.askstring(title="Date Assembled",
                                                            prompt="When was the module assembled? (dd/mm/yy)"))
    sheet.update_cell(row, 5, results['component_id'])
    sheet.update_cell(row, 6, simpledialog.askstring(title="Carrier Frame",
                                                            prompt="What is the Carrier Frame S/N?"))
    queue.put(20)
    sheet.update_cell(row, 7, f"https://itkpd-test.unicorncollege.cz/componentView?code={results['component']['code']}")
    sheet.update_cell(row, 8, results["assem_results"]["x_value"])
    sheet.update_cell(row, 9, results["assem_results"]["y_value"])
    queue.put(25)
    sheet.update_cell(row, 10, results["assem_results"]["avg_assem_thickness"][0])
    sheet.update_cell(row, 11, results["assem_results"]["avg_assem_thickness"][1])
    sheet.update_cell(row, 12, results["assem_results"]["avg_assem_thickness"][2])
    queue.put(30)
    sheet.update_cell(row, 13, results["assem_results"]["avg_assem_thickness"][3])
    sheet.update_cell(row, 14, mean(results["assem_results"]["avg_assem_thickness"]))
    sheet.update_cell(row, 15, results["assem_results"]["quad_stdev_all"])
    queue.put(35)
    sheet.update_cell(row, 19, results["assem_results"]["ftm_thickness"]*0.001)
    sheet.update_cell(row, 20, results["assem_results"]["hv_assem_thickness"]*0.001)

    queue.put(40)

def assembly_call(sheet: gspread.Worksheet,row: int,results: dict):

    """
    Yes/No call to state whether the hybrid flex has been assembled
    """
    if results['component']['componentType']['code'] == "PCB":
        call_choice = box.askquestion("Assembly Call", "Is this flex assembled?")
    else:
        call_choice = box.askquestion("Assembly Call", "Is this bare module assembled?")

    if call_choice == "yes":
        sheet.update_cell(row, 5, "Yes")
        sheet.format(f"E{row}", {"backgroundColor": {"red": 0.8,"green": 1.0,"blue": 0.8}})
    else: 
        sheet.update_cell(row, 5, "No")
        if results['component']['componentType']['code'] == "BARE_MODULE":
            sheet.format(f"E{row}", {"backgroundColor": {"red": 1.0,"green": 0.9,"blue": 0.9}})