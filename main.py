import re


class BasicMathChecker:
    def check_expression(self, expression):
        expr = expression.replace(' ', '')

        balance = 0
        for char in expr:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False, "Несбалансированные скобки"

        if balance != 0:
            return False, "Несбалансированные скобки"

        valid_chars = set('0123456789+-*/.() ')
        if not all(char in valid_chars for char in expr):
            return False, "Недопустимые символы"

        operators = set('+-*/')
        for i in range(len(expr) - 1):
            if expr[i] in operators and expr[i + 1] in operators:
                return False, "Два оператора подряд"

        return True, "Выражение корректно"

    def calculate(self, expression):

        try:
            result = eval(expression)
            return result
        except:
            return "Ошибка вычисления"

    def find_expressions_in_text(self, text):

        pattern = r'[(\d+\s*[+\-*/]\s*)+\d+]+|\d+\s*[+\-*/]\s*\([^)]+\)|\([^)]+\)\s*[+\-*/]\s*\d+'

        expressions = []
        lines = text.split('\n')

        for line_num, line in enumerate(lines, 1):

            if any(op in line for op in ['+', '-', '*', '/', '=']):

                potential_exprs = re.findall(r'[^=]+=[^=]+|[+\-*/()\d.\s]+', line)

                for expr in potential_exprs:
                    expr = expr.strip()

                    if (any(char.isdigit() for char in expr) and
                            any(op in expr for op in ['+', '-', '*', '/']) and
                            len(expr) > 1):
                        expressions.append({
                            'expression': expr,
                            'line_number': line_num,
                            'line_text': line.strip()
                        })

        return expressions

    def analyze_file(self, filename):

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()

            print(f"\n Анализ файла: {filename}")
            print("=" * 50)

            expressions = self.find_expressions_in_text(content)

            if not expressions:
                print("Математические выражения не найдены")
                return

            print(f"Найдено потенциальных выражений: {len(expressions)}")
            print("-" * 50)

            valid_count = 0
            for i, expr_info in enumerate(expressions, 1):
                expr = expr_info['expression']
                line_num = expr_info['line_number']

                print(f"\n{i}. Строка {line_num}: {expr_info['line_text']}")
                print(f"   Выражение: {expr}")

                is_valid, message = self.check_expression(expr)

                if is_valid:
                    valid_count += 1
                    result = self.calculate(expr)
                    print(f"   {message}")
                    print(f"   Результат: {result}")
                else:
                    print(f"   {message}")

            print(f"\n Итоги анализа:")
            print(f"   Всего выражений: {len(expressions)}")
            print(f"   Корректных: {valid_count}")
            print(f"   Некорректных: {len(expressions) - valid_count}")

        except FileNotFoundError:
            print(f"Ошибка: Файл '{filename}' не найден")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")


def simple_calculator():
    calculator = BasicMathChecker()

    while True:
        print("\n=== ПРОСТОЙ КАЛЬКУЛЯТОР ===")
        print("1 - Ввод выражения с клавиатуры")
        print("2 - Анализ текстового файла")
        print("3 - Выход")

        choice = input("\n➡ Выберите действие (1-3): ").strip()

        if choice == '1':
            keyboard_input_mode(calculator)
        elif choice == '2':
            file_analysis_mode(calculator)
        elif choice == '3':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


def keyboard_input_mode(calculator):
    print("\n--- РЕЖИМ ВВОДА С КЛАВИАТУРЫ ---")
    print("Вводите выражения для проверки и вычисления")
    print("Пример: 2+3, (4+5)*2, 10/2")
    print("Для возврата введите '0'")

    while True:
        user_input = input("\n➡ Введите выражение: ").strip()

        if user_input.lower() in ['0']:
            break

        if not user_input:
            continue

        is_valid, message = calculator.check_expression(user_input)

        if is_valid:
            result = calculator.calculate(user_input)
            print(f"{message}")
            print(f"Результат: {user_input} = {result}")
        else:
            print(f"{message}")


def file_analysis_mode(calculator):
    print("\n--- РЕЖИМ АНАЛИЗА ФАЙЛА ---")
    print("Введите путь к текстовому файлу для поиска математических выражений")
    print("Для возврата введите '0'")

    while True:
        filename = input("\n➡ Введите путь к файлу: ").strip()

        if filename.lower() in ['0']:
            break

        if not filename:
            continue

        calculator.analyze_file(filename)
        break


if __name__ == "__main__":
    print("Загрузка математического анализатора...")

    simple_calculator()
