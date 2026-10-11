import csv
import io
import os
import shutil
import tempfile
import time
from os import environ

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# the root url redirects to the Azure B2C sign-in page, which redirects back to the account page.
LOGIN_URL = 'https://a826-umax.dep.nyc.gov/'
TIMEOUT = 30
# text that appears once a tab's data has loaded; exporting before then downloads nothing.
LOADED_TEXT = {'Usage': 'Your total consumption', 'Billing': 'Total amount'}


# daily meter readings for the current month, as a list of lines ready to email / store.
def scrape_daily_usage():
    with Session() as s:
        print('getting daily usage...')
        rows = s.export_csv('Usage')
    return format_daily_usage(rows)


# returns [billed usage rows, bill rows] - each a list of dicts parsed from the billing export.
# the new site only offers one billing export (period, amount, HCF), so both come from it.
def scrape_monthly():
    with Session() as s:
        print('getting billing history...')
        rows = s.export_csv('Billing')
    return [rows, rows]


# rows: list of dicts from the Usage export. the export pads the rest of the month with index 0,
# so only rows with a meter index are real readings.
def format_daily_usage(rows):
    lines = ['daily meter readings!']
    for r in rows:
        if r['Index'].strip() in ('', '0'):
            continue
        lines.append('{0:<13} {1:>3} {2:<6} ${3:>7}  index {4}'.format(
            r['Time period'].strip(), r['Consumption'].strip(), r['Consumption unit'].strip(),
            r['Approximate charge'].strip(), r['Index'].strip()))
    return lines


def parse_csv(text):
    return list(csv.DictReader(io.StringIO(text.lstrip('﻿'))))


class Session:
    """Headless Chrome logged in to My DEP Account. Expects `user` and `pwd` in the environment."""

    def __enter__(self):
        self.dl_dir = tempfile.mkdtemp(prefix='dep-')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('window-size=1300,1400')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('prefs', {
            'download.default_directory': self.dl_dir,
            'download.prompt_for_download': False,
        })
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        self._login()
        return self

    def __exit__(self, *exc):
        self.driver.quit()
        shutil.rmtree(self.dl_dir, ignore_errors=True)

    def _login(self):
        d = self.driver
        d.get(LOGIN_URL)
        self.wait.until(EC.visibility_of_element_located((By.ID, 'signInName'))).send_keys(environ['user'])
        d.find_element(By.ID, 'password').send_keys(environ['pwd'])
        print('login values set.')
        d.find_element(By.ID, 'next').click()
        self.wait.until(EC.element_to_be_clickable((By.ID, 'NavMenu_Usage')))
        print('logged in.')

    # open a nav tab (Usage / Billing), click its "Export displayed data to Excel" button
    # (which actually downloads a csv) and return the parsed rows.
    def export_csv(self, tab):
        d = self.driver
        self.wait.until(EC.element_to_be_clickable((By.ID, 'NavMenu_' + tab))).click()
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), LOADED_TEXT[tab]))
        before = set(os.listdir(self.dl_dir))
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Export displayed data to Excel')]")))
        button.click()
        path = self._wait_for_download(before)
        with open(path, encoding='utf-8-sig') as f:
            return parse_csv(f.read())

    def _wait_for_download(self, before):
        deadline = time.time() + TIMEOUT
        while time.time() < deadline:
            new = set(os.listdir(self.dl_dir)) - before
            if new and not any(f.endswith('.crdownload') for f in new):
                return os.path.join(self.dl_dir, new.pop())
            time.sleep(0.5)
        raise TimeoutError('export download did not finish')
