import re
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        self._validate_phone(value) 
        super().__init__(value)

    def _validate_phone(self, value: str):
        """Перевіряє коректність номера телефону."""
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError(f"Invalid phone number: {value!r}. The number must be 10 digits long.")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str):
        """Додає новий телефон до запису."""
        if self.find_phone(phone) is not None:
            raise ValueError(f"Phone number {phone!r} already exists.")
        
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        """Видаляє телефон із запису."""
        found_phone = self.find_phone(phone)
        if found_phone is None:
            raise ValueError(f"Phone number {phone!r} not found.")
        
        self.phones.remove(found_phone)

    def edit_phone(self, old: str, new: str):
        """Замінює телефон на нове значення."""
        for i, phone in enumerate(self.phones):
            if phone.value == old:
                self.phones[i] = Phone(new)
                return
        
        raise ValueError(f"Phone number {old!r} not found.")

    def find_phone(self, phone: str) -> Phone | None:
        """Шукає телефон у записі."""
        for p in self.phones:
            if p.value == phone:
                return p
        
        return None

    def __str__(self):
        mask = "({0}{1}{2})-{3}{4}{5}-{6}{7}-{8}{9}"  # Так буде ще красивіше виводитись номер
        phones_str = '; '.join(mask.format(*p.value) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        """Додає запис до адресної книги."""
        if record.name.value in self.data:
            raise KeyError(f"Record for {record.name.value!r} already exists.")
        
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Record | None:
        """Знаходить запис за ім'ям контакта."""
        return self.data.get(name)

    def delete(self, name: str) -> Record:
        """Видаляє запис, повертаючи видалене значення."""
        if self.find(name) is None:
            raise KeyError(f"Name {name!r} not found.")
        
        return self.data.pop(name)
    
    def __str__(self):
        return "\n".join(str(self.data[name]) for name in sorted(self.data)) or "Address book is empty."
