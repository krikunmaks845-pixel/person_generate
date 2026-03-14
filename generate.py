
import random

names = ["Андрій","Олександр","Дмитро","Іван","Максим","Артем","Владислав","Богдан","Данило","Роман","Сергій",
               "Павло","Микола","Віктор","Ярослав","Кирило","Ігор","Тарас","Федір","Григорій","Леонід","Матвій",
               "Назар","Остап","Петро", "Анна","Олена","Наталія","Софія","Анастасія","Марія","Вікторія",
               "Ольга","Тетяна","Ірина","Катерина","Юлія","Дарина","Аліна","Соломія"]

surnames = ["Мельник","Шевченко","Коваленко","Бондаренко","Ткаченко","Ковальчук","Мороз","Кравченко",
            "Олійник","Шевчук","Поліщук","Лисенко","Савченко","Марченко","Котляр","Костенко",
            "Павленко","Харченко","Марчук","Петренко","Сидоренко","Іваненко","Бойко","Левченко",
            "Руденко","Сидоров","Попов","Василенко","Ковальов","Бондар","Колесник","Морозов",
            "Кравчук","Вовк","Хоменко","Романенко","Голуб","Мазур","Козак","Дідух"]

email_names = ["Andriy", "Oleksandr", "Dmytro", "Ivan", "Maksym", "Artem", "Vladyslav", "Bohdan", "Danylo", "Roman", "Serhiy", "Pavlo", "Mykola", "Viktor", "Yaroslav", "Kyrylo", "Ihor", "Taras", "Fedir", "Hryhoriy",
               "Leonid", "Matviy", "Nazar", "Ostap", "Petro", "Anna", "Olena", "Natalia", "Sofia", "Anastasia", "Maria", "Viktoria", "Olga", "Tetiana", "Iryna", "Kateryna", "Yulia", "Daryna", "Alina", "Solomiya"]

email_surnames = ["Melnyk", "Shevchenko", "Kovalenko", "Bondarenko", "Tkachenko", "Kovalchuk", "Moroz", "Kravchenko", "Oliynyk", "Shevchuk", "Polishchuk", "Lysenko", "Savchenko", "Marchenko", "Kotlyar", "Kostenko", "Pavlenko", "Kharchenko", "Marchuk", "Petrenko", "Sydorenko", "Ivanenko", "Boiko",
            "Levchenko", "Rudenko", "Sydorov", "Popov", "Vasylenko", "Kovalyov", "Bondar", "Kolesnyk", "Morozov", "Kravchuk", "Vovk", "Khomenko", "Romanenko", "Holub", "Mazur", "Kozak", "Didukh"]

def generate_age(min_age=18, max_age=65):
    return random.randint(min_age, max_age)

def generate_email(email_name):
    parts = email_name.lower().split()
    formats = [
        f"{parts[0]}{parts[1]}",
        f"{parts[0]}{parts[1]}{random.randint(1,999)}",
        f"{parts[0][0]}{parts[1]}"
    ]
    return f"{random.choice(formats)}@gmail.com"

def generate_person():
    name_index = random.randrange(len(names))
    surname_index = random.randrange(len(surnames))

    name = f"{names[name_index]} {surnames[surname_index]}"
    email_name = f"{email_names[name_index]} {email_surnames[surname_index]}"

    age = generate_age()
    email = generate_email(email_name)

    return {
        "name": name,
        "age": age,
        "email": email
    }

def generate_multiple(count=5):
    return [generate_person() for _ in range(count)]
