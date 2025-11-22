import os
import pickle
class Address:
    def __init__(self, mail_id, phone_number, house_no, building_number, road_number, street_name,land_mark, city, state, zip_code, Address_data_file):
        self.mail_id = mail_id
        self.phone_number = phone_number
        self.house_no = house_no
        self.building_number = building_number
        self.road_number = road_number
        self.street_name = street_name
        self.land_mark = land_mark
        self.city = city
        self.state= state
        self.zip_code = zip_code
        self.Address_data_file = Address_data_file

    def Address_upload(self):
        try:
            with open(self.Address_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if (self.mail_id) in data.keys():
            return False
        with open(self.Address_data_file, "wb") as write_file:
            data[self.mail_id] = [self.phone_number, self.house_no, self.building_number, self.road_number, self.street_name, self.land_mark, self.city, self.state, self.zip_code]
            pickle.dump(data, write_file)
        return True
    
    def update_address(self, mail_id, phone_number, house_no, building_number, road_number, street_name,land_mark, city, state, zip_code, Address_data_file):
        with open(Address_data_file, "rb") as read_file:
            data = pickle.load(read_file)
            if not isinstance(data, dict):
                data = {}
            if mail_id in data.keys():
                return False
        Address.delete_address(self.mail_id, Address_data_file)
        self.mail_id = mail_id
        self.phone_number = phone_number
        self.house_no = house_no
        self.building_number = building_number
        self.road_number = road_number
        self.street_name = street_name
        self.land_mark = land_mark
        self.city = city
        self.state = state
        self.zip_code = zip_code
        try:
            with open(Address_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        with open(Address_data_file, "wb") as write_file:
            data[self.mail_id] = [self.phone_number, self.house_no, self.building_number, self.road_number, self.street_name, self.land_mark, self.city, self.state, self.zip_code]
            pickle.dump(data, write_file)
        return True

    def getAddress(self, Address_data_file):
        try:
            with open(Address_data_file, "rb") as load_file:
                data = pickle.load(load_file)
                each_data = {self.mail_id: data.get(self.mail_id)}
                return each_data
        except (FileNotFoundError, EOFError):
            data = {}
        if not data:
            return None
        
    def delete_address(mail_id, Address_data_file):
        try:
            with open(Address_data_file, "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if mail_id in data.keys():
            data.pop(mail_id)
        with open(Address_data_file, "wb") as write_file:
            pickle.dump(data, write_file)
