"""
Задачка про лічильник: Створіть клас, який реалізує лічильник, що збільшується на 1 кожного разу,
 коли ви входите в його контекст, і виводить поточне значення лічильника при виході з контексту.
"""

# class Calc:
#     def __init__(self) -> None:
#         self.connected = 0

#     def __enter__(self):
#         self.connected +=1
#         return self

#     def __exit__(self, exception_type, exception_value, traceback):
#         print("Значення лічильника після виходу з контексту:", self.connected)
#         if exception_type is not None:
#             print("Some error!")
#         else:
#             print("No problem")

# p = Calc()

# with p as pc:
#     print(pc)

"""
Задачка про файлову систему: Створіть клас, який дозволяє автоматично відкривати і закривати файл у контексті.
 При вході в контекст відкрийте файл, а при виході - закрийте його.
"""

class AutoOpenClose:
    def __init__(self, file_name, mode, file=None) -> None:
        self.file_name = file_name
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.file_name, self.mode)
        return self.file
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()

my_file = AutoOpenClose("example.txt", "w")

with my_file as file:
    file.write("я записав шось в файл")
    