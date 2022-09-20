[TOC]

# Avoiding Scrapping Traps

## looking like a human

one of the main challenges for websites is to distinguish between human and bots.

as a scraper we try to look like a human by,

- using appropriate headers (user-agent as mobile browser, accept-language for changing language)
- handling cookies with JS
- throttle your speed

## common form security features

- hidden input field values (to stop bots from submitting incomplete forms, generate values on random or lure bots to fill in the wrong field)
- CSS traps 
  - CSS make pinpointing easier, but not always eg. a hidden form (and not limited to form, link, images, files and etc)
  - a hidden link could be a kill switch for the service to block the accessing IP address

## a human checklist

- if page is always empty it could be JS driven on client side
- always check when we are posting forms to post **ALL** required information and not including any traps in the correct format
- cookies
- 403 http error could be because the bot has been identified and thus been block from further accessing
- throttle your bot
- headers!
- not navigating to non visible contents