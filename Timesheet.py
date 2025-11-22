import random
import os
import pickle
import datetime
from Employee import Employee_data_file
from Client import Client_data_file
from Tasks import Task_data_file

script_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(script_folder, "Data")
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
Timesheet_data_file = os.path.join(data_folder, "Timesheet_data_file.txt")

class Timesheet:
    def __init__(self, timesheet_id, timesheet_date, employee_id, client_id, task_id, hours):
        self.timesheet_id = timesheet_id
        self.timesheet_date = timesheet_date
        self.employee_id = employee_id
        self.client_id = client_id
        self.task_id = task_id
        self.hours = hours
    
    def upload_timesheet(self):
        try:
            with open(Timesheet_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        data[self.timesheet_id] = [self.timesheet_id, self.timesheet_date, self.employee_id, self.client_id, self.task_id, self.hours]
        with open(Timesheet_data_file, "wb") as write_file:
            pickle.dump(data, write_file)
        print("Timesheet uploaded successfully" + self.timesheet_id)
        return True

    @staticmethod
    def updateTimesheet(timesheet_id):
        try:
            with open(Timesheet_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if (timesheet_id) in data.keys():
            timesheet_date = data.get(timesheet_id)[1]
            employee_id = None
            client_id = input("Enter the client id: ")
            task_id = input("Enter the task id: ")
            hours = int(input("Enter the hours: "))
            validated = validateTimesheetInputs(timesheet_date, client_id, task_id, hours)
            if not validated:
                return False
            with open(Timesheet_data_file, "wb") as write_file:
                data[timesheet_id] = [timesheet_date, employee_id, client_id, task_id, hours]
                pickle.dump(data, write_file)
            print("Timesheet updated successfully")
            return True
        else:
            print("Timesheet not found")
            return False
        
    @staticmethod
    def searchTimesheet(timesheet_id):
            try:
                with open(Timesheet_data_file, "rb") as read_file:
                    data = pickle.load(read_file)
                    if not isinstance(data, dict):
                        data = {}
            except (FileNotFoundError, EOFError):
                data = {}
            if (timesheet_id) in data.keys():
                return data.get(timesheet_id)
            else:
                return "The timesheet with id: " + timesheet_id + " not found in the system"

    @staticmethod
    def showAllTimesheets():
        try:
            with open(Timesheet_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                        data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        return data

    @staticmethod
    def createTimesheet():
            timesheet_id = genTimesheetId()
            timesheet_date = (datetime.datetime.now().strftime("%Y/%m/%d"))
            employee_id = input("Enter the employee id: ")
            client_id = input("Enter the client id: ")
            task_id = input("Enter the task id: ")
            hours = input("Enter the hours: ")
            validated = validateTimesheetInputs(timesheet_date, client_id, task_id, hours, employee_id)
            if not validated:
                return None
            timesheet = Timesheet(timesheet_id, timesheet_date, employee_id, client_id, task_id, hours)
            upload = timesheet.upload_timesheet()
            if upload:
                return timesheet_id
            return None
        

def genTimesheetId():
    return "TMS_" + str(random.randint(100000, 999999))

def validateTimesheetInputs(timesheet_date, client_id, task_id, hours, employee_id=None):
    try:
        with open(Employee_data_file, "rb") as employee_file, open(Client_data_file, "rb") as client_file, open(Task_data_file, "rb") as task_file:
            employee_data = pickle.load(employee_file)
            client_data = pickle.load(client_file)
            task_data = pickle.load(task_file)
            if not isinstance(employee_data, dict):
                employee_data = {}
            if not isinstance(client_data, dict):
                client_data = {}
            if not isinstance(task_data, dict):
                task_data = {}
    except (FileNotFoundError, EOFError):
        employee_data = {}
        client_data = {}
        task_data = {}
    if (employee_id) not in employee_data.keys() and employee_id is not None:
        print("Employee not found")
        return False
    
    if (client_id) not in client_data.keys():
        print("Client not found")
        return False
    
    if (task_id) not in task_data.keys():
        print("Task not found")
        return False
    
    if int(hours) > 8:
        print("Hours should not be more than 8")
        return False
    return True


