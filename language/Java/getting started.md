[TOC]

# a dumb guide to setup spring boot

requirements

- Intelllij IDEA or equivalent
- JDK 1.8 or later [(link)](https://www.oracle.com/java/technologies/javase-downloads.html)
- Maven 3.2+ [(link)](https://maven.apache.org/download.cgi)
- spring cli
- STS?

## JDK installation 

1. follow link to download latest or preferred JDK version.
2. install the executable
3. open up environment variables and set the JDK\bin path to

> java -version

## Maven / gradle installation

similar to JDK
add maven\bin to PATH

> mvn -v 

or

> gradle -v

## spring cli

similar to JDK
add spring\bin to PATH

> spring --version

### to test out spring

create a file app.groovy with the following code

```java
@RestController
class ThisWillActuallyRun {

    @RequestMapping("/")
    String home() {
        "Hello World!"
    }

}
```

> spring run app.groovy

check port localhost:8080

## others

[spring initializr](https://start.spring.io/) or spring init