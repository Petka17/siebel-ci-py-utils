import argparse
import os
import sys
import xml.etree.ElementTree as ET
import csv
import re


def __main__():
    parser = argparse.ArgumentParser(prog='inspect sif files')
    parser.add_argument('folder', help='Path to folder with sif files')
    args = parser.parse_args()

    execute(args.folder)


def execute(folder):
    projects = set()
    objects = []
    attr_digit_re = re.compile(r"\s(\d\_\w*=\".+?\")", re.MULTILINE)
    attr_col_re = re.compile(r"(\s\w*)\:(\w*=\".+?\")", re.MULTILINE)

    for file in os.listdir(folder):
        if file.endswith('.sif'):
            try:
                file_path = os.path.join(folder, file)

                with open(file_path, 'r') as f:
                    content = f.read()

                content = re.sub(attr_digit_re, r" xml__\1", content)
                content = re.sub(attr_col_re, r"\1__col__\2", content)

                repo = ET.fromstring(content)

                for project in repo:
                    if project.tag == 'PROJECT':
                        project_name = project.attrib['NAME']
                        projects.add(project_name)

                        for item in project:
                            objects.append([item.tag,
                                            item.attrib['NAME'],
                                            project_name,
                                            os.path.join(folder, file)])
            except ET.ParseError as e:
                print 'Error during parsing file %s: %s' % (file, e.message)
                print '%s' % sys.exc_info()[0]
            except AttributeError as e:
                print 'AttributeError with file %s: %s' % (file, e)
            except KeyError as e:
                print 'KeyError with file %s: %s' % (file, e.mesage)
            except:
                print 'Error with file %s: %s' % (file, sys.exc_info()[0])

    with open(os.path.join(folder, 'projects.txt'), 'w') as f:
        for project in list(projects):
            f.write('%s\n' % project)

    with open(os.path.join(folder, 'objects.csv'), 'wb') as csvfile:
        csvwriter = csv.writer(csvfile,
                               delimiter=';',
                               quotechar='\"',
                               quoting=csv.QUOTE_MINIMAL)

        csvwriter.writerow(['TYPE', 'NAME', 'PROJECT', 'FILE'])

        for row in objects:
            csvwriter.writerow(row)


if __name__ == '__main__':
    __main__()
