
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


def get_dependency_files(path: str) -> List[Dict[str, Dict[str, str]]] :
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirement.txt" or "packages.json"
    read() them, transform to a dict of dependencies and add it them to sbom_data -> {absolute_path : dependencies}
    """

    sbom_data_list = []

    accepted_files = ['requirement.txt', 'packages.json'] #eventually, can make it so that you can choosr which files you want

    for root, _, files in os.walk(path) :

        for f in files :
            if f in accepted_files :

                path = f'{root}\{f}' # sufficient with os.path?

                with open(path, 'r') as fd :

                    file_extension = os.path.splitext(f)[1]
                    dependencies = to_dict(fd.read(), file_extension, path)

                    sbom_data_list.append(dependencies)

                    fd.close()
                
    return sbom_data_list

def create_sbom(sbom_data: Dict[str, Dict[str, str]]) -> None: #maybe input of type Hashable instead
    """
    goes through all the files in dependency_files list (from get_dependency_files),
    extract the dependencies into a dict (using to_dict) with its corresponding file extension (file_extensions)
    and create a sbom from them using create_sbom(dependencies)

    for every file in sbom_data, create 
    """
    for absolute_path, dependencies in sbom_data.items() :
        write_to_csv(absolute_path, dependencies)
        write_to_json(absolute_path, dependencies)

def to_dict(file : str, file_extension: str, path: str) -> Dict[str, str]:
    """
    converts requirement.txt or packages.json text into dict = {name: {version, type, path}}
    """

    file_dict = {}

    extension_to_type = {'.json': 'npm', '.txt': 'pip'}

    if file_extension == '.json' :
        json_dict = json.loads(file)

        for name, version in json_dict['dependencies'].items() :
        # maybe add json_dict['devDependencies'] in file_dict too?
            file_dict[name] = {'version': version, 'type' : extension_to_type[file_extension], 'path': path}

    elif file_extension == '.txt' :
        lines = file.split('\n')
        for l in lines :
            l = l.split('==') # splits the line on ==
            name = l[0]
            version = l[1]

            file_dict[name] = {'version': version, 'type' : extension_to_type[file_extension], 'path': path}
    else :
        raise Exception('The file extension of this document is not supported. It should be .txt or .json.')
    
    
    return file_dict


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

