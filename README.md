# Worldle Solver

A tool to automatically run Wordle. It automates the browser, simulating the clicks and looking a the results. It requires python and selenium (so not trivial to use).


## Method

It's much better than random, but not fully optimal. The method of guessing is:

 - Guess an initial word (happens to be an answer from a while ago I generally use)
 - Check the result, and remove all non-matching words from the remaining possible words list
 - To find the 'best' next guess
-- Consider each next guessed word
-- Try each combination of a word to guess next, and what the actual answer might be
 -- For each guess, find the average number of words left across all possible answers (strictly uses the total rather than the average)
 -- Use the word with the lowest average, ie the word which on average will leave the fewest remaining words after that guess
 
The strategy above assume the harder mode, where only guesses matching previous results are allowed, and targets best average results rather than avoiding bad results.

## Improvements
 - At the moment, there is a wait for Wordle to update the results. I should change this to seeing that the last tile has turned (or the keyboard event listener is back on)
 - It's inefficient. Not so bad as there are a limited number of words, but I think the strategy is probably O(n<sup>3</sup>), with n=remaining words (combination of next word, actual word and each still allowed). I'm wondering about pre-computing a 'score' for combinations which might do better than O(n<sup>2</sup>)
 - I've assumed all words left are equally hard to distinguish. This isn't true, so a better information based strategy would do better (like the Wordle bot uses)
 - Set a cookie before starting to supress the GDPR cookies, as that is a bti messy at the moment to close them

## Technology
- I wanted to make it easier to run, but the site seems fairly solid on preventing cross site, and so I couldn't think of a way to do it just in a browser. But I didn't want to retype all of the answers into something else. Hence Python (because it's easier) and selenium.
- The Wordle site is a little bit painful with lots of shadow-root stuff. It's GDPR popups are also a bit of a hack to deal with.
- I'm thinking about an approach of pre-calculating the expected result for each combination of guess and actual word. (I think a result can fit in a byte as 3^5 < 2^8). So that might be an index for each possible result of about 5 million entries. Checking a guess/word combination is then a lookup plas a 1 byte compare. 
