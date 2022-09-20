[TOC]

# crawling through APIs

at core for a scrapping project an API is what defines the standardized syntax that allows one piece of software to communicate with another even though they might be written in different languages or structured differently. we shall focus on web API here. there is debate on where should we pass the parameter, through path or parameters but as long as it get the jobs done, anything is good enough. the response here is usually XML or json

## http methods and APIs

there are four main http methods GET, POST, PUT, DELETE.

- GET is where no changes to the information in the server database, only read
- POST is where we submit information
- PUT is less commonly used but its for us to update information
- DELETE does what its name suggest

except GET, other three allows user to to send information in the body of that request in addition to the URL or route

## undocumented APIs

the rise of undocumented APIs is due to the popularity of JS, many web applications adopted FE-BE separation approach thus given scrappers to leverage on these efficient data retrieval options. to discover them, we can use browser's developer tools to find out each result is returned and act accordingly. once we identified how these undocumented API works, we should document it down. some tools available including 'REMitchel/apiscraper' github project.

## what's next?

once we retrieve information, its up to the user to format the data such that it could provide value. if we only retrieve, that at best we could duplicate their database.

more on apis

- restful web apis by Learnard R., Mike A. and Sam R. (O'Reilly)
- designing APIs for the web (O'Reilly video by Mike A.)