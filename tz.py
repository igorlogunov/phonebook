def start_menu() -> None:
    """ Функция, реализующая стартовое меню справочника """
    print('\nОткрыть список контактов - введи 1\n'
        'Добавить новый контакт - введи 2\n'
        'Перейти к поиску контакта  - введи 3\n'
        'Чтобы отредактировать контакт, выбери его в списке')
    answer = 0
    try:
        answer = int(input())
    except ValueError:
        print('Введи число')
        start_menu()

    if answer == 1 or answer == 3:
        read_entry(answer)
    elif answer == 2:
        add_entry()
    elif answer == 0:
        pass
    else:
        print('Такая команда не предусмотрена. Попробуй ещё раз')
        start_menu()

def enter_entries(n: int, all_entries: list) -> None:
    """
    Функия, для постраничного вывода контактов из списка

    :param n: номер, с которого начинается вывод
    :param all_entries: полный список контактов
    """
    for ind, entry in enumerate(all_entries[n:n + 10]):
        clean = entry.split('_!')
        print(n + ind + 1, clean[0], clean[1], clean[2], 'Организация:', clean[3],
              'Рабочий:', clean[4], 'Личный:', clean[5][:-2])
    answer = 1
    try:
        answer = int(input('Предыдущие 10 записей - 1, следующие 10 записей - 2, '
                           'редактировать контакт - 3, '
                           'вернуться в главное меню - 0 \n'))
    except ValueError:
        print('Введите число')
        enter_entries(n, all_entries)

    if answer == 1:
        if (n - 10) < 0:
            print('Это первая страница')
            enter_entries(n, all_entries)
        else:
            enter_entries(n - 10, all_entries)
    elif answer == 2:
        if (n + 10) > len(all_entries):
            print('Это последняя страница')
            enter_entries(n, all_entries)
        else:
            enter_entries(n + 10, all_entries)
    elif answer == 3:
        try:
            contact = int(input('Контакт под каким номером нужно отредактировать? '))
            redact_entry(contact, all_entries)
        except ValueError:
            print('Контакта с таким номером не существует')
            enter_entries(n, all_entries)
    elif answer == 0:
        start_menu()
    else:
        print('Такая команда не предусмотрена. Попробуй ещё раз.')
        enter_entries(n, all_entries)

def read_entry(num: int) -> None:
    """
    Функция для считывания списка контактов из файла

    :param num: ответ пользователя, полученный в стартовом меню с выбором действий
    """
    with open('phone_book.txt', 'r', encoding='utf-8') as file:
        all_entries = file.readlines()
        if not all_entries:
            print('Пока нет записей')
        else:
            if num == 1:
                enter_entries(0, all_entries)
            if num == 3:
                search_entry(all_entries)

def add_entry() -> None:
    """ Функция, для добавления нового контакта в список """
    surname = input('Введи фамилию: ')
    name = input('Введи имя: ')
    patronymic = input('Введи отчество: ')
    company = input('Введи название организации: ')
    work_phone = input('Введи рабочий телефон: ')
    clean_work_phone = ''.join(sym for sym in work_phone if sym.isdigit())
    personal_phone = input('Введи личный телефон: ')
    clean_personal_phone = ''.join(sym for sym in personal_phone if sym.isdigit())
    new_entry = surname + '_!' + name + '_!' + patronymic + '_!' \
                + company + '_!' + clean_work_phone + '_!' + clean_personal_phone + '\n'
    with open('phone_book.txt', 'a', encoding='utf-8') as file:
        file.write(new_entry)
        print('Запись добавлена')
    return_menu = input('Продолжить работу?(да/нет) ')
    if return_menu.lower() == 'да':
        start_menu()
    else:
        exit()

