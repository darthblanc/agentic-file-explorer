from langchain_core.tools import ToolException
from setup_directory import construct_file_path
from file_dictionary import file_dict
from file import File
from rollback import commit_async
def read(path: str, data_dir: str | None = None) -> str:
    working_path = construct_file_path(path, data_dir)

    if path in file_dict:
        return file_dict.files[path].get_content()

    try:
        with open(working_path, "r") as fd:
            content = fd.read()
            file_dict.add(File.new_file(path, "text/plain"))
            return content
    except Exception as e:
        raise ToolException(e)

def write(path: str, content: str, data_dir: str | None = None) -> str:
    working_path = construct_file_path(path, data_dir)
    try:
        with open(working_path, "w") as fd:
            fd.write(content)
            file_dict.add(File.new_file(path, "text/plain"))
            commit_async(path, "write_txt", data_dir)
            return f"Write successful on {path}"
    except Exception as e:
        raise ToolException(e)

def append(path: str, content: str, data_dir: str | None = None) -> str:
    working_path = construct_file_path(path, data_dir)
    try:
        with open(working_path, "a") as fd:
            fd.write(f"\n{content}")
            file_dict.add(File.new_file(path, "text/plain"))
            commit_async(path, "append_txt", data_dir)
            return f"Write successful on {path}"
    except Exception as e:
        raise ToolException(e)

def clear(path: str, data_dir: str | None = None) -> str:
    working_path = construct_file_path(path, data_dir)
    try:
        with open(working_path, "w") as fd:
            fd.write("")
            file_dict.add(File.new_file(path, "text/plain"))
            commit_async(path, "clear_txt", data_dir)
            return f"Write successful on {path}"
    except Exception as e:
        raise ToolException(e)
