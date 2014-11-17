from __future__ import print_function

import yaml

def save_yaml(filename, yamlnode):
  yaml_str = yaml.dump(yamlnode, default_flow_style = False)
  #print(yaml_str)
  yaml_file = open(filename, 'w')
  yaml_file.write(yaml_str)
  yaml_file.close()


def string2int_list(s, sep = None):
  return [int(i) for i in s.split(sep)]


