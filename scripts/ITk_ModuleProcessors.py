"""
(Flex/Bare/Assem)Processor - classes designed for processing raw data from .DAT metrology files of
the bare flex, bare module and assembled module. They contain methods of extracting data slices for each
required component parts and filtering out data points that are out of specs i.e. contaminants that do not
correspond to the actual component.
"""

def process_template(valid_rows,valid_row_inf,row2_data,all_data):

    pull_sum = 0

    if not valid_rows:
        raise ValueError(f"No valid rows found with {valid_row_inf} in the given data range.")
    
    # Calculating average z-value (flex height) for the valid set
    for row in valid_rows:
        pull_z = row[2]
        pull_sum += pull_z
    
    avg_z = pull_sum / len(valid_rows)
    avg_z = float(avg_z)

    # Filtering boundaries for the average z-value to remove any out-of-spec points
    for row in valid_rows:
        if ((avg_z * (1 - 0.00035)) < row[2] < (avg_z * (1 + 0.00035))):
            # Appending newly fileterd z-values to quad_data and all filtered xyz-values to flex_data for plotting
            row2_data.append(row[2])
            all_data.append([row[0],row[1],row[2]])

class FlexProcessor:

    def __init__(self, data):
        # Set of data list to store filtered values 
        self.data = data
        self.quad_data = []
        self.jig1_data = []
        self.jig2_data = []
        self.jig3_data = []
        self.flex_data = []
    
    def process_quad1(self):

        valid_rows = [row for row in self.data[-308:-3] if row[0] >= 159.0]
        valid_rows_inf = "row[0] >= 159.0"

        process_template(valid_rows,valid_rows_inf,self.quad_data,self.flex_data)
                                                                        
    def process_quad2(self):

        valid_rows = [row for row in self.data[-618:-309] if 146.0 < row[0] <= 158.0]
        valid_rows_inf = "146.0 < row[0] <= 158.0"

        process_template(valid_rows,valid_rows_inf,self.quad_data,self.flex_data)

    def process_quad3(self):

        valid_rows = [row for row in self.data[-945:-619] if 130.0 < row[0] <= 145.0]
        valid_rows_inf = "130.0 < row[0] <= 145.0"

        process_template(valid_rows,valid_rows_inf,self.quad_data,self.flex_data)

    def process_quad4(self):

        valid_rows = [row for row in self.data[-1278:-946] if row[0] >= 146.0]
        valid_rows_inf = "row[0] >= 146.0"

        process_template(valid_rows,valid_rows_inf,self.quad_data,self.flex_data)
    
    def process_jig1(self):
        
        valid_rows = [row for row in self.data[73:181] if row[1] > 180.0 and row[0] < 146.0]
        valid_rows_inf = "row[1] > 180.0 and row[0] < 146.0"

        process_template(valid_rows,valid_rows_inf,[],self.flex_data)
    
    def process_jig2(self):
        
        valid_rows = [row for row in self.data[180:382] if 181.0 < row[1] < 190.0 and 147.0 < row[0] < 157.0]
        valid_rows_inf = "181.0 < row[1] < 190.0 and 147.0 < row[0] < 157.0"

        process_template(valid_rows,valid_rows_inf,[],self.flex_data)

    def process_jig3(self):
        
        valid_rows = [row for row in self.data[381:563] if 133.0 < row[1] < 145.0 and 135.0 < row[0] < 155.0]
        valid_rows_inf = "133.0 < row[1] < 145.0 and 135.0 < row[0] < 155.0"

        process_template(valid_rows,valid_rows_inf,[],self.flex_data)

    # Calling fucntion to process everything above at once
    def process_all(self):
        self.process_quad1()
        self.process_quad2()
        self.process_quad3()
        self.process_quad4()
        self.process_jig1()
        self.process_jig2()
        self.process_jig3()

