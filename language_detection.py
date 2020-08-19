"""

LANGUAGE DETECTOR SCRIPT
Author: Anas Mounsif - Università Degli Studi Della Basilicata

Requirements:
six
Python 3.8
Probably glob, ConfigParser

Usage:
[ python3 language_detection.py ] or [ python3 language_detection.py -h ] for more information.

* Consult config.ini and log.conf

"""

# ----------------------------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------------------------
# Importing Libraries
import langdetect as dl
import logging.config
import shutil as sh
import pytest
import argparse
import time
import csv
import re
import os

from pathlib import Path
from datetime import date
from glob import glob as gl
from typing import Tuple, Optional
from configparser import ConfigParser

# Importing Exceptions from Libraries
from langdetect.lang_detect_exception import LangDetectException

'''
# ----------------------------------------------------------------------------------------------------------------------
# ABOUT AUTHOR
# ----------------------------------------------------------------------------------------------------------------------
# Colors Configuration
_RED = '\033[91m'
_END = '\033[0m'

# Defining the script description
_DESCRIPTION = ' This script is able to filter repositories based on the language used for writing the README. ' \
               '\n Use the normal language translation library found at this address: ' \
               '{}https://github.com/Mimino666/langdetect{}' \
               '\n And implements regular expressions for cleaning the files to be translated from the markdowns.' \
               '\n At the end it generates a CSV file with all the information inside.' \
               '\n It also generates a log file where it is possible to consult the operations carried out ' \
               'as well as identify any problems. ' \
               '\n Use the {}config.ini{} to meet your needs.' \
               '\n\n For more information about this script see: ' \
               '{}https://github.com/anasmounsif/README-language-detector{}'.format(_RED, _END, _RED, _END, _RED, _END)

# Defining the script About Author
_ABOUT = " {}Anas Mounsif{} - University of Basilicata.".format(_RED, _END)

# Initiating the parser with a description
parser = argparse.ArgumentParser(description=_DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)

# Adding optional argument
parser.add_argument("-v", "--version", help=" show script version", action='version', version=' version: 1.0.8')
parser.add_argument("-a", "--author", help=" show author information", action='version', version=_ABOUT)
parser.parse_args()
'''

# ----------------------------------------------------------------------------------------------------------------------
# PREFERENCES
# ----------------------------------------------------------------------------------------------------------------------
# Load the configuration file - Make sure config.ini exists!
parser = ConfigParser()
parser.read('config.ini')

# Set to 0 for deterministic result, 1 for non-deterministic in config.ini
_OUTPUT_TYPE = 0 if int(parser.get("parameters", "translation_type")) == 0 else 1
# Set to 1 for output generation in config.ini, 0 for not
_CSV_OUTPUT = 0 if int(parser.get("files", "activate_csv_output")) == 0 else 1

# True if you want the script to move the repositories else False in config.ini - be care to ACCESS DENIED problem!
_MOVE = False if int((parser.get("parameters", "moving_feature"))) == 0 else True  # Just get the value

# Modify as needed in config.ini, but pay attention to folder's structure
_ENGLISH = Path(str(parser.get("destinations", "destination_english")))
_NOT_ENGLISH = Path(str(parser.get("destinations", "destination_not_english")))
_MIXED = Path(str(parser.get("destinations", "destination_mixed")))
_UNKNOWN = Path(str(parser.get("destinations", "destination_unknown")))

# CSV config params
_CSV = str(parser.get("files", "input"))  # Get input csv name from config.ini
_NEW_CSV = str(parser.get("files", "output"))  # Get output csv name from config.ini
_MIN_LENGTH = int(parser.get("parameters", "min_length"))  # Get min length for translation from config.ini
_FIELDNAMES = ['Index', 'CloneDirectory', 'ReadmeAnalyzed', 'Language',
               'Code1', 'Percentage1', 'Code2', 'Percentage2']  # Fieldnames structure of output.csv

