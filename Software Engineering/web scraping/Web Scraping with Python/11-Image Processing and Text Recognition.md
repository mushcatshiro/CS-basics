[TOC]

# Image Processing and Text Recognition 

CAPTCHAs.

image to texts with OCRs libraries, mainly focuses on Pillow and Tesseract. using Pillow to make image more machine readable and use Tesseract to recognize the image.

## processing Well-Formatted Text

a well formatted text should be written in one standard font (excluding handwriting, cursive or decorative ones), has crisp lines, well aligned without slanted letters and without cut-offs. this is a loose definition but it gives us a general idea. these text can be handled easily.

some preprocessing includes trimming pixels that are lower than certain thresholds to bring more contrast

```python
import pytesseract as pt
from pytesseract import Output
from PIL import Image
import numpy as np

def cleanFile(filePath, threshold):
    image = Image.open(filePath)
    image = image.point(lambda x: 0 if x < threshold else 255)
    return image

def getConfidence(image):
    data = pt.image_to_data(image, output_type=Output.DICT)
    text = data['text']
    confidences = []
    numChars = []
    for i in range(len(text)):
        if data['conf'][i] > -1:
            confidences.append(data['conf'][i])
            numChars.append(len(text[i]))
    return np.average(confidences, weights=numChars), sum(numChars)

filePath = 'path'
start = 130
step = 5
stop = 200

for threshold in range(start, stop, step):
    image = cleanFile(filePath, threshold)
    scores = getConfidence(image)
    print("th:" + str(threshold) + ", confidence: " + str(scores[0]) + " numChars " + str(scores[1]))
```

## scraping text from images on websites

amazon's book preview is usually not picked up by robots due to its an ajax call and well hidden in tags, we will attempt to retrieve with the following code. amazon allows crawling but run at your own risk.

```python
import time
from urllib.request import urlretrieve
from PIL import Image
import tesseract
from selenium import webdriver

def getImageText(imageUrl):
    urlretrieve(image, 'page.jpg')
    p = subprocess.Popen(['tesseract', 'page.jpg', 'page'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    with open('page.txt', 'r') as f:
    	print(f.read())

driver = webdriver.Chrome(executable_path="path")

driver.get('amazon/book/page')
time.sleep(2)
driver.find_element_by_id('img_id').click()
imageList = []

time.sleep(5)

while 'pointer' in driver.find_element_by_id('nextpageid').get_attribute('style'):
    driver.find_element_by_id('nextpageid').click()
    time.sleep(2)
    pages = driver.find_element_by_xpath('imagediv')
    if not len(pages):
        print('no pages found')
    for page in pages:
        image = page.get_attribute('sec')
        print(f'found image: {image}')
        if image not in imageList:
            imageList.append(image)
            getImageText(image)
driver.quit()
```

there will be error here and there if we ran the script above,

- markov chain analysis could help to to eliminate extremely uncommon phrase
- unique words could be stored to a dictionary word list and guess based on this dictionary
- we could train tesseract by providing it labeled datasets for a certain font

## captcha

we can practice against www.pythonscraping.com/humans-only

