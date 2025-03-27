#
# from dataclasses import dataclass, field
# from typing import List
#
#
# @dataclass
# class InventoryItem:
#     """Class for keeping track of an item in inventory."""
#     name: str
#     unit_price: float
#     quantity_on_hand: int = 0
#
#     def total_cost(self) -> float:
#         return self.unit_price * self.quantity_on_hand
#
#
# # Create some items
# item1 = InventoryItem("Widget", 3.50)
# item2 = InventoryItem("Gadget", 2.75, quantity_on_hand=10)
#
# print(f"Item 1: {item1}")
# print(f"Item 2: {item2}")
# print(f"Total cost of item2: ${item2.total_cost():.2f}")
#
# # Demonstrate automatic comparison
# item3 = InventoryItem("Widget", 3.50)
# print(f"\nAre item1 and item3 equal? {item1 == item3}")
#



from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    height: float
    email: str

# Creating an instance of the dataclass
person = Person(name="Alice", age=25, height=5.5, email="[email protected]")
print(person)



