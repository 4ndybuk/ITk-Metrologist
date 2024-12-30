from datetime import datetime, timezone
import re
from tkinter import simpledialog
import logging
import tkinter.messagebox as box
import webbrowser
from itkdb import Client

def upload_itk(component: dict,results: dict,client: Client,csv_path):
        
    """
    Uploading fucntion that takes the component information and metrology
    results as arguments. Sets the data to test-type schemas and uploads them
    deirectly to the ITk database.
    
    """

    # Date and time in ISO format for upload
    today = datetime.today().strftime('%d/%m/%Y')
    mydate = datetime.strptime(today, '%d/%m/%Y')
    datetimeobject = datetime.combine(mydate,datetime.now(timezone.utc).time())

    # Component dictionary for types and stage names
    test_dict = {"flextype": "PCB",
                "baretype": "BARE_MODULE",
                "assemtype": "MODULE",
                "flexstage": "PCB_RECEPTION_MODULE_SITE",
                "barestage": "BAREMODULERECEPTION",
                "assemstage": "MODULE/ASSEMBLY",
                "wirestage": "MODULE/WIREBONDING",
                "flextest": "METROLOGY",
                "baretest": "QUAD_BARE_MODULE_METROLOGY",
                "assemtest": "QUAD_MODULE_METROLOGY",
                "wiretest": "WIREBOND_PULL_TEST"}
    
    if re.match(test_dict["flextype"], component['componentType']['code'], re.IGNORECASE):

        # Prearing the upload template
        test_json = {
                    "component": component['code'],
                    "testType": "METROLOGY",
                    "institution": "LIV",
                    "runNumber": auto_run_number(component,test_dict["flextest"],[test_dict["flexstage"]],client),
                    "date": datetimeobject.astimezone().isoformat(timespec='milliseconds'),
                    "passed": check_passed(results["flex_results"]["pass_fail"]),
                    "problems": False,
                    "properties": {
                        "OPERATOR": simpledialog.askstring(title="Operator Name",
                                                            prompt="Please input operator name:"),
                        "INSTRUMENT": "Smartscope OGP",
                        "ANALYSIS_VERSION": None
                    },
                    "results": {
                        "X_DIMENSION": results["flex_results"]["x_dimension"],
                        "Y_DIMENSION": results["flex_results"]["y_dimension"],
                        "X-Y_DIMENSION_WITHIN_ENVELOP": results["flex_results"]["xy_envelope"],
                        "DIAMETER_DOWEL_HOLE_A": None,
                        "WIDTH_DOWEL_SLOT_B": None,
                        "AVERAGE_THICKNESS_FECHIP_PICKUP_AREAS": results["flex_results"]["avg_thickness"],
                        "STD_DEVIATION_THICKNESS_FECHIP_PICKUP_AREAS": results["flex_results"]["avg_stdev"],
                        "HV_CAPACITOR_THICKNESS": results["flex_results"]["hv_thickness"],
                        "HV_CAPACITOR_THICKNESS_WITHIN_ENVELOP": results["flex_results"]["hv_envelope"],
                        "AVERAGE_THICKNESS_POWER_CONNECTOR": results["flex_results"]["ftm_flex_thickness"]
                    }
                    }
        
        # Perform safety checks on the component before uploading
        safety_check(component,test_json,test_dict["flextype"],test_dict["flexstage"])

    if re.match(test_dict["baretype"],component['componentType']['code'], re.IGNORECASE):

        test_json = {
                    "component": component['code'],
                    "testType": "QUAD_BARE_MODULE_METROLOGY",
                    "institution": "LIV",
                    "runNumber": auto_run_number(component,test_dict["baretest"],[test_dict["barestage"]],client),
                    "date": datetimeobject.astimezone().isoformat(timespec='milliseconds'),
                    "passed": check_passed(results["bare_results"]["pass_fail"]),
                    "problems": False,
                    "properties": {
                        "ANALYSIS_VERSION": None
                    },
                    "results": {
                        "SENSOR_X": results["bare_results"]["sensor_x"],
                        "SENSOR_Y": results["bare_results"]["sensor_y"],
                        "SENSOR_THICKNESS": None,
                        "SENSOR_THICKNESS_STD_DEVIATION": None,
                        "FECHIPS_X": results["bare_results"]["fe_x"],
                        "FECHIPS_Y": results["bare_results"]["fe_y"],
                        "FECHIP_THICKNESS": results["bare_results"]["avg_fe_thickness"],
                        "FECHIP_THICKNESS_STD_DEVIATION": results["bare_results"]["avg_stdev_fe"],
                        "BARE_MODULE_THICKNESS": results["bare_results"]["avg_bare_thickness"],
                        "BARE_MODULE_THICKNESS_STD_DEVIATION": results["bare_results"]["avg_stdev_bare"]
                    }
                    }
        
        safety_check(component,test_json,test_dict["baretype"],test_dict["barestage"])
        
    if re.match(test_dict["assemtype"], component['componentType']['code'], re.IGNORECASE) and csv_path == "":
        
        test_json = {
                    "component": component['code'],
                    "testType": "QUAD_MODULE_METROLOGY",
                    "institution": "LIV",
                    "runNumber": auto_run_number(component,test_dict["assemtest"],[test_dict["assemstage"]],client),
                    "date": datetimeobject.astimezone().isoformat(timespec='milliseconds'),
                    "passed": check_passed(results["assem_results"]["pass_fail"]),
                    "problems": False,
                    "properties": {
                        "ANALYSIS_VERSION": None
                    },
                    "results": {
                        "DISTANCE_PCB_BARE_MODULE_TOP_LEFT": results["assem_results"]["fiducial_tl"],
                        "DISTANCE_PCB_BARE_MODULE_BOTTOM_RIGHT": results["assem_results"]["fiducial_br"],
                        "AVERAGE_THICKNESS": results["assem_results"]["avg_assem_thickness"],
                        "STD_DEVIATION_THICKNESS": None,
                        "THICKNESS_VARIATION_PICKUP_AREA": results["assem_results"]["quad_stdev_all"],
                        "THICKNESS_INCLUDING_POWER_CONNECTOR": results["assem_results"]["ftm_thickness"],
                        "HV_CAPACITOR_THICKNESS": results["assem_results"]["hv_assem_thickness"]
                    }
                    }
        
        safety_check(component,test_json,test_dict["assemtype"],test_dict["assemstage"])
    
    if re.match(test_dict["assemtype"], component['componentType']['code'], re.IGNORECASE) and csv_path != "":
        test_json = {

                    "component": component['code'],
                    "testType": "WIREBOND_PULL_TEST",
                    "institution": "LIV",
                    "runNumber": auto_run_number(component,test_dict["wiretest"],[test_dict["wirestage"]],client),
                    "date": datetimeobject.astimezone().isoformat(timespec='milliseconds'),
                    "passed": check_passed(results["pulltest"]["pass_fail"]),
                    "problems": False,
                    "properties": {
                        "INSTRUMENT": "Dage 4000 Plus",
                        "ANALYSIS_VERSION": None,  
                    },
                    "results": {
                        "WIRE_PULLS": results["pulltest"]["numberofwires"],
                        "PULL_STRENGTH": results["pulltest"]["mean_pull"],
                        "PULL_STRENGTH_ERROR": results["pulltest"]["standard_deviation"],
                        "WIRE_BREAKS_5G": results["pulltest"]["before5g_wires"],
                        "PULL_STRENGTH_MIN": results["pulltest"]["minimum_pull"],
                        "PULL_STRENGTH_MAX": results["pulltest"]["maximum_pull"],
                        "HEEL_BREAKS_ON_FE_CHIP": results["pulltest"]["percentage_2"],
                        "HEEL_BREAKS_ON_PCB": results["pulltest"]["percentage_1"],
                        "BOND_PEEL": results["pulltest"]["percentage_3or4"],
                        "LIFT_OFFS_LESS_THAN_7G": results["pulltest"]["percentage_less7"],
                        "DATA_UNAVAILABLE": False,
                        "PULL_STRENGTH_DATA": results["pulltest"]["pull_strength_data"]
                    }
                    }
        
        safety_check(component,test_json,test_dict["assemtype"],test_dict["wirestage"])

    # Attempting the upload of metrology values to the DB
    try:
        test_upload = client.post('uploadTestRunResults',json=test_json)
        
    except Exception as e:
        print(e)
        logging.error(e)
        return
    
    # Opening test web page
    webbrowser.open(f"https://itkpd-test.unicorncollege.cz/testRunView?id={test_upload['testRun']['id']}",new = 2)

