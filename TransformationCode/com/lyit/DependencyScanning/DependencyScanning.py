import time
from pathlib import Path

from bs4 import BeautifulSoup as beautifulSoup
import json
from com.lyit.DependencyScanning.GetDependencyProperties import GetDependencyProperties
from com.lyit.data.models.DependencyScanResultsModel import DependencyScanResultsModel
import os


class DependencyScanningMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DependencyScanning(metaclass=DependencyScanningMeta):

    __basePath = 'C:/Users/priyank/Documents/Resources/DependencyScanReport'

    def __scan_pom_file(self, pom_location):

        with open(pom_location, "r") as file:
            file_content = file.readlines()
            content = "".join(file_content)
            beautify_content = beautifulSoup(content, "lxml")
            results = beautify_content.find_all("dependency")
            dependencies = {}
            key = None
            value = None
            for res in results:
                for child in res.children:
                    if child.name == "groupid":
                        key = str(child.contents[0])
                    if child.name == "artifactid":
                        value = str(child.contents[0])
                    if key is not None and value is not None:
                        dependencies[key] = value
                        key = None
                        value = None
            return dependencies

    def scan_dependencies(self, source_pom_location, target_pom_location):
        results_model = DependencyScanResultsModel()

        source_pom_location = source_pom_location + "/pom.xml"
        target_pom_location = target_pom_location + "/pom.xml"
        source_pom_dependency_dictionary = self.__scan_pom_file(source_pom_location)
        target_pom_dependency_dictionary = self.__scan_pom_file(target_pom_location)

        value = {p: target_pom_dependency_dictionary[p]
                 for p in set(target_pom_dependency_dictionary) - set(source_pom_dependency_dictionary)}

        json_object = json.dumps(value, indent=4)
        print(json_object)
        results_model.set_extra_dependencies_in_target_dict(value)

        baseFileName = "extra_dependencies_in_target_"
        file_name = self.__generateReport(baseFileName, target_pom_location, value)
        results_model.set_extra_dependencies_in_target_report(file_name)

        value = {p: source_pom_dependency_dictionary[p]
                 for p in set(source_pom_dependency_dictionary) - set(target_pom_dependency_dictionary)}

        json_object = json.dumps(value, indent=4)
        print(json_object)
        results_model.set_extra_dependencies_in_source_dict(value)

        baseFileName = "extra_dependencies_in_source_"
        if len(value) == 0:
            value["NO extra dependencies in source"] = ""
        file_name = self.__generateReport(baseFileName, source_pom_location, value)
        results_model.set_extra_dependencies_in_source_report(file_name)

        required_dependency_dictionary = self.__get_dependencies()
        value = {p: source_pom_dependency_dictionary[p]
                 for p in set(source_pom_dependency_dictionary) - set(required_dependency_dictionary)}
        json_object = json.dumps(value, indent=4)
        baseFileName = "missing_required_dependencies_in_target_"
        self.__generateReport(baseFileName, source_pom_location, value)
        results_model.set_missing_required_dependencies_in_target(value)

        if len(value.items()) > 0:
            results_model.set_dependencies_satisfied(False)
        else:
            results_model.set_dependencies_satisfied(True)
        return results_model

    def __generateReport(self, basefileName, pom_location, value):
        path = self.__basePath + "/" + pom_location.split("/")[-2]
        if not os.path.isdir(path):
            Path(path).mkdir(parents=True, exist_ok=True)
        file_name = path + "/" + basefileName + str(int(time.time())) + ".json"
        with open(file_name, 'w') as outfile:
            json.dump(value, outfile, indent=4)
        return file_name

    def __get_dependencies(self):
        getDependencyProperties = GetDependencyProperties()
        return getDependencyProperties.get_dependencies_properties_ini()

#if __name__ == "__main__":
#    source_pom_location = "C:/Users/priyank/Documents/PythonWorkspace/TransformationCode/com/lyit/Resources/StagingArea/01a095a2e0904d3eb02ac61084740482/pom.xml"
#    target_pom_location = "C:/Users/priyank/Documents/PythonWorkspace/TransformationCode/com/lyit/Resources/TargetArea/0eecef0ee5a64339a3ce3d00c6e26a47/pom.xml"
#    dependencyScanning = DependencyScanning()
#    source = "C:\Users\priyank\Documents\Resources/pom.xml"
#    results_model = dependencyScanning.scan_pom_file(source)
#    print(results_model.get_dependencies_satisfied())
