from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')
driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(10)

driver.get('https://a826-amr.nyc.gov/mydepaccount/')

user = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_UserName')
pwd = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_Password')
login = driver.find_element_by_id('ctl00_BodyPlaceHolder_loginUser_LoginButton')

user.send_keys('user')
pwd.send_keys('password')
driver.get_screenshot_as_file('loginready.png')
login.click()
driver.get_screenshot_as_file('loggedin.png')

# reads history
print('getting reads history...')
usepage = driver.find_element_by_id('optionSeeMyWaterUse')
usepage.click()
checkelement = driver.find_element_by_id('col1')
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
print('element.text: {0}'.format(element.text))

# now get the bills...
billclick = driver.find_element_by_id('optionSeeMyBill')
billclick.click()
bills = driver.find_element_by_id('ctl00_ContentPlaceHolder1_contentBillHist')
print('bills: {0}'.format(bills.text))

driver.close()
driver.quit()

print('done.')
