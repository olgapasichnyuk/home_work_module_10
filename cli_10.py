from collections import UserDict


class Field:
    def __init__(self, name):
        self.value = name


class Name(Field):
    pass


class Phone(Field):
    pass


class Record(Field):
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                self.add_phone(new_phone_number)
                self.phones.remove(phone)
                return True

    def delete_phone(self, delete_number):
        for phone in self.phones:
            if phone.value == delete_number:
                self.phones.remove(phone)
                return True


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'There is no phone with that name, please enter valid name.'
        # except ValueError:
        # return 'Give me name and phone please'
        except IndexError:
            return 'Input please name and phone after the command "change" or "add"\nor name after the command "phone"'

    return inner


def exit_func():
    return 'Good bye!'


def start():
    return 'How can I help you?'


@input_error
def add_contact(name, phone):
    if address_book.data.get(name):
        return 'Contact already exist'

    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return 'The contact was added'


@input_error
def add_phone(name, phone):
    if address_book.data.get(name):
        record = address_book.data[name]
        record.add_phone(phone)
        return f'Phone number {phone} was added to contact with name {name}'
    else:
        return f'Contact with name {name} does not exist'


@input_error
def change(name, phone):
    new_phone = input('Input the new phone number: ')
    record = address_book.data[name]

    if record.change_phone(phone, new_phone) is True:
        return f'Phone number for contact with name {name}  was changed to {new_phone}'
    else:
        return 'Phone number does not exist'


@input_error
def delete_phone(name, phone):
    record = address_book.data[name]

    if record.delete_phone(phone) is True:
        return f'The contact with name {name} and phone {phone} was deleted'
    else:
        return 'Phone number does not exist'


@input_error
def show_phone(name):
    if name in address_book.data.keys():
        phones_list = []
        for phone in address_book.data[name].phones:
            phones_list.append(phone.value)
        return phones_list
    else:
        return f'The contacts book does not contain contact with name {name}'


def show_all():
    if not address_book.data:
        return 'Your contacts book is empty.'

    contacts = ''
    for name, record in address_book.items():
        phones = []
        for phone in record.phones:
            phones.append(phone.value)
        contacts += f'{name} | phones: {phones}\n'
    return contacts


def main():
    handler = {
        'hello': start,
        'show all': show_all,
        'add': add_contact,
        'add_phone': add_phone,
        'change': change,
        'phone': show_phone,
        'delete': delete_phone,
    }

    while True:
        user_input = input('Input the command').lower()
        parsed_input = user_input.split(' ')
        command = parsed_input[0]
        args_list = parsed_input[1:]

        if user_input in ['exit', 'close', 'good bye']:
            print(exit())
            break

        if user_input in handler.keys():
            msg = handler[user_input]()
            print(msg)
            continue

        elif handler.get(command):
            msg = handler[command](*args_list)
            print(msg)
            continue
        else:
            print('I do not understand the command')
            continue


if __name__ == '__main__':
    address_book = AddressBook()
    main()
