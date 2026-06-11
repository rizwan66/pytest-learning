class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
        self.is_active = True
        self._cart = []

    def deactivate(self):
        self.is_active = False

    def add_to_cart(self, item):
        self._cart.append(item)

    def remove_from_cart(self, item):
        self._cart.remove(item)

    def cart_total(self, prices: dict) -> float:
        return sum(prices.get(item, 0) for item in self._cart)

    def is_adult(self):
        return self.age >= 18

    def __repr__(self):
        return f"User(name={self.name!r}, email={self.email!r})"
