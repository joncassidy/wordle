import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# To Do:
# Check when a key can be pressed again (based on event listener on keys?

fullWordList = []

def getFullWordList():
    global fullWordList
    f = open("wordle_words.json")
    fullWordList = json.load(f)

class WordleController:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.currentRow = -1
        self.guesses = {}
        self.possibleWords = fullWordList

    def runBrowser(self):
        #self.driver.get("https://www.nytimes.com/dummyAddress")
        #self.driver.add_cookie({"name": "nyt-gdpr", "value": "0", "domain":".nytimes.com", "path":"/"})
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        assert "Wordle" in self.driver.title
        self.driver.find_element(By.ID, "pz-gdpr-btn-accept").click()

        self.gameAppContents = self.driver.find_element(By.TAG_NAME, "game-app").shadow_root
        self.keyboardContent = self.gameAppContents.find_element(By.TAG_NAME, "game-keyboard").shadow_root
        gameModalContents = self.gameAppContents.find_element(By.TAG_NAME, "game-modal").shadow_root
        gameIcon = gameModalContents.find_element(By.TAG_NAME, "game-icon")
        gameIcon.click()

        time.sleep(1)
        self.driver.execute_script("console.log('here')")
        gdprPopup = self.driver.find_element(By.CLASS_NAME, "pz-snackbar")
        self.driver.execute_script("arguments[0].style.display = 'none';", gdprPopup)

        self.haveGuess("moist")
        self.haveGuess(random.choice(self.possibleWords))
        self.haveGuess(random.choice(self.possibleWords))
        self.haveGuess(random.choice(self.possibleWords))
        self.haveGuess(random.choice(self.possibleWords))

    def haveGuess(self, word):
        #self.wait_for_element(tile % "5" + '::shadow [data-state*="e"]')
        self.currentRow+=1
        for i in range(5):
            self.typeLetter(word[i])
        self.typeLetter("\n")
        time.sleep(2)
        self.currentWord = word
        self.currentWordStatus = self.getCurrentStatus()
        if (all([s=='correct' for s in self.currentWordStatus])):
            print("Word is "+word)
            time.sleep(10)
            self.driver.close()
        else:
            self.guesses[word] = self.currentWordStatus
            self.updatePossibleWords()

    def wordIsAllowed(self, word):
        for i in range(5):
            guessLetter = self.currentWord[i]
            guessLetterStatus = self.currentWordStatus[i]
            if guessLetterStatus == "correct" and word[i] != guessLetter:
                return False
            if guessLetterStatus == "absent" and guessLetter in word:
                return False
            if guessLetterStatus == "present" and not(guessLetter in word):
                return False
        return True

    def updatePossibleWords(self):
        remainingPossibleWords = [w for w in self.possibleWords if self.wordIsAllowed(w)]
        self.possibleWords = remainingPossibleWords

    def typeLetter(self, letter):
        buttonName = 'button[data-key="%s"]' % letter
        if (letter == '\n'):
            button = self.keyboardContent.find_element(By.CLASS_NAME, 'one-and-a-half')
        else:
            button = self.keyboardContent.find_element(By.CSS_SELECTOR, buttonName)
        button.click()

    def getCurrentStatus(self):
        themeManager = self.gameAppContents.find_element(By.TAG_NAME, "game-theme-manager")
        allRows = themeManager.find_elements(By.TAG_NAME, "game-row")
        thisRowRoot = allRows[self.currentRow].shadow_root
        thisRowTiles = thisRowRoot.find_elements(By.TAG_NAME, "game-tile")
        status = [tile.get_attribute("evaluation") for tile in thisRowTiles]
        return status

if __name__ == '__main__':
    getFullWordList()
    wordle = WordleController()
    wordle.runBrowser()