# Regex patterns
_TABLES = r"^(\|[^\n]+\|\r?\n)((?:\|:?[-]+:?)+\|)(\n(?:\|[^\n]+\|\r?\n?)*)?$"  # pattern to recognize tables
_URLS = r"https?:\/\/?[\da-z\.-]+\.[a-z\.]{2,6}[\/\w \.-]*"  # pattern to recognize urls
_IMAGES = r"!\[[^\]]+\]\([^)]+\)"  # pattern to recognize images
_CODE_SNIPPETS = r"(```.+?```)"  # pattern to recognize code snippets
_LINKS = r"\[.*?\]\(.*?\)"  # pattern to recognize links
_HTML = r"\<.*?\>"  # pattern to recognize the html code
# _WARNING = r"[^A-Za-z0-9]"  # pattern to recognize all special characters - Also delete the Chinese Character!
_REMAINING_SPECIAL_CHARS = r"([#@\s]|:[)(])|\W"  # pattern to recognize all special characters
_ILLEGAL_STRING = r'^[_\W0-9]+$'  # pattern to recognize the only digits or special character

# GitHub Supported extension
_EXTENSIONS = ['*.markdown', '*.mkdn', '*.md', '*.mdown', '*.txt', '*.mdwn', '*.mkd']

# Init logger
logging.config.fileConfig(fname='log.conf', defaults={'logfilename': 'log'})
logger = logging.getLogger('sessionLogs')

# Config shortcut
MOVE_TO = sh.move
PATH = os.path
SEPARATOR = os.sep
TODAY = date.today()

# LOGS shortcut
DEBUG = logger.debug
INFO = logger.info
WARNING = logger.warning
ERROR = logger.error
CRITICAL = logger.critical

# Takes number of errors
_TOTAL_ERRORS = 0


# ----------------------------------------------------------------------------------------------------------------------
# UTILITY METHODS
# ----------------------------------------------------------------------------------------------------------------------
# Printing Exception
def _print_exception(e):
    print("ERROR: Something went wrong -> %s " % e)  # pragma: no cover


# Takes care of passing the text and the pattern to the stripper
def _refactor(repository, str_md, pattern) -> str:
    outcome = stripper(repository, str_md, pattern)
    return outcome


# Writing CSV
def _csv_writer(writer, row, destination, num_readme, lang,
                en_code, en_percentage, other_code, other_percentage):
    INFO("Writing CSV file!")  # pragma: no cover

    if not _MOVE:
        destination = row['CloneDirectory']

    # Writing
    writer.writerow({'Index': '%s' % row['Index'],
                     'CloneDirectory': '%s' % destination,
                     'ReadmeAnalyzed': '%s' % num_readme,
                     'Language': '%s' % lang,
                     'Code1': '%s' % en_code,
                     'Percentage1': '%s' % en_percentage,
                     'Code2': '%s' % other_code,
                     'Percentage2': '%s' % other_percentage
                     })


# Getting name of the repository
def _name_of(repo) -> str:
    return PATH.abspath(repo).split(PATH.sep)[-1]


# Getting absolute path of the Destination - if MOVE = True
def _destination(relative_destination, repository) -> str:
    return Path(PATH.abspath(relative_destination) + SEPARATOR + _name_of(repository))


# Checking if README.md exists in repository folder structure
def _find_all_md(repository_dir) -> []:
    paths_found = []

    # Getting all README
    for extension in _EXTENSIONS:
        # Passing "readme" and not variable README for correct execution of tests
        results = gl(PATH.join(repository_dir, '**', extension), recursive=True)
        found = [i for i in results if "readme" in PATH.basename(i.lower())]
        paths_found.extend(found)

    return paths_found


# Transform percentage to ##.#
def _format(percent) -> str:
    return "{:.1f}".format(100 * percent)


# Checking if README is valid
def is_valid(string) -> bool:
    condition = re.match(_ILLEGAL_STRING, string)
    return False if len(string) < _MIN_LENGTH or condition else True


# Checking the typology of the result and perform the detection
def _detector(target) -> []:  # pragma: no cover
    dl.DetectorFactory.seed = _OUTPUT_TYPE
    return dl.detect_langs(target)


# Checking if if english was detected
def _is_there_english(percentage) -> bool:
    return True if percentage > 0.0 else False


