import subprocess

from com.lyit.configuration.GetProperties import GetProperties
from com.lyit.data.models.TransformationInput import TransformationInput
from com.lyit.helper.CommandLIneExecutionFiles.RunCommandLine import RunCommandLine
from com.lyit.helper.CreateRepository import CreateRepository


class CommandLineFetchGitHubMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CommandLineFetchGitHub(metaclass=CommandLineFetchGitHubMeta):
    def execute_fetch_github_url(self, transformationInput: TransformationInput):
        properties = GetProperties()
        commands = properties.get_git_clone_commands()
        runCommandLine = RunCommandLine()
        createRepository = CreateRepository()
        _staging_area = createRepository.get_stagingArea_Dir()

        result = None
        result = self.fetchFilesFromGithub(_staging_area, commands, result, runCommandLine,
                                           transformationInput.get_source_github_url())

        if result.find("Error") == 0:
            raise Exception(result)

        _target_area = createRepository.get_targetArea_Dir()
        result = self.fetchFilesFromGithub(_target_area, commands, result, runCommandLine,
                                           transformationInput.get_target_github_url())

        if result.find("Error") == 0:
            raise Exception(result)
        return result

    def fetchFilesFromGithub(self, workspace, commands, result, runCommandLine, githuburl):
        for command in commands:
            command = command.strip()
            if command.find("<%githuburl%>") != -1:
                command = command.replace("<%githuburl%>", githuburl)
            if command.find("<%foldername%>") != -1:
                command = command.replace("<%foldername%>", workspace)
            try:
                return_code = runCommandLine.run_command_line(command, "run")
                if return_code != 0:
                    raise subprocess.CalledProcessError
                else:
                    result = "success"
            except Exception as e:
                print("Error occurred while executing command : " + command)
                print(e)
        return result


