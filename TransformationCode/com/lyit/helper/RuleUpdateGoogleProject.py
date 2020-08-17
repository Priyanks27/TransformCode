import os
from shutil import copyfile


class RuleUpdateGoogleProject:

    def __init__(self, project_templates_location="", project_base_location="", application="", service=""):
        self.__project_templates_location = project_templates_location
        self.__project_base_location = project_base_location
        self.__application = application
        self.__service = service

    # getter method
    def get_project_templates_location(self):
        return self.__project_templates_location

    # getter method
    def get_project_location(self):
        return self.__project_base_location

    # getter method
    def get_application(self):
        return self.__application

    # getter method
    def get_service(self):
        return self.__service

    # setter method
    def set_project_templates_location(self, project_templates_location):
        self.__project_templates_location = project_templates_location

    # setter method
    def set_project_location(self, project_location):
        self.__project_base_location = project_location

    # setter method
    def set_application(self, application):
        self.__application = application

    # setter method
    def set_service(self, service):
        self.__service = service

    def copy_web_app_folder(self, project_type):
        source = os.path.join(self.__project_templates_location, "webapp")
        destination = os.path.join(self.__project_base_location, "src/main")

        print(source)
        print(destination)

        #Check whether the directory structre already exists
        os.chdir(destination)
        if "webapp" not in os.listdir(destination):
            os.mkdir("webapp")
        destination_directory = os.path.join(destination, "webapp")
        os.chdir(destination_directory)

        self.copy_directory_with_files(destination_directory, source)

    def copy_directory_with_files(self, destination_directory, source):
        for source_directory, directory_names, file_names in os.walk(source):
            print(source_directory)
            print(directory_names)
            print(file_names)

            os.chdir(source_directory)
            if len(file_names) > 0:
                self.copy_files_in_directory(destination_directory, source_directory, file_names)

            if len(directory_names) == 0:
                return
            for directory_name in directory_names:
                source_directory = os.path.join(source_directory, directory_name)
                os.chdir(source_directory)
                destination_directory = os.path.join(destination_directory, directory_name)
                if not os.path.isdir(destination_directory):
                    os.mkdir(destination_directory)
                    os.chdir(destination_directory)

                # copy_files_in_directory(destination_directory, source_directory, )

    def copy_files_in_directory(self, destination_directory, source_directory_path, file_names):
        # Copy all the files in the current directory
        for file in file_names:
            copyfile(os.path.join(source_directory_path, file), os.path.join(destination_directory, file))


if __name__ == "__main__":
    transform = RuleUpdateGoogleProject("C:/Users/priyank/Documents/DissertationWorkspace/ProjectFiles",
                               "C:/Users/priyank/Documents/DissertationWorkspace/InventoryServiceGCPTemplate",
                               "multicloud",
                               "inventory-service")
    transform.copy_web_app_folder("generic_to_google")




