import os
import subprocess
import threading

from com.lyit.configuration.GetProperties import GetProperties
from com.lyit.helper.CommandLIneExecutionFiles.CommandLineChangeDirectory import CommandLineChangeDirectory
from com.lyit.helper.CommandLIneExecutionFiles.CommandLineFetchGitHub import CommandLineFetchGitHub
from com.lyit.helper.CommandLIneExecutionFiles.CommandLineGitPush import CommandLineGitPush


class CommandLineExecutorMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CommandLineExecutor(metaclass=CommandLineExecutorMeta):
    def execute(self, commandSequence, payload):

        if commandSequence is "FetchGitHub":
            commandLineFetchGitHub = CommandLineFetchGitHub()
            thread = threading.Thread(target=commandLineFetchGitHub.execute_fetch_github_url, args=[payload])
            thread.start()
            thread.join()
            #commandLineFetchGitHub.execute_fetch_github_url(payload)

        if commandSequence is "gitpush":
            commandLineGitPush = CommandLineGitPush()
            commandLineGitPush.execute_git_push(payload)

        if commandSequence is "ChangeDirectory":
            commandLineChangeDirectory = CommandLineChangeDirectory()
            commandLineChangeDirectory.execute_change_directory(payload)


