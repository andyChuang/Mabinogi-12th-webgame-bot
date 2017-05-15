# coding=UTF-8
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import utils

def main():
    driver_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
    print driver_path
    driver = webdriver.Chrome(driver_path)
    driver.get("https://tw.event.beanfun.com/mabinogi/e20170511/index.aspx")
    print driver.title
    user = utils.load_account("account.json")

    dice_game(driver, user)

def login(driver, user):
    # Login elements is in iframe, should switch to it
    login_iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ifmForm1"))
    )
    driver.switch_to_frame(login_iframe)
    login_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn_login"))
    )
    account = driver.find_element_by_id("t_AccountID")
    account.send_keys(user["account"])
    password = driver.find_element_by_id("t_Password")
    password.send_keys(user["password"])
    login_btn.click()

    # Choose game account
    game_account_selector = driver.find_element_by_id("ddl_service_account")
    for option in game_account_selector.find_elements_by_tag_name('option'):
        if option.text == user["game_account"]:
            option.click()
            driver.find_element_by_id("btn_send_service_account").click()
            break

def dice_game(driver, user):
    # Find dice game
    dice_entry = driver.execute_script("return $('a[href=\"Dice.aspx\"]')[0]")
    dice_entry.click()

    # If not logon
    try:
        login(driver, user)

        while i_have_coin_haha(driver):
            # Start to dice
            go_dice = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "btnGoDice"))
            )
            time.sleep(random.randint(2, 5))
            driver.execute_script("arguments[0].click()", go_dice)
            # Continue game
            continue_game = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='btn_B']/input[@id='btnGoDice']"))
            )
            time.sleep(random.randint(2, 5))
            driver.execute_script("arguments[0].click()", continue_game)
        print "No coin."

    finally:
        print "Game over."

def i_have_coin_haha(driver):
    coin_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "coin"))
    )
    coin = coin_field.text.encode('utf-8').split("剩餘代幣：")[1]
    return int(coin) > 0

if __name__ == '__main__':
    main()