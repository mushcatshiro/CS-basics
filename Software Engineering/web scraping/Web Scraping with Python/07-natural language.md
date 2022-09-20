[TOC]

# Reading and Writing in Natural Language

text analysis has more impact than one can imagine in search engine, where the principal behind it is just statistics. some great example includes google images search and shazam music search. upon obtaining n-grams from previous chapter, what can we work with it? at a basic level, we can obtain common word pattern, or common phrases. furthermore, it can be used to create natural sounding data summaries by going back to the original text and extracting sentences around some of the popular phrases.

by using the n-gram code we have from previous chapter, with an addition of the following filtering

````python
def isCommon(ngram):
    commonWords = ['the', ...]
    for word in ngram:
        if word in commonWords:
            return True
    return False
````

note: *common words is time sensitive, common words in 18th century might be different from those in 21th century, thus using front common words is a safer bet*

and parsing through one of the US president speech, we can extract the key topics from the speech. next we would like to write a text summary, but how? the easiest approach would be using the top 5 common 2-grams and find the first sentence with the 2-grams, this can form a passable text summary of the speech. to obtain better result we can consider 3-grams or even 4-grams depending on the corpus. another approach would be looking for sentences that contain the most popular n-grams or highest percentage of popular n-grams, depending on the corpus it may favor longer sentences, in this case we must form a custom scoring metric.

## markov models

markov text generators is implemented by analyzing large set of random events, where one discrete event is followed by another discrete event with a certain probability

````mermaid
graph TD
sunny -- 20% --> cloudy
cloudy -- 15% --> sunny
sunny -- 70% --> sunny
cloudy -- 70% --> cloudy
cloudy -- 15% --> rainy
rainy -- 25% --> cloudy
rainy -- 50% --> rainy
rainy -- 25% --> sunny
sunny -- 10% --> rainy
````

a theoretical weather system

properties of a markov model:

- all percentages leading away from any node must add up to 100% => it will always lead to somewhere else in the next step
- there is only 3 possibilities for the weather at a given time, but we can generate infinite list of weather states
- only the current state can influence what's the next state
- it might be more difficult to reach some node than others

some application including google page ranking system is partially based on MC model.

### text generation with markov models

````python
def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def	retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

def buildWordDict(text):
    text = text.replace('\n', ' ')
    text = text.replace('"', '')
    
    punctuation = [',', '.', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, f' {symbol} ')
    words = text.split(' ')
    words = [word for word in words if word != '']
    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[word[i-1]]:
            wordDict[words[i-1][words[i]]] = 0
        wordDict[words[i-1]words[i]] += 1
    return wordDict

text = str(urlopen('url').read(), 'utf-8')
wordDict = buildWordDict(text)
length = 100
chain = ['I']
for i in range(0, length):
    newWord = retrieveRandomWord(wordDict[chain[-1]])
    chain.append(newWord)
````

basically given a starting word it will propagates down until the given length. markov model tend to perform well if the corpus given has similar writing style. we can also generate / predict the text with higher n-grams.

although its interesting application of MC however its not the practical use of MC, instead it should help the crawler think, which its greatest usage being PageRank algorithm - by crawling huge amount of pages, upon analyzing rank the most relevant page for the user.

## conclusion of six degree of wikipedia

most of the cs problems are directed graphs, we incline to solve football __ (player) single direction problem than water <=> H2O kind of problem. using breadth first search is a good option for this wikipedia example. we need to know there exists both DAG and UAG problem in scrapping (to get out from infinite loop).

## NLTK

- statistical analysis (most frequent, bigrams)

````python
from nltk import Text, word_tokenize

# we always start with Text object
tokens = word_tokenize('a quick brown fox jump over the fence')
text = Text(tokens)
````

- lexicographical analysis (homonyms, we could feedback to NLTK and train it to improve tagging?)