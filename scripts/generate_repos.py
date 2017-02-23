"""Generate terraform dsl for creating docker repos from json."""
import json
import os


def tfecr(name):
    """Create tf block for creating repo."""
    block = 'resource "aws_ecr_repository" "{0}" {{\n'.format(name)
    block += '    name = "{0}"\n'.format(name)
    block += '}\n\n'
    return block


def gentf(data):
    """Generate the tf file."""
    output = ""
    for repo in data['repos']:
        output += tfecr(repo['name'])
    return output


basepath = os.path.dirname(os.path.abspath(__file__))

jsonfile = open(basepath + '/../configs/' + 'dtr_repo_list.json', 'r')

data = json.load(jsonfile)

f = open(basepath + '/../terraform/dtr/' + 'ecr.tf', 'w')

f.write(gentf(data))


