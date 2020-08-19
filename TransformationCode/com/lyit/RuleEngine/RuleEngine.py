from com.lyit.RuleEngine.RuleCassandraTransformToH2 import RuleCassandraTransformToH2
from com.lyit.configuration.GetProperties import GetProperties


class RuleEngineMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RuleEngine(metaclass=RuleEngineMeta):

    def check_rules_against_dependencies_google(self, dependency_scan_results_model):
        getProperties = GetProperties()
        source_dict = dependency_scan_results_model.get_extra_dependencies_in_source_dict()
        target_dict = dependency_scan_results_model.get_extra_dependencies_in_target_dict()
        supported_source_list = getProperties.get_supported_environment_source_dependencies()
        for key in source_dict:
            if key == 'NO extra dependencies in source':
                return True
            if key not in supported_source_list:
                return source_dict[key]
        for key in target_dict:
            if key not in supported_source_list:
                return source_dict[key]
        return 'True'

    def check_rules_against_dependencies_aws(self, dependency_scan_results_model):
        getProperties = GetProperties()
        source_dict = dependency_scan_results_model.get_extra_dependencies_in_source_dict()
        target_dict = dependency_scan_results_model.get_extra_dependencies_in_target_dict()
        supported_source_list = getProperties.get_supported_environment_source_dependencies()
        for key in source_dict:
            if key not in supported_source_list:
                return False
        for key in target_dict:
            if key not in supported_source_list:
                return False
        return True

        return True

    def transform_unsupported_dependencies(self, unsupported_dependency, staging_area):
        if unsupported_dependency.find('cassandra') != -1:
            rule_cassandra_transform_to_h2 = RuleCassandraTransformToH2()
            return rule_cassandra_transform_to_h2.load_rule_lib_cassandra_to_h2(staging_area=staging_area)
        return False
