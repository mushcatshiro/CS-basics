[TOC]

# Scraping Javascript

to be able to scrap effective at large scale, we need to get ourselves familiar with JS libraries as executing javascript with python is slow

## js libraries

### jquery

jQuery is usually dynamically creating HTML content that appears **AFTER** javascript is executed, using methods we have been using will results in scraping pre-loaded page instead of the content of interest.

### google analytics

one of the most popular user tracking tools available. its easy to identify if a page have google analytics enabled, where we can find

````javascript
'.google-analytics.com/ga.js'
````

sites with google analytics must be handled carefully to prevent it picking up there is a scraping activity on going, make sure to discard any cookies used for analytics or discard the cookie.

### google maps

understanding how google maps works makes it easy to obtain well-formatted longitude / latitude coordinates and addresses, the easiest and common way to denote a location on google maps is through a marker 

````javascript
// markers can be inserted as such
var marker = new google.maps.Marker({
    position: new google.maps.LatLng(-23, 131),
    map: map,
    title: 'some marker text'
})
````

just apply regex to resolve it to find content between LatLng( and ). once the information is obtained, we can use google's reverse geocoding api to resolve these coordinates

## ajax and dynamic HTML (DHTML)

not to be fooled by the static look of a page, it could have DHTML running in the background. for such situations we can either

- user python package that can execute JS, or
- scrape directly from JS

## executing JS in python with selenium

selinium works by automating browsers to load target website, retrieve information and, or take screenshots / assert certain action happen on the website, thus it **requires** third party browser to run. to run jobs in the background we can use headless browsers like PhantomJS in lieu of a actual browser. one thing to point out is that its not recommended to set waiting time instead use the following example to wait for stuffs

````python
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element(By.ID, 'name'))
finally:
    driver.close()
````

## handling redirects

client side redirects is where the redirection is done before the page content is sent, it can be tricky to tell if its a client side redirect or a server side redirect, it makes differences to a scrapper. server side redirect can be handled easily with python libraries, but client side redirect involves JS which is where selenium comes in. the key is actually to know when the redirection is done. this can be achieved similarly as above where we waits for some indications by repeatedly calls the element until selenium throws StaleElementReferenceException (element is no longer attached)

## some notes on JS

having server side rendering is not a showstopper and might open up opportunities eg. api exposure.