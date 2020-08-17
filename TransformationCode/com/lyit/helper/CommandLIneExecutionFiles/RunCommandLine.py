import os
import subprocess


class RunCommandLineMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RunCommandLine(metaclass=RunCommandLineMeta):
    def run_command_line(self, payload, method="run"):
        print(method)
        print("Executing command : " + payload)
        if method is "run":
            p = subprocess.run(payload, shell=True, check=True)
            print(p)
            return p.returncode
        if method is "chdir":
            os.chdir(payload)