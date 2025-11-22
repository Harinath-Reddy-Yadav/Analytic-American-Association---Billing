import pickle
import os
import random
import re
from Employee import Employee, Employee_data_file
from Client import Client, Client_data_file
from Timesheet import Timesheet, Timesheet_data_file
from Tasks import Task, Task_data_file
import datetime
import sys

script_folder = os.path.dirname(os.path.abspath(__file__))
employee_invoice_path = os.path.join(script_folder, "employee_bill.txt")
client_invoice_path = os.path.join(script_folder, "client_bill.txt")

def generateEmployeeBill():
    Id = input("Enter the employee id: ")
    if not Id.startswith("EMP_"):
        return "Invalid Employee Id"
    with open(Timesheet_data_file, "rb") as time_file, open(Employee_data_file, "rb") as emp_file:
        time_data = pickle.load(time_file)
        emp_data = pickle.load(emp_file)
        if not isinstance(time_data, dict):
            time_data = {}
        if not isinstance(emp_data, dict):
            emp_data = {}
    total_hours = 0
    count = 0
    for value in time_data.values():
        if Id in value:
            today_date = datetime.datetime.now().strftime("%Y/%m/%d")
            if value[1] <= today_date and value[2] == Id:
                total_hours += int(value[-1])
                count += 1
    if count == 0:
        return "The Employee Id not found"
    with open(employee_invoice_path, "w") as write_file:
        employee_info = Employee.searchEmployee(Id)
        employee_name = employee_info[0]
        employee_bill_rate = employee_info[1]
        write_file.write("-> Analytic American Association <-".center(100, "-"))
        write_file.write("\n\n\n")
        write_file.write("Employee Invoice".center(100, "-"))
        write_file.write("\n\n\n")
        write_file.write(" ".ljust(10, " ") + "Employee Id "+ " ".rjust(50, " ") + ": "+ Id+"\n")
        write_file.write(" ".ljust(10, " ") + "Employee Name "+ " ".rjust(50, " ") + ": "+ employee_name+"\n")
        write_file.write(" ".ljust(10, " ") + "Employee Bill Rate "+ " ".rjust(50, " ") + ": "+ employee_bill_rate+"\n")
        write_file.write(" ".ljust(10, " ") + "Employee Total Hours "+ " ".rjust(50, " ") + ": "+ str(total_hours)+"\n")
        write_file.write("-".center(100, "-"))
        write_file.write("\n")
        write_file.write(" ".ljust(10, " ") + "Employee Total Bill "+ " ".rjust(50, " ") + ": "+ str(total_hours * int(employee_bill_rate.strip("$")))+"\n")
    return "Employee Bill Generated Successfully"

def generateClientBill():
    Id = input("Enter the client id: ")
    if not Id.startswith("CLT_"):
        return "Invalid Client Id"
    with open(Timesheet_data_file, "rb") as time_file, open(Client_data_file, "rb") as client_file:
        time_data = pickle.load(time_file)
        client_data = pickle.load(client_file)
        if not isinstance(time_data, dict):
            time_data = {}
        if not isinstance(client_data, dict):
            client_data = {}
    total_hours = 0
    for value in time_data.values():
        if Id in value:
            today_date = datetime.datetime.now().strftime("%Y/%m/%d")
            if value[1] <= today_date and value[2] == Id:
                total_hours += int(value[-1])
        else :
            print("The Client Id not found")
    with open(client_invoice_path, "w") as write_file:
        client_info = Client.searchClient(Id)
        client_name = client_info[0]
        client_bill_rate = client_info[2]
        write_file.write("-> Analytic American Association <-".center(100, "-"))
        write_file.write("\n\n\n")
        write_file.write("Client Invoice".center(100, "-"))
        write_file.write("\n\n\n")
        write_file.write("Client Id ".rjust(20, " ") + ": "+ Id+"\n")
        write_file.write("Client Name ".rjust(20, " ") + ": "+ client_name+"\n")
        write_file.write("Client Bill Rate ".rjust(20, " ") + ": "+ client_bill_rate+"\n")
        write_file.write("Client Total Hours ".rjust(20, " ") + ": "+ str(total_hours)+"\n")
        write_file.write("-".center(100, "-"))
        write_file.write("\n")
        write_file.write(" ".ljust(20, " ") + "Client Total Bill "+ " ".rjust(50, " ") + ": "+ str(total_hours * client_bill_rate)+"\n")
    return "Client Bill Generated Successfully"

