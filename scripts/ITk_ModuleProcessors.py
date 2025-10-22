"""
(Flex/Bare/Assem)Processor - classes designed for processing raw data from .DAT metrology files of
the bare flex, bare module and assembled module. They contain methods of extracting data slices for each
required component parts and filtering out data points that are out of specs i.e. contaminants that do not
correspond to the actual component.
"""
from statistics import median

def process_template(valid_rows,valid_row_inf):

    if not valid_rows:
        raise ValueError(f"No valid rows found with {valid_row_inf} in the given data range.")
    
    # Median Absolute Deviation
    z_values = [row[2] for row in valid_rows]
    m = median(z_values)
    mad = median(abs(z - m) for z in z_values)

    row2_data = [row[2] for row in valid_rows if abs(row[2] - m) <= 3 * mad]
    all_data = [row for row in valid_rows if abs(row[2] - m) <= 3 * mad]

    return row2_data, all_data

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

        self.quad_data, self.flex_data = process_template(valid_rows,valid_rows_inf)
                                                                        
    def process_quad2(self):

        valid_rows = [row for row in self.data[-618:-309] if 146.0 < row[0] <= 158.0]
        valid_rows_inf = "146.0 < row[0] <= 158.0"

        self.quad_data, self.flex_data = process_template(valid_rows,valid_rows_inf)

    def process_quad3(self):

        valid_rows = [row for row in self.data if 130.0 < row[0] < 140.0 and 155.0 < row[1] < 170.0]
        valid_rows_inf = "130.0 < row[0] <= 145.0 and 155.0 < row[1] < 170.0"

        self.quad_data, self.flex_data = process_template(valid_rows,valid_rows_inf)

    def process_quad4(self):

        valid_rows = [row for row in self.data[-1278:-946] if row[0] >= 146.0]
        valid_rows_inf = "row[0] >= 146.0"

        self.quad_data, self.flex_data = process_template(valid_rows,valid_rows_inf)
    
    def process_jig1(self):
        
        valid_rows = [row for row in self.data[785:899] if row[1] > 180.0 and row[0] < 146.0]
        valid_rows_inf = "row[1] > 180.0 and row[0] < 146.0"

        self.jig1_data, self.flex_data = process_template(valid_rows,valid_rows_inf)
    
    def process_jig2(self):
        
        valid_rows = [row for row in self.data if 181.0 < row[1] < 190.0 and 148.0 < row[0] < 157.0]
        valid_rows_inf = "181.0 < row[1] < 190.0 and 148.0 < row[0] < 157.0"

        self.jig2_data, self.flex_data = process_template(valid_rows,valid_rows_inf)

    def process_jig3(self):
        
        valid_rows = [row for row in self.data if 134.0 < row[1] < 150.0 and 135.0 < row[0] < 150.0]
        valid_rows_inf = "134.0 < row[1] < 150.0 and 135.0 < row[0] < 150.0"

        self.jig3_data, self.flex_data = process_template(valid_rows,valid_rows_inf)

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
        self.fe_data = []
        self.bare_data = []
    
    def process_sensor1(self):
        
        valid_rows = [row for row in self.data if 132 < row[0] < 161 and 146 < row[1] < 175]
        valid_rows_inf = "132 < row[0] 161 and 146 < row[1] < 175"

        self.sensor_data, self.bare_data = process_template(valid_rows,valid_rows_inf)

    def process_sensor2(self):
       
        valid_rows = [row for row in self.data if 146 < row[0] < 148 and 132 < row[1] < 189]
        valid_rows_inf = "146 < row[0] < 148 and 132 < row[1] < 189"

        self.sensor_data, self.bare_data = process_template(valid_rows,valid_rows_inf)

    def process_sensor3(self):
       
        valid_rows = [row for row in self.data if 118 < row[0] < 176 and 159 < row[1] < 162]
        valid_rows_inf = "118 < row[0] < 176 and 159 < row[1] < 162"

        self.sensor_data, self.bare_data = process_template(valid_rows,valid_rows_inf)

    def process_fe1(self):
        
        valid_rows = [row for row in self.data if 147 < row[0] < 177 and 130 < row[1] < 162]
        valid_rows_inf = "147.00 < row[0] < 177.00 and 130.00 < row[1] < 162.00"

        self.fe_data, self.bare_data = process_template(valid_rows,valid_rows_inf)

    def process_fe2(self):
        
        valid_rows = [row for row in self.data if 126 < row[0] < 132 and 169 < row[1] < 176]
        valid_rows_inf = "126.00 < row[0] < 133.00 and 169.00 < row[1] < 176.00"

        self.fe_data, self.bare_data = process_template(valid_rows,valid_rows_inf)

    def process_fe3(self):
        
        valid_rows = [row for row in self.data if 140 < row[0] < 147 and 183 < row[1] < 191]
        valid_rows_inf = "140.00 < row[0] < 147.00 and 183.00 < row[1] < 191.00"

        self.fe_data, self.bare_data = process_template(valid_rows,valid_rows_inf)

    def process_all(self):
        self.process_sensor1()
        self.process_sensor2()
        self.process_sensor3()
        self.process_fe1()
        self.process_fe2()
        self.process_fe3()
        self.full_z_data = self.sensor_data + self.fe_data

