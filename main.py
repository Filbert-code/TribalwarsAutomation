import json
import os
from datetime import datetime, timedelta
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import json
import time

endpoint = 'https://en138.tribalwars.net/game.php?'
quicklink_loot_assistant_href = '/game.php?village=20145&screen=am_farm'


def load_cookies(driver):
    with open('cookie.txt', 'r') as f:
        key_value_list = f.read().split('; ')
    cookies = {k: v for k, v in [kv.split('=') for kv in key_value_list]}
    for k, v in cookies.items():
         print(k, v)
    for k, v in cookies.items():
        driver.add_cookie({'name': k, 'value': v})


def run_bot():
    # chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    tribalwars_base_url = 'https://www.tribalwars.net/en-dk/'

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    driver.get(tribalwars_base_url)
    load_cookies(driver)
    print('Cookies loaded')

    driver.get(endpoint)

    # click the world button for world 131
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'world_button_active'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Loot Assistant'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'LA Enhancer'))).click()
    #
    # # LA Enhancer settings configuration
    # # ----------------------------------
    # # hide wall lvl
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'enable_walls'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'wall_value'))).send_keys('0')
    # # hide reports if partial losses or full losses
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'yellow'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'red_yellow'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'red'))).click()
    # # villages plundered in the last _ minutes
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'enable_time'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'time_value'))).send_keys('40')
    # # villages sent to in the last _ minutes
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'hide_recent_farms'))).click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'hide_recent_time'))).send_keys('40')
    # # change upper limit of load pages
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'end_page'))).send_keys('10')
    #
    # # get number of lc
    # lc_count = int(driver.find_element(By.CLASS_NAME, 'unit-item-light').text)
    # print('LC count: ', lc_count)
    # # get number of scouts
    # scout_count = int(driver.find_element(By.CLASS_NAME, 'unit-item-spy').text)
    # print('Scouts count: ', scout_count)
    #
    # sleep(2)
    # # click the apply button
    # submit_button = driver.find_element(By.CSS_SELECTOR, "input[value='Apply']")
    # submit_button.click()
    #
    # sleep(2)
    #
    # # send out LC and scouts
    # for _ in range(lc_count // 3):
    #     if scout_count <= 0:
    #         break
    #     sleep(0.4)
    #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'body'))).send_keys('a')
    #     scout_count -= 1
    #     lc_count -= 3
    #
    # # send out the remaining calvary
    # for _ in range(lc_count // 3):
    #     sleep(0.4)
    #     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'body'))).send_keys('b')

    sleep(2)

    driver.close()


def bot_loop():
    should_run_first_time = input('Run bot for the first iteration? (y/n): ')
    start_time = datetime.now()
    last_execution_time = datetime.now()
    while True:
        if should_run_first_time.lower() != 'n':
            try:
                run_bot()
            except Exception as e:
                print('Bot failed with exception: ', e)
        else:
            should_run_first_time = 'y'
        next_execution_time = last_execution_time + timedelta(minutes=45)
        # print the next execution time in hh:mm:ss format
        print('\nNext execution time: ', next_execution_time.strftime('%H:%M:%S'))
        print('Time since start: ', (datetime.now() - start_time))
        print('------------------------\n')

        # sleep for 45 minutes
        time.sleep(45 * 60)
        last_execution_time = datetime.now()

        # if it's been 8 hours, ask for the new cookie
        if datetime.now() - start_time > timedelta(hours=8):
            print('Time has reached 8 hours, terminating bot')
            get_new_cookie = input('Input new Cookie: ')
            # delete the old cookie file
            os.remove('cookie.txt')
            with open('cookie.txt', 'w') as f:
                f.write(get_new_cookie)


if __name__ == '__main__':
    bot_loop()
