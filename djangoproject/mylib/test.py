from datetime import date
# class Osoba: 
#     def __init__(self, imie): 
#         self.imie = imie

#     @property
#     def imie1(self): 
#         return self.imie

#     @imie1.setter
#     def imie2(self, i): 
#         self.imie = i

# class Person: 
#     num_of_people = 0 

#     def __init__(self, name): 
#         self.name= name
#         Person.num_of_people+= 1

#     @classmethod
#     def get_num_of_people(cls): 
#         return cls.num_of_people
    
#     def __str__(self):
#         return f"name= {self.name}, people= {Person.num_of_people}"
    
# p = Person("nam1")
# print(p, ", ", p.get_num_of_people())


mydate = date.fromisoformat("2025-05-21")
print("Date:", mydate.year, mydate.month, mydate.day)