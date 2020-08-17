import uuid
import os

class CreateRepositoryMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CreateRepository(metaclass=CreateRepositoryMeta):

    __stagingAreaDir = None
    __targetAreaDir = None
    __basePathStaging = '../Resources/StagingArea/'
    __basePathTarget = '../Resources/TargetArea/'

    def get_stagingArea_Dir(self):
        return self.__stagingAreaDir

    def get_targetArea_Dir(self):
        return self.__targetAreaDir

    def createstagigArea(self):
        stagingAreaDir = os.path.join(self.__basePathStaging, uuid.uuid4().hex)
        if not os.path.isdir(stagingAreaDir):
            os.mkdir(stagingAreaDir)
        self.__stagingAreaDir = stagingAreaDir
        return stagingAreaDir

    def createTargetArea(self):
        targetAreaDir = os.path.join(self.__basePathTarget, uuid.uuid4().hex)
        if not os.path.isdir(targetAreaDir):
            os.mkdir(targetAreaDir)
        self.__targetAreaDir = targetAreaDir
        return targetAreaDir


#if __name__ == "__main__":
#    createRepository = CreateRepository()
#    for i in range(10):
#        print(createRepository.createstagigArea())
#        print(createRepository.createTargetArea())
