
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


def get_dependency_files(path: str) -> Tuple[List[str], List[str], List[str]] :
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirement.txt" or "packages.json"
    read() them and append them to dependency_files
    Appends their file exttension to file_extensions

    len(dependency_files) == len(file_extensions). Each index corresponds to a file and its extension
    """
    dependency_files = []
    file_extensions = []
    file_paths = []

    accepted_files = ['requirement.txt', 'packages.json']

    for root, _, files in os.walk(path) :

        for f in files :
            if f in accepted_files :

                absolute_path = f'{root}\{f}'
                with open(absolute_path, 'r') as fd :
                    dependency_files.append(fd.read())

                    extension = os.path.splitext(f)[1]
                    file_extensions.append(extension)

                    file_paths.append(absolute_path)

                    fd.close()
                
    return dependency_files, file_extensions, file_paths

def read_dependencies(dependecy_files: Iterable[str], file_extensions: Iterable[str]) -> None:
    """
    goes through all the files in dependency_files list (from get_dependency_files),
    extract the dependencies into a dict (using to_dict) with its corresponding file extension (file_extensions)
    and create a sbom from them using create_sbom(dependencies)
    """
    pass 

def to_dict(file : str, file_type: str) -> Dict[str, str]:
    """
    converts requirement.txt or packages.json text into dict = {name: version}
    """

    file_dict = {}

    if file_type == '.json' :
        json_dict = json.loads(file)
        file_dict = json_dict['dependencies']
        # maybe add json_dict['devDependencies'] in file_dict too?

    elif file_type == '.txt' :
        lines = file.split('\n')
        for l in lines :
            l = l.split('==')
            name = l[0]
            version = l[1]

            file_dict[name] = version
    
    
    return file_dict


def create_sbom(dependencies: Dict[str,str]) -> None: #maybe Hashable type
    """
    dependencies is {name: version}

    Creates sbom.csv/json and writes to it
    """
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

