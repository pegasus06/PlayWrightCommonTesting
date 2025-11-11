import yaml, os


class ReadYaml(object):

    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(file=self.filename, mode="r", encoding='utf8', ) as f:
            data = f.read()
        data_yaml = yaml.load(data, Loader=yaml.FullLoader)
        return data_yaml


if __name__ == '__main__':
    pass
