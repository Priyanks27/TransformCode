import os


class CommandLineChangeDirectoryMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class CommandLineChangeDirectory(metaclass=CommandLineChangeDirectoryMeta):
    def execute_change_directory(self, directory):
        if os.path.isdir(directory):
            os.chdir(directory)
