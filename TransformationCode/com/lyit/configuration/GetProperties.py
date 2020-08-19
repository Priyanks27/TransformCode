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


    def get_supported_environment_source_dependencies(self):
        print(os.getcwd())
        commands = []
        supported_environment_ini_file = '../RuleEngine/SupportedEnvironmentSource.ini'
        with open(supported_environment_ini_file) as file:
            for line in file.readlines():
                commands.append(line)
        return commands

    def get_supported_environment_target_google_dependencies(self):
        print(os.getcwd())
        commands = []
        supported_environment_ini_file = '../RuleEngine/SupportedEnvironmentTargetGoogle.ini'
        with open(supported_environment_ini_file) as file:
            for line in file.readlines():
                commands.append(line)
        return commands

    def get_transform_unsupported_dependency(self, unsupported_dependency):
        transform_unsupported_dependency__ini_file = '../RuleEngine/TransformUnSupportedDependency.ini'
        with open(transform_unsupported_dependency__ini_file) as file:
            for line in file.readlines():
                if unsupported_dependency.find(line) != -1:
                    return True
        return False

    def get_lines_to_be_removed_from_model(self):
        lines_to_be_removed_from_model_ini_file = '../RuleEngine/RemoveLinesFromModel.ini'
        lines = []
        with open(lines_to_be_removed_from_model_ini_file) as file:
            for line in file.readlines():
                lines.append(line)
            return lines

    def get_lines_to_be_added_to_model(self):
        lines_to_be_added_to_model_ini_file = '../RuleEngine/AddLinesToModel.ini'
        lines = []
        with open(lines_to_be_added_to_model_ini_file) as file:
            for line in file.readlines():
                lines.append(line)
        return lines

    def get_update_imports_statement_repository(self):
        lines_to_be_added_to_model_ini_file = '../RuleEngine/UpdateImportStatementInRepository.ini'
        lines = []
        with open(lines_to_be_added_to_model_ini_file) as file:
            for line in file.readlines():
                lines.append(line)
        return lines


if __name__ == "__main__":
    getProperties = GetProperties()
    commands = getProperties.get_gitCloneCommands()
    for command in commands:
        print(command)