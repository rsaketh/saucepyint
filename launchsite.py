import pytest
import os
from selenium import webdriver
from _pytest.runner import runtestprotocol


@pytest.fixture
def driver(request):
    sauce_username = os.getenv("SAUCE_USERNAME")
    sauce_access_key = os.getenv("SAUCE_ACCESS_KEY")
    remote_url = "http://{}:{}@ondemand.saucelabs.com/wd/hub".format(sauce_username, sauce_access_key)

    sauceOptions = {
        "screenResolution": "1280x768",
        "platformName": "Windows 10",
        "browserVersion": "101.0",
        "seleniumVersion": "3.11.0",
        'name': 'Sauce Test Launch Tesla site',
        'extendedDebugging': True,
        'capturePerformance': True
    }

    chromeOpts = {
        'platformName': "Windows 10",
        'browserName': "chrome",
        'browserVersion': '101.0',
        'sauce:options': sauceOptions
    }


#    browser = webdriver.Remote(remote_url, desired_capabilities=chromeOpts)
#   yield browser
#   browser.quit()


def pytest_runtest_protocol(item, nextitem, driver):
    reports = runtestprotocol(item, nextitem=nextitem)
    for report in reports:
        if report.when == 'call':
            driver.execute_script('sauce:job-result={}'.format(report.outcome))
    return True


def test_should_open_safari(driver):
    driver.get("https://tesla.com/")
    actual_title = driver.title
    expected_title = "Electric Cars, Solar & Clean Energy | Tesla"
    assert expected_title == actual_title
