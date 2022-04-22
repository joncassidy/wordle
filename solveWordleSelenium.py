import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# To Do:
# Check when a key can be pressed again (based on event listener on keys?) rather than waiting
# Work out best next word based on number then left

fullWordList = []

def getFullWordList():
    global fullWordList
    f = open("wordle_words.json")
    fullWordList = json.load(f)

class WordleController:
    def __init__(self):
        self.currentRow = -1
        self.guesses = {}
        self.possibleWords = fullWordList

    def runBrowser(self):
        self.driver = webdriver.Chrome()
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
        self.haveGuess(self.getBestGuess())
        self.haveGuess(self.getBestGuess())
        self.haveGuess(self.getBestGuess())
        self.haveGuess(self.getBestGuess())
        self.haveGuess(self.getBestGuess())
        #self.haveGuess(random.choice(self.possibleWords))

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
            time.sleep(5)
            self.driver.close()
        else:
            self.guesses[word] = self.currentWordStatus
            self.updatePossibleWords()
        print(len(self.possibleWords), "words left")

    def getBestGuess(self):
        minRemaining = (len(self.possibleWords))**2
        bestNextGuess = ''
        for nextGuess in self.possibleWords:
            wordsRemaining = 0
            for actualAnswer in self.possibleWords:
#            remainingPossibleWords = [w for w in self.possibleWords if wordIsAllowed(w, self.currentWord, self.currentWordStatus)]
                wordsRemaining += sum(map(lambda x : wordIsAllowed(x, nextGuess, checkWord(actualAnswer, nextGuess)), self.possibleWords))
            if wordsRemaining < minRemaining:
                minRemaining = wordsRemaining
                bestNextGuess = nextGuess
        print("Best guess", bestNextGuess)
        return bestNextGuess

    def updatePossibleWords(self):
        remainingPossibleWords = [w for w in self.possibleWords if wordIsAllowed(w, self.currentWord, self.currentWordStatus)]
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

    def test(self):
        self.currentWord = 'colon'
        self.currentWordStatus = ['absent', 'present','absent', 'absent', 'absent']
        print(self.wordIsAllowed('oxide'))

def checkWord(answer, guess):
    result = ['','','','','']
    for i in range(5):
        if answer[i] == guess[i]:
            result[i] = 'correct'
            continue
        if guess[i] in answer[i]:
            if guess.count(i) > 1:
                if guess.find(guess[i]) < i:
                    result[i] = 'absent'
                    continue
            else:
                result[i] = 'present'
                continue
        result[i] = 'absent'
    return result

def wordIsAllowed(targetWord, guess, guessResult):
    for i in range(5):
        guessLetter = guess[i]
        guessLetterStatus = guessResult[i]
        if guessLetterStatus == "correct" and targetWord[i] != guessLetter:
            return False
        if guessLetterStatus == "absent" and guessLetter in targetWord:
            # need to check if the letter is also elsewhere in the guess and present or correct
            if guess.count(guessLetter) > 1:
                letterPositions = [i for i, letter in enumerate(guess) if letter == guessLetter]
                letterResults = [guessResult[i] for i in letterPositions]
                if (letterResults.count("correct") + letterResults.count("present")) > 0:
                    pass
                else:
                    return False
            else:
                 return False
        if guessLetterStatus == "present" and not(guessLetter in targetWord):
            return False
        if guessLetterStatus == "present" and targetWord[i] == guessLetter:
            return False
    return True

if __name__ == '__main__':
    getFullWordList()
    wordle = WordleController()
    wordle.runBrowser()