def redact_entry(contact: int, all_entries: list) -> None:
    """
    Функция для редактирования существующего контакта

    :param contact: порядковый номер контакта для редактирования, выбранный клиентом
    :param all_entries: полный список контактов
    """
    with open('phone_book.txt', 'w', encoding='utf-8') as file:
        for ind, entry in enumerate(all_entries):
            if ind + 1 == contact:
                surname = input('Введи фамилию: ')
                name = input('Введи имя: ')
                patronymic = input('Введи отчество: ')
                company = input('Введи название организации: ')
                work_phone = input('Введи рабочий телефон: ')
                clean_work_phone = ''.join(sym for sym in work_phone if sym.isdigit())
                personal_phone = input('Введи личный телефон: ')
                clean_personal_phone = ''.join(sym for sym in personal_phone if sym.isdigit())
                new_entry = surname + '_!' + name + '_!' + patronymic + '_!' \
                            + company + '_!' + clean_work_phone + '_!' + clean_personal_phone + '\n'
                file.write(new_entry)
            else:
                file.write(entry)
    return_menu = input('Продолжить работу?(да/нет) ')
    if return_menu.lower() == 'да':
        start_menu()
    else:
        exit()

def search_entry(all_entries: list) -> None:
    """
    Функция, реализующая поиск контактов в списке по различным характеристикам

    :param all_entries: полный список контактов
    """
    answer = 0
    try:
        answer = int(input('По какой характеристике искать запись?\n'
                       'ФИО - введи 1, организация - введи 2, телефон - введи 3 '))
    except ValueError:
        print('Введи число')
        search_entry(all_entries)
    count = 0
    if answer == 1:
        fio_search = input('Введи ФИО полностью(через пробел) или отдельно(фамилию, имя или отчество): ').lower()
        full_fio_search = fio_search.split()
        for entry in all_entries:
            clean = entry.split('_!')
            if fio_search in clean[0].lower() or fio_search in clean[1].lower() or fio_search in clean[2].lower():
                count += 1
                print(clean[0], clean[1], clean[2], 'Организация:', clean[3],
              'Рабочий:', clean[4], 'Личный:', clean[5][:-2])
            fio = [clean[0].lower(), clean[1].lower(), clean[2].lower()]
            if fio == full_fio_search:
                count += 1
                print(clean[0], clean[1], clean[2], 'Организация:', clean[3],
                      'Рабочий:', clean[4], 'Личный:', clean[5][:-2])
        if count == 0:
            print('Контакт не найден')
        return_menu = input('Продолжить работу?(да/нет) ')
        if return_menu.lower() == 'да':
            start_menu()
        else:
            exit()
    elif answer == 2:
        text_search = input('Введи текст для поиска: ').lower()
        for entry in all_entries:
            clean = entry.split('_!')
            if text_search in clean[3].lower():
                count += 1
                print(clean[0], clean[1], clean[2], 'Организация:', clean[3],
                      'Рабочий:', clean[4], 'Личный:', clean[5][:-2])
        if count == 0:
            print('Контакт не найден')
        return_menu = input('Продолжить работу?(да/нет) ')
        if return_menu.lower() == 'да':
            start_menu()
        else:
            exit()
    elif answer == 3:
        num_search = input('Введи номер для поиска(без 8): ')
        clean_num_search = ''.join(sym for sym in num_search if sym.isdigit())
        for entry in all_entries:
            clean = entry.split('_!')
            if clean_num_search in clean[4] or clean_num_search in clean[5]:
                count += 1
                print(clean[0], clean[1], clean[2], 'Организация:', clean[3],
                      'Рабочий:', clean[4], 'Личный:', clean[5][:-2])
        if count == 0:
            print('Контакт не найден')
        return_menu = input('Продолжить работу?(да/нет) ')
        if return_menu.lower() == 'да':
            start_menu()
        else:
            exit()
    else:
        print('Такая команда не предусмотрена. Попробуй ещё раз')
        search_entry(all_entries)


print('Привет! Это твой телефонный справочник')
with open('phone_book.txt', 'a', encoding='utf-8'):
    pass
start_menu()
