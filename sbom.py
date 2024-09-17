
from typing import Iterable, Hashable, List, Dict, Tuple
import os
import sys
import json
import csv

"""
Structure:

   dir
    | repo1
        | requirement.txt
    | repo2 
        |  packages.json

"""


def get_dependency_files(path: str, accepted_files = ['requirement.txt', 'packages.json']) -> List[Dict[str, str]] :
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirement.txt" or "packages.json"
    parse them using parse_data() into a dict sbom_data -> {name: {version, type, path}}
    """

    sbom_data = []

    for root, _, files in os.walk(path) :

        for f in files :
            if f in accepted_files :

                path = f'{root}\{f}' 

                try :
                    with open(path, 'r') as fd :

                        file_content = fd.read()
                        file_extension = os.path.splitext(f)[1]

                        parse_data(sbom_data, file_content, file_extension, path)

                        fd.close()
                except : 
                    print("error: Coundn't parse the file at {path}")

    return sbom_data

def create_sbom(sbom_data: Dict[str, Dict[str, str]]) -> None: #maybe input of type Hashable instead
    """
    for every dependency in sbom_data, write it to a file using write_to_csv and write_to_json
    """
    try :
        path = write_to_csv(sbom_data)
        print(f'Saved SBOM in CSV format to {path}')
    except :
        print("error: Couldn't save SBOM in CSV format")

    try :
        path = write_to_json(sbom_data)
        print(f'Saved SBOM in JSON format to {path}')
    except:
        print(f"error: Couldn't save SBOM in JSON format")

def parse_data(sbom_data: List[Dict[str, str]], file_content : str, file_extension: str, path: str) -> None:
    """
    adds data from requirement.txt / packages.json to the sbom_data -> {name: {version, type, path}}
    """
    extension_to_type = {'.json': 'npm', '.txt': 'pip'}

    if file_extension == '.json' :
        json_dict = json.loads(file_content)

        for name, version in json_dict['dependencies'].items() :
        # maybe add json_dict['devDependencies'] in file_dict too?
            dependency = {'name': name, 'version': version, 'type' : extension_to_type[file_extension], 'path': path}
            sbom_data.append(dependency)

    elif file_extension == '.txt' :
        lines = file_content.split('\n')
        for l in lines :
            l = l.split('==') # splits the line on ==
            name = l[0]
            version = l[1]

            dependency = {'name': name, 'version': version, 'type' : extension_to_type[file_extension], 'path': path}
            sbom_data.append(dependency)
    else :
        raise Exception('error: The file extension of this document is not supported. It should be .txt or .json.')
    


def write_to_csv(sbom_data: List[Dict[str, str]]) -> str:
    
    with open('sbom.csv', 'w', newline= '') as fd :
        fieldnames = ['name', 'version', 'type', 'path']
        writer = csv.DictWriter(fd, fieldnames)
        writer.writeheader()
        writer.writerows(sbom_data)
        
        file_name = fd.name

        fd.close()

    return os.path.abspath(file_name)


def write_to_json(sbom_data: List[Dict[str, str]]) -> str:
    
    with open('sbom.json', 'w') as fd:
        json.dump(sbom_data, fd, indent='\t')

        file_name = fd.name

        fd.close()
    
    return os.path.abspath(file_name)


def main() -> None :
    """
    get path from argument (sys.argv)
    and run dependency_files = get_dependency_files(path)
    then from it run read_dependencies(dependency_files)
    """
    # could use regex to check if input is on the right format

    pass


if __name__ == "__main__" :
    main()

