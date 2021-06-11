#!/bin/env python
import sys, getopt
import csv
from jinja2 import Template
# from jinja2 import Environment, FileSystemLoader, select_autoescape

base_svg = "./base-svg.svg"
destination_doc_name = "output-doc"
destination_svg = f'./{destination_doc_name}.svg'
source_csv = "./test.csv"

x_label = "Scaled X [mm]"
y_label = "Scaled Y [mm]" 

svg_doc_details = {
  'name': destination_doc_name,
  'width': '558.8',
  'height': '215.9',
  'units': 'mm'
}

path = {
  'id': 20,
  'points': []
}

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

def read_points_from_csv(csv_filename):
  points = []
  with open(csv_filename, 'r', newline='') as f:
    r = csv.reader(f, delimiter=',')
    header = r.__next__()
    x_index = header.index(x_label)
    y_index = header.index(y_label)
    for row in r:
      points.append(Point(row[x_index], row[y_index]))
      # print(f'point: {row[x_index]}, {row[y_index]}')
  return points

def get_args():
  argv = sys.argv[1:]
  help_string = 'make_an_svg.py [-h]  -i <input csv>  [-o <output svg>]'
  detail_help_string = 'make_an_svg.py  [-h|--help]  -i|--input-csv <path>  [-o|--output-svg <path>]'
  try:
    opts, args = getopt.getopt(argv,"hi:o:",["help","input-csv=","output-svg="])
  except getopt.GetoptError:
    print(help_string)
    sys.exit(2)
  if '-h' in opts:
    print('help reqd')
  for opt, arg in opts:
    if opt in ('-h', '--help'):
      print(detail_help_string)
      sys.exit()
    elif opt in ("-i", "--input-csv"):
      source_csv = arg
    elif opt in ("-o", "--output-svg"):
      destination_svg = arg
  print('Input file is: ', source_csv)
  print('Output file is: ', destination_svg)
  return source_csv, destination_svg

source_csv, destination_svg = get_args()

points = read_points_from_csv(source_csv)
path['points'].extend(points)

# loader = FileSystemLoader(base_svg)
# # loader = PackageLoader
# autoescape=select_autoescape(
#   enabled_extensions=('xml')
# )
# jinja_env = Environment(loader=loader, autoescape=autoescape)

print('done reading points')
result = ''
with open(base_svg, 'r') as src:
  template = Template(src.read())
  result = template.render(details=svg_doc_details, path=path)

# template = jinja_env.get_template(base_svg)
print(result)
with open(destination_svg, 'w') as f:
  f.write(result)

