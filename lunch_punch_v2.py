from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import service
import time
import getpass
import datetime
import sys

# Initiate WebDriver in headless mode
# NOTE: Make sure the webdriver is in the same path as the file!


options = Options()
options.headless = True
options.EnableVerboseLogging = False
try:
    driver = webdriver.Chrome(options=options)
except:
    print('Chrome not 108....')
    try:
        driver = webdriver.Chrome(options=options)
    except:
        print('Chrome not 109....')
        driver = webdriver.Chrome(options=options)

USERNAME = input("Username: ")
PASS = getpass.getpass()


def login(driver):
    # Login using username and password (ASSUMES NO AUTHENTICATION)
    driver.get('https://portalapps.insperity.com/QuickPunch/')
    print("Logging in...")
    input_elements = driver.find_elements(By.TAG_NAME, 'input')
    user_input = (f for f in input_elements if f.accessible_name == 'Username')
    pass_input = (f for f in input_elements if f.accessible_name == 'Password')
    submit_input = (f for f in input_elements if f.accessible_name == 'Log In')

    next(user_input).send_keys(USERNAME)
    next(pass_input).send_keys(PASS)
    next(submit_input).click()
    time.sleep(2)
    if driver.title == 'Quick Punch':
        print('Logged in successfully')
        return True
    else:
        print('WRONG CREDENTIALS')
        return False


def logout():
    print('Logging out...')
    driver.find_element(By.LINK_TEXT, 'Log Out').click()


def clock(driver, button_name):
    # Clock in or out depending passed button option and log out
    clocking_buttons = driver.find_elements(By.TAG_NAME, 'button')
    print("Clocking operation...")
    for button in clocking_buttons:
        if button.accessible_name == button_name:
            # CONTROL: UNCOMMENT TO MAKE PROGRAM PUNCH
            button.click()
            print('Clock operation successful')
    time.sleep(3)
    logout()


def sleepUntil(hour, minute):
    print(f'waiting until {hour}:{minute}...')
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, hour, minute)
    if t.timestamp() > future.timestamp():
        print("That time already passed")
        sys.exit()
    time.sleep((future - t).total_seconds())


def main():
    try:
        # Clock out for lunch (should already be logged in)
        time.sleep(3)
        clock(driver, "OUT FOR LUNCH")
        if driver.title != 'Quick Punch':
            print("Log Out successful")

        # Wait 30 mins
        print("Waiting 30 minutes to clock in...")
        for i in range(3):
            time.sleep(600)
            print('10 minutes passed...')
        print('Full 30 minutes passed, clocking back in.')

        # Login and clock back in
        login(driver)
        time.sleep(3)
        clock(driver, "IN FROM LUNCH")
        if driver.title != 'Quick Punch':
            print("Log Out successful")

        # Close driver
        driver.close()

    except:
        print("Something Went Wrong with either the website or your login")


if __name__ == '__main__':
    # Get user time and wait until then to execute script
    custom_time = input("Leave blank to clock out now\nTime to clock out[hh:mm 24 hour]: ")

    # Try credentials to check validation before waiting
    try:
        if custom_time.replace(" ", '') != '' or custom_time.find(':') == 2:
            print('Checking Credentials...')
            login(driver)
            logout()
            sleepUntil(int(custom_time[:2]), int(custom_time[3:]))
            print("Time reached")
        if login(driver):
            main()
    except:
        print("ERROR something went wrong")

    # Close script out after 10 seconds
    print("DONE\nClosing in 10 seconds...")
    time.sleep(10)
    sys.exit()