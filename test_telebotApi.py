tests = {
    1: ('В сутках 24 часа?', {'A': 'Да', 'B': 'Нет', 'C': 'Больше 24', 'D': 'Меньше',}, 'A'),
    2: ('Сколько дней в году?', {'A': '100', 'B': '360', 'C': '280', 'D': '365',}, 'D'),
    3: ('Сколько дней в неделе?', {'A': '3', 'B': '4', 'C': '7', 'D': 'Не знаю',}, 'C'),
    4: ('Сколько дней в фервале (каждые 4 года)?', {'A': '31', 'B': '29', 'C': '28', 'D': '30',}, 'B'),
    5: ('Сколько секунд в одном часу?', {'A': '3600', 'B': '60', 'C': '1000', 'D': '100',}, 'A'),
}



for i, j in tests.items():
    if i == 1:
        print(j[1])
        print(list(j[1].keys()))
        print(list(j[1].values()))
        print(j[1]["A"])
        print(j[1]["B"])
        print(j[1]["C"])
        print(j[1]["D"])
