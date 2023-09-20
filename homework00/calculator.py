import math
import typing as tp


def calc(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    if command == "+":
        return num_1 + num_2
    if command == "-":
        return num_1 - num_2
    if command == "*":
        return num_1 * num_2
    if command == "/":
        return num_1 / num_2
    if command == "**":
        return num_1**num_2
    return f"Неизвестный оператор: {command!r}."


def calc_solo(num_1: float, command: str) -> tp.Union[float, str]:
    if command == "**2":
        return num_1**2
    if command == "sin":
        return math.sin(num_1)
    if command == "cos":
        return math.cos(num_1)
    if command == "tg":
        return math.tan(num_1)
    if command == "ln":
        return math.log(num_1, math.e)
    if command == "lg":
        return math.log10(num_1)
    return f"Неизвестный оператор: {command!r}."


if __name__ == "__main__":
    a = ["**2", "sin", "cos", "tg", "ln", "lg"]
    while True:  # программа выполняется до ввода 0 вместо команды
        COMMAND = input("Введите оперaцию > ")
        if COMMAND.isdigit() and int(COMMAND) == 0:
            break
        FLAG = True
        while FLAG:
            FLAG_2 = True
            try:
                NUM_1 = float(input("Первое число > "))
            except ValueError:
                print("Вы ввели не число. Попробуйте снова.")
            else:
                if COMMAND in a:
                    print(calc_solo(NUM_1, COMMAND))
                else:
                    while FLAG_2:
                        try:
                            NUM_2 = float(input("Второе число > "))
                        except ValueError:
                            print("Вы ввели не число. Попробуйте снова.")
                        else:
                            print(calc(NUM_1, NUM_2, COMMAND))
                            FLAG_2 = False
                FLAG = False


# if __name__ == "__main__":
#     str1 = input('Введите выражение, разделяя числа и операции пробелами: ').split()
#     first_pri = ['**', 'sin', 'cos', 'tg', 'ln', 'lg']
#     d = {}
#     for i in range(len(str1)):
#         if str1[i] in first_pri and str1[i] not in d:
#             d[str1[i]] = [str1[i-1], str1[i+1]]
#         elif str1[i] in first_pri:
#             d[str1[i]] += 1
#     print(str1, d)
