import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

fullWordList = []
def getFullWordList():
    global fullWordList
    f = open("wordle_words.json")
    fullWordList = json.load(f)

def runBrowser():
    driver = webdriver.Chrome()
    print(driver.service.process.pid)
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    assert "Wordle" in driver.title
    driver.find_element(By.ID, "pz-gdpr-btn-accept").click()

    gameAppContents = driver.find_element(By.TAG_NAME, "game-app").shadow_root
    gameModalContents = gameAppContents.find_element(By.TAG_NAME, "game-modal").shadow_root
    gameIcon = gameModalContents.find_element(By.TAG_NAME, "game-icon")
    gameIcon.click()
    wholeBoard = gameAppContents.find_element(By.ID, "board")
    rows = wholeBoard.find_elements(By.TAG_NAME, "game-row")
    row1 = rows[0].shadow_root
    typeLetter(gameAppContents, "c")
    typeLetter(gameAppContents, "r")
    typeLetter(gameAppContents, "a")
    typeLetter(gameAppContents, "n")
    typeLetter(gameAppContents, "e")
    time.sleep(2)
    #assert "No results found." not in driver.page_source
    driver.close()

def typeLetter(gameAppContents, letter):
    keyboardContent = gameAppContents.find_element(By.TAG_NAME, "game-keyboard").shadow_root
    buttonName = 'button[data-key="%s"]' % letter
    buttonA = keyboardContent.find_element(By.CSS_SELECTOR, buttonName)
    buttonA.click()

if __name__ == '__main__':
    getFullWordList()
    runBrowser()