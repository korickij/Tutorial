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
    else:
        saved_nama_phone[name] = phone
        return "Contact added successfully"

@decorator_error
def change_func(name, phone, saved_nama_phone):
    if name in saved_nama_phone:
        saved_nama_phone[name]=phone
    else:
        raise KeyError("Enter user name")

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
        ad, name, phone = user_input.split(" ")
        # print(change_func(name, phone, saved_nama_phone))
        return change_func(name, phone, saved_nama_phone)
    elif user_input.startswith("phone"):
        ad,name = user_input.split(" ")
        # print(phone_func(name, saved_nama_phone))
        return phone_func(name, saved_nama_phone)
    elif user_input == "show all":
        # print (saved_nama_phone)
        return saved_nama_phone
                
def main():
    
    saved_nama_phone = {}

    while True:
        user_input = input("Enter comand: ").lower()

        if user_input=="good bye" or user_input=="close" or user_input=="exit":
            print ("Good bye!")
            break
        res = parser(user_input, saved_nama_phone)
        print(res)




if __name__ == "__main__":
    main()