def auto_run_number(component,test_type,stage_list,client: Client):

    """
    Generating a run number for a given test type based on already uploaded tests
    """

    # Mapping a filtering map for the component list
    map_input = {"code": component['code'],
                    "serialNumber": component['serialNumber'],
                    "testType": test_type,
                    "state": "ready",
                    "stage": stage_list}
    
    test_list = client.get('listTestRunsByComponent',
                            json={"filterMap": map_input,
                                    "force": False,
                                    "contextType": "none",
                                    "outputType": "object",
                                    "pageInfo": {"pageSize": 200}
                                    })
    
    if not test_list:
        logging.info("""
                        No familiar tests found for the component,
                        Assigning Run Number -> 1
                        """)
        return str(1)
    else:
        return str(test_list.total + 1)


def check_passed(list: list):
    """
    Checks whether there is a failed test in the whole group of variables.
    If at least one is failed then the whole metrology does not pass.
    """

    if all(list) == True:
        result = True
    else:
        result = False
    return result

def safety_check(component,test_json,type,stage):
    
    """
    Performs a safety check on the given component by assuring the right component
    type and stage are set before metrology/pull-test is uploaded 
    """

    # Safety checks for component type, stage and location
    if component['componentType']['code'] != type:
        logging.warning(f"""
                        WARNING:
                        The component you have chosen does not match the type necessary 
                        for metrology upload. Please press Go Back and check for the right
                        file to import.

                        >>> Ceasing upload now...
                        """)
        return
    
    if component['currentLocation']['code'] != "LIV":
        logging.warning(f"""
                        WARNING:
                        The ccomponent you have chosen is not currently located at Liverpool.
                        Please ensure the component has been shipped to LIV before proceeding 
                        with uploading.

                        >>> Ceasing upload now...
                        """)
        return

    if component['currentStage']['code'] != stage:
        logging.error(f"""
                        WARNING:
                        Component stage in DB {component['currentStage']['code']}
                        does not match that requested "{stage}".

                        Displaying a prompt for Retroaction...
                        """)
        stage_call(stage,test_json)

def stage_call(stage,test_json):
    """
    A pop-up YES/NO window for setting a Retroactive mode for uploading:
        YES - sets the test_josn as isRetroactive: True
        NO = Stopping the upload process and returning to the step before
    """

    call_choice = box.askquestion("Component Stage", f"""
                        Component stage does not match the 
                        one required for metrology upload.
                        Would you like to set the component as
                        Retroactive?
                                """)
    if call_choice == "yes":
        try:
            test_json["stage"] = stage
            test_json["isRetroactive"] = True

            logging.info(f"""
                        Setting the component for Retroactive upload.
                        Continuing with the metrology upload...
                        >>>
                        """)
            
        except Exception as e:
            print(e)
            logging.info(f"{e}")
            box.showerror("Error", "Could not set the component as Retroactive")
    else:
        box.showinfo("Upload Status", "Stopping the upload process")
        return