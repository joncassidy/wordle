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
    row1 = rows[0]
    tile = rows[0].shadow_root.findElement(By.CLASS_NAME, "tile")
    tile.clear()
    tile.send_keys("r")
    tile.send_keys(Keys.TAB)
    assert "No results found." not in driver.page_source
    driver.close()

if __name__ == '__main__':
    getFullWordList()
    runBrowser()