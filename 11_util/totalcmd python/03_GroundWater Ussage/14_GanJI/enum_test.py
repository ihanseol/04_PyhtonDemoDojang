from enum import Enum, Flag, auto, unique

# Regular enum with validation
@unique
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

try:
    # This will raise an error due to duplicate value
    @unique
    class InvalidColor(Enum):
        RED = 1
        GREEN = 1  # Duplicate value!
except ValueError as e:
    print(f"Error creating enum with duplicate values: {e}")

# Flag enum demonstrating bitwise operations
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

# Combine permissions
full_access = Permission.READ | Permission.WRITE | Permission.EXECUTE

print("\nFlag operations:")
print(f"Full access permissions: {full_access}")
print(f"Has read permission: {Permission.READ in full_access}")
print(f"Has execute permission: {Permission.EXECUTE in full_access}")

# Check individual permissions
read_only = Permission.READ
print(f"\nRead-only permissions:")
print(f"Has read permission: {Permission.READ in read_only}")
print(f"Has write permission: {Permission.WRITE in read_only}")



