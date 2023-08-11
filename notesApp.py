import datetime
import json
import os
import random
from pathlib import Path


def create_note(notes: list):
    note = dict(
        note_id=get_id(),
        note_title=input("Введите заголовок заметки >>> ").upper(),
        note_body=input("Введите тело заметки >>> \n"),
        create_date=format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )
    notes.append(note)

    save_in_file(note)
    return note


def delite_note(notes: list):
    id = input('Введите ID заметки, которую нужно удалить\n>>> ')
    found = list(filter(lambda el: id in str(el['note_id']), notes))
    print(found)

    if len(found) <= 0:
        print('Такой заметки нет :с')
    elif len(found) > 0:
        ind = notes.index(found[0])
        notes.pop(ind)

    file_name = str(found[0].get('note_id')) + ". " + found[0].get('note_title')
    print(file_name)
    path = file_path(file_name)
    if os.path.exists(path):
        os.remove(path)
    else:
        print("Такой заметки не существует")


def edit_note(notes: list):
    id = input('Введите ID заметки, которую нужно изменить\n>>> ')
    found = list(filter(lambda el: id in str(el['note_id']), notes))
    if len(found) == 0:
        print("Такой заметки не существует!")
        return notes
    print(found)
    ind = 0
    res = 0
    for i in notes:
        if i == found[0]:
            res = ind
        ind += 1

    print("Вы хотите поменять ТЕЛО(T) или ЗАГОЛОВОК(З) заметки? Или ПОЛНОСТЬЮ(П) изменить заметку?")
    print()
    command = input("Т/З/П >>> ").upper()

    if command == "Т":
        notes[res]["note_body"] = input("Введите новое тело заметки >>> ")
        change_date = {"change_date": format(datetime.datetime.now())}
        notes[res].update(change_date)
    if command == "З":
        notes[res]["note_title"] = input("Введите новое заголовок заметки >>> ")
        change_date = {"change_date": format(datetime.datetime.now())}
        notes[res].update(change_date)
    if command == "П":
        notes[res]["note_title"] = input("Введите новое заголовок заметки >>> ")
        notes[res]["note_body"] = input("Введите новое тело заметки >>> ")
        change_date = {"change_date": format(datetime.datetime.now())}
        notes[res].update(change_date)

    save_in_file(notes[res])

    return notes


def add_note(notes: list):
    id = input('Введите ID заметки, которую нужно изменить\n>>> ')
    found = list(filter(lambda el: id in str(el['note_id']), notes))
    print(found)
    ind = 0
    res = 0
    for i in notes:
        if i == found[0]:
            res = ind
        ind += 1

    adds = " " + input("Введите дополнение к телу заметки >>> ")
    notes[res]["note_body"] += adds
    change_date = {"change_date": format(datetime.datetime.now())}
    notes[res].update(change_date)

    delite_note(notes[res])
    save_in_file(notes[res])

    return notes


def file_path(file_name):
    return os.path.join(os.path.dirname(__file__), f'User/Notes/{file_name}.json')


def save_in_file(note: dict):
    path = file_path(f"{note.get('note_id')}. {note.get('note_title')}")

    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(note, file, ensure_ascii=False)


def load_from_file():
    file_name = input("Введите ID и заголовок заметки, которую необходимо прочитать в формате <id. NAME> ").upper()
    path = file_path(file_name)

    with open(path, 'r', encoding='UTF-8') as file:
        data = json.load(file)

    temp_list = [data]

    show_on_screen(temp_list)
    return data


def show_on_screen(notes: list) -> None:
    decode_keys = dict(
        note_id='ID: ',
        note_title='Заголовок: ',
        note_body='Тело заметки: \n',
        create_date='Создана: ',
        change_date='Изменено: '
    )
    pretty_text = str()

    notes = sorted(notes, key=lambda x: datetime.datetime.strptime(x['create_date'], '%Y-%m-%d %H:%M:%S'), reverse=False)

    for num, elem in enumerate(notes, 1):
        pretty_text += f'Заметка №{num}:\n'
        pretty_text += '\n'.join(f'{decode_keys[k]} {v}' for k, v in elem.items())
        pretty_text += '\n________\n'
    print(pretty_text)


def show_all_on_screen(notes: list):
    show_on_screen(notes)


def add_notes_list() -> list:
    notes = []
    directory = 'User/Notes'
    pathlist = Path(directory).glob('*.json')
    for path in pathlist:
        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)
        notes.append(data)
    return notes


def get_id():
    note_id = random.randint(0, 100)
    while id_set.__contains__(note_id):
        note_id = random.randint(0, 100)

    id_set.add(note_id)
    return note_id


def menu(data: list):
    command = -1
    commands = [
        'Выйти из меню',
        'Показать все заметки',
        'Создать заметку',
        'Удалить заметку',
        'Изменить заметку',
        'Дополнить заметку',
        'Прочитать заметку'
    ]
    while command != 0:
        print('=====МЕНЮ=====')
        print('\n'.join(f'{n}. {v}' for n, v in enumerate(commands)))
        command = int(input(f'\nУкажите номер команды: \n'))
        if command == 1:
            show_on_screen(data)
        elif command == 2:
            create_note(data)
        elif command == 3:
            delite_note(data)
        elif command == 4:
            edit_note(data)
        elif command == 5:
            add_note(data)
        elif command == 6:
            load_from_file()
        elif command == 0:
            print("До встречи!")
        else:
            print(f'Такой команды не существует!\n')


def main() -> None:
    notes = add_notes_list()
    menu(notes)


id_set = set()

if __name__ == '__main__':
    main()
