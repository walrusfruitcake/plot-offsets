#!/bin/env python
from jinja2 import Template
# from jinja2 import Environment, FileSystemLoader, select_autoescape

base_svg = "./base-svg.svg"
destination_svg = "./output.svg"
destination_doc_name = "output-doc"

svg_doc_details = {
  'name': 'output-doc.svg'
}

path = {
  'id': 20,
  'points': []
}

path['points'].append({'x': 60.1, 'y': 140.2})
path['points'].append({'x': 94.1, 'y': 40.2})

# loader = FileSystemLoader(base_svg)
# # loader = PackageLoader
# autoescape=select_autoescape(
#   enabled_extensions=('xml')
# )
# jinja_env = Environment(loader=loader, autoescape=autoescape)

src = open(base_svg, 'r')

template = Template(src.read())
src.close()

# template = jinja_env.get_template(base_svg)
result = template.render(details=svg_doc_details, path=path)

print(result)

