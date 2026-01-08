# Eminder

Eminder is a personal assistant application which can schedualize tasks and will distribute notifications to designated destinations upon predefined timings. 
It includes an AI-powered feature to automatically create and schedualize tasks based on user input.

## Installation

* MySQL DB: The application is using a MySQL database to store tasks and recipients and more. There is an sql script file and also one MySQL workbench mwb-file with EER-model included, inside the dbmodel folder which can be utilized to set up a fit for purpose database.
* Integrations: To send mail, discord messages and to use AI feature, the application is using Google Gmail API, Discord webhook and Gemini API key. 

Please set the parameters properly in the .env file. There is an .env.template file provided in the root folder, please rename to .env and enter your own details.

Prerequisites
```bash
Python 3.10+
MySQL server installed on the machine that will host the DB
API keys for Gmail, Discord, and Gemini to use integration functions
```

To set up db:
```bash
# Example on how to create the database on a Linux machine with MySQl
mysql -u root < Eminder/dbmodel/EminderSchedulerDB.sql

# Example on how to create a db-user and grant privileges to the db. The details can then be entered into the .env file so the application can connect..
CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON EminderSchedulerDB.* TO 'user'@'localhost';
```

To install the Python applicaton:
```bash
# Set up a virtual environment (venv). Not mandatory but recommended.
python3 -m venv .venv

# Activate venv. Note! .venv/Scripts/activate if Windows, .venv/bin/activate if Linux
source .venv/bin/activate

# Install the Eminder project
pip install -e .

# Start the application from anywhere inside project folder, just type eminder
eminder

# Alternatively
python3 -m eminder

# To start the scheduler service which is responsible for notification distribution, it's also possible to start via the main menu:
python3 -m eminder:schedulerservice

# To uninstall the project:
pip uninstall eminder
```

## Usage

When starting the application a main menu is displayed where the user can make different choices, for example create tasks and connect them to designated recipients. 
The tasks will be delivered to the recipients upon desired trigger time.
The available types is: once, daily, weekly, monthly, interval, yearly.
There is a feature to let AI create the tasks based on user input which is very powerful.

Besides from this, one instance of the schedulemanager should be run as a service in the background which will handle the trigger checks and distribution of notifications!

The application also generates a performance report measuring operation times and generates files in the reports folder.
There is a logger that records relevant actions and generates .txt files which are located in the logs folder.

## Project structure
```bash
├── dbmodel
│   ├── EminderSchedulerDB.mwb
│   └── EminderSchedulerDB.sql
├── logs
├── reports
├── src
│   └── eminder
│       ├── analysis
│       │   ├── __init__.py
│       │   └── performance.py
│       ├── db
│       │   ├── __init__.py
│       │   └── dbactions.py
│       ├── integrations
│       │   ├── __init__.py
│       │   ├── aimanager.py
│       │   ├── discord_out.py
│       │   └── mail_out.py
│       ├── services
│       │   ├── __init__.py
│       │   ├── recipientmanager.py
│       │   ├── reports.py
│       │   ├── schedulemanager.py
│       │   └── taskmanager.py
│       ├── utils
│       │   ├── __init__.py
│       │   └── logger.py
│       ├── validation
│       │   ├── __init__.py
│       │   └── inputvalidation.py
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── main.py
│       └── schedulerservice.py
├── .env.template
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Ideas for the future

* User management system 
* Web front with navigation and extended functionality
* Application published and hosted publicly

## License
MIT License
```bash
Copyright (c) 2026 Emil Sjokvist

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
