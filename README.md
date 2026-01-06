# Eminder

Eminder is a personal assistant application which can schedualize tasks and will distribute notifications to designated destinations upon predefined timings. 
AI feature to schedualize tasks is included.


## Installation

* MySQL DB: The application is using a MySQL database to store tasks and recipients and more. There is an sql script file and also one MySQL workbench mwb-file with EER-model included, inside the dbmodel folder which can be utilized to set up a fit for purpose database.
* Integrations: To send mail, discord messages and to use AI feature, the application is using Google Gmail API, Discord webhook and Gemini API key. 

Please set the parameters properly in the .env file.

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

# Active venv. Note! /Scripts/ if Windows, /bin/ if Linux
source .venv/Scripts/activate

# Install the Eminder project
pip install -e .

# Start the application from anywhere inside project folder, just type eminder
eminder

# Alternatively
python3 -m eminder

# To start the scheduler service which is responsible for notification distribution, it's also possible to start is via the main menu:
python3 -m eminder:schedulerservice

# To uninstall the project:
pip uninstall eminder

```

## Usage

When starting the application a main menu is displayed where the user can make different choises.
Besides from this, the schedulemanager should be run as a service in the background to handle the distribution of the notifications!

