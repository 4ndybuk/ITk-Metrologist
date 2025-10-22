from ITk_Importers import acquire_data
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import Qt
import logging
import re
from ITk_ModuleProcessors import *
from statistics import stdev,mean
import math
from itkdb import Client
import json

def met_measurements(dat_path,sta_path,dat_basename: str,sta_basename: str,client: Client):
    
    new_dat = acquire_data(dat_path)
    new_sta = acquire_data(sta_path)

    dat_prefix = dat_basename[:14]
    sta_prefix = sta_basename[:14]

    # Initialize results to None
    results = {"flex_results": None,
               "bare_results": None,
               "assem_results": None,
               "mass": None,
               "carrier": None}

    # If the serial numbers match execute the measurements
    if dat_prefix == sta_prefix:

        # Retrieving component information from the database
        try:
            component_id = dat_prefix
            component = client.get('getComponent',
                                json={"component":component_id,
                                        "alternativeIdentifier":False})
        except:
            logging.error("Component not found")
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
            QMessageBox.critical(None,"Error", "Component not found!",
                                     QMessageBox.Ok)
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
            return False, None
        
        # Retrieving component mass measurement for Google Sheet input
        def get_mass(code: str):
            try:
                test_id = [item['id']
                        for element in component['tests']
                        for item in element['testRuns'][0:]
                        if element['code'] == code]
                test_run = client.get('getTestRun',
                                        json={"testRun": test_id[0]})
                mass = test_run['results'][0]['value']
                return mass
            except:
                logging.error("Mass Measurement test run has not been found in the database" \
                "\nConsider uploading it first before updating Google Sheets")
            
        logging.info(f"""
                Component mongoDB ID: {component['code']}
                Component ATLAS ID: {component['serialNumber']}
                Component alternative ID: {component['alternativeIdentifier']}
                Component current stage: {component['currentStage']['code']}
                Component type: {component['componentType']['code']}
                Component location: {component['currentLocation']['code']}
                    """)

        # File name types stores in dictionary
        patterns = {"flex": r"^([a-z0-9]+)_vc3_bare_flex_metrology\.(DAT|STA)",
                    "bare": r"^([a-z0-9]+)_vc3_bare_module_metrology\.(DAT|STA)",
                    "assem": r"^([a-z0-9]+)_vc3_assembled_module_metrology\.(DAT|STA)"}

        if re.match(patterns["flex"], dat_basename, re.IGNORECASE) and re.match(patterns["flex"], sta_basename, re.IGNORECASE):

            processor = FlexProcessor(new_dat)
            processor.process_all()
            
            # Standard deviation of the pick up points
            avg_stdev = stdev(processor.quad_data)

            # List to store Pass or Fail variables that will decide whether metrology has passed
            flex_pass_fail = []

            y_dimension = new_sta[-1][0]
            x_dimension = new_sta[-2][0]
            ga_thickness = [row[2] for row in new_sta[-9:-5] if row[2] < 1.300]
            avg_thickness = round(mean(ga_thickness),4)
            ftm_flex_thickness = new_sta[-10][2]
            hv_thickness_list = [row[2] for row in new_sta[-13:-10] if row[2] > ftm_flex_thickness]

            # Ensuring that there is only one value pulled from the list which corresponds to the HV cap
            if len(hv_thickness_list) == 1:
                hv_thickness = hv_thickness_list[0]
            else:
                QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
                QMessageBox.critical(None,"Error", "Cannot extract the value of the HV capacitor thickness\n\nPlease check the .STA file",
                                     QMessageBox.Ok)
                QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
                logging.error("HV capacitor thickness does not contain exactly one element in the .STA file\n\nPlease check the file")
            
            # Chekcing that the X and Y values fit within acceptable specifications
            xy_envelope = 39.50 <= x_dimension <= 39.70 and 40.50 <= y_dimension <= 40.70
            flex_pass_fail.append(xy_envelope)
           
            # Same specification check for the HV cap
            hv_envelope = 1.701 <= hv_thickness <= 2.001
            flex_pass_fail.append(hv_envelope)
                        
            # And same specification check for indiviudal pick-up point thickness and FTM
            for row in ga_thickness:
                ga_pass = 0.201 <= row <= 0.301
                flex_pass_fail.append(ga_pass)
                            
            ftm_pass = 1.521 <= ftm_flex_thickness <= 1.761
            flex_pass_fail.append(ftm_pass)
                       
            logging.info(f"""
            Average thickness of all pick up areas [mm]: {round(avg_thickness,3)}mm
            Thickness of each pick up area [mm]: {ga_thickness}.
            Thickness including the black body of power connector (excluding pins) [mm]: {ftm_flex_thickness}mm
            HV capacitor thickness [mm]: {hv_thickness}mm
            HV capacitor thickness within envelope: {hv_envelope}.
            Std deviation of thickness of all pick-up areas [mm]: {round(avg_stdev,4)}mm
            X-Y dimension within envelope: {xy_envelope}.
            X dimension [mm]: {x_dimension}mm
            Y dimension [mm]: {y_dimension}mm

            Are you happy with these measurements? If yes, press Upload to ITk/Upload to Sheets
                        """)
            
            results["flex_results"] = {"pass_fail": flex_pass_fail,
                                       "avg_thickness": round(avg_thickness,3),
                                       "quad_thickness": ga_thickness,
                                       "ftm_flex_thickness": ftm_flex_thickness,
                                       "hv_thickness": hv_thickness,
                                       "hv_envelope": hv_envelope,
                                       "avg_stdev": round(avg_stdev,4),
                                       "xy_envelope": xy_envelope,
                                       "x_dimension": x_dimension,
                                       "y_dimension": y_dimension}
            results['mass'] = get_mass("MASS")
        
        if re.match(patterns["bare"], dat_basename, re.IGNORECASE) and re.match(patterns["bare"], sta_basename, re.IGNORECASE):

            processor = BareProcessor(new_dat)
            processor.process_all()

            # Standard deviations for the sensor and FE chips
            avg_stdev_fe = stdev(processor.fe_data)
            avg_stdev_bare = stdev(processor.sensor_data)

            # Pass/Fail list
            bare_pass_fail = []
            
            avg_bare_thickness = [float(val)*1000 for val in new_sta[-1]][0]
            avg_fe_thickness = [float(val)*1000 for val in new_sta[-3]][0]
            fe_y = new_sta[-5][0]
            fe_x = new_sta[-6][0]
            sensor_y = new_sta[-7][0]
            sensor_x = new_sta[-8][0]

            # Pass/Fail criteria
            fe_pass = 40.200 <= fe_y <= 40.450 and 42.00 <= fe_x <= 42.350
            bare_pass_fail.append(fe_pass)

            sensor_pass = 41.00 <= sensor_y <= 41.15 and 39.2 <= sensor_x <= 39.80
            bare_pass_fail.append(sensor_pass)

            bare_thick_pass = 250.0 <= avg_bare_thickness <= 415.0
            bare_pass_fail.append(bare_thick_pass)
                        
            fe_thick_pass = 80.0 <= avg_fe_thickness <= 250.0
            bare_pass_fail.append(fe_thick_pass)
           
            logging.info(f"""
                Average bare module thickness [µm]: {round(avg_bare_thickness)}µm
                Std deviation of bare module thickness [µm]: {round(avg_stdev_bare*1000,3)}µm
                FE chips x dimension [mm]: {fe_x}mm 
                FE chips y dimension [mm]: {fe_y}mm
                Average FE chip thickness [µm]: {round(avg_fe_thickness)}µm
                Std deviation of FE chip thickness [µm]: {round(avg_stdev_fe*1000,3)}µm
                Sensor dimension in x [mm]: {sensor_x}mm
                Sensor dimension in y [mm]: {sensor_y}mm
                
                Are you happy with these measurements? If yes, press Upload to ITk/Upload to Sheets
                        """)
            
            results["bare_results"] = {"pass_fail": bare_pass_fail,
                                       "avg_bare_thickness": round(avg_bare_thickness),
                                       "avg_stdev_bare": round(avg_stdev_bare*1000,3),
                                       "fe_x": fe_x,
                                       "fe_y": fe_y,
                                       "avg_fe_thickness": round(avg_fe_thickness),
                                       "avg_stdev_fe": round(avg_stdev_fe*1000,3),
                                       "sensor_x": sensor_x,
                                       "sensor_y": sensor_y}
            results['mass'] = get_mass("MASS_MEASUREMENT")
            
        if re.match(patterns["assem"], dat_basename, re.IGNORECASE) and re.match(patterns["assem"], sta_basename, re.IGNORECASE):

            # removing the last row in the list if it doesn't equal to 1 element
            # affects automated value fetching from the data set
            if len(new_sta[-1]) != 1:
                last_element = new_sta.pop()

            processor = AssemProcessor(new_dat)
            processor.process_all()

            # Standard deviation of the pick up points
            quad_stdev_all = round(stdev(processor.assem_quad)*1000,2)

            # Pass/Fail List
            assem_pass_fail = []
            
            ftm_thickness = [float(val)*1000 for val in new_sta[-1]][0]
            hv_assem_thickness = [float(val)*1000 for val in new_sta[-2]][0]
            fiducial_br = new_sta[-3][:2]
            fiducial_tl = new_sta[-4][:2]
            avg_assem_thickness = [float(row[2])*1000 for row in new_sta[-15:-11] if row[2] < 0.800]
            x_value = [float(val) for val in new_sta[-7] if len(new_sta[-7]) == 1][0]
            y_value = [float(val) for val in new_sta[-6] if 40.0 < val < 42.0][0]

            # Modified fiducial values to be in µm units
            fiducial_br_micro = [round(fp*1000) for fp in fiducial_br]
            fiducial_tl_micro = [round(fp*1000) for fp in fiducial_tl]

            #Pass/Fail Criteria

            ftm_pass = 1831.0 <= ftm_thickness <= 2231.0
            assem_pass_fail.append(ftm_pass)

            hv_pass = 2011.0 <= hv_assem_thickness <= 2581.0
            assem_pass_fail.append(hv_pass)
           
            for row in avg_assem_thickness:
                assem_pass = row <= 771.0
                assem_pass_fail.append(assem_pass)
            
            def within_bounds(x,y):
                return 2.119 <= x <= 2.319 and 0.650 <= y <= 0.850
            
            fbr_pass = within_bounds(*fiducial_br)
            ftl_pass = within_bounds(*fiducial_tl)

            assem_pass_fail.extend([fbr_pass,ftl_pass])

            # Retrieve the carrier serial number
            try:
                carrier = [
                    element['component']['serialNumber']
                    for element in component['children']
                    if element['type']['code'] == "CARRIER"
                ][0]
                results['carrier'] = carrier
            except:
                logging.info("The carrier serial number is not associated with the module in the database\n" \
                "Consider updating this information before uploading to Google Sheets")

            logging.info(f"""
    Average module thickness at FE chip pick-up areas, 1 per FE [μm]: {avg_assem_thickness}
    Distance of PCB fiducial to bare module fiducial bottom right (x and y) [µm]: {fiducial_br_micro}
    Distance of PCB fiducial to bare module fiducial top left (x and y) [µm]: {fiducial_tl_micro}
    HV capacitor thickness [µm]: {hv_assem_thickness}µm
    Thickness including the black body of power connector (excluding pins) [µm]: {ftm_thickness}µm
    Thickness variation of the 4 pick-up areas [µm]: {quad_stdev_all}µm
    
    Are you happy with these measurements? If yes, press Upload to ITk/Upload to Sheets
                        """)
            
            results["assem_results"] = {"pass_fail": assem_pass_fail,
                                        "avg_assem_thickness": avg_assem_thickness,
                                        "fiducial_br": fiducial_br_micro,
                                        "fiducial_tl": fiducial_tl_micro,
                                        "hv_assem_thickness": hv_assem_thickness,
                                        "ftm_thickness": ftm_thickness,
                                        "quad_stdev_all": quad_stdev_all,
                                        "x_value": x_value,
                                        "y_value": y_value}
            results['mass'] = get_mass("MASS_MEASUREMENT")

        results["component_id"] = component_id
        results["component"] = component
        results["token"] = None
        
        return True, results
    else: 
        return False, None
    
