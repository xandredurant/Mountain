# Mountain Sprint

![Mountain Sprint Demo](demo.gif)

Mountain Sprint is a Python application that simulates the flow of water down a mountain. This project was developed as a part of the CTU First Year Project.

## Overview

This application retrieves data points from text files, loads them into a database, and then from the database draws a top-down view of a mountain using the data points. The program then simulates how water would run down the mountain, providing an interesting visual representation.

## Project Structure

The project is organized as follows:

mountain/
│
├── App/
│ ├── CreateDb.sql
│ └── mountain.py
│
└── Data/
├── logo.png
├── large.txt
├── medium.txt
├── small.txt
└── trivial.txt

- **App/**: Contains application-related files.
  - `CreateDb.sql`: SQL script to create the database, tables, and fields.
  - `mountain.py`: The main Python script for the Mountain Sprint application.

- **Data/**: Contains data files used by the application.
  - `logo.png`: Logo or image used in the project.
  - `large.txt`, `medium.txt`, `small.txt`, `trivial.txt`: Text files containing data points for the mountain simulation.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server/sql-server-downloads) installed and running.
- [Python 3.x](https://www.python.org/downloads/) installed on your machine.

## Installation

Follow these steps to set up and run the Mountain Sprint application:

1. Clone the repository:

   ```shell
   git clone https://github.com/xandredurant/Mountain
   
2. Navigate to the project directory:
    cd mountain

3. Create a virtual environment (optional but recommended):
    python -m venv venv
    source venv/bin/activate

4. Install Python dependencies:
    pip install pyodbc pyqt5

5. Open App/mountain.py in a text editor of your choice and locate the following line:
    self.cnxn_str = ("DSN=MySQLServer;"
                 "SERVER=DESKTOP-EFKRIC4;"
                 "Database=MountainDb;"
                 "Trusted_Connection=yes;")
                 
  Modify the self.cnxn_str line with your specific SQL Server connection details. Replace SERVER, Database, and other   parameters with your SQL Server configuration.  

6. Execute the SQL script to set up the database:
    sqlcmd -S your-server-name -d your-database-name -U your-username -P your-password -i App/CreateDb.sql

7. Run the Mountain Sprint application:
    python App/mountain.py

## Contributing
If you would like to contribute to this project or report issues, please follow the contributing guidelines.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
