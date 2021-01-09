[TOC]

# On Intellij IDEA

## adding new dependencies

find and add the following into the pom.xml

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <version>3.1</version>
    </dependency>
</dependencies>
```

should be added automatically to local

## changing CE maven repository

go to settings find maven and tick override to change