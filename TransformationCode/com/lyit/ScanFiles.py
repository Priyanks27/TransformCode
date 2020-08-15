from shutil import copyfile
import subprocess
import os
import os.path
import getpass

SourceProject = "GoogleCloud"
IntermediateProject = "SpringBoot"
TargetProject = "AWS"
ProjectFileLocations = "C:/Users/priyank/Documents/DissertationWorkspace/ProjectFiles"
project_location = "C:/Users/priyank/Documents/DissertationWorkspace/ProjectFiles"
key_file_name = "infinity-285116-e251fab2bd91.json"
destination = "C:/Users/priyank/Documents/DissertationWorkspace/InventoryServiceGCPTemplate/src/main/resources"
explore_model_class = ""
explore_repository = ""
loadRuleSet = ""
custom_configuration = "dev"
custom_configuration_path = "C:/Users/%username%/AppData/Roaming/gcloud/configurations"

def check_file_exists(file):
    if os.path.isfile(file):
        return True
    return False


def delete_file_if_exists(file):
    if check_file_exists(file):
        os.remove(file)


def copy_key_file():
    source_path = os.path.join(project_location, key_file_name)
    print(source_path)
    destination_path = os.path.join(destination, key_file_name)
    print(destination_path)
    delete_file_if_exists(destination_path)
    copyfile(source_path, destination_path)


def copy_config_file():
    source_path = os.path.join(project_location, custom_configuration)
    print(source_path)
    destination_path = os.path.join(destination, custom_configuration)
    print(destination_path)
    delete_file_if_exists(destination_path)
    copyfile(source_path, destination_path)


def scan_files():
    # copy the key , project.json file from resources folder to project folder
    copy_key_file()
    #copy_config_file()


def run_command_line(payload, method="run"):
    print(method)
    print("Executing command : " + payload)
    if method is "run":
        p = subprocess.run(payload, shell=True, check=True)
        print(p)
        return p.returncode
    if method is "chdir":
        os.chdir(payload)


def get_configuration_file():
    print(os.path.join(custom_configuration_path, custom_configuration))
    return os.path.join(custom_configuration_path, custom_configuration)


def get_username():
    print(getpass.getuser())
    return getpass.getuser()


def execute_command():
    try:
        command1 = "C:/Users/priyank/Documents/DissertationWorkspace/InventoryServiceGCPTemplate/src/main/resources"
        return_code = run_command_line(command1, "chdir")
        if return_code is not None:
            raise subprocess.CalledProcessError

        command2 = "gcloud auth activate-service-account --key-file=infinity-285116-e251fab2bd91.json"
        return_code = run_command_line(command2)
        if return_code != 0:
            raise subprocess.CalledProcessError

        try:
            command3 = "gcloud config configurations create " + get_configuration_file()
            command3 = command3.replace("%username%", get_username())
            return_code = run_command_line(command3)
            if return_code != 0:
                raise subprocess.CalledProcessError
        except Exception as e:
            print("Configuration Exists!")
            print(e)

        command4 = "gcloud config configurations activate " + custom_configuration
        return_code = run_command_line(command4)
        if return_code != 0:
            raise subprocess.CalledProcessError

    except subprocess.CalledProcessError as e:
        print("Error occurred while executing command: ")
        print(e)
    except Exception as e:
        print("Error occurred while executing command")
        print(e)


if __name__ == "__main__":
    scan_files()
    execute_command()