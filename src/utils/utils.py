"""Contains utility functions for the project"""


from os import makedirs, path
from shutil import rmtree
from datetime import datetime
import unicodedata
import re

from .logger import logger
from ..constants import USER_INPUT_YES


def pause() -> None:
    """Pause the terminal until user hits Enter"""
    _: str = input('Press Enter to continue . . .')


def create_directory(directory: str, force: bool | None = None) -> bool:
    """Remove (if force=True) and create a directory

    Args:
        - directory (str): A directory to create
        - force (bool | None): Whether to remove the directory if it exists. Default to None to ask for user input [Y/n]

    Raise:
        - PermissionError: If the directory cannot be removed due to permission error

    Returns:
        - bool: True if the directory was created, False if it was already created
    """
    if path.exists(path=directory):
        if force is False:
            pass
        elif force is True or input(
                f'{directory} already exists. Force create it [Y/n]: ') in USER_INPUT_YES:
            try:
                rmtree(path=directory)
            except PermissionError as e:
                logger.error(msg=e)
                raise e
            logger.info(msg=f'\'{directory}\' was removed recursively!')
        else:
            logger.info(
                msg=f'Skip creating \'{directory}\'')
            return False
    makedirs(name=directory)
    logger.info(msg=f'\'{directory}\' was created!')
    return True


def remove_directory(directory: str) -> bool:
    """Remove a directory

    Args:
        - directory (str): A directory to remove

    Raise:
        - PermissionError: If the directory cannot be removed due to permission error

    Returns:
        - bool: True if the directory was removed, False if it was not found
    """
    if path.exists(path=directory):
        try:
            rmtree(path=directory)
        except PermissionError as e:
            logger.error(msg=e)
            raise e
        logger.info(msg=f'\'{directory}\' was removed recursively!')
        return True
    logger.info(
        msg=f'\'{directory}\' was not found. Skip removing it')
    return False


def datetime_name() -> str:
    """Get the datetime name (%Y-%m-%d %H-%M-%S-%f)

    Returns:
        - str: The datetime name
    """
    return datetime.now().strftime('%Y-%m-%d %H-%M-%S-%f')


def slugify(value, allow_unicode=True):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.

    Taken from https://github.com/django/django/blob/66e47ac69a7e71cf32eee312d05668d8f1ba24bb/django/utils/text.py#L452
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def create_page_link(link: str, page_num: int) -> str:
    """create the page link
    Agrs:
        - link(str) : link without page
        - page_num(int):The number of page
    Returns:
        - link with page
    """
    if re.search(r'&page=\d+', link):
        return re.sub(r'&page=\d+', f'&page={page_num}', link)
    else:
        return f"{link}&page={page_num}"
