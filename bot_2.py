from collections import UserDict
from datetime import datetime, timedelta
import pickle


class AddressBook(UserDict):

    N = 5
    
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def remove_item(self, name):
        if name in self.data:
            del self.data[name]
            return "Contact deleted successfully"
        else:
            raise ValueError("Key not found")
    #-----------domaska_11 AddressBook реализует метод iterator-----------------

    def iterator(self, n=None):
        n = n or self.N
        output = []
        for k in self:
            output.append(str(self[k]))
            if len(output) >= n:
                yield "\n".join(output)
                output = []

        yield "\n".join(output)
        
    #-----------domaska_11 AddressBook реализует метод iterator-----------------
    #-----------domaska_12
    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)
    
    def load_from_file(self, filename):
        with open(filename, "rb") as file:
            self.data = pickle.load(file)
    #-----------domaska_12
class Field:
    value = None

    def __init__(self, value):
        self.value = value
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value})"

#-----------domaska_11 Добавим поле для дня рождения Birthday
class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value  
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use dd-mm-yyyy")
        self.__value = new_value

    def days_to_birthday(self):
        today = datetime.now().date()
        birthday = datetime.strptime(self.__value, "%d-%m-%Y").replace(year=today.year)
        return (birthday - today).days


#-----------domaska_11 Добавим поле для дня рождения Birthday

class Name(Field):
    pass

#-----------domaska_11 добавим функционал проверки на правильность приведенных значений для полей Phone
class Phone(Field):
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        self.__value = new_value
        # if not isinstance(new_value, str) or len(new_value) != 10 or not new_value.isdigit():
        #     raise ValueError("Invalid phone number")
        # else:
        #     self.__value = new_value

#-----------domaska_11 добавим функционал проверки на правильность приведенных значений для полей Phone
class Record:
    name = None
    phones = None

    def __init__(self, name, phones = None, birthday=None) -> None:
        self.name = name
        self.phones = phones if phones else []
        self.birthday = Birthday(birthday) if birthday else None #-----------domaska_11 добавив необовязкове поле
    def add_phone(self, phone):
        self.phones.append(phone)

    def change_ph(self, old_phone, new_phone):
        new_phone = Phone(new_phone)

        for i, v in enumerate(self.phones):
            if v.value == old_phone:
                self.phones[i] = new_phone
                return True
        
        raise ValueError("Old phone not found")

    
    def __repr__(self) -> str:
        """це для красоти коли робиш print"""
        return f"Record({self.name}, {self.phones})"

#-----------------------------

def decorator_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            return str(exc)
    return wrapper

@decorator_error
def hello_func():
    return "How can I help you?"

@decorator_error
def add_func(name, phone, saved_nama_phone):
    if not name or not phone:
        raise ValueError("Enter name and phone please")
    
    # saved_nama_phone[name] = phone
    name = Name(name)
    phone = Phone(phone)
    
    if name in saved_nama_phone:
        record = saved_nama_phone[name]
        record.add_phone(phone)
    else:
        record = Record(name)
    
    record.add_phone(phone)
    
    if name not in saved_nama_phone:
        saved_nama_phone.add_record(record)
    
    return "Contact added successfully"

@decorator_error
def change_func(name, old_phone, new_phone, saved_nama_phone): 
    record = saved_nama_phone.get(name)
    if record is None:
         raise KeyError("Enter user name")

    result = record.change_ph(old_phone, new_phone)
    if result:
        return "Contact changed successfully"
    
    return "Contact not changed"


@decorator_error    
def remove_func(name, saved_nama_phone):
    record = saved_nama_phone[name]
    print ("To sho v record" ,record)
    if record is None:
         raise KeyError("No")
    result = saved_nama_phone.remove_item(name)
    if result:
        return "Contact del successfully"
    
    return "Contact not del"

@decorator_error
def phone_func(name, saved_nama_phone):
    if name in saved_nama_phone:
        return saved_nama_phone[name]
    else:
        raise KeyError("Enter user name")

@decorator_error
def show_all_func(saved_nama_phone):
    iterator = AddressBook(n)

    for i in iterator:
        print(i)

@decorator_error
def search_func(keyword, saved_nama_phone):
    results = []

    for record in saved_nama_phone.values():
        name = record.name.value
        phones = [phone.value for phone in record.phones]

        if keyword in name or any(keyword in phone for phone in phones):
            results.append(record)

    return results
                
@decorator_error       
def parser(user_input, saved_nama_phone):
    if user_input == "hello":
        return hello_func()
            # print (hello_func())
    elif user_input.startswith("add"):
        ad, name, phone = user_input.split(" ")
        # print(add_func(name, phone, saved_nama_phone))
        return add_func(name, phone, saved_nama_phone)
    elif user_input.startswith("change"):
        ad, name, old_phone, new_phone = user_input.split(" ")
        # print(change_func(name, phone, saved_nama_phone))
        return change_func(name, old_phone, new_phone, saved_nama_phone)  #old_phone, #new_phone  замість phone?
    elif user_input.startswith("remove"):
        ad, name = user_input.split(" ")
        return remove_func(name, saved_nama_phone)  #old_phone, #new_phone  замість phone?
    elif user_input.startswith("phone"):
        ad,name = user_input.split(" ")
        # print(phone_func(name, saved_nama_phone))
        return phone_func(name, saved_nama_phone)
    elif user_input == "show all":
        # print (saved_nama_phone)
        # return saved_nama_phone
        out = [r for r in saved_nama_phone.iterator()]
        return "\n".join(out)
    #------------domashka 12 - пошук по буквах цифрах і тд
    elif user_input.startswith("search"):
        ad,keyword = user_input.split(" ")
        
        return search_func(keyword, saved_nama_phone)
    #------------domashka 12 - пошук по буквах цифрах і тд
                
def main():
    # n = 5
    # saved_nama_phone = {}
    saved_nama_phone = AddressBook()

    while True:
        user_input = input("Enter comand: ").lower()

        if user_input=="good bye" or user_input=="close" or user_input=="exit":
            print ("Good bye!")
            break
        if user_input == "save":
            saved_nama_phone.save_to_file(filename)
            print("Address book saved to file.")
            continue
        
        if user_input == "load":
            saved_nama_phone.load_from_file(filename)
            print("Address book loaded from file.")
            continue

        res = parser(user_input, saved_nama_phone)
        print(res)




if __name__ == "__main__":
    main()
