from m_gitupdated import *
import yaml

def main():
    rootLocation = ""
    argLength = len(sys.argv)
    if (os.path.exists("folders.yml")):
        with open(r'folders.yml') as file:
            folderFile = yaml.full_load(file)
    key = "root"
    if folderFile.get(key) is not None:
        rootLocation = folderFile.get(key)
    elif (len(sys.argv) > 1):
        # Check argument length. If path specified as argument, use that
        rootLocation = sys.argv[1]
    else:
        # Else, prompt user for root folder location
        rootLocation = promptForLocation()

    rootLocation = os.path.expanduser(rootLocation)

    print(bcolors.HEADER, "Root file location is: ", bcolors.ENDC, rootLocation)
    shouldFF = promptForFF()
    printSpace()

    try:
        if folderFile.get("repo_relative_paths") is not None:
            folderList = folderFile.get("repo_relative_paths")
        else:
            folderList = os.listdir(rootLocation)
        for folder in folderList:
            currentLocation = rootLocation + folder
            try:
                repo = git.Repo(currentLocation)
                assert not repo.bare
                printRepo(repo, currentLocation, shouldFF)
            except git.exc.NoSuchPathError as exception:
                continue
                # print("NoSuchPathError: ", exception)
                # printSpace()
            except git.exc.InvalidGitRepositoryError as exception:
                continue
                # print("InvalidGitRepositoryError: ", exception)
                # printSpace()    
    except FileNotFoundError as exception:
        print(bcolors.FAIL + "File location: \"" + rootLocation + "\" not valid. Please try again." + bcolors.ENDC)


# Call the main method and run GitUpdated
main()