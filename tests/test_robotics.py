import pytest
from bs4 import BeautifulSoup
from ..robotics import Robot
import re

@pytest.fixture(scope="module")
def robot():
    r = Robot("Quandrinaut")
    yield r
    r.close_browser()

@pytest.fixture(scope="module")
def einstein_soup():
    einstein_url = "https://en.wikipedia.org/wiki/Albert_Einstein"
    robot = Robot("Quandrinaut")
    robot.open_webpage(einstein_url)
    soup = BeautifulSoup(robot.get_page_source(), "html.parser")
    robot.close_browser()
    return soup

def test_find_birth_death_dates(einstein_soup):
    robot = Robot("Quandrinaut")
    born, died = robot.find_birth_death_dates(einstein_soup)
    assert born == "(1879-03-14)"
    assert died == "(1955-04-18)"

def test_calculate_age():
    robot = Robot("Quandrinaut")
    age = robot.calculate_age("(1879-03-14)", "(1955-04-18)")
    assert age == 76

def test_get_first_paragraph(einstein_soup):
    robot = Robot("Quandrinaut")
    first_paragraph = robot.get_first_paragraph(einstein_soup)
    assert re.match(r"Albert Einstein.*?physicist", first_paragraph)

def test_get_field_of_work(einstein_soup):
    robot = Robot("Quandrinaut")
    field_of_work = robot.get_field_of_work(einstein_soup)
    assert "Physics" in field_of_work

def test_get_birthplace(einstein_soup):
    robot = Robot("Quandrinaut")
    birthplace = robot.get_birthplace(einstein_soup)
    assert "Ulm, Kingdom of Württemberg, German Empire" in birthplace
