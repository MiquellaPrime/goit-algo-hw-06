import re
from collections import UserDict


def validate_phone(phone: str):
    """Нормалізує та превіряє номер телефону."""
    cleaned_phone = re.sub(r"\D+", "", phone)

    if len(cleaned_phone) != 10:
        raise ValueError(f"Invalid phone: {cleaned_phone}")
    
    return cleaned_phone


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone: str):
        super().__init__(validate_phone(phone))


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str):
        """Додає новий телефон до запису."""
        if self.find_phone(phone) is not None:
            raise ValueError(f"Phone number '{phone}' already exists.")
        
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """Видаляє телефон із запису."""
        found_phone = self.find_phone(phone)
        if found_phone is None:
            raise ValueError(f"Phone number '{phone}' not found.")
        
        self.phones.remove(found_phone)

    def edit_phone(self, old: str, new: str):
        """Замінює телефон на нове значення."""
        for i, phone in enumerate(self.phones):
            if phone.value == old:
                self.phones[i] = Phone(new)
                return
        
        raise ValueError(f"Phone number '{old}' not found.")

    def find_phone(self, phone: str) -> Phone | None:
        """Шукає телефон у записі."""
        for p in self.phones:
            if p.value == phone:
                return p
        
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        """Додає запис до адресної книги."""
        if record.name.value in self.data:
            raise KeyError(f"Record for '{record.name.value}' already exists.")
        
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Record | None:
        """Знаходить запис за ім'ям контакта."""
        return self.data.get(name)

    def delete(self, name: str) -> Record:
        """Видаляє запис, повертаючи видалене значення."""
        if self.find(name) is None:
            raise KeyError(f"Name '{name}' not found.")
        
        return self.data.pop(name)
    
    def __str__(self):
        return "\n".join(str(self.data[name]) for name in sorted(self.data)) or "Address book is empty."
