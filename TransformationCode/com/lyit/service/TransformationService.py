from com.lyit.TransformTarget.TransformCode import TransformCode
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

        #Create a staging area
        createRepository = CreateRepository()
        _stagingArea = createRepository.createstagigArea()
        _targetARea = createRepository.createTargetArea()

        commandLineExecutor = CommandLineExecutor()
        #Fetch git URL
        commandLineExecutor.execute("FetchGitHub", transformationInput)

        #Scan : compare POM.xmls of targetArea and staging area : if answer is Yes
        # Then copy src folder to target and push changes
        #target repo should be existing and cpnnected to cloud build

        #Copy functionality
        transformCode = TransformCode()
        updated_dir = transformCode.TransformCode(_stagingArea, _targetARea)

        # Deploy by pushing the target to its git branch
        if transformationInput.get_is_deploy() == "true":
            commandLineExecutor.execute("gitpush", transformationInput)

        import os
        print(os.path.realpath(updated_dir))
        return updated_dir