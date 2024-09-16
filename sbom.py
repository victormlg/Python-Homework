
from typing import Iterable, Hashable, List, Dict, Tuple


"""
Structure:

   dir
    | repo1
        | requirement.txt
    | repo2 
        |  packages.json

"""


def get_dependency_files(path: str) -> Tuple[List[str], List[str]] :
    """
    from the dir that the path links to, iterate through all its subdirs and files
    find all the files called "requirement.txt" or "packages.json"
    read() them and append them to dependency_files
    Appends their file exttension to file_extensions

    len(dependency_files) == len(file_extensions). Each index corresponds to a file and its extension
    """
    dependency_files = []
    file_extensions = []

    return dependency_files, file_extensions

def read_dependencies(dependecy_files: Iterable[str], file_extensions: Iterable[str]) -> None:
    """
    goes through all the files in dependency_files list (from get_dependency_files),
    extract the dependencies into a dict (using to_dict) with its corresponding file extension (file_extensions)
    and create a sbom from them using create_sbom(dependencies)
    """
    pass 

def to_dict(file : str, file_type: str) -> Dict[str, str]:
    """
    converts requirement.txt or packages.json to dict = {name: version}
    """
    
    file_dict = {}
    
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

