from  Address import Address
import re
import os
import pickle
import random

script_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(script_folder, "Data")
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
Client_data_file = os.path.join(data_folder, "Client_data_file.txt")
Address_data_file = os.path.join(data_folder, "Client_address_info.txt")

class Client:
    def __init__(self, client_id, client_name, client_description, std_bill_rate, mail_id, phone_number, house_no, building_number,
                 road_number, street_name, land_mark, city, state, zip_code):
        self.client_id = client_id
        self.client_name = client_name
        self.client_description = client_description
        self.std_bill_rate = std_bill_rate
        self.client_address = Address(mail_id, phone_number, house_no, building_number,road_number, street_name, land_mark, city, state, zip_code, Address_data_file)


    def Client_upload(self):
        try:
            with open(Client_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if (self.client_id) in data.keys():
            self.client_id = genClientId()
        valid_mail_id = self.client_address.Address_upload()
        if not valid_mail_id:
            return False
        with open(Client_data_file, "wb") as write_file:
            data[self.client_id] = [self.client_name, self.client_description, self.std_bill_rate, self.client_address]
            pickle.dump(data, write_file)
        return True
    
    @staticmethod
    def updateClient(client_id):
        try:
            with open(Client_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if (client_id) in data.keys():
            client_name = data.get(client_id)[0]
            client_description = input("Enter the client description: ")
            std_bill_rate = input("Enter the standard bill rate: ")+"$"
            mail_id = input("Enter the mail id: ")
            phone_number = input("Enter the phone number: ")
            house_no = input("Enter the house number: ")
            building_number = input("Enter the building number: ")
            road_number = input("Enter the road number: ")
            street_name = input("Enter the street name: ")
            land_mark = input("Enter the land mark: ")
            city = input("Enter the city: ")
            state = input("Enter the state: ")
            zip_code = input("Enter the zip code: ")   
            validated = validateClientInputs(client_name, std_bill_rate, client_description, mail_id, phone_number, house_no, building_number, road_number, street_name, land_mark, city, state, zip_code)
            if not validated:
                return False
            with open(Client_data_file, "wb") as write_file:
                addr_obj = data.get(client_id)[-1]
                adrees_updated = Address.update_address(addr_obj, mail_id, phone_number, house_no, building_number, road_number, street_name, land_mark, city, state, zip_code, Address_data_file)
                if not adrees_updated:
                    return False
                data[client_id] = [client_name, client_description, std_bill_rate, addr_obj]
                pickle.dump(data, write_file)
            print("Client updated successfully")
            return True
    
    @staticmethod
    def deleteClient(client_id):
        try:
            with open(Client_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if (client_id) in data.keys():
            addr_obj = data.get(client_id)[-1]
            Address.delete_address(addr_obj, Address_data_file)
            del data[client_id]
            with open(Client_data_file, "wb") as write_file:
                pickle.dump(data, write_file)
            print("Client deleted successfully")
            return True
        else:
            print("Client not found")
            return False

    @staticmethod
    def searchClient(client_id):
        try:
            with open(Client_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if (client_id) in data.keys():
            addr_obj = data.get(client_id)[-1]
            address = Address.getAddress(addr_obj, Address_data_file)
            data.get(client_id)[-1] = address
            return data.get(client_id)
        else:
            return "The client with id " + client_id + " is not available in the system"

    @staticmethod
    def showAllClients():
        try:
            with open(Client_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
                final_data = {}
                for key, value in data.items():
                    address_object = data.get(key)[-1]
                    address = Address.getAddress(address_object, Address_data_file)
                    value[-1] = address
                    final_data[key] = value
        except (FileNotFoundError, EOFError):
            final_data = {}
        return final_data

    @staticmethod
    def createClient():
        client_id = genClientId()
        client_name = input("Enter the client name: ")
        client_description = input("Enter the client description: ")
        std_bill_rate = input("Enter the standard bill rate: ")+"$"
        mail_id = input("Enter the mail id: ")
        phone_number = input("Enter the phone number: ")
        house_no = input("Enter the house number: ")
        building_number = input("Enter the building number: ")
        road_number = input("Enter the road number: ")
        street_name = input("Enter the street name: ")
        land_mark = input("Enter the land mark: ")
        city = input("Enter the city: ")
        state = input("Enter the state: ")
        zip_code = input("Enter the zip code: ")
        validated = validateClientInputs(client_name, std_bill_rate, client_description, mail_id, phone_number, house_no, building_number, road_number, street_name, land_mark, city, state, zip_code)
        if not validated:
            return None
        client = Client(client_id, client_name, client_description, std_bill_rate, mail_id, phone_number, house_no, building_number, road_number, street_name, land_mark, city, state, zip_code)
        client_id = genClientId()
        client.Client_upload()

        return client_id
    @staticmethod
    def bulk_upload_from_file(file):
        with open(file, "r") as t_file:
            data_from_file = t_file.readlines()[1:]
            for index,line in enumerate(data_from_file):
                data_in_tuple = tuple(line.strip('\n').split(','))
                #Extracting Client data
                Client_Name,Client_Description,Standart_Bill_Rate = data_in_tuple[0], data_in_tuple[3], data_in_tuple[4]
                #Extracting mail_id and phone_number
                Mail_Id,Phone_Number = data_in_tuple[1:3]

                #Extracting addresss
                House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code = data_in_tuple[5:]
                
                validated = validateClientInputs(Client_Name,Client_Description,Standart_Bill_Rate, Mail_Id,Phone_Number, House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code, index)
                if validated:
                    Client_Id = genClientId()
                    Client_date = Client(Client_Id, Client_Name,Client_Description,Standart_Bill_Rate, Mail_Id,Phone_Number, House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code)
                    Client_date.Client_upload()


def validateClientInputs(client_name, std_bill_rate, client_description, Mail_Id,Phone_Number, House_Number,Building_Number,Road_Number,Street_Name,Landmark,City,State,Zip_Code, index=None):
    valid_client_name_and_description = r'^[A-Za-z0-9_\- ]+$'
    valid_mail = r'^[A-Za-z0-9._+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$'
    valid_building_number = r'^[0-9A-Za-z\-/\\#@.,\s]+$'

    #Valid Employee Name
    if not re.fullmatch(valid_client_name_and_description, client_name):
        print(f"Invalid characters in client name {client_name} at line {index + 1}")
    
    #Valid Standart_Bill_Rate
    try:
        float(std_bill_rate.strip().replace('$','').replace(',', ''))
    except ValueError:
        print (f"The {std_bill_rate} is not valid standard bill rate")
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
    

def genClientId():
        random_number = ''
        for i in range(7):
            random_number +=  str(random.randint(0, 9))
        return ("CLT_"+random_number)


if __name__ == "__main__":
    #bulk_upload_from_file("Clients.csv")
    Client.updateClient("CLT_3840042")
    print("The updated client is ", Client.searchClient("CLT_3840042"))
    print("Delete client ", Client.deleteClient("CLT_3840042"))
    print("The updated client is ", Client.searchClient("CLT_3840042"))
    print(Client.showAllClients())