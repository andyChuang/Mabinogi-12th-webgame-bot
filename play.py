# coding=UTF-8
import os, argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import utils

MABINOGI_URL = "https://tw.event.beanfun.com/mabinogi/e20170511/index.aspx"

def main(game_type):
    driver_path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
    users = utils.load_account("account.json")

    for user in users:
        driver = get_driver(driver_path)
        start_new_session(driver, user, game_type)
        stop_session(driver)

def start_new_session(driver, user, game_type):
    driver.get(MABINOGI_URL)
    game.get(game_type, login)(driver, user)

def stop_session(driver):
    driver.close()

def get_driver(driver_path):
    driver = webdriver.Chrome(driver_path)
    return driver

def login(driver, user):
    # Use dice game as login entry page
    dice_entry = driver.execute_script("return $('a[href=\"Dice.aspx\"]')[0]")
    dice_entry.click()
    login_routine(driver, user)
    time.sleep(3)

def login_routine(driver, user):
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
        login_routine(driver, user)

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
        print "User %s game over." % user["account"]

def redeem_all_luckyeggs(driver, user):
    ferris_wheel = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "gacha_ferriswheel"))
    )
    ferris_wheel.click()

    try:
        login_routine(driver, user)

        redeem_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href='LuckyEgg_Exchange.aspx']"))
        )
        driver.execute_script("arguments[0].click()", redeem_btn)

        while(True):
            redeem_first_luckyegg(driver)
    except Exception as e:
        print "It seems there's no luckyegg of this user. Go next."


def redeem_first_luckyegg(driver):
        luckyegg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(\
                (By.ID, "ItemListRepeater_ctl00_DoExchange"))
        )
        driver.execute_script("arguments[0].click()", luckyegg)

        submit_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@id='btnExchange']"))
        )
        driver.execute_script("arguments[0].click()", submit_btn)
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        redeem_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btnExchange")))
        driver.execute_script("arguments[0].click()", redeem_btn)

def i_have_coin_haha(driver):
    coin_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "coin"))
    )
    coin = coin_field.text.encode('utf-8').split("剩餘代幣：")[1]
    return int(coin) > 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compile smart contracts')

    parser.add_argument('--game_type', \
                        help='Its value is one of %s and %s' % ('login', 'dice'),
                        default='login')

    args = parser.parse_args()

    game = {
        "login": login,
        "dice": dice_game,
        "redeem": redeem_all_luckyeggs
    }

    main(args.game_type)