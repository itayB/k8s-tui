import os

import yaml


def load_versions():
    # file = '/Users/itaybittan/workspace/dy-helm/releases/recs/rcom-server/values/values_dyaws_us-east-1_prod.yaml'
    # load_versions_from_file(file)
    path = '/Users/itaybittan/workspace/dy-helm/releases'
    res = scan_tree(path)
    pass


def scan_tree(path):
    namespaces = dict()
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_dir():
                other_namespaces = scan_tree(entry.path)
                if other_namespaces:
                    namespaces.update(other_namespaces)
            if entry.name.endswith(".yaml") and entry.is_file():
                # logger.info(entry.name)
                versions = load_versions_from_file(entry.path)
                if versions is not None:
                    namespace = path.split('/')[-3]
                    filename = entry.name.split('.')[0]
                    region = filename.split('_')[2]
                    env = filename.split('_')[3]
                    for name, value in versions.items():
                        namespaces[entry.name] = versions
    return namespaces


def load_versions_from_file(file):
    res = dict()
    with open(file, 'r') as stream:
        try:
            values = yaml.safe_load(stream)
            for service in values.keys():
                res[service] = dict()
                for name, container in values[service]['podTemplate']['containers'].items():
                    tag = container['image']['tag']
                    res[service][name] = tag

        except (yaml.YAMLError, Exception) as exc:
            # print(exc)
            return None
    return res
