[TOC]

# data structures - collections and generics

ArrayList does not have sort method and is not the only collections.

-  TreeSet - python equivalent of sorted set
- HashMap - python equivalent of dict
- LinkedList - alternate of ArrayList with better performance for insert / delete from the middle of the collection
- HashSet - python equivalent of sorted dict?
- LinkedHashMap - ?

using TreeSet might be a good idea to solve sorting problems, but with a little extra overhead. TreeSet ensures after every insert, the collection remains sorted.

to sort an ArrayList, we can see Collection class has sort method, and it takes a List as input argument, ArrayList implements List which means ArrayList can be input as the argument... thus

```java
import java.util.*;
import java.io.*;

public class Jukebox {
    ArrayList<String> songList = new ArrayList<String>();
    public static void main(String[] args) {
        new Jukebox1().go();
    }
    public void go() {
        getSongs();
        System.out.println(songList);
        Collections.sort(songList); // here is where will go wrong
        System.out.println(songList);
    }
    void getSongs() {
        try {
            File file = new File("SongList.txt");
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line = null;
            while ((line= reader.readLine()) != null) {
                addSong(line);
            }
        } catch(Exception ex) {
            ex.printStackTrace();
        }
    }
    void addSong(String lineToParse) {
        String[] tokens = lineToParse.split("/");
        songList.add(tokens[0]);
    }
}
// if we change song from string to object, we just overrides the toString method
// this is because when we call System.out.println(SongObject) it will call toString method
// and the changes to the code above is just <String> to <Song>
class Song {
    // bla bla bla...
    public String toString() {
        return title;
    }
}
// sadly it wont comple
// instead
class Song implements Comparable<Song> {
    String title;
    String artist;
    String rating;
    String bpm;

    public int compareTo(Song s) {
        return title.compareTo(s.getTitle());
    }
}
// what if we want to compare the artist too?
public class Jukebox {
    // bla bla bla...
    class ArtistCompare implements Comparator<Song> {
        public int compare(Song one, Song two) {
            return one.getArtist().compareTo(two.getArtist());
        }
    }
    public void go() {
        // bla...
        ArtistCompare artistCompare = new ArtistCompare();
        Collections.sort(songList, artistCompare);
        // bla...
    }
}
```

- in the documentation it says sort sort List \<T> which refers to generics for type-safety.
- comparator is external to the element type, eg. song. we can create as many as possible.