import os
from com.lyit.configuration.GetProperties import GetProperties


class RuleCassandraTransformToH2Meta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RuleCassandraTransformToH2(metaclass=RuleCassandraTransformToH2Meta):

    __class_name = None
    __constructor = None

    def get_class_name(self):
        return self.__class_name

    def get_constructor(self):
        return self.__constructor

    def set_class_name(self, _classname):
        self.__class_name = _classname

    def set_constructor(self, _constructor):
        self.__constructor = _constructor

    def get_models_base_class_path(self, staging_area):
        for source_directory, directory_names, file_names in os.walk(staging_area):
            if "models" in directory_names:
                return source_directory + "/models"

    def get_all_models_on_path(self, path):
        for source_directory, directory_names, file_names in os.walk(path):
            return file_names

    def get_repository_base_class_path(self, staging_area):
        for source_directory, directory_names, file_names in os.walk(staging_area):
            if "repository" in directory_names:
                return source_directory + "/repository"

    def get_all_repositories_on_path(self, path):
        for source_directory, directory_names, file_names in os.walk(path):
            return file_names

    def get_lines_to_be_removed_from_model(self):
        get_properties = GetProperties()
        return get_properties.get_lines_to_be_removed_from_model()

    def get_lines_to_be_added_from_model(self):
        get_properties = GetProperties()
        return get_properties.get_lines_to_be_added_to_model()

    def strip_list(self, list):
        updated_list = []
        for item in list:
            updated_list.append(item.strip())
        return updated_list

    def add_annotations_before_class(self, lines, lines_to_be_added):
        index = None
        for counter in range(len(lines) - 1):
            if lines[counter].strip().find("class") != -1:
                index = counter
                break
        counter = 0
        for line_to_be_added in lines_to_be_added:
            lines.insert(index, line_to_be_added + "\n")
        return lines

    def add_id_generated_value(self, lines):
        index = None
        for counter in range(len(lines) - 1):
            if lines[counter].strip().find("id") != -1:
                index = counter
                break
        if index is not None:
            lines.insert(index, "    @Id\n")
            lines.insert(index + 1, "    @GeneratedValue\n")
        return lines

    def remove_annotated_index(self, lines):
        annotations_index_to_be_removed = []
        for counter in range(len(lines) - 1):
            if lines[counter].strip().startswith("@"):
                annotations_index_to_be_removed.append(counter)
            if lines[counter].strip().find(self.get_class_name()) != -1:
                annotations_index_to_be_removed.append(counter)
                break

        start_index = annotations_index_to_be_removed[0]
        end_index = annotations_index_to_be_removed[-1]
        del lines[start_index: end_index]
        return lines

    def remove_constructor(self, lines):
        annotations_index_to_be_removed = []
        for counter in range(len(lines) - 1):
            if lines[counter].strip().find(self.__constructor) != -1:
                annotations_index_to_be_removed.append(counter)
            if lines[counter].strip().find("}") != -1:
                annotations_index_to_be_removed.append(counter)
                break

        start_index = annotations_index_to_be_removed[0]
        end_index = annotations_index_to_be_removed[-1] + 1
        del lines[start_index: end_index]
        return lines

    def remove_elements_from_list(self, model_lines, model_remove_lines):
        updated_list = []
        for line in model_lines:
            if line.strip() not in model_remove_lines:
                updated_list.append(line)
            if line.strip().find("class") != -1:
                self.set_class_name(line.split(" ")[2])
                self.set_constructor(self.get_class_name() + "()")
        return updated_list

    def update_cassandra_to_jpa(self, repo_lines):
        updated_list = []
        for line in repo_lines:
            if line.find("extends CassandraRepository") != -1:
                line = line.replace("extends CassandraRepository", "extends JpaRepository")
                updated_list.append(line)
            else:
                updated_list.append(line)
        return updated_list

    def update_repo_lines(self, repo_lines, repo_lines_to_be_updated):
        index = None
        line_to_be_removed = repo_lines_to_be_updated[0]
        line_to_be_added = repo_lines_to_be_updated[1]
        for counter in range(len(repo_lines)):
            if repo_lines[counter].strip() == line_to_be_removed:
                index = counter
                break
        del repo_lines[index]
        repo_lines.insert(index, line_to_be_added + "\n")
        return repo_lines

    def get_repo_lines_to_be_updated(self):
        getProperties = GetProperties()
        return getProperties.get_update_imports_statement_repository()

    def transform_model(self, model):
        model_lines = []
        model_add_lines = self.get_lines_to_be_added_from_model()
        model_remove_lines = self.get_lines_to_be_removed_from_model()
        with open(model, "r") as model_file:
            model_lines = model_file.readlines()

        model_remove_lines = self.strip_list(model_remove_lines)
        model_add_lines = self.strip_list(model_add_lines)
        model_lines = self.remove_elements_from_list(model_lines, model_remove_lines)
        model_lines = self.remove_annotated_index(model_lines)
        model_lines = self.remove_constructor(model_lines)

        model_lines = self.add_id_generated_value(model_lines)
        model_lines = self.add_annotations_before_class(model_lines, model_add_lines)

        with open(model, "w") as model_updated_file:
            model_updated_file.writelines(model_lines)


    def transform_repository(self, repository):
        print(repository)

        repo_lines = []
        repo_lines_to_updated = self.get_repo_lines_to_be_updated()
        with open(repository, "r") as repo_file:
            repo_lines = repo_file.readlines()

        repo_lines_to_updated = self.strip_list(repo_lines_to_updated)
        repo_lines = self.update_repo_lines(repo_lines, repo_lines_to_updated)
        repo_lines = self.update_cassandra_to_jpa(repo_lines)

        with open(repository, "w") as repo_updated_file:
            repo_updated_file.writelines(repo_lines)


    def load_rule_lib_cassandra_to_h2(self, staging_area):
        print(staging_area)

        try:
            repository_base_class_path = self.get_repository_base_class_path(staging_area)
            repositories = self.get_all_repositories_on_path(repository_base_class_path)
            for repository in repositories:
                self.transform_repository(os.path.join(repository_base_class_path, repository))
        except Exception as e:
            print("Exception occurred while transforming model from unsupported dependency")
            return False


        try:
            models_base_class_path = self.get_models_base_class_path(staging_area)
            models = self.get_all_models_on_path(models_base_class_path)
            for model in models:
                self.transform_model(os.path.join(models_base_class_path, model))
        except Exception as e:
            print("Exception occurred while transforming model from unsupported dependency")
            return False

        return True


if __name__ == "__main__":
    staging_area = "C:/Users/priyank/Documents/Resources/StagingArea/8cb6897969bc4fdd8edfa95f6f751ee9"
    rule_Cassandra_Transform_To_H2 = RuleCassandraTransformToH2()
    rule_Cassandra_Transform_To_H2.load_rule_lib_cassandra_to_h2(staging_area=staging_area)