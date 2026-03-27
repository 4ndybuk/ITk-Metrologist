# ITk Metrologist
Processing and inspection tool for ATLAS ITk module production. Enables automated submission of raw metrology and wirebonding data
to the Production Database as well as component inspection functionalities to validate assembly correctness. 

## Details
![itkdb](https://img.shields.io/badge/itkdb-0.6.17-brightgreen)  
![PySide6](https://img.shields.io/badge/PySide6-6.10.0-brightgreen)  
![Plotly](https://img.shields.io/badge/Plotly-6.3.1-brightgreen)  
![License](https://img.shields.io/badge/license-GPLv3.0-blue)  

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Acknowledgments](#acknowledgments)
- [License](#license) 

## Installation
1. **Clone the repository**
```bash
   git clone https://github.com/4ndybuk/ITk-Metrologist.git
   cd ITk-Metrologist
```
2. **Install dependencies**
```bash
   pip install -r requirements.txt
```
3. **Set up credentials**  
• Obtain a credentials.json file (Google Sheets API), or use your own  
• Place the file in the assets/ directory  
4. **Run the application**
```bash
   python main.py
```

## Usage
1. The program requires an existing account to the ITk Production Database, use both access codes to login
2. To make the login process easier, Open the ⚙️  in the toolbar, store your passwords in the env file and save it
3. Have your bluetooth QR/barcode connected to the device to be used for the "Scan Components" feature

## Features
1. **Metrology Data Pipeline** - 
Parse .STA and .DAT files and upload extracted measurements to the ATLAS production database as component test records.
2. **3D Visualisation Tools** - 
Generate interactive 3D plots of pixel components (pre- and post-processing) to indetify spatial inconsistencies and defects.
3. **Wirebonding Data Integration** - 
Process wirebonding datasets and automate structured uploads to the production database.
4. **IREF Trim Bit Analysis** - 
Retrieve IREF trim bit values from bare modules and provide graphical visualisation of FE chip orinetation prior to assembly.
5. **Component Management Interface** - 
Custom table system for efficient component organisation, supporting both barcode scanner input and manual entry workflows.
6. **Integrated Project Toolbar** - 
Dockable toolbar with quick access to project-relevant tools, dashboards, and resources.
## Acknowledgments
1. Thanks to Pixel perfect, zafdesign, Freepik and Stockio from www.flaticon.com for Icons
2. GUI designed using QT Framework for Python - PySide6
3. Program powered by itkdb - ITk Production Database API wrapper
4. Graphical plots by Plotly - www.plotly.com

## License
1. This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
