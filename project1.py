from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.contacts = {}
    
    def add_record(self, record):
        self.contacts[record.name.value] = record
    
    def find(self, name):
        return self.contacts.get(name)
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.contacts.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                days_until_bday = (bday_this_year - today).days
                if days_until_bday <= 7:
                    greeting_date = bday_this_year
                    if greeting_date.weekday() >= 5:
                        greeting_date += timedelta(days=(7 - greeting_date.weekday()))
                    upcoming.append({"name": record.name.value, "birthday": greeting_date.strftime("%d.%m.%Y")})
        return upcoming

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError, KeyError) as e:
            return str(e)
    return wrapper

@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added."
    return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Birthday not found."

@input_error
def birthdays(args, book):
    return book.get_upcoming_birthdays()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
