# Python-Homework

Software Bill of Materials (SBOM): Command line tool for finding and documenting dependencies and
their versions

### Instructions

To run the programme, run:

```python3 sbom.py path```

Path is the path to a directory containing several repositories. The path can be absolute or relative.

The programme will iterate through all the repositories and find "package.json", "package-lock.json" or "requirements.txt". It will extract their dependencies and create a SBOM (Software bill of materials) which will be written to sbom.csv and sbom.json. 

The SBOM contains the name, version, type, absolute path and git commit hash for every dependency.

### Known Issues

- repo_count counts all the files called "package.json", "package-lock.json" or "requirements.txt", even if they're empty
- git sends a warning if get_commit() is called in a non-git directory. 
    - In this case, the git commit hash will have the value "None" in the output file.
- The code is limited by the formatting of the .json and .txt files.
    - if "requirement.txt" is not correctly formatted, or doesn't include a version, the version will have the value "None" in the output file.

### Ideas

In the future, we could add a column for the last time a dependency has been updated, with a timer that shows how long time has passed since the last update and a the date of the last update

We could then check this timer, and look for updates for the dependencies that exceed a certain threshold of time. This would ensure that all the dependencies are up to date.

We could also add some function that would preprocess the input path, to make sure that it will be written in a correct format, or transform it so that it is in the correct format. 
