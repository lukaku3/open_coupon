import unittest
import os
import re
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
# from sub import subClass

class MyTestCase(unittest.TestCase):
    login_account = 'xxxxxx'
    login_password = 'yyyyy'
    base_url='https://www.ncsoft.jp/login/login?retURL=https%3A%2F%2Fwww.ncsoft.jp%2Flineage2classic%2F'
    iframe_selector = 'div._popup_box > div.iframe_container > iframe'
    server_num = 2#'2:アインハザード, 3:グランカイン'
    charctor_num = 3#'受け取るキャラクタ。上から(ｎ+1)番目'

    def setUp(self):
        # ----- launch visible
        #        self.driver = webdriver.Remote(
        #           command_executor= self.selenium_server,
        #            desired_capabilities=DesiredCapabilities.CHROME)
        # ----- launch background start
        opts = Options()
        # opts.binary_location = self.browser_path
        # opts.add_argument('--headless')
        opts.add_argument('--disable-gpu')
        opts.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=opts)
        # self.driver = webdriver.Chrome(executable_path="/c/Users/kazuh/bin/chromedriver", chrome_options=opts)

    def test_something(self):
        self.driver.get(self.base_url)
        self.do_login()
        self.mv_coupon_page()
        c = 0
        while True:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'table.article_list')))
                c = self.searchL2c()
                if c is not None:
                    css = '#content > table > tbody > tr:nth-child(%s) > td:nth-child(6) a' % c
                    self.driver.find_element_by_css_selector(css).click()
                    self.select_svr_and_chararactor()
                else:
                    href = None
                    href = self.driver.find_element_by_css_selector('div.paging_area > div.paging > a.pagenav.next').get_attribute('href')
                    self.driver.get(href)
                    c = None
                    continue
                c = None
            # except OSError as err:
            #     print("OS error: {0}".format(err))
            #     print('問題があったor全部網羅したかどちらか')
            except NoSuchElementException:
                print("No SuchElement.")
                print("done.")
                break
            except:
                print("done.")
                break

        self.assertEqual(True, True)

    def do_login(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnLogin')))
        self.driver.find_element_by_id('account').send_keys(self.login_account)
        self.driver.find_element_by_id('password').send_keys(self.login_password)
        element.click()

    def mv_coupon_page(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Setting')))
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul.lnb >  li[an="charge"]')))
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li[an="charge"] li[an="couponHistory"] > a')))
        element.click()

    def switch_iframe(self, iframe_selector):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, iframe_selector)))
        iframe = self.driver.find_element_by_css_selector(iframe_selector)
        self.driver = self.driver.switch_to.frame(iframe)

    def select_svr_and_chararactor(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.iframe_selector)))
        iframe = self.driver.find_element_by_css_selector(self.iframe_selector)
        self.driver.switch_to.frame(iframe)
        self.select_iframe_parts('fieldset > span:nth-child(1) > label > span > span')
        self.select_iframe_parts('body > div.selectbox > ul > li:nth-child(%s)' % self.server_num)
        self.select_iframe_parts('fieldset > span:nth-child(2) > label > span > span')
        self.select_iframe_parts('body > div.selectbox > ul > li:nth-child(%s)' % self.charctor_num)
        self.driver.find_element_by_css_selector('div.content.content_v2  div.popup_pos > div.btn_c > a:nth-child(1)').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('div.content.content_v2 > div > div.btn_c > a.btn_v2').click()
        time.sleep(1)
        self.driver.find_element_by_css_selector('div.content.content_v2 > div > div.btn_c > a.btn_v3').click()
        self.driver.switch_to.default_content()
        pass

    def select_iframe_parts(self, css_selector):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        time.sleep(1)
        element.click()

    def searchL2c(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        tbl = soup.find_all('table', class_='article_list')[0]
        rows = tbl.find_all('tr')
        ptn = re.compile(r'^\[L2C\]', re.IGNORECASE)
        c = 1
        for row in rows:
            line = row.find_all('td')
            if len(line) > 0:
                td_txt = line[2].p.text.strip()
                if ptn.match(td_txt) is not None:
                    return c
                c += 1

if __name__ == '__main__':
    unittest.main()
