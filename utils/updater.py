"""Fetch newer files from a git repo, ignore unchanged files. Originally from racing ball, adapted to use here"""

import urllib.request, json, base64, os, time

def get(URL: str):
    # Returns content of the response to a GET request
    with urllib.request.urlopen(URL) as response:
        return response.read()

def update():
    if_run: str = ""
    if_depends: str = ""
    while if_depends.lower() not in ["y", "n"]:
        if_depends = input("Fetch dependencies after updating? (y/n): ")
    while if_run.lower() not in ["y", "n"]:
        if_run = input("Run the game after updating? (y/n): ")

    REPO_TREE: str = "https://api.github.com/repos/HyperSourceGithub/hyperair/git/trees/main?recursive=1"
    COOLDOWN: float= 0.5                                    # Delay between HTTP requests to prevent rate limiting

    print (f"Getting repository tree: {REPO_TREE}")
    files = json.loads(get(REPO_TREE))['tree']

    trees: list = []
    blobs: list = []

    try:
        with open("utils/local_checksums.json", "+r") as checksum_file:
            checksums :dict= json.load(checksum_file)
    except FileNotFoundError:
        with open("utils/local_checksums.json","+w") as checksum_file:
            checksum_file.write("[]")
            checksums :dict= {}

    for file in files:
        if file["type"] == "blob":
            try:                                            # Only update files which have changed
                if file["sha"] != checksums[file["path"]]:
                    print(f"New / Updated file: {file['path']}...")
                    blobs.append(file)
                else:
                    print(f"Checksum matches for: {file['path']}, not updating...")
            except KeyError:
                blobs.append(file)
        else:                                               # File is a tree
            trees.append(file)

    for folder in trees:                                    # Create folders
        try:
            print(f"Creating {folder['path']}")
            os.mkdir(folder["path"])
        except FileExistsError:
            print(f"{folder['path']} already exists")

    with open("utils/local_checksums.json", "+w") as checksum_file:
        for blob in blobs:
            try:
                with open(blob["path"], "+wb") as file:
                    print (f"Getting {blob['url']}")
                    checksums[blob["path"]] = blob["sha"]
                    file_data  = json.loads(get(blob["url"]))
                    file_b64   = file_data["content"]
                    file_bytes = base64.b64decode(file_b64)
                    print (f"Writing {blob['path']}")
                    file.write(file_bytes)
                time.sleep(COOLDOWN)
            except Exception as e:
                print (f"Exception {e} of type {type(e)}")
        json.dump(checksums, checksum_file, indent=4)

    if if_depends.lower() == "y":
        os.system('"pip install -r requirements.txt"')
    if if_run.lower() == "y":
        os.system('"python3 main.py"')
