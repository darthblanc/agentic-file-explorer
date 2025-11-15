import re

def strip_base_directory(path: str):
    return re.sub(r"^data([\s\S]*)", r".\1", path)
