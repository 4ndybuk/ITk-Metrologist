# ITk Metrologist
Multifunctional program designed for data analysis, management and automation within CERN's Inner Tracker Pixel Core Assembly.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Acknowledgments](#acknowledgments)
- [License](#license) ![License](https://img.shields.io/badge/license-GPLv3.0-blue)

## Installation
1. Ensure that you have the latest version of Python on your device - Link: https://www.python.org/downloads/
2. In the Python folder, open Python Launcher and ensure that you have the interpreter path set and "Allow override with #! in script" is left unchecked
3. Run the "Install Packages.py" file which will install all the required dependencies
4. Use "main.py" to run the program at any times

## Usage
1. The program requires an existing account to the ITk Production Database, use both passwords to login
2. To make the login process easier, Open the ⚙️ in the toolbar, store your passwords in the file and save it
3. Have your bluetooth QR/barcode connected to the device to be used for the "Scan Components" feature

## Features
1. Metrology - Analyses data obtained from each of the pixel assembly stages: Hybrid Flex, Bare Module and Assembled Module. Takes .DAT and .STA file as inputs, displays information on the custom logger and allows uploads to the production database and Google sheets
2. Wirebonding - Analyses data obtained from the wirebond pull tests. Takes .CSV file as an input, displays information on the custom logger and allows upload to the production database only
3. IREF Fetcher - Retrieves information from the database about the IREF bit values of bare modules and displays the chip orientations based on their hexadecimal encoding
4. Scan Components - Stores QR/barcode scanned components in a table for more efficient list organsiation and instant access to the component's profile in the production database

## Acknowledgments
1. Thanks to Pixel perfect (gear), zafdesign (webApp), Freepik (information and gsheets) and Stockio (database) from www.flaticon.com for Icons
2. Program designed using QT Framework for Python - PySide6 (https://img.shields.io/badge/PySide6-6.7.2-brightorange)
3. Program powered by itkdb - ITk Production Database wrapper API (https://img.shields.io/badge/itkdb-0.6.8-brightorange)

## License
1. This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
