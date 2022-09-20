[TOC]

# data cleaning

to deal with errant punctuation, inconsistent capitalizations, line breaks, misspellings and etc.

## cleaning in code

in linguistics, n-gram refers to a sequence of n words used in text and speech. when doing natural language analysis, it can often be handy to break up a piece of text by looking for commonly used n-grams, or recurring set of words that are often used together.

```python
# a comprehensive n-gram without nltk

def cleanedSentence(sentence):
    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation + string.whitespace) for word in sentence]
    sentence = [word for wordd in sentence if len(word) > 1 or (word.lower() == 'a' or word.lower() == 'i')]
    return sentence

def cleanInput(content):
    content = re.sub('\n|[[\d+\]]', ' ', content)
    content = bytes(content, 'utf-8')
    content = content.decode('ascii', 'ignore')
    sentences = content.split('. ')
    return [cleanedSentence(sentence) for sentence in sentences]

def getNGramsFromSentence(content, n):
    output = []
    for i in range(len(content) - n + 1):
        output.append(content[i: i + n])
    return output

def getNGrams(content, n):
    content = cleanedSentence(content)
    ngrams = []
    for sentence in content:
        ngrams.extend(getNGramsFromSentence(sentence, n))
    return ngrams
```

note: *string.whitespace includes tabs, line breaks and nonbreaking spaces*

## data normalization

a process of ensuring strings are linguistically or logically equivalent to each other, ie 111-123-1234 is equivalent to 111.123.1234 for us phone number.

another issue with the ngram code block above is that it doesn't handle repeated n-grams nicely, ie save a record of frequency or only store unique n-grams. we can utilize python build in library collection to do this. the disadvantage of this approach is it can't store mutable objects / unhashable objects thus we need to join the list back to strings. another approach is to use dict / json to handle, however it requires more management.

````python
from collection import Counter

def getNGrams(content, n):
    content = content.lower() # to prevent repeated ngrams with different casing
    content = cleanedSentence(content)
    ngrams = Counter()
    for sentence in content:
        newNGrams = [' '.join(ngram) for ngram in getNGramsFromSentence(sentence, n)]
        ngrams.update(newNGrams)
    return ngrams
````

there is a lot to put to thought when we are doing data normalization, especially to consider how much processing power and time is reasonable. for example we could standardize 1st, 2nd to first, second but this adds to additional resources. writing a script for a new corpus is difficult as we might not know what to expect and usually its impossible to read the corpus entirely. tool that may help: openrefine. it can help to do filtering, cleaning and etc.