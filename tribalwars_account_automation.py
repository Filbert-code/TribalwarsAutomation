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


QUICKLINK_LOOT_ASSISTANT_HREF = '/game.php?village=20145&screen=am_farm'


class TribalwarsAccountAutomation:
    def __init__(self):
        self.endpoint = 'https://en138.tribalwars.net/game.php?'
        self.tribalwars_base_url = 'https://www.tribalwars.net/'
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def bot_loop(self):
        should_run_first_time = input('Run bot for the first iteration? (y/n): ')
        start_time = datetime.now()
        last_execution_time = datetime.now()
        while True:
            if should_run_first_time.lower() != 'n':
                try:
                    self.run_bot()
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

    def run_bot(self):
        self.driver.get(self.tribalwars_base_url)
        self.load_cookies()
        print('Cookies loaded')

        self.driver.get(self.endpoint)

        queue_new_buildings()
        queue_new_units()
        make_market_transactions()
        send_out_units_for_looting()


        # click the world button for world 138
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'world_button_active'))).click()
        # TODO: add new building to the headquarters queue

    def load_cookies(self):
        with open('cookie.txt', 'r') as f:
            key_value_list = f.read().split('; ')
        cookies = {k: v for k, v in [kv.split('=') for kv in key_value_list]}
        for k, v in cookies.items():
            print(k, v)
        for k, v in cookies.items():
            self.driver.add_cookie({'name': k, 'value': v})
                    
    def la_enhancer_stuff(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Loot Assistant'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, 'LA Enhancer'))).click()

        # LA Enhancer settings configuration
        # ----------------------------------
        # hide wall lvl
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'enable_walls'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'wall_value'))).send_keys('0')
        # hide reports if partial losses or full losses
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'yellow'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'red_yellow'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'red'))).click()
        # villages plundered in the last _ minutes
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'enable_time'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'time_value'))).send_keys('40')
        # villages sent to in the last _ minutes
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'hide_recent_farms'))).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'hide_recent_time'))).send_keys('40')
        # change upper limit of load pages
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'end_page'))).send_keys('10')

        # get number of lc
        lc_count = int(self.driver.find_element(By.CLASS_NAME, 'unit-item-light').text)
        print('LC count: ', lc_count)
        # get number of scouts
        scout_count = int(self.driver.find_element(By.CLASS_NAME, 'unit-item-spy').text)
        print('Scouts count: ', scout_count)

        sleep(2)
        # click the apply button
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[value='Apply']")
        submit_button.click()

        sleep(2)

        # send out LC and scouts
        for _ in range(lc_count // 3):
            if scout_count <= 0:
                break
            sleep(0.4)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'body'))).send_keys('a')
            scout_count -= 1
            lc_count -= 3

        # send out the remaining calvary
        for _ in range(lc_count // 3):
            sleep(0.4)
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'body'))).send_keys('b')


if __name__ == '__main__':
    bot = TribalwarsAccountAutomation()
    bot.bot_loop()
