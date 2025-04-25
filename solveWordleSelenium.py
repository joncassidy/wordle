import json
import time
#import multiprocessing as mp
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# To Do:
# Check when a key can be pressed again (based on event listener on keys?) rather than waiting

ABSENT = 'a'
PRESENT = 'p'
CORRECT = 'c'

fullWordList = []
#pool = mp.Pool(mp.cpu_count())

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
        wait=WebDriverWait(self.driver,5)
        #self.driver.get("https://www.nytimes.com/dummyAddress")
        #self.driver.add_cookie({"name": "nyt-gdpr", "value": "0", "domain":".nytimes.com", "path":"/"})
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        assert "Wordle" in self.driver.title
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fides-accept-all-button")))
        self.driver.find_element(By.CLASS_NAME, "fides-accept-all-button").click()
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "purr-blocker-card__button")))
        self.driver.find_element(By.CLASS_NAME, "purr-blocker-card__button").click()
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='Play']")))
        self.driver.find_element(By.CSS_SELECTOR, "[data-testid='Play']").click()
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[aria-label='Close']")))
        self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Close']").click()
        time.sleep(1)
        #self.gameAppContents = self.driver.find_element(By.ID, "wordle-app-game")
        #self.keyboardContent = self.gameAppContents.find_element(By.TAG_NAME, "game-keyboard").shadow_root
        #gameModalContents = self.gameAppContents.find_element(By.TAG_NAME, "game-modal").shadow_root
        #gameIcon = gameModalContents.find_element(By.TAG_NAME, "game-icon")
        #gameIcon.click()

        time.sleep(1)
        self.driver.execute_script("console.log('here')")
#        gdprPopup = self.driver.find_element(By.CLASS_NAME, "pz-snackbar")
#        self.driver.execute_script("arguments[0].style.display = 'none';", gdprPopup)

        self.haveGuess("moist")
        self.haveGuess(getBestGuess(self.possibleWords))
        self.haveGuess(getBestGuess(self.possibleWords))
        self.haveGuess(getBestGuess(self.possibleWords))
        self.haveGuess(getBestGuess(self.possibleWords))
        self.haveGuess(getBestGuess(self.possibleWords))
        #self.haveGuess(random.choice(self.possibleWords))

    def haveGuess(self, word):
        #self.wait_for_element(tile % "5" + '::shadow [data-state*="e"]')
        self.currentRow+=1
        #for i in range(5):
        #    self.typeLetter(word[i])
        #self.typeLetter("\n")
        ActionChains(self.driver).send_keys(word).perform()
        ActionChains(self.driver).send_keys(Keys.RETURN).perform()
        time.sleep(2)
        self.currentWord = word
        self.currentWordStatus = self.getCurrentStatus()
        if (all([s==CORRECT for s in self.currentWordStatus])):
            print("Word is "+word)
            time.sleep(5)
            self.driver.close()
        else:
            self.guesses[word] = self.currentWordStatus
            self.updatePossibleWords()
        print(len(self.possibleWords), "words left")


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

    def getCurrentStatusOLD(self):
        themeManager = self.gameAppContents.find_element(By.TAG_NAME, "game-theme-manager")
        allRows = themeManager.find_elements(By.TAG_NAME, "game-row")
        thisRowRoot = allRows[self.currentRow].shadow_root
        thisRowTiles = thisRowRoot.find_elements(By.TAG_NAME, "game-tile")
        status = [tile.get_attribute("evaluation")[0] for tile in thisRowTiles]
        return status
    def getCurrentStatus(self):
        thisRow = self.driver.find_element(By.CSS_SELECTOR, f"[aria-label='Row {self.currentRow+1}']")
        status = [tile.get_attribute("data-state")[0] for tile in thisRow.find_elements(By.CSS_SELECTOR, "[class^='Tile-module_tile']") ]
        return status
    def test(self):
        self.currentWord = 'colon'
        self.currentWordStatus = [ABSENT, PRESENT, ABSENT, ABSENT, ABSENT]
        print(self.wordIsAllowed('plant'))

    def tryAllWords(self):
        possibleWords = self.possibleWords
        for targetWord in self.possibleWords:
            found = False
            currentGuess = "moist"
            i = 0
            while not(found):
                currentGuessStatus = checkWord(targetWord,currentGuess)
                if (all([s == CORRECT for s in currentGuessStatus])):
                    found = True
                    print(targetWord + " found in " + str(i) + " guesses")
                else:
                    remainingPossibleWords = [w for w in possibleWords if wordIsAllowed(w, currentGuess, currentGuessStatus)]
                currentGuess = getBestGuess(remainingPossibleWords)
                i+=1

def getBestGuess(possibleWords):
    minRemaining = (len(possibleWords)+1)**2
    bestNextGuess = ''
    for nextGuess in possibleWords:
        wordsRemaining = 0
        for actualAnswer in possibleWords:
            wordsRemaining += sum(map(lambda x : wordIsAllowed(x, nextGuess, checkWord(actualAnswer, nextGuess)), possibleWords))
            #wordsRemaining += sum([pool.apply(wordIsAllowed(x, nextGuess, checkWord(actualAnswer, nextGuess)) for x in possibleWords)])
            #pool.close()
        if wordsRemaining < minRemaining:
            minRemaining = wordsRemaining
            bestNextGuess = nextGuess
    return bestNextGuess

def checkWord(answer, guess):
    result = ['','','','','']
    for i in range(5):
#        print(guess, answer, i)
        if answer[i] == guess[i]:
            result[i] = CORRECT
            continue
        if guess[i] in answer:
            if guess.count(guess[i]) > 1:
                if guess.find(guess[i]) < i:
                    result[i] = ABSENT
                    continue
                else:
                    result[i] = PRESENT
                    continue
            else:
                result[i] = PRESENT
                continue
        result[i] = ABSENT
    return result

def wordIsAllowed(targetWord, guess, guessResult):
    for i in range(5):
        guessLetter = guess[i]
        guessLetterStatus = guessResult[i]
        if guessLetterStatus == CORRECT and targetWord[i] != guessLetter:
            return False
        if guessLetterStatus == ABSENT and guessLetter in targetWord:
            # need to check if the letter is also elsewhere in the guess and present or correct
            if guess.count(guessLetter) > 1:
                letterPositions = [i for i, letter in enumerate(guess) if letter == guessLetter]
                letterResults = [guessResult[i] for i in letterPositions]
                if (letterResults.count(CORRECT) + letterResults.count(PRESENT)) > 0:
                    pass
                else:
                    return False
            else:
                 return False
        if guessLetterStatus == PRESENT and not(guessLetter in targetWord):
            return False
        if guessLetterStatus == PRESENT and targetWord[i] == guessLetter:
            return False
    return True

if __name__ == '__main__':
    getFullWordList()
    wordle = WordleController()
    #wordle.tryAllWords()
    wordle.runBrowser()
