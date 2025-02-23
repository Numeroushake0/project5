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
    
    def __str__(self):
        phones = ", ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"{self.name.value}: Phones: {phones}, Birthday: {birthday}"

class AddressBook:
    def __init__(self):
        self.records = {}
    
    def add_record(self, record):
        self.records[record.name.value] = record
    
    def find(self, name):
        return self.records.get(name)
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.records.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                delta = (bday - today).days
                if 0 <= delta < 7:
                    if bday.weekday() >= 5:
                        bday += timedelta(days=(7 - bday.weekday()))
                    upcoming.append({"name": record.name.value, "birthday": bday.strftime("%d.%m.%Y")})
        return upcoming
