
from typing import List, Dict
import os
import sys
import json
import csv

"""
Structure:

   dir
    | repo1
        | requirements.txt
    | repo2 
        |  package.json

"""


def get_dependency_files(root_path: str, accepted_files = ['requirements.txt', 'package.json']) -> List[Dict[str, str]] :
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirements.txt" or "package.json"
    parse them using parse_data() into a list sbom_data -> [{'name':name, 'version':version, 'type':type, 'path':path}]
    """

    if not os.path.isdir(root_path) :
        raise NotADirectoryError('directory path not valid')

    sbom_data = []

    i =0
    for root, dirs, files in os.walk(root_path) :

        if i==0 :
            repo_number = len(dirs)

        i+=1

        for f in files :
            if f in accepted_files :

                path = os.path.join(root, f)
            
                with open(path, 'r') as fd :

                    file_content = fd.read()
                    file_extension = os.path.splitext(f)[1]

                    parse_data(sbom_data, file_content, file_extension, path)

                    fd.close()

    if not sbom_data :
        raise FileNotFoundError('no dependency file found ')
    
    print(f"Found {repo_number} repositories in '{root_path}'")

    return sbom_data

def create_sbom(sbom_data: Dict[str, Dict[str, str]]) -> None: #maybe input of type Hashable instead
    """
    converts sbom_data into sbom.csv and sbom.json
    """

    csv_path = write_to_csv(sbom_data)
    if csv_path :
        print(f"Saved SBOM in CSV format to '{csv_path}'")

    
    json_path = write_to_json(sbom_data)
    if json_path :
        print(f"Saved SBOM in JSON format to '{json_path}'")

def parse_data(sbom_data: List[Dict[str, str]], file_content : str, file_extension: str, path: str) -> None:
    """
    adds data from requirements.txt / package.json to the sbom_data -> [{'name':name, 'version':version, 'type':type, 'path':path}]
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
        raise Exception('the file extension of this document is not supported. It should be .txt or .json.')
    


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
    # could use regex to check if input is on the right format

    try :
        path = sys.argv[1]
        sbom_data = get_dependency_files(path)
        create_sbom(sbom_data)

    except IndexError as e: # sys.argv
        print(f'Error 1: {e}')
        sys.exit(1)

    except FileNotFoundError as e: # sbom_data = [] or file doesn't exist
        print(f'Error 2: {e}')
        sys.exit(1)

    except NotADirectoryError as e: # wrong path to dir
        print(f'Error 3: {e}')
        sys.exit(1)

if __name__ == "__main__" :
    main()

