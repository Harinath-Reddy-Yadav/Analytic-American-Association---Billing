import pickle
import random
import re
import os

# create Data folder to store the Tasks info
script_folder = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(script_folder, "Data")
if not os.path.isdir(data_folder):    #  create directory if not present
    os.mkdir(data_folder)
Task_data_file = os.path.join(data_folder, "Task_info.txt")

class Task:
    def __init__(self, Task_Id, task_name, chargeable, rate_card='0$'):
        self.Task_Id = Task_Id
        self.task_name = task_name
        self.chargeable = chargeable
        self.rate_card = rate_card
    

    def Task_upload(self):
        try:
            with open("Data\Task_info.txt", "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        with open("Data\Task_info.txt", "wb") as write_file:
            if (self.Task_Id) in data.keys():
                self.Task_Id = genTaskId()
            data[self.Task_Id] = [self.task_name, self.chargeable, self.rate_card]
            pickle.dump(data, write_file)
    
    @staticmethod
    def update_task(Taks_Id):
        try:
            with open("Data\Task_info.txt", "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if Taks_Id in data.keys():
            task_name = input("Please enter the task_name: ")
            chargeable= input("Please provide chargeable or not (Yes/No)")
            if re.fullmatch(r'(?i)true|yes', chargeable.strip()):
                rate_card = input("Enter the rate_card value")
            else:
                rate_card = None
            valid_inputs = validateTaskInputs(task_name, chargeable, rate_card)
            if not valid_inputs:
                return False
            data[Taks_Id] = [task_name, chargeable, rate_card]
            with open("Data\Task_info.txt", "wb") as update_file:
                    pickle.dump(data, update_file)
            return True
        else:
            return False

    @staticmethod
    def delete_task(Task_Id):
        try:
            with open("Data\Task_info.txt", "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if Task_Id in data.keys():
            data.pop(Task_Id)
            with open("Data\Task_info.txt", "wb") as update_file:
                pickle.dump(data, update_file)
            return True
        else:
            return False

    @staticmethod
    def search_task( Task_Id):
        try:
            with open("Data\Task_info.txt", "rb") as read_file:
                data = pickle.load(read_file)
                if not isinstance(data, dict):
                    data = {}
        except (FileNotFoundError, EOFError):
            data = {}
        if Task_Id in data.keys():
            task =  data.get(Task_Id)
            return task
        else:
            return "The task with id " + Task_Id + " is not available in the system"
    
    @staticmethod
    def ShowAllTasks():
        try:
            with open("Data\Task_info.txt", "rb") as load_file:
                data = pickle.load(load_file)
            return data
        except (FileNotFoundError, EOFError):
            return {}
    
    @staticmethod
    def createtask():
        task_name = input("Please enter the task_name: ")
        chargeable= input("Please provide chargeable or not (Yes/No)")
        if re.fullmatch(r'(?i)true|yes', chargeable.strip()):
            rate_card = input("Enter the rate_card value")
        else:
            rate_card = None
        valid_inputs = validateTaskInputs(task_name, chargeable, rate_card)
        if not valid_inputs:
            return False
        Task_Id = genTaskId()
        new_task = Task(Task_Id, task_name, chargeable, rate_card) 
        new_task.Task_upload()
        return Task_Id

    @staticmethod
    def task_bulk_upload(file):
        with open(file, "r") as t_file:
            Tasks = t_file.readlines()[1:]
            for index,line in enumerate(Tasks):
                task_name, chargeable, rate_card = tuple(line.strip('\n').split(','))
                validated = validateTaskInputs(task_name, chargeable, rate_card,index)
                if validated:
                    Task_Id = genTaskId()
                    if re.fullmatch(r'(?i)true|yes', chargeable.strip()):
                        new_task = Task(Task_Id, task_name, chargeable, rate_card) 
                        new_task.Task_upload()
                    else:
                        new_task = Task(Task_Id, task_name, chargeable) 
                    new_task.Task_upload()
                else:
                    return False
        return True


def genTaskId():
        random_number = ''
        for i in range(7):
            random_number +=  str(random.randint(0, 9))
        return ("TSK_"+random_number)

def validateTaskInputs(task_name, chargeable, rate_card, index = 0):
    valid_task_name = r'^[A-Za-z0-9_\- ]+$'
    valid_chargeable = r'(?i)true|false|yes|no'

    # Validate task_name
    if not re.fullmatch(valid_task_name, task_name):
        print(f"Invalid characters in task name at line {index + 1}")
        return False

    # Validate chargeable
    if not re.fullmatch(valid_chargeable, chargeable):
        print(f"Invalid value for chargeable at line {index + 1}")
        return False

    # Validate rate_card only if chargeable is True/Yes
    if re.fullmatch(r'(?i)true|yes', chargeable.strip()):
        cleaned_rate = rate_card.strip().replace('$','').replace(',', '')
        try:
            float(cleaned_rate)
        except ValueError:
            print(f"Invalid rate_card for chargeable task at line {index + 1}")
            return False

    return True

if __name__ == "__main__":
    Task.update_task("TSK_8225955")