# Analyzing json
def _analyze_results(results) -> Tuple[float, float]:
    en_base = 0.0
    other_base = 0.0

    # Scanning detections
    for detection in results["Detections"]:
        for value in detection["Detection"]:

            if value["code"] == "en":
                en_base += float(value["percentage"])
            else:
                other_base += float(value["percentage"])

    return en_base, other_base


# Transforming local percentage into global
def _parse_results(en, other) -> Tuple[float, float]:
    eng_percentage = float(en / (en + other))
    other_percentage = float(other / (en + other))

    return eng_percentage if en > 0.0 else 0, other_percentage if other > 0.0 else 0


# Getting information for Log summary
def _log_info() -> Tuple[float, str, str, str]:
    start_time = time.time()

    is_move = "Shift ACTIVATED." if _MOVE else "Shift DISABLED."
    is_csv = "CSV generation ACTIVATED." if _CSV_OUTPUT else "CSV generation DISABLED."
    is_deterministic = "Deterministic algorithm ACTIVATED." \
        if _OUTPUT_TYPE == 0 else "Non Deterministic algorithm ACTIVATED."

    return start_time, is_move, is_csv, is_deterministic


# Getting Error counter
def increment_error():
    DEBUG("Incrementing Error counter!")  # pragma: no cover
    global _TOTAL_ERRORS
    _TOTAL_ERRORS += 1


# ----------------------------------------------------------------------------------------------------------------------
# MAIN METHODS
# ----------------------------------------------------------------------------------------------------------------------
# Takes care of replacing the target
def stripper(repository, txt, pattern) -> Optional[str]:
    file = txt

    match_pattern = re.findall(pattern, txt, re.MULTILINE | re.DOTALL)
    if match_pattern:
        new_file = re.sub(pattern, '', file, flags=re.S)
        return new_file
    else:
        return None


# Takes care of checking the text and replacing the targets
def strip_inspector(repository, str_md) -> str:

    # Removing Markdown Code Snippets
    str_from_cs = _refactor(repository, str_md, _CODE_SNIPPETS)
    str_md = str_from_cs if str_from_cs is not None else str_md

    # Removing Table Markdown
    str_from_tables = _refactor(repository, str_md, _TABLES)
    str_md = str_from_tables if str_from_tables is not None else str_md

    # Removing Markdown Links
    str_from_links = _refactor(repository, str_md, _LINKS)
    str_md = str_from_links if str_from_links is not None else str_md

    # Removing Markdown Images
    str_from_images = _refactor(repository, str_md, _IMAGES)
    str_md = str_from_images if str_from_images is not None else str_md

    # Removing Markdown URLs
    str_from_urls = _refactor(repository, str_md, _URLS)
    str_md = str_from_urls if str_from_urls is not None else str_md

    # Removing Html Markdown
    str_from_html = _refactor(repository, str_md, _HTML)
    str_md = str_from_html if str_from_html is not None else str_md

    # Removing All Remaining Special Characters
    str_from_all = _refactor(repository, str_md, _REMAINING_SPECIAL_CHARS)
    str_md = str_from_all if str_from_all is not None else str_md

    # TODO: Add other patterns...

    return str_md


