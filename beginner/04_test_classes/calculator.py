class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(("add", a, b, result))
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(("subtract", a, b, result))
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(("multiply", a, b, result))
        return result

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("division by zero")
        result = a / b
        self.history.append(("divide", a, b, result))
        return result

    def clear_history(self):
        self.history.clear()

    def last_result(self):
        if not self.history:
            return None
        return self.history[-1][-1]
