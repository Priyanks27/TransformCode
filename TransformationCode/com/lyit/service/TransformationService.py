import os
import time

from com.lyit.DependencyScanning.DependencyScanning import DependencyScanning
from com.lyit.Reporting.Reporting import Reporting
from com.lyit.RuleEngine.RuleEngine import RuleEngine
from com.lyit.RuleEngine.UpdateGoogleProject import UpdateGoogleProject
from com.lyit.TransformTarget.TransformCode import TransformCode
from com.lyit.configuration.GetProperties import GetProperties
from com.lyit.helper.CommandLIneExecutionFiles.CommandLineExecutor import CommandLineExecutor
from com.lyit.helper.CreateRepository import CreateRepository


class TransformationServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class TransformationService(metaclass=TransformationServiceMeta):

    __results_location = "C:/Users/priyank/Documents/Resources/TransformationResults"

    def transform(self, transformationInput):
        print(transformationInput.get_source_github_url())
        print(transformationInput.get_targetcloudprovider())

        # Create report file which will be used to add status at each step and their result
        reporting = Reporting(transformation_input=transformationInput)

        # 1. Create a staging area
        createRepository = CreateRepository()

        try:
            _stagingArea = createRepository.get_stagingArea_Dir()
            _targetARea = createRepository.get_targetArea_Dir()
        except Exception as e:
            error = "Error occurred while creating staging area : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Staging and Target area created")

        commandLineExecutor = CommandLineExecutor()
        # 2. Fetch git URL
        try:
            commandLineExecutor.execute("FetchGitHub", transformationInput)
        except Exception as e:
            error = "Error occurred while fetching Git URL : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Git hub fetch URL Success")


        # 3. Scan : compare POM.xmls of targetArea and staging area : if answer is Yes
        # Then copy src folder to target and push changes
        # Target repo should be existing and connected to cloud build
        dependencyScanning = DependencyScanning()
        try:
            dependency_scan_results_model = dependencyScanning.scan_dependencies(_stagingArea, _targetARea)
        except Exception as e:
            error = "Error occurred while scanning dependencies : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Scanning dependencies done")

        # 4. Dependencies failed and the code cannot be transformed
        if not dependency_scan_results_model.get_dependencies_satisfied():
            return dependency_scan_results_model

        ruleEngine = RuleEngine()
        try:
            isSourceSupported = ruleEngine.check_rules_against_dependencies_google(dependency_scan_results_model)
        except Exception as e:
            error = "Error occurred while checking rules against dependencies : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Rules checked against dependencies")

        try:

            if str(isSourceSupported) != 'True':
                getProperties = GetProperties()
                can_transform_unsupported_dependency = getProperties. \
                    get_transform_unsupported_dependency(unsupported_dependency=isSourceSupported)
                if not can_transform_unsupported_dependency:
                    return "Unsupported dependency cannot be transformed!"
                else:
                    # 5. Transform unsupported dependencies
                    isTransformed = ruleEngine.transform_unsupported_dependencies(unsupported_dependency=isSourceSupported,
                                                                  staging_area=_stagingArea)
                    if not isTransformed:
                        return "Unsupported dependency transformation failed."
        except Exception as e:
            error = "Error occurred while transforming unsupported dependencies : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Unsupported dependencies checked")

        # 6. Copy functionality : transform code
        transform_code = TransformCode()
        try:
            updated_dir = transform_code.TransformCode(_stagingArea, _targetARea)
        except Exception as e:
            error = "Error occurred while transforming code by copying into template folder : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Transformation done by copying src to template folder")

        # 7. Check if the solution is Google, then copy ServletInitalizer
        try:
            if str(transformationInput.get_targetcloudprovider()).lower() == "google":
                update_google_project = UpdateGoogleProject()
                update_google_project.copy_servlet_initializer(_targetARea)
        except Exception as e:
            error = "Error occurred while copying ServletInitalizer for Google dependencies : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Google dependency checked for ServletInitalizer")

        # 8. Deploy by pushing the target to its git branch
        try:
            if transformationInput.get_is_deploy() == "true":
                commandLineExecutor.execute("gitpush", transformationInput)
        except Exception as e:
            error = "Error occurred while Git push : " + e
            return reporting.add_to_report(error=error)

        reporting.add_to_report(error="Success : Code pushed to Git, check Code Build pipeline!")

        return os.path.realpath(updated_dir)
