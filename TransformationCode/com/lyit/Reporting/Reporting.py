import time


class ReportingMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Reporting(metaclass=ReportingMeta):
    __report_location = None
    __report_full_path = None

    def __init__(self, transformation_input):
        self.__report_location = "C:/Users/priyank/Documents/Resources/TransformationResults/"
        self.__report_full_path = self.__report_location + "report_" + str(int(time.time())) + ".txt"
        with open(self.__report_full_path, "w") as file:
            transformation_input
            file.write("get_source_github_url : " + transformation_input.get_source_github_url() + "\n"
                       + "get_target_github_url : " + transformation_input.get_target_github_url() + "\n"
                       + "get_targetcloudprovider :  " + transformation_input.get_targetcloudprovider() + "\n"
                       + " is_deploy :  " + transformation_input.get_is_deploy()) + "\n"
            file.close()

    def add_to_report(self, error):
        print(error)
        with open(self.__report_full_path, "a") as file:
            file.write(error + "\n")
            file.close()
        return error
