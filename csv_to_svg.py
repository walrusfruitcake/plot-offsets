#!/bin/env python
import argparse
import csv
from jinja2 import Template
# from jinja2 import Environment, FileSystemLoader, select_autoescape

base_svg = "./base-svg.svg"
destination_doc_name = "output-doc"
destination_svg = f'./{destination_doc_name}.svg'
source_csv = "./test.csv"

x_label_default = "Scaled X [mm]"
y_label_default = "Scaled Y [mm]"

svg_doc_details = {
  'name': destination_doc_name,
  'width': '558.8',
  'height': '215.9',
  'units': 'mm'
}

paths = []

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Path:
  def __init__(self, path_id, points):
    self.id = path_id
    self.points = points

class CsvDeets:
  def __init__(self, csv_files, x_label, y_label):
    self.csv_files = csv_files
    self.x_label = x_label
    self.y_label = y_label

def read_points_from_csv(csv_filename, x_label, y_label):
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
  parser = argparse.ArgumentParser(description='Build an svg of points from a csv of offsets')
  parser.add_argument('input_csv', metavar='CSV', type=str, nargs='+',
          help='the input csv(s) containing offset positions, one path per csv file')
  parser.add_argument('-x', '--x-label', metavar='label', type=str,
          help='the column label for the x values (default \'x\')', default=x_label_default)
  parser.add_argument('-y', '--y-label', metavar='label', type=str,
          help='the column label for the y values (default \'y\')', default=y_label_default)
  parser.add_argument('-o', '--output-svg', metavar='file', type=str,
          help='the output svg filepath (default stdout)', default='-')
  args = parser.parse_args()
  csv_details = CsvDeets(args.input_csv, args.x_label, args.y_label)
  return csv_details, args.output_svg

# print(get_args())

if __name__=='__main__':
  csv_details, destination_svg = get_args()
  # print(csv_details.csv_files, csv_details.x_label)

  id_start=28
  print(csv_details.csv_files)
  for i, csv_file in enumerate(csv_details.csv_files):
    points = read_points_from_csv(csv_file, csv_details.x_label, csv_details.y_label)
    # print(points)
    path_id = i + id_start
    path_to_add = Path(path_id, points)
    # path['points'].extend(points)
    paths.append(path_to_add)

  # print('done reading points')
  result = ''
  with open(base_svg, 'r') as src:
    template = Template(src.read())
    result = template.render(details=svg_doc_details, paths=paths)

  if (destination_svg == '-'):
    print(result)
  else:
    with open(destination_svg, 'w') as f:
      f.write(result)

