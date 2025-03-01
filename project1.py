from collections import UserDict
import re
from datetime import datetime, timedelta

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments provided."
        except KeyError:
            return "Contact not found."
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if not re.match(r'^\d{10}$', new_phone):
            raise ValueError("New phone number must be 10 digits.")
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Old phone not found.")

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                day, month, year = map(int, record.birthday.value.split('.'))
                bday = datetime(year=today.year, month=month, day=day).date()
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                if 0 <= (bday - today).days <= 7:
                    if bday.weekday() >= 5:
                        bday += timedelta(days=(7 - bday.weekday()))
                    upcoming.append({"name": record.name.value, "birthday": bday.strftime('%d.%m.%Y')})
        return upcoming

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name) or Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added or updated."

@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Phone number updated."
    return "Contact not found."

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is {record.birthday.value}"
    return "Birthday not found."

@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    return "\n".join([f"{b['name']}: {b['birthday']}" for b in upcoming]) or "No upcoming birthdays."

@input_error
def show_all(args, book):
    return "\n".join(str(record) for record in book.data.values()) or "No contacts found."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ").strip().lower()
        command, *args = user_input.split()
        
        commands = {
            "add": add_contact,
            "change": change_phone,
            "phone": lambda args, book: book.find(args[0]) or "Contact not found.",
            "all": show_all,
            "add-birthday": add_birthday,
            "show-birthday": show_birthday,
            "birthdays": birthdays,
            "exit": lambda args, book: exit("Good bye!"),
            "close": lambda args, book: exit("Good bye!"),
            "hello": lambda args, book: "How can I help you?"
        }
        
        handler = commands.get(command, lambda args, book: "Invalid command.")
        print(handler(args, book))

if __name__ == "__main__":
    main()