class AssemProcessor:

    def __init__(self,data):
        self.data = data
        self.assem_ga1 = []
        self.assem_ga2 = []
        self.assem_ga3 = []
        self.assem_ga4 = []
        self.assem_sens1 = []
        self.assem_sens2 = []
        self.assem_sens3 = []
        self.assem_data = []

    def process_assem_ga1(self):

        valid_rows = [row for row in self.data if 136.00 < row[0] < 138.00 and 159.00 < row[1] < 161.00]
        valid_rows_inf = "136.00 < row[0] < 138.00 and 159.00 < row[1] < 161.00"

        self.assem_ga1, self.assem_data = process_template(valid_rows,valid_rows_inf)

    def process_assem_ga2(self):

        valid_rows = [row for row in self.data if 147.00 < row[0] < 151.00 and 148.00 < row[1] < 152.00]
        valid_rows_inf = "147.00 < row[0] < 151.00 and 148.00 < row[1] < 152.00"

        self.assem_ga2, self.assem_data = process_template(valid_rows,valid_rows_inf)
               
    def process_assem_ga3(self):

        valid_rows = [row for row in self.data if 158.00 < row[0] < 162.00 and 158.00 < row[1] < 162.00]
        valid_rows_inf = "158.00 < row[0] < 162.00 and 158.00 < row[1] < 162.00"

        self.assem_ga3, self.assem_data = process_template(valid_rows,valid_rows_inf)

    def process_assem_ga4(self):

        valid_rows = [row for row in self.data if 146.00 < row[0] < 149.00 and 172.00 < row[1] < 174.00]
        valid_rows_inf = "147.00 < row[0] < 149.00 and row[1] > 172.00"
        
        self.assem_ga4, self.assem_data = process_template(valid_rows,valid_rows_inf)

    def process_assem_sens1(self):

        valid_rows = [row for row in self.data if 118.00 < row[0] < 132.00 and 147.00 < row[1] < 160.00]
        valid_rows_inf = "138.00 < row[0] < 146.00 and 133.00 < row[1] < 141.00"

        self.assem_sens1, self.assem_data = process_template(valid_rows,valid_rows_inf)

    def process_assem_sens2(self):
        
        valid_rows = [row for row in self.data if 137.00 < row[0] < 146.00 and 132.00 < row[1] < 142.00]
        valid_rows_inf = "137.00 < row[0] < 146.00 and row[1] < 142.00"

        self.assem_sens2, self.assem_data = process_template(valid_rows,valid_rows_inf)

    def process_assem_sens3(self):

        valid_rows = [row for row in self.data if 147.00 < row[0] < 157.00 and 179.00 < row[1] < 190.00]
        valid_rows_inf = "147.00 < row[0] and 179.00 < row[1]"

        self.assem_sens3, self.assem_data = process_template(valid_rows,valid_rows_inf)

    def process_all(self):
        self.process_assem_ga1()
        self.process_assem_ga2()
        self.process_assem_ga3()
        self.process_assem_ga4()
        self.process_assem_sens1()
        self.process_assem_sens2()
        self.process_assem_sens3()
        self.assem_quad = self.assem_ga1 + self.assem_ga2 + self.assem_ga3 + self.assem_ga4