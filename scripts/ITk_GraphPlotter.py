import logging
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from ITk_Importers import acquire_data 
import os 
import re
from ITk_ModuleProcessors import *
from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import Qt

def graph_plot(dat_path):
    
    plot_data = acquire_data(dat_path)
    file_basename = os.path.basename(dat_path)
    component_id = file_basename[:14]

    # Specifying unprocessed and processed data for each assembly component
    if re.match(r"^([a-z0-9]+)_vc3_bare_flex_metrology\.DAT", file_basename, re.IGNORECASE):

        # Processed data and points
        processor = FlexProcessor(plot_data)
        processor.process_all()
        process_points = np.array(processor.flex_data)

        x2 = process_points[:-3,0]
        y2 = process_points[:-3,1]
        z2 = process_points[:-3,2]

        # Unprocessed data and points
        points = np.array(plot_data)

        x = points[:-3,0]
        y = points[:-3,1]
        z = points[:-3,2]

        # Data points colour for the graph traces
        map_color = "blue"
        
    elif re.match(r"^([a-z0-9]+)_vc3_bare_module_metrology\.DAT", file_basename, re.IGNORECASE):

        processor = BareProcessor(plot_data)
        processor.process_all()
        process_points = np.array(processor.bare_data)
        
        x2 = process_points[0:,0]
        y2 = process_points[0:,1]
        z2 = process_points[0:,2]

        points_data = [row for row in plot_data if row[1] > 0.0 and row[2] > 50.0]
        points = np.array(points_data)
        
        x = points[0:,0]
        y = points[0:,1]
        z = points[0:,2]

        map_color = "green"

    elif re.match(r"^([a-z0-9]+)_vc3_assembled_module_metrology\.DAT", file_basename, re.IGNORECASE):

        processor = AssemProcessor(plot_data)
        processor.process_all()
        process_points = np.array(processor.assem_data)

        x2 = process_points[0:,0]
        y2 = process_points[0:,1]
        z2 = process_points[0:,2]

        points = np.array(plot_data)

        x = points[0:,0]
        y = points[0:,1]
        z = points[0:,2]

        map_color = "red"

    else:
        print("Incorrect file type - Please choose the right .DAT file")
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
        QMessageBox.critical(None,"Error", "Incorrect file type\n\nPlease choose the right .DAT file",
                             QMessageBox.Ok)
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, False)

    # Initialising figure with subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scatter3d"}, {"type": "scatter3d"}]], 
                        subplot_titles=(f"{component_id} - Unprocessed Data",f"{component_id} - Processed Data"))
    
    # Adding 3D scatter traces for unprocessed and processed data 
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', name="Unprocessed", marker= dict(size=10, color="orange", opacity=0.8)), row=1, col=1)
    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z2, mode='markers',name="Processed", marker=dict(size=10, color=map_color, opacity=0.8)), row=1, col=2)

    # Configuring X,Y and Z axes for their range and title
    # Unprocessed plot
    fig.update_layout(scene=dict(xaxis = dict(nticks = 4, range=[120, 195], title = 'X - COORDINATES'),
                                 yaxis = dict(nticks = 4, range=[120, 193], title = 'Y - COORDINATES'),
                                 zaxis = dict(nticks = 4, range=[53, 55], title = 'Z - HEIGHT')))
    # Processed plot
    fig.update_layout(scene2=dict(xaxis = dict(nticks = 4, range=[120, 195], title = 'X - COORDINATES'),
                                  yaxis = dict(nticks = 4, range=[120, 193], title = 'Y - COORDINATES'),
                                  zaxis = dict(nticks = 4, range=[53, 55], title = 'Z - HEIGHT')))

    logging.info(f"""
                    
                    Metrology plot for {file_basename} has been created
                    
                    """)
    
    # Display the plots
    fig.show()