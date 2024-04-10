import os


def has_path(file_name) -> bool:  # if file_name include path like c:\\user\\this ...
    head, tail = os.path.split(file_name)
    print(f"The filename head :'{head}'  tail : {tail}  includes a path. Performing action...")

    if head:
        return True
    else:
        return False


has_path(r"d:\05_Send\pythonProject\TesseractTest.py")
