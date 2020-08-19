import os
from shutil import copyfile


class UpdateGoogleProject:

    def get_base_dir_servlet(self, target_area):
        for source_directory, directory_names, file_names in os.walk(target_area):
            for file in file_names:
                if file.lower().find("application") != -1:
                    return source_directory

    def copy_servlet_initializer(self, target_area):
        source_path = '../Resources/GoogleApp/ServletInitializer.java'
        target_path = self.get_base_dir_servlet(target_area) + "/ServletInitializer.java"
        copyfile(source_path, target_path)