def main():
    employee_bulk_file = "Employee.csv"
    client_bulk_file = "Clients.csv"
    task_bulk_file = "tasks.csv"
    while True:
        print("-> Analytic American Association <-".center(80, "-"))
        print(" ".rjust(30), "1. Employee")
        print(" ".rjust(30), "2. Client")
        print(" ".rjust(30), "3. Tasks")
        print(" ".rjust(30), "4. Timesheet")
        print(" ".rjust(30), "5. Billing")
        print(" ".rjust(30), "6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            employees(employee_bulk_file)
        elif choice == "2":
            clients(client_bulk_file)
        elif choice == "3":
            tasks(task_bulk_file)
        elif choice == "4":
            timesheets()
        elif choice == "5":
            print(" ".rjust(30), "1. Generate Employee Bill")
            print(" ".rjust(30), "2. Generate Client Bill")
            print(" ".rjust(30), "3. Back")
            print(" ".rjust(30), "4. Exit")
            billing_choice = input("Enter your choice: ")
            if billing_choice == "1":
                print(generateEmployeeBill())
            elif billing_choice == "2":
                print(generateClientBill())
            elif billing_choice == "3":
                break
            elif billing_choice == "4":
                sys.exit()
            else:
                print("Invalid choice")
        elif choice == "6":
            sys.exit()
        else:
            print("Invalid choice")

def tasks(task_bulk_file):
    while True:
        print(" ".rjust(30), "1. Create a new Task")
        print(" ".rjust(30), "2. Update a Task")
        print(" ".rjust(30), "3. Delete a Task")
        print(" ".rjust(30), "4. Search a Task")
        print(" ".rjust(30), "5. Show all Tasks")
        print(" ".rjust(30), "6. Bulk upload Tasks")
        print(" ".rjust(30), "7. Back")
        print(" ".rjust(30), "8. Exit")
        task_choice = input("Enter your choice: ")
        if task_choice == "1":
            task_id = Task.createtask()
            if task_id:
                print("Task created successfully with id: ", task_id)
            else:
                print("Task creation failed")
        elif task_choice == "2":
            task_id = input("Enter the task id: ")
            updated_task = Task.update_task(task_id)
            if updated_task:
                print("Task updated successfully. please find updated details below")
                Task.search_task(updated_task)
            else:
                print("Task update failed")
        elif task_choice == "3":
            task_id = input("Enter the task id: ")
            deleted_task = Task.delete_task(task_id)
            if deleted_task:
                print("Task deleted successfully with id: ", task_id)
            else:
                print("Task deletion failed")
        elif task_choice == "4":
            task_id = input("Enter the task id: ")
            task_data = Task.search_task(task_id)
            if task_data:
                print(task_data)
            else:
                print("Task search failed")
        elif task_choice == "5":
            tasks_data = Task.ShowAllTasks()
            if tasks_data:
                for key, value in tasks_data.items():
                    print(key, value , sep=" : ")
            else:
                print("no tasks are available in the system")
        elif task_choice == "6":
            Task.task_bulk_upload(task_bulk_file)
            print("Bulk upload completed successfully")
        elif task_choice == "7":
            break
        elif task_choice == "8":
            sys.exit()
        else:
            print("Invalid choice")

def timesheets():
    while True:
        print(" ".ljust(30), "1. Fill the Timesheet")
        print(" ".ljust(30), "2. Update the Timesheet")
        print(" ".ljust(30), "3. Search the Timesheet")
        print(" ".ljust(30), "4. Show all Timesheets")
        print(" ".ljust(30), "5. Back")
        print(" ".ljust(30), "6. Exit")
        timesheet_choice = input("Enter your choice: ")
        if timesheet_choice == "1":
            timesheet_id = Timesheet.createTimesheet()
            if timesheet_id:
                print("Timesheet created successfully with id: ", timesheet_id)
            else:
                print("Timesheet creation failed")
        elif timesheet_choice == "2":
            timesheet_id = input("Enter the timesheet id: ")
            updated_timesheet = Timesheet.updateTimesheet(timesheet_id)
            if updated_timesheet:
                print("Timesheet updated successfully. please find updated details below")
                print(Timesheet.searchTimesheet(timesheet_id))
            else:
                print("Timesheet update failed")
        elif timesheet_choice == "3":
            timesheet_id = input("Enter the timesheet id: ")
            timesheet_data = Timesheet.searchTimesheet(timesheet_id)
            if timesheet_data:
                print(timesheet_data)
            else:
                print("Timesheet search failed")
        elif timesheet_choice == "4":
            timesheets_data = Timesheet.showAllTimesheets()
            if timesheets_data:
                for key, value in timesheets_data.items():
                    print(key, value , sep=" : ")
            else:
                print("no timesheets are available in the system")
        elif timesheet_choice == "5":
            break
        elif timesheet_choice == "6":
            sys.exit()
        else:
            print("Invalid choice")

def employees(employee_bulk_file):
    while True:
        print(" ".rjust(30), "1. Create a new Employee")
        print(" ".rjust(30), "2. Update a Employee")
        print(" ".rjust(30), "3. Delete a Employee")
        print(" ".rjust(30), "4. Search a Employee")
        print(" ".rjust(30), "5. Show all Employees")
        print(" ".rjust(30), "6. Bulk upload Employees")
        print(" ".rjust(30), "7. Back")
        print(" ".rjust(30), "8. Exit")
        emp_choice = input("Enter your choice: ")
        if emp_choice == "1":
            employee_id = Employee.createEmployee()
            if employee_id:
                print("Employee created successfully with id: ", employee_id)
            else:
                print("Employee creation failed")
        elif emp_choice == "2":
            employee_id = input("Enter the employee id: ")
            updated_employee = Employee.update_employee(employee_id)
            if updated_employee:
                print("Employee updated successfully. please find updated details below")
                print(Employee.searchEmployee(employee_id))
            else:
                print("Employee update failed")
        elif emp_choice == "3":
            employee_id = input("Enter the employee id: ")
            deleted_employee = Employee.deleteEmployee(employee_id)
            if deleted_employee:
                print("Employee deleted successfully with id: ", employee_id)
            else:
                print("Employee deletion failed")
        elif emp_choice == "4":
            employee_id = input("Enter the employee id: ")
            employee_data = Employee.searchEmployee(employee_id)
            if employee_data:
                print(employee_data)
            else:
                print("Employee search failed")
        elif emp_choice == "5":
            employees_data = Employee.showAllEmployees()
            if employees_data:
                for key, value in employees_data.items():
                    print(key, value , sep=" : ")
            else:
                print("no employees are available in the system")
        elif emp_choice == "6":
            Employee.bulk_upload_from_file(employee_bulk_file)
            print("Bulk upload completed successfully")
        elif emp_choice == "7":
            break
        elif emp_choice == "8":
            sys.exit()
        else:
            print("Invalid choice. Please enter the correct choice")

def clients(client_bulk_file):
    while True:
        print(" ".rjust(30), "1. Create a new Client")
        print(" ".rjust(30), "2. Update a Client")
        print(" ".rjust(30), "3. Delete a Client")
        print(" ".rjust(30), "4. Search a Client")
        print(" ".rjust(30), "5. Show all Clients")
        print(" ".rjust(30), "6. Bulk upload Clients")
        print(" ".rjust(30), "7. Back")
        print(" ".rjust(30), "8. Exit")
        client_choice = input("Enter your choice: ")
        if client_choice == "1":
            client_id = Client.createClient()
            if client_id:
                print("Client created successfully with id: ", client_id)
            else:
                print("Client creation failed")
        elif client_choice == "2":
            client_id = input("Enter the client id: ")
            updated_client = Client.updateClient(client_id)
            if updated_client:
                print("Client updated successfully. please find updated details below")
                print(Client.searchClient(client_id))
            else:
                print("The Client with id", client_id, "is not available in the system")
        elif client_choice == "3":
            client_id = input("Enter the client id: ")
            deleted_client = Client.deleteClient(client_id)
            if deleted_client:
                print("Client deleted successfully with id: ", client_id)
            else:
                print("Client deletion failed")
        elif client_choice == "4":
            client_id = input("Enter the client id: ")
            client_data = Client.searchClient(client_id)
            if client_data:
                print(client_data)
            else:
                print("Client search failed")
        elif client_choice == "5":
            clients_data = Client.showAllClients()
            if clients_data:
                for key, value in clients_data.items():
                    print(key, value , sep=" : ")
            else:
                print("no clients are available in the system")
        elif client_choice == "6":
            Client.bulk_upload_from_file(client_bulk_file)
            print("Bulk upload completed successfully")
        elif client_choice == "7":
            break
        elif client_choice == "8":
            sys.exit()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()