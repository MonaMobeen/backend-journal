from dataclasses import dataclass


# ---------- Classes and Objects ----------
class Dog:
    # ---------- Class Attribute ----------
    # Shared by ALL instances of this class, unless overridden per-instance
    species = "Canis familiaris"

    # ---------- __init__ and Instance Attributes ----------
    def __init__(self, name: str, age: int):
        self.name = name   # instance attribute - unique to each object
        self.age = age
        self._energy = 100  # "protected" attribute (see Encapsulation below)

    # ---------- Instance Method ----------
    def bark(self):
        return f"{self.name} says Woof!"

    def __repr__(self):
        return f"Dog(name={self.name!r}, age={self.age})"


# Creating objects (instances) from the class
dog1 = Dog("Rex", 3)
dog2 = Dog("Buddy", 5)

print(dog1.bark())
print(f"Both dogs share species: {dog1.species}, {dog2.species}")
print(f"Repr example: {dog1}")


# ---------- Encapsulation ----------
class BankAccount:
    """
    Encapsulation means controlling access to internal data.
    The underscore prefix (_balance) signals "internal use only" by convention
    (Python doesn't strictly enforce privacy, but this is the standard pattern).
    """

    def __init__(self, owner: str, balance: float = 0):
        self.owner = owner
        self._balance = balance  # internal state, not meant to be set directly

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount

    def withdraw(self, amount: float):
        if amount > self._balance:
            raise ValueError("Insufficient funds.")
        self._balance -= amount

    # ---------- Properties ----------
    @property
    def balance(self):
        """Exposes _balance as a read-only attribute: account.balance (no parentheses)."""
        return self._balance


account = BankAccount("Frozen", 100)
account.deposit(50)
print(f"Balance after deposit: {account.balance}")


# ---------- Inheritance ----------
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."


class Cat(Animal):  # Cat inherits everything from Animal
    def speak(self):  # ---------- Polymorphism: overriding the parent's method ----------
        return f"{self.name} says Meow!"


class Bird(Animal):
    def speak(self):
        return f"{self.name} says Tweet!"


animals = [Animal("Generic Animal"), Cat("Whiskers"), Bird("Tweety")]
print("Polymorphism example - same method call, different behavior per class:")
for animal in animals:
    print(animal.speak())


# ---------- Composition ----------
class Engine:
    def start(self):
        return "Engine started."


class Car:
    """
    Composition: a Car HAS-AN Engine, rather than a Car BEING an Engine
    (which inheritance would imply). Prefer composition when the
    relationship is "has a part", not "is a type of".
    """

    def __init__(self, brand: str):
        self.brand = brand
        self.engine = Engine()  # Car is composed of an Engine

    def start(self):
        return f"{self.brand}: {self.engine.start()}"


car = Car("Toyota")
print(car.start())


# ---------- @classmethod and @staticmethod ----------
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float):
        """
        classmethod receives the CLASS itself (cls), not an instance.
        Useful for alternative constructors.
        """
        celsius = (fahrenheit - 32) * 5 / 9
        return cls(celsius)

    @staticmethod
    def is_freezing(celsius: float) -> bool:
        """
        staticmethod receives neither self nor cls - it's just a regular
        function that logically belongs to this class.
        """
        return celsius <= 0


temp = Temperature.from_fahrenheit(98.6)
print(f"Converted temperature: {temp.celsius:.2f}C")
print(f"Is 0C freezing? {Temperature.is_freezing(0)}")


# ---------- Dataclasses ----------
@dataclass
class User:
    """
    @dataclass automatically generates __init__, __repr__, and __eq__
    for simple data-holding classes - no need to write boilerplate.
    """
    name: str
    age: int


user = User(name="Frozen", age=25)
print(f"Dataclass example: {user}")


# ---------- When a function/dict is simpler than a class ----------
# If you're just holding data with no behavior, a dict or dataclass is often
# simpler than a full class with methods. Reserve full classes for when
# you need behavior (methods) tightly coupled to the data.

def calculate_total(price: float, quantity: int) -> float:
    """A plain function is simpler here - no state needs to be tracked."""
    return price * quantity


print(f"Simple function instead of a class: {calculate_total(10, 3)}")