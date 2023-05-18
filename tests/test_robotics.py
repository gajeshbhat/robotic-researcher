from lib.robotics import Robot
from unittest.mock import patch

def test_robot_init():
    robot = Robot('TestRobot', ['Ada Lovelace'])
    assert robot.name == 'TestRobot'
    assert robot.scientists == ['Ada Lovelace']

@patch.object(Robot, '_get_page_source')
def test_get_scientist_page_soup(mock_get_source):
    mock_get_source.return_value = "<html><body><h1>Test Page</h1></body></html>"
    robot = Robot('TestRobot', ['Ada Lovelace'])
    soup = robot.get_scientist_page_soup('Ada Lovelace')
    assert soup.h1.string == 'Test Page'