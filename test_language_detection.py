"""
TEST LANGUAGE DETECTOR SCRIPT
Author: Anas Mounsif - Università Degli Studi Della Basilicata

Requirements:
Python 3.8
PyTest

Usage:
RECOMMENDED: [ pytest ] in test_detector folder
Or [ py.test -k <method_name> -v ] for testing specific method.
For more information about PyTest visit: https://docs.pytest.org/en/stable/contents.html
"""

# IMPORTS
# ----------------------------------------------------------------------------------------------------------------------
# Importing Libraries
import language_detection as dt
import pytest
from pathlib import Path as sysPath
import os

# Config shortcut
PATH = os.path

# Directories and files for Testing
repo_withMd = sysPath("repositories_test/repo_withReadme/")
repo_withNoMd = sysPath("repositories_test/repo_withNoReadme/")
repo_withNestedMd = sysPath("repositories_test/repo_withNestedReadme/")
repo_withRenamedMd = sysPath("repositories_test/repo_withRenamedReadme/")

repo_withEmptyMd = sysPath("repositories_test/repo_withEmptyReadme/")
repo_withFullMd = sysPath("repositories_test/repo_withFullReadme/")

# Regex Tests
md_withTable = sysPath("repositories_test/README_files/README_table.md")
md_withLink = sysPath("repositories_test/README_files/README_link.md")
md_withImage = sysPath("repositories_test/README_files/README_image.md")
md_withCodeSnippet = sysPath("repositories_test/README_files/README_codeSnippet.md")
md_withCodeUrl = sysPath("repositories_test/README_files/README_url.md")
md_withHtml = sysPath("repositories_test/README_files/README_html.md")
md_withRemaining = sysPath("repositories_test/README_files/README_remaining.md")
md_all = sysPath("repositories_test/README_files/README_all.md")


# Test Methods   
# ----------------------------------------------------------------------------------------------------------------------
# Test Exists method
def test_exists():
    there_is_md = dt._find_all_md(repo_withMd)
    there_no_md = dt._find_all_md(repo_withNoMd)
    nested_md = dt._find_all_md(repo_withNestedMd)
    renamed_md = dt._find_all_md(repo_withRenamedMd)
    if there_is_md and not there_no_md and nested_md and renamed_md:
        assert True
    else:
        assert False


# Test if readme is empty and not
def test_empty_full():
    with open(PATH.abspath(dt._find_all_md(repo_withEmptyMd)[0]), 'r', encoding='utf8') as f:
        test_string_1 = dt.strip_inspector("", f.read()).replace("\n", " ")
    with open(PATH.abspath(dt._find_all_md(repo_withFullMd)[0]), 'r', encoding='utf8') as f:
        test_string_2 = dt.strip_inspector("", f.read()).replace("\n", " ")
    if test_string_1 and not test_string_1.isspace() and \
            test_string_2 and not test_string_2.isspace():
        assert True
    else:
        assert False


