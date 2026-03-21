import os
from uuid import uuid4


def hashed_name(instance, filename, folder):
    _, extension = os.path.splitext(filename)
    new_filename = f"{uuid4()}{extension.lower()}"
    return os.path.join(folder, new_filename)
