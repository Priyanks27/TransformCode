import os
import subprocess
import time

from com.lyit.configuration.GetProperties import GetProperties
from com.lyit.data.models.TransformationInput import TransformationInput
from com.lyit.helper.CommandLIneExecutionFiles.RunCommandLine import RunCommandLine
from com.lyit.helper.CreateRepository import CreateRepository


class CommandLineGitPushMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CommandLineGitPush(metaclass=CommandLineGitPushMeta):

    def execute_git_push(self, transformationInput: TransformationInput):
        properties = GetProperties()
        commands = properties.get_git_push_command_file()
        runCommandLine = RunCommandLine()
        createRepository = CreateRepository()
        _target_area = createRepository.get_targetArea_Dir()
        original_cur_dir = os.getcwd()
        result = None
        try:
            os.chdir(_target_area)
            for command in commands:
                command = command.strip()
                if command.find("<%message%>") != -1:
                    command = command.replace("<%message%>", "\"Automated check in at " +
                                              str(int(time.time())) + "\"")
                return_code = runCommandLine.run_command_line(command, "run")
                if return_code != 0:
                    raise subprocess.CalledProcessError
                else:
                    result = "success"
        except Exception as e:
            print("Error occurred while executing command : " + command)
            print(e)
            os.chdir(original_cur_dir)
            result = str(e)

        os.chdir(original_cur_dir)
        return result
