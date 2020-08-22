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

    def __str__(self):
        return "Transformation Input   : \n" \
                + "source_github_url   : " + self.__source_github_url, "\n" \
                + "target_github_url   : " + self.__target_github_url, "\n" \
                + "targetcloudprovider : " + self.__targetcloudprovider, "\n" \
                + "isDeploy            : " + self.__isDeploy + "\n"
