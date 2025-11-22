import pickle
import os
import random
import re
from Address import Address
import datetime

# create Data folder to store the Employee info
script_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(script_folder, "Data")
if not os.path.isdir(data_folder):    #  create directory if not present
    os.mkdir(data_folder)
Employee_data_file = os.path.join(data_folder, "Employee_info.txt")
Address_data_file = os.path.join(data_folder, "Employee_Address_info.txt")


class Employee:
    def __init__(self, employee_id, employee_name, std_bill_rate,
                 mail_id, phone_number, house_no, building_number,
                 road_number, street_name, land_mark, city, state, zip_code):
        self.employee_Id = employee_id
        self.employee_name = employee_name
        self.std_bill_rate = std_bill_rate
        # keep an Address instance for easy storage/use
        self.employee_address = Address(mail_id, phone_number, house_no, building_number,road_number, street_name, land_mark, city, state, zip_code, Address_data_file)

    def Employee_upload(self):
        try:
            with open(Employee_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        valid_mail = Address.Address_upload(self.employee_address)
        if valid_mail:
            with open(Employee_data_file, "wb") as write_file:
                if (self.employee_Id) in data.keys():
                    self.employee_Id = genEmployeeId()
                data[self.employee_Id] = [self.employee_name, self.std_bill_rate, self.employee_address]
                pickle.dump(data, write_file)
    @staticmethod
    def update_employee(employee_Id):
        try:
            with open(Employee_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if employee_Id in data:
            employee_name = data.get(employee_Id)[0]
            mail_id = input("Please provide the mail ID: ")
            phone_number = input("Please provide the phone number: ")
            house_no = input("Please provide the house number: ")
            building_number = input("Please provide the building number: ")
            road_number = input("Please provide the road number: ")
            street_name = input("Please provide the street name: ")
            land_mark = input("Please provide the landmark: ")
            city = input("Please provide the city: ")
            state = input("Please provide the state: ")
            zip_code = input("Please provide the ZIP code: ")
            standard_bill_rate = input("Please enter the standard Bill rate: ")+"$"
            validated =  ValidateEmployeeInputs(employee_name,standard_bill_rate, mail_id, phone_number, house_no, building_number, road_number, street_name,land_mark, city, state, zip_code, Address_data_file)
            if not validated:
                return False
            addr_obj = data.get(employee_Id)[-1]
            address_update = Address.update_address(addr_obj,mail_id, phone_number, house_no, building_number, road_number, street_name,land_mark, city, state, zip_code, Address_data_file)
            data[employee_Id] = [employee_name, standard_bill_rate, addr_obj] 
            if address_update:
                with open(Employee_data_file, "wb") as write_file:
                    pickle.dump(data, write_file)
                    return True
            else:
                return False

    @staticmethod
    def searchEmployee(employee_id):
        try:
            with open(Employee_data_file, "rb") as load_file:
                data = pickle.load(load_file)
        except (FileNotFoundError, EOFError):
            data = {}
        if employee_id in data:
            obj = data.get(employee_id)[-1]
            address =  Address.getAddress(obj, Address_data_file)
            data.get(employee_id)[-1] = str(address)
            return data.get(employee_id)
        return "The Employee with Id " + employee_id + " not found in the system"
    
    @staticmethod
    def deleteEmployee(employee_id):
        try:
            with open(Employee_data_file, "rb") as load_file:
                data = pickle.load(load_file)
        except (FileNotFoundError, EOFError):
            data = {}
        if employee_id in data.keys():
            Address.delete_address(data.get(employee_id)[-1], Address_data_file)
            data.pop(employee_id)
            with open(Employee_data_file, "wb") as write_file:
                pickle.dump(data, write_file)
            return "Employee deleted successfully"
        return "The Employee with Id " + employee_id + " not found"

    @staticmethod
    def showAllEmployees():
        try:
            with open(Employee_data_file, "rb") as load_file:
                data = pickle.load(load_file)
                if not isinstance(data, dict):
                    data = {}
                final_data = {}
                for key, value in data.items():
                    address_obj = value[-1]
                    address_info = Address.getAddress(address_obj, Address_data_file)
                    value[-1] = str(address_info)
                    final_data[key] = value
                return final_data
        except (FileNotFoundError, EOFError):
            return {}

    @staticmethod
    def createEmployee():
        employee_id = genEmployeeId()
        employee_name = input("Enter the employee name: ")
        employee_mail_id = input("Enter the employee mail id: ")
        employee_phone_number = input("Enter the employee phone number: ")
        employee_house_number = input("Enter the employee house number: ")
        employee_building_number = input("Enter the employee building number: ")
        employee_road_number = input("Enter the employee road number: ")
        employee_street_name = input("Enter the employee street name: ")
        employee_landmark = input("Enter the employee landmark: ")
        employee_city = input("Enter the employee city: ")
        employee_state = input("Enter the employee state: ")
        employee_zip_code = input("Enter the employee zip code: ")
        employee_standart_bill_rate = input("Enter the employee standart bill rate: ")+"$"
        validated = ValidateEmployeeInputs(employee_name, employee_standart_bill_rate, employee_mail_id, employee_phone_number, employee_house_number, employee_building_number, employee_road_number, employee_street_name, employee_landmark, employee_city, employee_state, employee_zip_code)
        if not validated:
            return None
        employee = Employee(employee_id, employee_name, employee_mail_id, employee_phone_number, employee_standart_bill_rate, employee_house_number, employee_building_number, employee_road_number, employee_street_name, employee_landmark, employee_city, employee_state, employee_zip_code)
        employee.Employee_upload()
        return employee_id
    
    @staticmethod
    def bulk_upload_from_file(file):
        with open(file, "r") as t_file:
            data_from_file = t_file.readlines()[1:]
            for index,line in enumerate(data_from_file):
                data_in_tuple = tuple(line.strip('\n').split(','))
                #Extracting Employee data
                Employee_Name,Standart_Bill_Rate = data_in_tuple[0], data_in_tuple[3]
                #Extracting mail_id and phone_number
                Mail_Id,Phone_Number = data_in_tuple[1:3]

                #Extracting addresss
                House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code = data_in_tuple[4:]
                
                validated = ValidateEmployeeInputs(Employee_Name,Standart_Bill_Rate, Mail_Id,Phone_Number, House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code, index)
                if validated:
                    Employee_Id = genEmployeeId()
                    Employee_date = Employee(Employee_Id, Employee_Name,Standart_Bill_Rate, Mail_Id,Phone_Number, House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code)
                    Employee_date.Employee_upload()



def genEmployeeId():
        random_number = ''
        for i in range(7):
            random_number +=  str(random.randint(0, 9))
        return ("EMP_"+random_number)


def ValidateEmployeeInputs(Employee_Name,Standart_Bill_Rate, Mail_Id,Phone_Number, House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code, index=None):
    valid_employee_name = r'^[A-Za-z0-9_\- ]+$'
    valid_mail = r'^[A-Za-z0-9._+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$'
    valid_building_number = r'^[0-9A-Za-z\-/\\#@.,\s]+$'

    #Valid Employee Name
    if not re.fullmatch(valid_employee_name, Employee_Name):
        print(f"Invalid characters in Employee name {Employee_Name} at line {index + 1}")
    
    #Valid Standart_Bill_Rate
    try:
        float(Standart_Bill_Rate.strip().replace('$','').replace(',', ''))
    except ValueError:
        print (f"The {Standart_Bill_Rate} is not valid standard bill rate")
        return False

    # Validate mail_id
    if not re.fullmatch(valid_mail, Mail_Id):
        print(f"The mail id {Mail_Id} is not valid at the line {index + 1}")
        return False

    # Validate Phone Number
    if Phone_Number.startswith("+91"):
        invalid = False
        if len(Phone_Number)> 12 or not Phone_Number.isdigit():
            invalid = True
        elif len(Phone_Number) > 10 or not Phone_Number.isdigit():
            invalid = True
            print(f"The phone number {Phone_Number} is not valid at the line {index + 1}")
        if invalid:
            return False
        
    #Validating House number and road number
    if not House_Number.isascii():
        print(f"The House Number {House_Number} is not valid at the line {index + 1}")
        return False
    elif not Road_Number.isascii():
        print(f"The Road Number {Road_Number} is not valid at the line {index + 1}")
        return False
    
    #Validate building number
    if not re.fullmatch(valid_building_number, Building_Number):
        print(f"The Building Number {Building_Number} is not valid at the line {index + 1}")
        return False
    
    #Validate Street Name, Landmark
    if not re.fullmatch(r'^[A-Za-z0-9\s]+$', Street_Name):
        print(f"The Street Name {Street_Name} is not valid at the line {index + 1}")
        return False
    elif not re.fullmatch(r'^[A-Za-z0-9\s]+$', Landmark):
        print(f"The Landmark {Landmark} is not valid at the line {index + 1}")
        return False
    
    #Valid city, state
    if not City.replace(" ","").isalpha():
        print(f"The City {City} is not valid at the line {index + 1}")
        return False
    elif not State.replace(" ","").isalpha():
        print(f"The State {State} is not valid at the line {index + 1}")
        return False

    #Validate Zip
    if not Zip_Code.isdigit():
        print(f"The Zip code is not valid at the line {index + 1}")
        return False
    return True


if  __name__ == "__main__":
    file1 = "Employee.csv"
    #bulk_upload_from_file(file1)
    Employee.deleteEmployee("EMP_2411985")
    #print("Updated Employee Data")
    print(Employee.searchEmployee("EMP_2411985"))
    print("-"*100)
    # with open(Employee_data_file, 'rb') as f1, open(Address_data_file, 'rb') as f2:
    #     data1 = pickle.load(f1)
    #     print("-"*100)
    #     print(data1)
    #     data2 = pickle.load(f2)
    #     print("-"*100)
    #     print(data2)
