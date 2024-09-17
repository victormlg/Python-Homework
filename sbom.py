
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


def get_dependency_files(path: str) -> Dict[str, Dict[str, str]] :
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirement.txt" or "packages.json"
    read() them, transform to a dict of dependencies and add it them to sbom_data -> {absolute_path : dependencies}
    """

    sbom_data = {}

    accepted_files = ['requirement.txt', 'packages.json'] #eventually, can make it so that you can choosr which files you want

    for root, _, files in os.walk(path) :

        for f in files :
            if f in accepted_files :

                absolute_path = f'{root}\{f}'

                with open(absolute_path, 'r') as fd :

                    file_extension = os.path.splitext(f)[1]
                    dependencies = to_dict(fd.read(), file_extension)

                    sbom_data[absolute_path] = dependencies

                    fd.close()
                
    return sbom_data

def create_sbom(sbom_data: Dict[str, Dict[str, str]]) -> None: #maybe input of type Hashable instead
    """
    goes through all the files in dependency_files list (from get_dependency_files),
    extract the dependencies into a dict (using to_dict) with its corresponding file extension (file_extensions)
    and create a sbom from them using create_sbom(dependencies)

    for every file in sbom_data, create 
    """
    for absolute_path, dependencies in sbom_data.items() :
        write_to_csv()
        write_to_json()

def to_dict(file : str, file_extension: str) -> Dict[str, str]:
    """
    converts requirement.txt or packages.json text into dict = {name: version}
    """

    file_dict = {}

    if file_extension == '.json' :
        json_dict = json.loads(file)
        file_dict = json_dict['dependencies']
        # maybe add json_dict['devDependencies'] in file_dict too?

    elif file_extension == '.txt' :
        lines = file.split('\n')
        for l in lines :
            l = l.split('==')
            name = l[0]
            version = l[1]

            file_dict[name] = version
    else :
        raise Exception('The file extension of this document is not supported. It should be .txt or .json.')
    
    
    return file_dict


def write_to_csv(absolute_path: str, dependencies: Dict[str, str]) -> None:
    pass 

def write_to_json(absolute_path: str, dependencies: Dict[str, str]) -> None:
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

