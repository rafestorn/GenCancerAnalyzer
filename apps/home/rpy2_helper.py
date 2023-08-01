import logging
import os
import platform
from functools import lru_cache
from rpy2.situation import get_r_home, get_rlib_path


def _fix_r_home():
    """
    Fix the R_HOME env var if we need to
    """
    r_home = os.environ.get("R_HOME")

    if r_home:
        os.environ["R_HOME"] = r_home.replace("\\", "/")

    if not get_r_home():
        raise OSError("R_HOME is not set.")


def _add_dll_directory():
    """
    Adds the platform's R library path to the allowed library
    load dirs. Stops weird DLL loading issues if you are using
    R in a different path than the system install dir.

    Only applicable on Windows
    """

    if "add_dll_directory" not in dir(os):
        return  # not windows

    r_home = get_r_home()
    system = platform.system()
    dll_location = get_rlib_path(r_home, system)
    dll_files_location = os.path.dirname(dll_location)

    if dll_files_location not in os.getenv("PATH"):
        logging.warn(f"R DLL location is not in the path: {dll_files_location}")

    # fix security in recent Python versions
    os.add_dll_directory(dll_files_location)


@lru_cache
def get_robjects():
    """
    Fix path and DLL loading issues before loading rpy2
    """
    _fix_r_home()
    _add_dll_directory()

    from rpy2 import robjects

    return robjects