# Test elimination of tables
def test_remove_table():
    with open(PATH.abspath(md_withTable), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt._refactor("", str_md, dt._TABLES)
        if output and not output.isspace():
            assert False
        else:
            assert True


# Test elimination of links
def test_remove_links():
    with open(PATH.abspath(md_withLink), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt._refactor("", str_md, dt._LINKS)
        if output and not output.isspace():
            assert False
        else:
            assert True


# Test elimination of URLs
def test_remove_urls():
    with open(PATH.abspath(md_withCodeUrl), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt._refactor("", str_md, dt._URLS)
        if output and not output.isspace():
            assert False
        else:
            assert True


# Test elimination of images
def test_remove_images():
    with open(PATH.abspath(md_withImage), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt._refactor("", str_md, dt._IMAGES)
        if output and not output.isspace():
            assert False
        else:
            assert True


# Test elimination of code snippet
def test_remove_code_snippet():
    with open(PATH.abspath(md_withCodeSnippet), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt._refactor("", str_md, dt._CODE_SNIPPETS)
        if output and not output.isspace():
            assert False
        else:
            assert True


# Test elimination of Html
def test_remove_html():
    with open(PATH.abspath(md_withHtml), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt._refactor("", str_md, dt._HTML)
        if output.strip() == 'The HTML - test regex.':
            assert True
        else:
            assert False


# Test elimination all Remaining Special Character
def test_remove_remaining():
    with open(PATH.abspath(md_withRemaining), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt._refactor("", str_md, dt._REMAINING_SPECIAL_CHARS)
        if output.strip() == 'TesTtEStTesT的模拟仿真程序':
            assert True
        else:
            assert False


# Test elimination of all markdowns
def test_all_markdown_removal():
    with open(PATH.abspath(md_all), 'r', encoding='utf8') as f:
        str_md = f.read()
        output = dt.strip_inspector("", str_md)
        if output.strip() == 'TESTTESTTEE':
            assert True
        else:
            assert False


# Test the correct transformation of the percentages
def test_format():
    percentage = 0.499928373951075347813
    assert dt._format(percentage) == str(50.0)


# Test if destination folders exists
@pytest.mark.xfail(reason="Folders must exists to pass the test!")  # COMMENT if folders exists
def test_isdir():
    if PATH.isdir(dt._ENGLISH) and PATH.isdir(dt._NOT_ENGLISH) \
            and PATH.isdir(dt._MIXED) and PATH.isdir(dt._UNKNOWN):
        assert True
    else:
        assert False


# Test if string contains is valid method
def test_is_valid():
    digit_condition = dt._is_valid("12351236523875")
    min_length_condition = dt._is_valid("less than %s " % dt._MIN_LENGTH)
    special_char_condition = dt._is_valid("???_+><#$%@")
    if not digit_condition and not min_length_condition and not special_char_condition:
        assert True
    else:
        assert False


# Test if correct execution of name of
def test_name_of():
    path = "/root/user/folder/nested_folder"
    name = dt._name_of(path)
    if name == 'nested_folder':
        assert True
    else:
        assert False


# Test if there is not english
def test_is_there_english():
    percentage_of_english = 0.0
    if not dt._is_there_english(percentage_of_english):
        assert True
    else:
        assert False


# Test if percentage are properly formatted
def test_percentage_parser():
    en = 100.0
    other = 300.0
    eng_percentage, other_percentage = dt._parse_results(en, other)
    if eng_percentage == 0.25 and other_percentage == 0.75:
        assert True
    else:
        assert False


def test_analyze_results():
    detections = {
        "Detections": [{
            "Detection": [
                {"code": "en", "percentage": 0.4},
                {"code": "en", "percentage": 0.3},
                {"code": "cn", "percentage": 0.7},
                {"code": "it", "percentage": 0.6},
                {"code": "cn", "percentage": 1.0},
                {"code": "en", "percentage": 1.0}
            ]
        }]
    }
    en_base, other_base = dt._analyze_results(detections)
    assert en_base == 1.7
    assert other_base == 2.3


def test_increment_error():
    dt.increment_error()
    dt.increment_error()
    dt.increment_error()
    dt.increment_error()
    dt.increment_error()
    assert dt._TOTAL_ERRORS == 5


def test_fail_inspector():
    dt._CSV_OUTPUT = 0
    english_detections1 = {
        "Detections": [{
            "Detection": [
                {"code": "en", "percentage": 0.9},
                {"code": "cn", "percentage": 0.1}
            ]
        }]
    }
    assert dt.inspector(english_detections1, "", None, None, 0) == "english"
    not_english_detections = {
        "Detections": [{
            "Detection": [
                {"code": "cn", "percentage": 0.9},
                {"code": "cn", "percentage": 0.1}
            ]
        }]
    }
    assert dt.inspector(not_english_detections, "", None, None, 0) == "not english"
    mixed_detections = {
        "Detections": [{
            "Detection": [
                {"code": "en", "percentage": 1.0},
                {"code": "cn", "percentage": 1.0}
            ]
        }]
    }
    assert dt.inspector(mixed_detections, "", None, None, 0) == "mixed"


