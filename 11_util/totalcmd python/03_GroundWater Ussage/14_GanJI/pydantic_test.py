
from pydantic import BaseModel
from datetime import date
from typing import Optional


class User(BaseModel):
    name: str
    email: str
    birth_date: Optional[date] = None

    class Config:
        # Allow extra fields
        extra = "allow"
        # Change the model name
        title = "UserModel"

    def get_age(self) -> int:
        if not self.birth_date:
            return 0
        today = date.today()
        return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))


# Create a valid user
user = User(name="John Doe", email="john@example.com")
print("Valid user:")
print(user)
print(f"Age: {user.get_age()}")

# Create a user with birth date
user_with_age = User(name="Jane Doe", email="jane@example.com", birth_date=date(1990, 1, 1))
print("\nUser with birth date:")
print(user_with_age)
print(f"Age: {user_with_age.get_age()}")

# Try creating an invalid user
try:
    invalid_user = User(name=123, email="invalid-email")
except Exception as e:
    print("\nValidation error:")
    print(str(e))