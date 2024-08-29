def input_columns(table):
    columns = {
        "users": ["id", "name", "age"],
        "products": ["pid", "prod", "quantity"],
        "sales": ["sid", "id", "pid"]
    }

    # Проверка существования таблицы
    if table not in columns:
        print("Таблица не найдена.")
        return None

    # Выбор полей для отображения
    available_fields = columns[table]
    fields = input(
        f"Выберите одно или несколько полей {available_fields} для отображения (или введите * для всех): ").strip().split()

    # Проверка корректности введенных полей
    if fields == ["*"]:
        fields = available_fields
    elif not set(fields).issubset(available_fields):
        print("Введены некорректные поля. Будет использовано значение *.")
        fields = available_fields

    # Запрос условия для фильтрации
    if len(fields) == 1:
        value = input(f"Введите значение для поля {fields[0]} (или '0' для всех значений): ").strip()
        if value != '0':
            sign = input(f"Введите знак сравнения (>, <, >=, <=, =): ").strip()
            if sign not in ['>', '<', '>=', '<=', '=']:
                print("Некорректный знак сравнения. Будет использовано значение =.")
                sign = '='
            return f"SELECT * FROM {table} WHERE {fields[0]} {sign} %s", (value,)
    elif len(fields) > 1:
        return f"SELECT {', '.join(fields)} FROM {table}", ()

    return f"SELECT * FROM {table}", ()
