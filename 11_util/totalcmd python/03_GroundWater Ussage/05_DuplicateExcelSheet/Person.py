class Person:
    """
    Represents a person with a name, age, and optional address.
    """

    def __init__(self, name: str, age: int, address: str = None):
        """
        Initializes a Person object.

        Args:
            name (str): The name of the person.
            age (int): The age of the person.
            address (str, optional): The address of the person. Defaults to None.

        Raises:
            TypeError: If name is not a string or age is not an integer.
            ValueError: If age is negative.
        """
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(age, int):
            raise TypeError("Age must be an integer.")
        if age < 0:
            raise ValueError("Age cannot be negative.")

        self.name = name
        self.age = age
        self.address = address

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_address(self):
        """
        Returns the address of the person.
        """
        return self.address

    def __str__(self):
        """
        Returns a string representation of the Person object.

        Returns:
            str: A string in the format "Name: [name], Age: [age], Address: [address]"
                 or "Name: [name], Age: [age]" if address is None.
        """
        if self.address:
            return f"Name: {self.name}, Age: {self.age}, Address: {self.address}"
        else:
            return f"Name: {self.name}, Age: {self.age}"

    def __repr__(self):
        """
        Returns a detailed string representation of the Person object.

        Returns:
            str: A string in the format "Person(name='[name]', age=[age], address='[address]')"
                 or "Person(name='[name]', age=[age])" if address is None.
        """
        if self.address:
            return f"Person(name='{self.name}', age={self.age}, address='{self.address}')"
        else:
            return f"Person(name='{self.name}', age={self.age})"

    def celebrate_birthday(self):
        """
        Increments the person's age by 1.
        """
        self.age += 1
        print(f"Happy Birthday, {self.name}! You are now {self.age} years old.")

    def update_address(self, new_address: str):
        """
        Updates the person's address.

        Args:
            new_address (str): The new address.

        Raises:
            TypeError: If new_address is not a string.
        """
        if not isinstance(new_address, str):
            raise TypeError("New address must be a string.")
        self.address = new_address
        print(f"{self.name}'s address has been updated to: {self.address}")



def main():
    person1 = Person("Alice", 25, "123 Main St")
    person2 = Person("Bob", 30)

    print(person1)
    print(person2)


if __name__ == "__main__":
    main()