# Analyzes the result and decides the destination of the repositories
def inspector(detections, repo, writer, row, num) -> str:
    try:
        DEBUG("~ Analyzing detection results")  # pragma: no cover

        en_base, other_base = _analyze_results(detections)
        en_final, other_final = _parse_results(en_base, other_base)

        # Formatting percentage
        other = _format(other_final)
        en = _format(en_final)

        INFO("!! How much English is there in the repository? --> {} %".format(en))  # pragma: no cover

        # Checking if README is english
        if _is_there_english(en_base) and en_final >= 0.90:

            DEBUG("Repository is written in english.")  # pragma: no cover

            # Writing CSV
            if _CSV_OUTPUT:
                oth = '' if en_final == 1.0 else 'others'
                oth_percentage = '' if en_final == 1.0 else other

                _csv_writer(writer, row, _destination(_ENGLISH, repo),
                            num, 'english', 'en', en, oth, oth_percentage)

            if _MOVE:
                INFO("OPERATION: Moving repository to 'english' folder "
                     "because README is written in english!")  # pragma: no cover
                MOVE_TO(repo, "%s" % _ENGLISH)

            return "english"

        # Checking if README is mixed
        if _is_there_english(en_base) > 0 and 0.10 < en_final < 0.90:

            INFO("Repository is written in multiple languages.")  # pragma: no cover

            # Writing CSV
            if _CSV_OUTPUT:
                _csv_writer(writer, row, _destination(_MIXED, repo),
                            num, 'mixed', 'en', en, 'others', other)

            if _MOVE:
                INFO("OPERATION: Moving repository to 'mixed' folder because "
                     "README is written in different languages!")  # pragma: no cover
                MOVE_TO(repo, "%s" % _MIXED)

            return "mixed"

        # checking if README is not in English
        if not _is_there_english(en_base) or en_final <= 0.10:

            INFO("Repository is not written in english.")  # pragma: no cover

            # Writing CSV
            if _CSV_OUTPUT:
                if en_final > 0.0:
                    _csv_writer(writer, row, _destination(_NOT_ENGLISH, repo),
                                num, 'not english', 'en', en, 'others', other)
                else:
                    _csv_writer(writer, row, _destination(_NOT_ENGLISH, repo),
                                num, 'not english', 'others', other, '', '')

            if _MOVE:
                INFO("OPERATION: Moving repository to 'not english' folder because "
                     "README isn't written in english!")  # pragma: no cover
                MOVE_TO(repo, "%s" % _NOT_ENGLISH)

            return "not english"

    # Catching exceptions
    except Exception as ex:

        # Incrementing error counter
        increment_error()

        CRITICAL("Exception caught: ", exc_info=True)  # pragma: no cover
        _print_exception(" Catched by inspector method on repository: {} - {} ".format(_name_of(repo), ex))


