
class ResultStages:

    __instance = None

    results_stages = [
        "FetchGit",
        "ScanningPom",
        "RuleMatching",
        "TransformUnsupportedDependencies"
        "CopyFiles"
        "CheckCloudProvider"
        "GitPush"
    ]

    @staticmethod
    def getInstance():
        if ResultStages.__instance is None:
            ResultStages()
        return ResultStages.__instance

    def __init__(self):
        if ResultStages.__instance is not None:
            raise Exception("Cannot be instantiated twice, singleton class")
        else:
            ResultStages.__instance = self

    def get_result_stages(self):
        return self.__result_stages

    def set_result_stages(self, result_stages):
        self.__result_stages = result_stages


if __name__ == "__main__":
    r = ResultStages()
    print(r)

    r = ResultStages.getInstance()
    print(r)

    r = ResultStages.getInstance()
    print(r)