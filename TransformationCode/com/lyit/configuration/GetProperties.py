import configparser
import os

class GetPropertiesMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GetProperties(metaclass=GetPropertiesMeta):
    def get_properties_ini(self):
        config = configparser.ConfigParser()
        return config.read('properties.ini')


    def get_git_clone_commands(self):
        print(os.getcwd())
        commands = []
        gitCloneCommandsFile = '../configuration/CommandLineExecutionFiles/GitCloneCommands.txt'
        with open(gitCloneCommandsFile) as file:
            for line in file.readlines():
                commands.append(line)
        return commands

    def get_git_push_command_file(self):
        print(os.getcwd())
        commands = []
        gitPushCommandsFile = '../configuration/CommandLineExecutionFiles/GitPushCommandsFile.txt'
        with open(gitPushCommandsFile) as file:
            for line in file.readlines():
                commands.append(line)
        return commands

#if __name__ == "__main__":
#    getProperties = GetProperties()
#    commands = getProperties.get_gitCloneCommands()
#    for command in commands:
#        print(command)