import subprocess
from typing import Dict
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


def get_dependency_files(
    root_path: str, accepted_files=["requirements.txt", "package.json", "package-lock.json"]
) -> Dict[str, Dict[str, str]]:
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirements.txt" or "package.json"
    parse them using parse_data() into a list sbom_data -> [{'name':name, 'version':version, 'type':type, 'path':path}]
    """

    if not os.path.isdir(root_path):
        raise NotADirectoryError("directory path not valid")

    sbom_data = {}

    repo_number = 0
    for root, _, files in os.walk(root_path):

        for f in files:
            if f in accepted_files:

                path = os.path.join(root, f)
                commit_hash = get_commit(root)

                with open(path, "r") as fd:

                    file_content = fd.read()
                    file_extension = os.path.splitext(f)[1]

                    parse_data(
                        sbom_data, file_content, file_extension, path, commit_hash
                    )
                    repo_number += 1

    if not sbom_data:
        raise FileNotFoundError("no dependency found ")

    print(
        f"Found {repo_number} repositories in '{root_path}'"
    ) 
    print(len(sbom_data))
    return sbom_data


def get_commit(path: str) -> str:

    if not os.path.isdir(path):
        raise NotADirectoryError("directory path not valid")

    try:
        return (
            subprocess.check_output(["git", "log", "--format=%H", "-n", "1"], cwd=path)
            .decode("utf-8")
            .strip()
        )
    except:
        return "None"


def create_sbom(
    sbom_data: Dict[str, Dict[str, str]]
) -> None:  # maybe input of type Hashable instead
    """
    converts sbom_data into sbom.csv and sbom.json
    """

    csv_path = write_to_csv(sbom_data)
    if csv_path:
        print(f"Saved SBOM in CSV format to '{csv_path}'")

    json_path = write_to_json(sbom_data)
    if json_path:
        print(f"Saved SBOM in JSON format to '{json_path}'")


def parse_data(
    sbom_data: Dict[str, Dict[str, str]],
    file_content: str,
    file_extension: str,
    path: str,
    commit_hash: str,
) -> None:
    """
    adds data from requirements.txt / package.json to the sbom_data -> [{'name':name, 'version':version, 'type':type, 'path':path}]
    """
    extension_to_type = {".json": "npm", ".txt": "pip"}

    if not file_content:  # checks if the file is empty
        print(f"File at '{path}' is empty")
        return

    if file_extension == ".json":
        
        depencencies = unpack_json(file_content)    

        if not depencencies:
            print(f"No dependencies in {path}")
            return

        for name, version in depencencies.items():
            dependency = {
                "name": name,
                "version": version,
                "type": extension_to_type[file_extension],
                "path": path,
                "commit": commit_hash,
            }
            sbom_data[name] = dependency

    elif file_extension == ".txt":
        lines = file_content.split()
        for l in lines:

            l = l.split("==")  # splits the line on ==

            if len(l) == 2:
                version = l[1]
            else:
                version = "None"  # None if doesn't exist OR not correct format
            name = l[0]

            dependency = {
                "name": name,
                "version": version,
                "type": extension_to_type[file_extension],
                "path": path,
                "commit": commit_hash,
            }
            sbom_data[name] = dependency

    else:
        raise Exception(
            "the file extension of this document is not supported. It should be .txt or .json."
        )
    
def unpack_json(file_content: str) -> Dict[str, str]:
    json_dict = json.loads(file_content)

    # if the file is package.json
    package_dependencies = json_dict.get("dependencies")
    if package_dependencies: 
        return package_dependencies

    # if the file is package-lock.json
    packages = json_dict.get('packages')
    if not packages :
        return 
    
    package_lock_dependencies = {}
    
    for package in packages.values() :
        dependencies = package.get('dependencies')
        if dependencies :
            package_lock_dependencies |= dependencies #merges the dependency dicts from all the different packages
    
    return package_lock_dependencies

    


def write_to_csv(sbom_data: Dict[str, Dict[str, str]]) -> str:

    with open("sbom.csv", "w", newline="") as fd:
        data_list = [dependency for dependency in sbom_data.values()] #unpacks dicts of the sbom_data into a list, so that it can be used by the csv writer
        fieldnames = ["name", "version", "type", "path", "commit"]
        writer = csv.DictWriter(fd, fieldnames)
        writer.writeheader()
        writer.writerows(data_list)

        file_name = fd.name

    return os.path.abspath(file_name)


def write_to_json(sbom_data: Dict[str, Dict[str, str]]) -> str:

    with open("sbom.json", "w") as fd:
        json.dump(sbom_data, fd, indent="\t")

        file_name = fd.name

    return os.path.abspath(file_name)


def main() -> None:

    try:
        if len(sys.argv) != 2:
            raise Exception("one argument should be given")

        path = sys.argv[1]
        sbom_data = get_dependency_files(path)
        create_sbom(sbom_data)

    except Exception as e:
        print(f"Error : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
