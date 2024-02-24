from collections import namedtuple


def init_calculator():
    result = 0

    def add(number):
        nonlocal result
        result += number

    def subtract(number):
        nonlocal result
        result -= number

    def multiply(number):
        nonlocal result
        result *= number

    def divide(number):
        nonlocal result
        result /= number

    def get_result():
        return result

    Calculator = namedtuple(
        "Calculator", ["Add", "Subtract", "Divide", "Multiply", "Get_result"]
    )

    return Calculator(add, subtract, divide, multiply, get_result)


Calci = init_calculator()

Calci.Add(5)
Calci.Subtract(1)
Calci.Multiply(2)
print(Calci.Get_result())
