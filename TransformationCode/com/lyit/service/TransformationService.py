from com.lyit.DependencyScanning.DependencyScanning import DependencyScanning
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
    def transform(self, transformationInput):
        print(transformationInput.get_source_github_url())
        print(transformationInput.get_targetcloudprovider())

        # 1. Create a staging area
        createRepository = CreateRepository()
        _stagingArea = createRepository.get_stagingArea_Dir()
        _targetARea = createRepository.get_targetArea_Dir()

        commandLineExecutor = CommandLineExecutor()
        # 2. Fetch git URL
        commandLineExecutor.execute("FetchGitHub", transformationInput)

        # 3. Scan : compare POM.xmls of targetArea and staging area : if answer is Yes
        # Then copy src folder to target and push changes
        # Target repo should be existing and connected to cloud build
        dependencyScanning = DependencyScanning()
        dependency_scan_results_model = dependencyScanning.scan_dependencies(_stagingArea, _targetARea)

        # 4. Dependencies failed and the code cannot be transformed
        if not dependency_scan_results_model.get_dependencies_satisfied():
            return dependency_scan_results_model

        ruleEngine = RuleEngine()
        isSourceSupported = ruleEngine.check_rules_against_dependencies_google(dependency_scan_results_model)

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


        # 6. Copy functionality : transform code
        transform_code = TransformCode()
        updated_dir = transform_code.TransformCode(_stagingArea, _targetARea)

        # 7. Check if the solution is Google, then copy ServletInitalizer
        if str(transformationInput.get_targetcloudprovider()).lower() == "google":
            update_google_project = UpdateGoogleProject()
            update_google_project.copy_servlet_initializer(_targetARea)

        # 7. Deploy by pushing the target to its git branch
        if transformationInput.get_is_deploy() == "true":
            commandLineExecutor.execute("gitpush", transformationInput)

        import os
        print(os.path.realpath(updated_dir))
        return updated_dir
