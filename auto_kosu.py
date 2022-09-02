from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta

from config.settings import *

# デフォルトでは3日前の月工数管理. それ以外の月の工数管理をしたい場合はここを変更してください
# default: プログラム実行日9/4 -> 9月の工数管理, プログラム実行日9/3 -> 8月の工数管理
# MONTHは二文字のstrで入力: ex 8月 -> "08"
MONTH = None

if MONTH:
    if type(MONTH) == str and len(MONTH) == 2:
        str_month = MONTH
    else:
        raise ValueError('MONTH must be string and length is 2. ex:) "08"')
else:
    str_month = datetime.strftime(datetime.today() - timedelta(days=3), "%m")

print(f"running auto kosu... {str_month}月")

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://id.jobcan.jp/users/sign_in")
driver.find_element(By.XPATH, '//*[@id="new_user_google"]/a').click()
time.sleep(1)
element = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
element.send_keys(EMAIL)
element.send_keys(Keys.ENTER)
time.sleep(1)
element = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
element.send_keys(PASS)
element.send_keys(Keys.ENTER)

time.sleep(1)
ele = driver.find_element(
    By.XPATH, "/html/body/div[1]/header/nav/div/div[2]/ul/li[3]/a"
)
ele.click()

time.sleep(1)
driver.switch_to.window(driver.window_handles[1])
driver.close()
driver.switch_to.window(driver.window_handles[0])
time.sleep(0.5)
driver.get("https://ssl.jobcan.jp/employee/man-hour-manage")
time.sleep(1)
selector = driver.find_element(
    By.XPATH,
    "/html/body/div/div/div[2]/main/div/div[2]/div/h5/div/div/form/div/div[2]/select[2]",
)
Select(selector).select_by_visible_text(str_month)
elements = driver.find_elements(
    By.XPATH, '//*[@id="search-result"]/table/tbody/tr/td/div'
)

day_num = len(elements)
for i in range(day_num):
    try:
        driver.get("https://ssl.jobcan.jp/employee/man-hour-manage")
        time.sleep(0.4)
        selector = driver.find_element(
            By.XPATH,
            "/html/body/div/div/div[2]/main/div/div[2]/div/h5/div/div/form/div/div[2]/select[2]",
        )
        Select(selector).select_by_visible_text(str_month)
        elements = driver.find_elements(
            By.XPATH, '//*[@id="search-result"]/table/tbody/tr/td/div'
        )
        ele = elements[i]

        ele.click()
        time.sleep(0.5)
        # print(driver.page_source)
        modal = driver.find_element(By.XPATH, '//*[@id="man-hour-manage-modal"]')

        sel = modal.find_element(By.XPATH, '//*[@id="select-template"]/select')
        Select(sel).select_by_value("1")
        work_time = modal.find_element(
            By.XPATH, '//*[@id="man-hour-manage-modal"]'
        ).text.split("\n")[0][-5:]
        time.sleep(0.5)
        modal = driver.find_element(By.XPATH, '//*[@id="man-hour-manage-modal"]')
        input_form = modal.find_element(
            By.XPATH, '//*[@id="edit-menu-contents"]/table/tbody/tr[2]/td[4]/input[1]'
        )

        input_form.clear()
        # input_form.send_keys(Keys.CONTROL + "a")
        input_form.send_keys(work_time)

        time.sleep(0.2)
        modal = driver.find_element(By.XPATH, '//*[@id="man-hour-manage-modal"]')
        savebutton = modal.find_element(By.XPATH, '//*[@id="save"]')
        savebutton.click()
        time.sleep(0.2)
        try:
            savebutton.click()
        except:
            pass
        time.sleep(0.2)
    except:
        continue
