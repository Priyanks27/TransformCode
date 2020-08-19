import uuid
import os

import uuid as uuid


class CreateRepositoryMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class CreateRepository(metaclass=CreateRepositoryMeta):

    def __init__(self):
        uniqueId = uuid.uuid4().hex
        self.__stagingAreaDir = self.__createstagingArea(uniqueId)
        self.__targetAreaDir = self.__createTargetArea(uniqueId)

    __stagingAreaDir = None
    __targetAreaDir = None
    __basePathStaging = 'C:/Users/priyank/Documents/Resources/StagingArea/'
    __basePathTarget = 'C:/Users/priyank/Documents/Resources/TargetArea/'

    def get_stagingArea_Dir(self):
        return self.__stagingAreaDir

    def get_targetArea_Dir(self):
        return self.__targetAreaDir


    def __createstagingArea(self, uniqueId):
        stagingAreaDir = os.path.join(self.__basePathStaging, uniqueId)
        if not os.path.isdir(stagingAreaDir):
            os.mkdir(stagingAreaDir)
        self.__stagingAreaDir = stagingAreaDir
        return stagingAreaDir

    def __createTargetArea(self, uniqueId):
        targetAreaDir = os.path.join(self.__basePathTarget, uniqueId)
        if not os.path.isdir(targetAreaDir):
            os.mkdir(targetAreaDir)
        self.__targetAreaDir = targetAreaDir
        return targetAreaDir


#if __name__ == "__main__":
#    createRepository = CreateRepository()
#    for i in range(10):
#        print(createRepository.createstagigArea())
#        print(createRepository.createTargetArea())
