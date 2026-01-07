# Eminder

Eminder is a personal assistant application which can schedualize tasks and will distribute notifications to designated destinations upon predefined timings. 
AI feature to schedualize tasks is included.


## Installation

* MySQL DB: The application is using a MySQL database to store tasks and recipients and more. There is an sql script file and also one MySQL workbench mwb-file with EER-model included, inside the dbmodel folder which can be utilized to set up a fit for purpose database.
* Integrations: To send mail, discord messages and to use AI feature, the application is using Google Gmail API, Discord webhook and Gemini API key. 

Please set the parameters properly in the .env file. There is an .env.template file provided in the root folder, please rename to .env and enter your own details.

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

# Ideas for the future

* User management system 

* Web front

* Application published publicly