# ----------------------------------------------------------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------------------------------------------------------
def main():
    try:
        DEBUG("Opening input CSV file.")  # pragma: no cover

        with open(_CSV, encoding='utf-8', errors='ignore') as srcfile:
            readers = csv.DictReader(srcfile, delimiter=',')

            DEBUG("Creating output CSV file.")  # pragma: no cover

            with open(_NEW_CSV, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=_FIELDNAMES)
                writer.writeheader()  # Writing fields

                DEBUG("Scanning CSV rows...\n\n")  # pragma: no cover

                for row in readers:

                    INFO("\n\n")  # pragma: no cover
                    repo_src = row['CloneDirectory']  # Taking the path from CSV

                    # Checking if the repository cannot be cloned
                    if 'null' in repo_src:
                        WARNING("Can't access because repository cannot be cloned! ")  # pragma: no cover
                        _csv_writer(writer, row, 'null', '', '', '', '', '', '')

                        continue

                    else:
                        INFO("[ Analyzing Repository: %s ]" % _name_of(repo_src).upper())  # pragma: no cover
                        INFO("Repository src: %s" % repo_src)  # pragma: no cover

                    readme_paths = _find_all_md(repo_src)  # Checking if readme exist in directory and its subdirs

                    # Scanning files in repository
                    if readme_paths:
                        INFO("README found = %s" % len(readme_paths))  # pragma: no cover

                        # defining the json for the results
                        detections = {
                            "Detections": []
                        }

                        idx = 0  # Index that counts the number of the readme being analyzed

                        # Scanning all readme in repository
                        for readme in readme_paths:
                            try:
                                idx += 1  # Increasing index

                                log = "* Opening Readme." if len(readme_paths) == 1 else "* Opening Readme n.%s" % idx
                                DEBUG(log)  # pragma: no cover
                                INFO("README path: %s" % readme)  # pragma: no cover

                                with open(readme, 'r', encoding='utf-8', errors='ignore') as f:
                                    DEBUG("Trying to clean the readme.")  # pragma: no cover

                                    str_md = strip_inspector(_name_of(repo_src), f.read())  # Cleaning

                                DEBUG("Readme closed.")  # pragma: no cover
                                DEBUG("Checking if readme is empty.")  # pragma: no cover

                                # Doing checks after closing target
                                if str_md and not str_md.isspace() and is_valid(str_md):
                                    DEBUG("Readme ISN'T EMPTY.")  # pragma: no cover

                                    try:
                                        DEBUG("Entering in the Language Detection phase.")  # pragma: no cover
                                        results = _detector(str_md)  # Managing the result of the language detector

                                    # Catching exceptions
                                    except LangDetectException:

                                        # Incrementing error counter
                                        increment_error()

                                        ERROR("Exception caught: ", exc_info=True)  # pragma: no cover
                                        print("Problem on repository: {}, Passing to Language Detector empty string,"
                                              "probably not null, but without characters!".format(_name_of(repo_src)))

                                        pass

                                    else:
                                        log = "Multiple languages detected!" if len(results) > 1 \
                                            else "language detected!"
                                        DEBUG(log)  # pragma: no cover

                                        for result in results:

                                            INFO("LANGUAGE DETECTED: {} with {}% confidence."
                                                 .format(result.lang, _format(result.prob)))  # pragma: no cover
                                            DEBUG("Loading the results into a data structure.")  # pragma: no cover

                                            detections["Detections"].append({"Detection": [
                                                {
                                                    "code": result.lang,
                                                    "percentage": result.prob
                                                }
                                            ]})

                                else:
                                    WARNING("README IS EMPTY!")  # pragma: no cover

                            # Catching exceptions
                            except EnvironmentError: # pragma: no cover

                                # Incrementing error counter
                                increment_error()

                                ERROR("Exception caught: ", exc_info=True)  # pragma: no cover
                                print("Problem on readme n.{} of the repository: {}! "
                                      "probably alias detected!".format(idx, _name_of(repo_src)))

                                pass

                        # Checking for results
                        if len(detections['Detections']) > 0:

                            DEBUG("Entering in the Data Study phase!")  # pragma: no cover
                            results_info = inspector(detections, repo_src, writer, row, len(readme_paths))
                            print("{} -> {}".format(_name_of(repo_src), results_info))

                        else:
                            WARNING("No written readme found!")  # pragma: no cover

                            # Writing CSV
                            if _CSV_OUTPUT:
                                _csv_writer(writer, row, _destination(_UNKNOWN, repo_src),
                                            len(readme_paths), 'unknown', '', '', '', '')

                            if _MOVE:
                                INFO("OPERATION: Moving repository to 'unknown' folder, "
                                     "because README is empty!")  # pragma: no cover
                                MOVE_TO(repo_src, "%s" % _UNKNOWN)

                    else:
                        WARNING("README does not exist, or the format is not supported!")  # pragma: no cover

                        # Writing CSV
                        if _CSV_OUTPUT:
                            _csv_writer(writer, row, _destination(_UNKNOWN, repo_src),
                                        0, 'unknown', '', '', '', '')

                        if _MOVE:
                            INFO("OPERATION: Moving repository to 'unknown' folder, because "
                                 "README does not exist!")  # pragma: no cover
                            MOVE_TO(repo_src, "%s" % _UNKNOWN)

    # Catching exceptions
    except Exception as ex:

        # Incrementing error counter
        increment_error()

        CRITICAL("Exception caught: ", exc_info=True)  # pragma: no cover
        _print_exception(" Catched by main method on repository: {} - {} ".format(_name_of(repo_src), ex))


# ----------------------------------------------------------------------------------------------------------------------
# START
# ----------------------------------------------------------------------------------------------------------------------
# Summary logs
_start_time, _is_move, _is_csv, _is_deterministic = _log_info()

INFO("{} - STARTING SCRIPT..."
     "\n\nScript Config\n"
     "- - - - - - - - - - - - - - - - - - - -"
     "\n- {}\n- {}\n- {}\n"
     "- - - - - - - - - - - - - - - - - - - -"
     "\n\n-->\n".format(TODAY.strftime("%d/%m/%Y"), _is_move, _is_deterministic, _is_csv))  # pragma: no cover


# Starting Detector Script
def init():  # pragma: no cover
    if __name__ == "__main__":  # So you can use [ detector.py ] individual methods for testing or as a module!
        main()


# Calculates the execution time of the script
_TOTAL_TIME = time.time() - _start_time
INFO("\n\nFinished in: {} seconds with {} Errors.".format(_TOTAL_TIME, _TOTAL_ERRORS))  # pragma: no cover
