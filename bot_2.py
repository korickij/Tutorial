from collections import UserDict

class AddressBook(UserDict):
    
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def remove_item(self, name):
        if name in self.data:
            del self.data[name]
            return "Contact deleted successfully"
        else:
            raise ValueError("Key not found")


class Field:
    value = None

    def __init__(self, value):
        self.value = value
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value})"

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    name = None
    phones = None

    def __init__(self, name, phones = None) -> None:
        self.name = name
        self.phones = phones if phones else []

    def add_phone(self, phone):
        self.phones.append(phone)

    def change_ph(self, old_phone, new_phone):
        new_phone = Phone(new_phone)

        for i, v in enumerate(self.phones):
            if v.value == old_phone:
                self.phones[i] = new_phone
                return True
        
        raise ValueError("Old phone not found")
    
    # def remove_item(self, name, saved_nama_phone):
    #     del saved_nama_phone[name]
    #     raise ValueError("Old phone not found")

    
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
    if record is None:
         raise KeyError("No")
    result = saved_nama_phone.remove_item(name)
    if result:
        return "Contact del successfully"
    
    return "Contact not del"
    # if name in saved_nama_phone:
    #     del saved_nama_phone[name]
    # else:
    #     raise KeyError("Key not found")

@decorator_error
def phone_func(name, saved_nama_phone):
    if name in saved_nama_phone:
        return saved_nama_phone[name]
    else:
        raise KeyError("Enter user name")

@decorator_error
def show_all_func(saved_nama_phone):
    if not saved_nama_phone:
        return "slovnuk porozhnij"
    else:
        res = ""
        for name, phone in saved_nama_phone.items():
            res += (f"{name}:{phone}\n")
        return res

                
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
        return saved_nama_phone
                
def main():
    
    # saved_nama_phone = {}
    saved_nama_phone = AddressBook()

    while True:
        user_input = input("Enter comand: ").lower()

        if user_input=="good bye" or user_input=="close" or user_input=="exit":
            print ("Good bye!")
            break
        res = parser(user_input, saved_nama_phone)
        print(res)




if __name__ == "__main__":
    main()
