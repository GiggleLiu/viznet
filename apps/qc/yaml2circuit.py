import yaml, os
from viznet import DynamicShow, dict2circuit

def parseyaml():
    with open(os.path.dirname(__file__)+'/circuit.yaml') as f:
        datamap = yaml.safe_load(f)
    print(datamap)
    with DynamicShow(figsize=(6, 6)) as ds:
        dict2circuit(datamap)

if __name__ == '__main__':
    parseyaml()
