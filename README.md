# Worldle Solver

A tool to automatically run Wordle. It automates the browser, simulating the clicks and looking a the results. It requires python and selenium (so not trivial to use).


## Method

It's better than random, but not the most optimal. The method of guessing is:

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
 - I assume all words left are equally hard to distinguish. This isn't true, so a better information based strategy would do better (like the Wordle bot uses)