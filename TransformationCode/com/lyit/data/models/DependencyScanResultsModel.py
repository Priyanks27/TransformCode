class DependencyScanResultsModel:

    def __init__(self):
        pass

    def get_extra_dependencies_in_source_dict(self):
        return self.__extra_dependencies_in_source_dict

    def get_extra_dependencies_in_source_report(self):
        return self.__extra_dependencies_in_source_report

    def get_extra_dependencies_in_target_dict(self):
        return self.__extra_dependencies_in_target_dict

    def get_extra_dependencies_in_target_report(self):
        return self.__extra_dependencies_in_target_report

    def get_missing_required_dependencies_in_source(self):
        return self.__missing_required_dependencies_in_source

    def get_dependencies_satisfied(self):
        return self.__can_transform

    def set_extra_dependencies_in_source_dict(self, _extra_dependencies_in_source_dict):
        self.__extra_dependencies_in_source_dict = _extra_dependencies_in_source_dict

    def set_extra_dependencies_in_source_report(self, _extra_dependencies_in_source_report):
        self.__extra_dependencies_in_source_report = _extra_dependencies_in_source_report

    def set_extra_dependencies_in_target_dict(self, _extra_dependencies_in_target_dict):
        self.__extra_dependencies_in_target_dict = _extra_dependencies_in_target_dict

    def set_extra_dependencies_in_target_report(self, _extra_dependencies_in_target_report):
        self.__extra_dependencies_in_target_report = _extra_dependencies_in_target_report

    def set_missing_required_dependencies_in_source(self, _missing_required_dependencies_in_source):
        self.__missing_required_dependencies_in_source = _missing_required_dependencies_in_source

    def set_dependencies_satisfied(self, _can_transform):
        self.__can_transform = _can_transform
