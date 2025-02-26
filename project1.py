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
            return "Invalid input. Please provide the correct arguments."
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
        for phone in self.phones:
            if phone.value == old_phone:
                try:
                    Phone(new_phone)
                    phone.value = new_phone
                    return
                except ValueError:
                    raise ValueError("New phone number is not valid.")
        raise ValueError("Old phone not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = self.birthday.value if self.birthday else "No birthday set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

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
                bday_day, bday_month, bday_year = map(int, record.birthday.value.split('.'))
                bday_this_year = datetime(today.year, bday_month, bday_day).date()
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                days_to_bday = (bday_this_year - today).days
                if 0 <= days_to_bday <= 7:
                    if bday_this_year.weekday() >= 5:
                        bday_this_year += timedelta(days=(7 - bday_this_year.weekday()))
                    upcoming.append({"name": record.name.value, "birthday": bday_this_year.strftime("%d.%m.%Y")})
        return upcoming

def parse_input(user_input):
    return user_input.strip().split(" ", 1)

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args.split()
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book):
    name, birthday = args.split()
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book):
    name = args.strip()
    record = book.find(name)
    if not record or not record.birthday:
        return "No birthday found."
    return f"{name}'s birthday is {record.birthday.value}"

@input_error
def birthdays(_, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join([f"{b['name']}: {b['birthday']}" for b in upcoming])

@input_error
def change_phone(args, book):
    name, old_phone, new_phone = args.split()
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Phone number changed."

@input_error
def show_all_contacts(_, book):
    if not book:
        return "No contacts in the address book."
    return "\n".join(str(record) for record in book.values())

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        command = command.lower()  
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "change":
            print(change_phone(args, book))
        elif command == "all":
            print(show_all_contacts(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
 main()
