
from typing import Iterable, Hashable, List, Dict, Tuple
import os
import sys
import json

"""
Structure:

   dir
    | repo1
        | requirement.txt
    | repo2 
        |  packages.json

"""


def get_dependency_files(path: str, accepted_files = ['requirement.txt', 'packages.json']) -> Dict[str, Dict[str, str]] :
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirement.txt" or "packages.json"
    parse them using parse_data() into a dict sbom_data -> {name: {version, type, path}}
    """

    sbom_data = {}

    for root, _, files in os.walk(path) :

        for f in files :
            if f in accepted_files :

                path = f'{root}\{f}' # sufficient with os.path?

                with open(path, 'r') as fd :

                    file_extension = os.path.splitext(f)[1]
                    file_content = fd.read()

                    parse_data(sbom_data, file_content, file_extension, path)

                    fd.close()
                
    return sbom_data

def create_sbom(sbom_data: Dict[str, Dict[str, str]]) -> None: #maybe input of type Hashable instead
    """
    for every dependency in sbom_data, write it to a file using write_to_csv and write_to_json
    """
    for absolute_path, dependencies in sbom_data.items() :
        write_to_csv(absolute_path, dependencies)
        write_to_json(absolute_path, dependencies)

def parse_data(sbom_data: Dict[str, Dict[str, str]], file_content : str, file_extension: str, path: str):
    """
    adds data from requirement.txt / packages.json to the sbom_data -> {name: {version, type, path}}
    """
    extension_to_type = {'.json': 'npm', '.txt': 'pip'}

    if file_extension == '.json' :
        json_dict = json.loads(file_content)

        for name, version in json_dict['dependencies'].items() :
        # maybe add json_dict['devDependencies'] in file_dict too?
            sbom_data[name] = {'version': version, 'type' : extension_to_type[file_extension], 'path': path}

    elif file_extension == '.txt' :
        lines = file_content.split('\n')
        for l in lines :
            l = l.split('==') # splits the line on ==
            name = l[0]
            version = l[1]

            sbom_data[name] = {'version': version, 'type' : extension_to_type[file_extension], 'path': path}
    else :
        raise Exception('The file extension of this document is not supported. It should be .txt or .json.')
    


def write_to_csv(absolute_path: str, dependencies: Dict[str, str]) -> None:
    
    # with open('sbom.csv', 'a') as fd :
    pass


def write_to_json(absolute_path: str, dependencies: Dict[str, str]) -> None:
    
    # with open('sbom.json', 'w') as fd:
    #     json.dump(dependencies, fd)
    pass


def main() -> None :
    """
    get path from argument (sys.argv)
    and run dependency_files = get_dependency_files(path)
    then from it run read_dependencies(dependency_files)
    """
    pass


if __name__ == "__main__" :
    main()

