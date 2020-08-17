class TransformationInput:

    def __init__(self, source_github_url, target_github_url, targetcloudprovider, isDeploy):
        self.__source_github_url = source_github_url
        self.__target_github_url = target_github_url
        self.__targetcloudprovider = targetcloudprovider
        self.__isDeploy = isDeploy

    def get_target_github_url(self):
        return self.__target_github_url

    def get_source_github_url(self):
        return self.__source_github_url

    def get_targetcloudprovider(self):
        return self.__targetcloudprovider

    def get_is_deploy(self):
        return self.__isDeploy