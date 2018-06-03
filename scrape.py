from selenium import webdriver
from os import environ


# scrape website data. expects login and passwor in environment variables.
# returns text for historical water consumption and billing data.
def scrape_data():
    result = []
    # setup chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=options)
    driver.implicitly_wait(10)
    driver.get('https://a826-amr.nyc.gov/mydepaccount/')

    # login
    user = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_UserName')
    pwd = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_Password')
    login = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_LoginButton')
    user.send_keys(environ.get('user'))
    pwd.send_keys(environ.get('pwd'))
    login.click()

    # reads history
    print('getting reads history...')
    usepage = driver.find_element_by_id('optionSeeMyWaterUse')
    usepage.click()
    driver.find_element_by_id('col1')
    # select monthly usage for year
    selbox = driver.find_element_by_id('ctl00_ContentPlaceHolder1_ddlGraphMode')
    print('check element found.')
    selbox.send_keys('Monthly Usage for Year')
    viewbtn = driver.find_element_by_id('ctl00_ContentPlaceHolder1_btnViewGraph')
    driver.get_screenshot_as_file('graphselect.png')
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
    result.append(bills.text.split('\n'))

    # tidy up
    driver.close()
    driver.quit()
    return result
