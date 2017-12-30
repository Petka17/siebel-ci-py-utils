import argparse
import os
import sys
import xml.etree.ElementTree as ET
import csv


def __main__():
    parser = argparse.ArgumentParser(prog='inspect sif files')
    parser.add_argument('folder', help='Path to folder with sif files')
    args = parser.parse_args()

    folder = args.folder

    projects = set()
    objects = []

    try:
        for file in os.listdir(folder):
            if file.endswith('.sif'):
                sif = ET.parse(os.path.join(folder, file))
                repo = sif.getroot()

                try:
                    for project in repo:
                        if project.tag == 'PROJECT':
                            project_name = project.attrib['NAME']
                            projects.add(project_name)

                            for item in project:
                                objects.append([item.tag,
                                                item.attrib['NAME'],
                                                project_name,
                                                file])
                except KeyError as e:
                    print 'KeyError with file %s: %s' % (file, e.mesage)
                except:
                    print 'Error with file %s: %s' % (file, sys.exc_info()[0])
    except ET.ParseError as e:
        print 'Error during parsing %s' % e.message
        exit(1)

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
