import configparser
import os


class GetDependencyPropertiesMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class GetDependencyProperties(metaclass=GetDependencyPropertiesMeta):
    def get_dependencies_properties_ini(self):
        config = configparser.ConfigParser()
        config_file_path = '../DependencyScanning/GenericDependencies.ini'
        config.read(config_file_path)
        dict = {}
        for key in config['dependencies']:
            dict[key] = config['dependencies'][key]
        return dict


#if __name__ == "__main__":
#    getDependencyProperties = GetDependencyProperties()
#    key = getDependencyProperties.get_dependencies_properties_ini()
#    print(key)
