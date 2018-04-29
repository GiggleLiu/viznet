import yaml, pdb

with open('test.yaml') as f:
    datamap = yaml.safe_load(f)
print(datamap)
pdb.set_trace()
