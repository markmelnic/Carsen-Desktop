
from selenium import webdriver
import selenium.webdriver.chrome.options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random
import time


#GENERIC_URL = 'https://www.mobile.de/'
GENERIC_URL = 'https://suchen.mobile.de/fahrzeuge/search.html?vc=Car&dam=0&lang=en'


# ================== driver procedures ===================
# ================== driver boot procedure
def boot():
    # manage notifications
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)

    # driver itself
    dv = webdriver.Chrome(chrome_options = chrome_options, executable_path = r"./drivers/chromedriver80.exe")
    return dv


# ================== kill the driver
def killd(dv):
    dv.quit()

# ================== first dv.get
def startSearcher(dv):
    dv.get(GENERIC_URL)


# ================== website processes ===================
def firstSearch(dv, carMake, carModel):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    # ================== accept cookies
    time.sleep(3)
    try:
        cookiesAccept = dv.find_element_by_id("gdpr-consent-accept-button")
        cookiesAccept.click()
    except:
        try:
            cookiesAccept = dv.find_element_by_css_selector(".consent-btn.orange")
            cookiesAccept.click()
        except:
            None

    # ================== selectors
    # select any
    time.sleep(1)
    any = "any"
    makeSelector = dv.find_element_by_id("selectMake1-ds")
    for i in range(len(any)):
        makeSelector.send_keys(any[i])
    time.sleep(0.2)
    makeSelector.send_keys(Keys.ENTER)
    # manufacturer selector
    time.sleep(0.5)
    makeSelector = dv.find_element_by_id("selectMake1-ds")
    for i in range(len(carMake)):
        makeSelector.send_keys(carMake[i])
    time.sleep(0.2)
    makeSelector.send_keys(Keys.ENTER)

    '''
    # select any
    makeSelector = dv.find_element_by_id("selectModel1-ds")
    for i in range(len(any)):
        makeSelector.send_keys(any[i])
    time.sleep(0.2)
    '''
    # model selector
    time.sleep(0.7)
    modelSelector = dv.find_element_by_id("selectModel1-ds")
    for i in range(len(carModel)):
        modelSelector.send_keys(carModel[i])
    time.sleep(0.2)
    modelSelector.send_keys(Keys.ENTER)

    # price range selector
    # WIP

    # registration years range selector
    # WIP

    # kilometer range selector
    # WIP

    # power range selector
    # WIP

    # cubic capacity selector (in cm^3)
    # WIP

    # click search button
    time.sleep(0.1)
    searchButton = dv.find_element_by_id("dsp-upper-search-btn")
    searchButton.click()


# ================== see current URL
def curURL(dv):
    WebDriverWait(dv, 20).until(EC.visibility_of_all_elements_located)
    time.sleep(1)
    currentURL = dv.current_url
    return currentURL


# ================== navigate to next page
def nextPage(dv, currentURL, currentPage):
    tempLink = []
    
    if currentPage + 1 == 1:
        nextLink = currentURL
        nextLink += "&pageNumber=2"
    else:
        i = 0
        while i < len(currentURL):
            i = currentURL.find("pageNumber=", i)
            if i == -1:
                break
            tempLink.append(i + len("pageNumber="))
            i += len("pageNumber=")
            i = currentURL.find("&", i)
            tempLink.append(i)

        nextLink = ''
        for i in range(tempLink[0]):
            nextLink += currentURL[i]

        nextLink += str(currentPage + 2)

        for i in range(len(currentURL) - i - tempLink[0] - len(str(currentPage + 2))):
            nextLink += currentURL[i + tempLink[0] + len(str(currentPage + 2))]

    return nextLink