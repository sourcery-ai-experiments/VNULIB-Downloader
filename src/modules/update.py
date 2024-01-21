"""Update the tool"""


from requests import get, Response
from json import loads

from ..utils.printColor import printInfo, printSuccess, printError, printWarning

from ..CONSTANTS import REPOSITORY_URL, VERSION


def getVersionsFromRepository(repo_url: str = REPOSITORY_URL) -> list[str]:
    """Get versions from repository exclude beta versions

    Params:
        - repo_url (str) = REPOSITORY_URL: Repository URL

    Returns:
        - list[str]: List of versions
    """
    api_url: str = 'https://api.github.com/repos/' + \
        REPOSITORY_URL.split('/')[-2] + REPOSITORY_URL.split('/')[-1] + '/tags'
    response: Response = get(f'{repo_url}/releases')
    if response.status_code == 200:
        versions = []
        for version in loads(response.text):
            versions.append(version['name'])
        printInfo(message='Successfully get versions from repository')
        return versions
    else:
        printError(message='Failed to get versions from repository')
        return []


def compareVersion(version: str, to_compare_version: str) -> int:
    """Compare two versions

    Params:
        - version (str): Version to compare
        - to_compare_version (str): Version to be compared

        Returns:
            - int: 1 if version > to_compare_version, -1 if version < to_compare_version, 0 if version == to_compare_version"""
    extracted_version: list[str] = version.split('.')
    extracted_to_compare_version: list[str] = to_compare_version.split('.')
    for i in range(len(version)):
        if int(extracted_version[i]) > int(extracted_to_compare_version[i]):
            return 1
        elif int(extracted_version[i]) < int(extracted_to_compare_version[i]):
            return -1
    return 0


def checkNeedToUpdate(current_version: str, VERSIONS: list[str]) -> bool:
    """Check if it needs to update the tool or not

    Params:
        - current_version (str): Current version
        - VERSIONS (list[str]): List of versions from repository

    Returns:
        - bool: True if it needs to update the tool, False if not
    """
    if 'beta' in current_version:
        for version in [version for version in VERSIONS if 'beta' in version]:
            match compareVersion(version=current_version, to_compare_version=version):
                case -1:
                    printInfo(message='Your tool is not up-to-date')
                    return True
                case 0:
                    printSuccess(message='Your tool is up-to-date')
                    return False
                case 1:
                    printWarning(
                        message='Your tool version is not in the repository')
                    return False
    else:
        for version in [version for version in VERSIONS if 'beta' not in version]:
            match compareVersion(version=current_version, to_compare_version=version):
                case -1:
                    printInfo(message='Your tool is not up-to-date')
                    return True
                case 0:
                    printSuccess(message='Your tool is up-to-date')
                    return False
                case 1:
                    printWarning(
                        message='Your tool version is not in the repository')
                    return False
    return False


def updateTheTool() -> None:
    """Update thee tool function

    Params:
        - None

    Returns:
        - None
    """
    versions: list[str] = getVersionsFromRepository(
        repo_url=REPOSITORY_URL)
    if checkNeedToUpdate(current_version=VERSION, VERSIONS=versions):
        printInfo(message='Updating the tool... (Not implemented yet)')
        pass  # implement later
    else:
        printInfo(message='Skip updating the tool')
