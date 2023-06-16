from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):
    # def __inti__(self, n):
    #     super().__init__()
    #     self.n = n
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
    # def __iter__(self):
    #     self.current = 0
    #     self.keys = list(self.data.keys())
    #     return self
    
    # def __next__(self):
    #     if self.current >= len(self.keys):
    #         raise StopIteration
    #     start = self.current
    #     end = end = start + self.n if start + self.n <= len(self._keys) else len(self._keys)
    #     self.current = end
    #     return [self.data[key] for key in self.keys[start:end]]
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


class Field:
    value = None

    def __init__(self, value):
        self.value = value
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value})"

#-----------domaska_11 Добавим поле для дня рождения Birthday
class Birthday(Field):
    def __init__(self, value):
        pass

    def validator(self, value):
        try:
            datetime.strptime(self.value, "%d-%m-%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use dd-mm-yyyy")
        return value

    def days_to_birthday(self):
        today = datetime.now().date() #просто дата без минут секунд і мікросекунд
        birthday = datetime.strftime(self.value, "%d-%m-%Y").replace(year=today.year)
        return (birthday - today).days

#-----------domaska_11 Добавим поле для дня рождения Birthday

class Name(Field):
    pass

#-----------domaska_11 добавим функционал проверки на правильность приведенных значений для полей Phone
class Phone(Field):
    def __init__(self, value):
        pass

    def validator(self, value):
        
        if not isinstance(value, str) or len(value) != 10 or not value.isdigit():
            raise ValueError("Invalid phone number")
        return value

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
    # if not saved_nama_phone:
    #     return "slovnuk porozhnij"
    # else:
    #     res = ""
    #     for name, phone in saved_nama_phone.items():
    #         res += (f"{name}:{phone}\n")
    #     return res

                
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
                
def main():
    # n = 5
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
