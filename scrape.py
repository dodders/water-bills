from selenium import webdriver
from os import environ
import requests
import logging
from selenium.webdriver.remote.remote_connection import LOGGER


def scrape_daily_usage():
    driver = getdriver()
    # reads history
    print('getting water use...')
    usepage = driver.find_element_by_id('optionSeeMyWaterUse')
    print('found water use...')
    usepage.click()
    readshistory = driver.find_element_by_id('optionReadsHistory')
    print('found reads history...')
    readshistory.click()
    readstable = driver.find_element_by_id('ctl00_ContentPlaceHolder1_divSimpleMeterDay')
    print('reads table!:' + readstable.text)
    reads = readstable.text.split('\n')
    driver.close()
    driver.quit()
    return format_daily_usage(reads)


def format_daily_usage(usage):
    return ['daily meter readings!'] + [x.strip() for x in usage[4:-1]]


# scrape website data. expects login and passwor in environment variables.
# returns text for historical water consumption and billing data.
def scrape_monthly():
    driver = getdriver()
    # reads history
    print('getting reads history...')
    usepage = driver.find_element_by_id('optionSeeMyWaterUse')
    print('found reads history...')
    usepage.click()
    driver.find_element_by_id('col1')
    # select monthly usage for year
    selbox = driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlGraphMode')
    print('check element found.')
    selbox.send_keys('Monthly Usage for Year')
    viewbtn = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnViewGraph')
    # driver.get_screenshot_as_file('graphselect.png')
    viewbtn.click()
    # now get history rather than graph...
    hist = driver.find_element_by_id('optionReadsHistory')
    hist.click()
    # wait for the table to render...
    element = driver.find_element_by_id('ctl00_ContentPlaceHolder1_divSimpleMeter')
    result.append(element.text.split('\n'))

    # now get the bills...
    billclick = driver.find_element_by_id('optionSeeMyBill')
    billclick.click()
    bills = driver.find_element_by_id('ctl00_ContentPlaceHolder1_contentBillHist')
    result = bills.text.split('\n')

    # tidy up
    driver.close()
    driver.quit()
    return result


def getdriver():
    # test page
    r = requests.get('https://a826-amr.nyc.gov/mydepaccount/')
    print('test get result:', r)
    # setup chrome driver
    LOGGER.setLevel(logging.DEBUG)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options, service_args=["--verbose"])
    driver.implicitly_wait(20)
    print('driver set up...')
    driver.get('https://a826-amr.nyc.gov/mydepaccount/')
    print('login page retrieved...')

    # login
    user = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_UserName')
    pwd = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_Password')
    print('login elements found...')
    user.send_keys(environ.get('user'))
    pwd.send_keys(environ.get('pwd'))
    print('login values set.')

    login = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_LoginButton')
    print('login button found.')
    login.click()
    print('login clicked.')
    return driver
