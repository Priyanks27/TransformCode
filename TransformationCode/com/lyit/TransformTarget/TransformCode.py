from shutil import copytree
from shutil import rmtree
import os

class TransformCodeMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class TransformCode(metaclass=TransformCodeMeta):
    def TransformCode(self, stagingArea, targetArea):
        #stagingArea = "C:/Users/priyank/Documents/PythonWorkspace/TransformationCode/com/lyit/Resources/StagingArea/a4b44bb71df34397b17f5102389c3fe9"
        #targetArea = "C:/Users/priyank/Documents/PythonWorkspace/TransformationCode/com/lyit/Resources/TargetArea/be50acedaee64ce681b2a9fe579d5740"

        sourceSrc = stagingArea + "/src/main/java"
        targetSrc = targetArea + "/src/main/java"
        rmtree(targetSrc)
        copytree(sourceSrc, targetSrc)
        return targetArea