def csv_measurements(csv_list: list,csv_basename: str,client: Client):

    results = {"pulltest": None}
    
    # Retrieving component information from the database
    try:
        component_id = csv_basename
        component = client.get('getComponent',
                            json={"component":component_id,
                                    "alternativeIdentifier":False})
    except:
        logging.error("Component not found")
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
        QMessageBox.critical(None,"Error", "Component not found!",
                                    QMessageBox.Ok)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)
        return None
        
    logging.info(f"""
                Component mongoDB ID: {component['code']}
                Component ATLAS ID: {component['serialNumber']}
                Component alternative ID: {component['alternativeIdentifier']}
                Component current stage: {component['currentStage']['code']}
                Component type: {component['componentType']['code']}
                Component location: {component['currentLocation']['code']}
                """)
    
    pull_pass_fail = []
    
    # Extracting pull test values [g]
    pull_list = [row[3] for row in csv_list[19:] if row[0] == "TEST"]
    val_pull_list = [float(value) for value in pull_list]

    # Taking a mean average value and standard deviation
    mean_pull = mean(val_pull_list)
    standard_deviation = stdev(val_pull_list)

    # Pass/Fail Criteria
    if mean_pull >= 8.00:
        mean_pass = True
        pull_pass_fail.append(mean_pass)
    else:
        mean_pass = False
        pull_pass_fail.append(mean_pass)

    if standard_deviation <= 1.50:
        stdev_pass = True
        pull_pass_fail.append(stdev_pass)
    else:
        stdev_pass = False
        pull_pass_fail.append(stdev_pass)

    # Obtaining values that break before 5g strength
    before5g_wires = [value for value in val_pull_list if value < 5.0]
    if len(before5g_wires) == 0:
        before5g_wires = 0
        b5g_pass = True
        pull_pass_fail.append(b5g_pass)
    else:
        b5g_pass = False
        pull_pass_fail.append(b5g_pass)

    # Minimum and maximum values
    minimum_pull = min(val_pull_list)
    maximum_pull = max(val_pull_list)

    # Obtaining the pull grades, failure type and pull location
    # {[x1,y1,z1],[x2,y2,z2]...} where x = pull strength, failure type integer, pull location
    grade_list = [row[2] for row in csv_list[19:] if row[0] == "TEST"]
    val_grade_list = [float(value) for value in grade_list]
    grade_webApp = list(map(grade_mapping, val_grade_list))
    # Copying the grade list to appropriate pull location
    pull_location = list(map(grade_mapping, val_grade_list))
    five_count_1 = pull_location[:10].count(5)
    pull_location[:10-five_count_1] = [1]*(10-five_count_1)
    five_count_2 = pull_location[(10-five_count_1):(15-five_count_1)].count(5)
    pull_location[(10-five_count_1):(15-(five_count_1+five_count_2))] = [2]*((15-five_count_2)-10)
    pull_location[(15-(five_count_1+five_count_2)):] = [3]*(len(pull_location)-(15-(five_count_1+five_count_2)))
    pull_strength_data = [[[x],[y],[z]] for x,y,z in zip(val_pull_list,grade_webApp,pull_location)]
    pull_strength_display = list(zip(grade_webApp,pull_location))

    # Percentage of specific grade pulls
    percentage_2 = (len([val for val in grade_webApp if val == 2])
                            /len(grade_webApp))*100
    percentage_1 = (len([val for val in grade_webApp if val == 1])
                            /len(grade_webApp))*100
    percentage_3or4 = (len([val for val in grade_webApp if val == 3 or val == 4])
                            /len(grade_webApp))*100
    
    # Percentage of bondpeels less that 7g
    bondpeel_val = [x for x,y in zip(val_pull_list,grade_webApp) if y == 3 or y == 4]
    bondpeel_less7 = [val for val in bondpeel_val if val < 7.0]
    if len(bondpeel_less7) == 0:
        percentage_less7 = float(0.0)
    else:
        percentage_less7 = (len(bondpeel_less7)/len(grade_webApp))*100
    
    if percentage_3or4 < 10.00:
        per3or4_pass = True
        pull_pass_fail.append(per3or4_pass)
    else:
        per3or4_pass = False
        pull_pass_fail.append(per3or4_pass)
    
    logging.info(f"""
        Mean pull strength [g]: {round(mean_pull,3)}
        Std deviation of pull strength [g]: {round(standard_deviation,3)}
        Number of wires breaking before 5g: {before5g_wires}
        Minimum pull strength [g]: {minimum_pull}
        Maximum pull strength [g]: {maximum_pull}
        Percentage of heel breaks on FE chips [%]: {round(percentage_2,2)}
        Percentage of heel breaks on PCB [%]: {round(percentage_1,2)}
        Percentage of bond peel on FE chip or PCB [%]: {round(percentage_3or4,2)}
        Percentage of bond peel < 7g [%]: {round(percentage_less7,2)}
        Data Unavailable: False
        Number of wires pulled: {len(grade_webApp)}
        Pull grades data array:
        
        (x,y) - x = failure grade, y = GAx location
        
        {organised_list(pull_strength_display,5)}

        Are you happy with these measurements? If yes, press Upload to ITk

        """)
    
    results["pulltest"] = {"pass_fail": pull_pass_fail,
                           "mean_pull": round(mean_pull,3),
                           "standard_deviation": round(standard_deviation,3),
                           "before5g_wires": before5g_wires,
                           "minimum_pull": round(minimum_pull,3),
                           "maximum_pull": round(maximum_pull,3),
                           "percentage_2": round(percentage_2,2),
                           "percentage_1": round(percentage_1,2),
                           "percentage_3or4": round(percentage_3or4,2),
                           "percentage_less7": round(percentage_less7,2),
                           "numberofwires": len(grade_webApp),
                           "pull_strength_data": pull_strength_data}
    
    results["component_id"] = component_id
    results["component"] = component
    results["token"] = "token"

    return results
    
def grade_mapping(grade):
    """
    Method designed to change the grading criteria for the upload
    and map it to the original grade list above
    """

    if grade >= 4:
        return grade - 1
    elif grade == 3:
        return 0
    else:
        return int(grade)

def organised_list(data,elements_per_row):
    rows = []
    for i in range(0,len(data),elements_per_row):
        row = data[i:i + elements_per_row]
        rows.append(' '.join(map(str,row)))
    return '\n        '.join(rows)

def combined_deviation(N_i,sigma_i,mean_i):
    """
    Calculates the standard deviation from combined variance of mutliple subsets
    """
    # Calcualte weighted mean of the subsets
    weighted_mean = sum([x*y for x,y in zip(N_i,mean_i)])/sum(N_i)
    # Calculate overall variance
    combined_variance = sum([x*((y**2)+(z-weighted_mean)**2) for x,y,z in zip(N_i,sigma_i,mean_i)])/sum(N_i)
    return math.sqrt(combined_variance)