class BareProcessor:

    def __init__(self,data):
        self.data = data
        self.sensor_data = []
        self.fe1_data = []
        self.fe2_data = []
        self.fe3_data = []
        self.bare_data = []
    
    def process_sensor1(self):
        
        valid_rows = [row for row in self.data[-783:-1] if row[1] > 146.00]
        valid_rows_inf = "row[1] > 146.00"

        process_template(valid_rows,valid_rows_inf,self.sensor_data,self.bare_data)

    def process_sensor2(self):
       
        valid_rows = [row for row in self.data[-1919:-783] if row[0] < 148.00]
        valid_rows_inf = "row[0] < 148.00"

        process_template(valid_rows,valid_rows_inf,self.sensor_data,self.bare_data)

    def process_sensor3(self):
       
        valid_rows = [row for row in self.data[-3055:-1918] if row[1] > 158.00]
        valid_rows_inf = "row[1] > 158.00"

        process_template(valid_rows,valid_rows_inf,self.sensor_data,self.bare_data)

    def process_fe1(self):
        
        valid_rows = [row for row in self.data[-3854:-3054] if 147.00 < row[0] < 177.00 and 130.00 < row[1] < 162.00]
        valid_rows_inf = "147.00 < row[0] < 177.00 and 130.00 < row[1] < 162.00"

        process_template(valid_rows,valid_rows_inf,self.fe1_data,self.bare_data)

    def process_fe2(self):
        
        valid_rows = [row for row in self.data[-4006:-3853] if 126.00 < row[0] < 133.00 and 169.00 < row[1] < 176.00]
        valid_rows_inf = "126.00 < row[0] < 133.00 and 169.00 < row[1] < 176.00"

        process_template(valid_rows,valid_rows_inf,self.fe2_data,self.bare_data)

    def process_fe3(self):
        
        valid_rows = [row for row in self.data[-4156:-4005] if 140.00 < row[0] < 147.00 and 183.00 < row[1] < 191.00]
        valid_rows_inf = "140.00 < row[0] < 147.00 and 183.00 < row[1] < 191.00"

        process_template(valid_rows,valid_rows_inf,self.fe3_data,self.bare_data)

    def process_all(self):
        self.process_sensor1()
        self.process_sensor2()
        self.process_sensor3()
        self.process_fe1()
        self.process_fe2()
        self.process_fe3()
        self.full_z_data = self.sensor_data + self.fe1_data + self.fe2_data + self.fe3_data

class AssemProcessor:

    def __init__(self,data):
        self.data = data
        self.assem_quad1 = []
        self.assem_quad2 = []
        self.assem_quad3 = []
        self.assem_quad4 = []
        self.assem_fe1 = []
        self.assem_fe2 = []
        self.assem_fe3 = []
        self.assem_data = []

    def process_assem_q1(self):

        valid_rows = [row for row in self.data[-829:-566] if 160.00 < row[0] < 162.00 and 159.00 < row[1] < 161.00]
        valid_rows_inf = "160.00 < row[0] < 162.00 and 159.00 < row[1] < 161.00"

        process_template(valid_rows,valid_rows_inf,self.assem_quad1,self.assem_data)

    def process_assem_q2(self):

        valid_rows = [row for row in self.data[-1085:-827] if 147.00 < row[0] < 149.00 and 146.00 < row[1] < 148.00]
        valid_rows_inf = "147.00 < row[0] < 149.00 and 146.00 < row[1] < 148.00"

        process_template(valid_rows,valid_rows_inf,self.assem_quad2,self.assem_data)
               
    def process_assem_q3(self):

        valid_rows = [row for row in self.data[-1331:-1081] if 131.00 < row[0] < 133.00 and 159.00 < row[1] < 160.00]
        valid_rows_inf = "131.00 < row[0] < 133.00 and 159.00 < row[1] < 160.00"

        process_template(valid_rows,valid_rows_inf,self.assem_quad3,self.assem_data)

    def process_assem_q4(self):

        valid_rows = [row for row in self.data[-1582:-1328] if 147.00 < row[0] < 148.00 and 172.00 < row[1] < 174.00]
        valid_rows_inf = "147.00 < row[0] < 148.00 and 172.00 < row[1] < 174.00"
        
        process_template(valid_rows,valid_rows_inf,self.assem_quad4,self.assem_data)

    def process_assem_fe1(self):

        valid_rows = [row for row in self.data[-1809:-1605] if 138.00 < row[0] < 146.00 and 133.00 < row[1] < 141.00]
        valid_rows_inf = "138.00 < row[0] < 146.00 and 133.00 < row[1] < 141.00"

        process_template(valid_rows,valid_rows_inf,self.assem_fe1,self.assem_data)

    def process_assem_fe2(self):
        
        valid_rows = [row for row in self.data[-2150:-1806] if 118.00 < row[0] < 132.00 and 147.00 < row[1] < 160.00]
        valid_rows_inf = "118.00 < row[0] < 132.00 and 147.00 < row[1] < 160.00"

        process_template(valid_rows,valid_rows_inf,self.assem_fe2,self.assem_data)

    def process_assem_fe3(self):

        valid_rows = [row for row in self.data[-2391:-2147] if 147.00 < row[0] < 157.00 and 180.00 < row[1] < 189.00]
        valid_rows_inf = "147.00 < row[0] < 157.00 and 180.00 < row[1] < 189.00"

        process_template(valid_rows,valid_rows_inf,self.assem_fe3,self.assem_data)

    def process_all(self):
        self.process_assem_q1()
        self.process_assem_q2()
        self.process_assem_q3()
        self.process_assem_q4()
        self.process_assem_fe1()
        self.process_assem_fe2()
        self.process_assem_fe3()
        self.assem_quad = self.assem_quad1 + self.assem_quad2 + self.assem_quad3 + self.assem_quad4