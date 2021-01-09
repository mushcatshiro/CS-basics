[TOC]

# methods

battleship game

shiro's version before looking at textbook

> this is purely eyeball compilation -- 05012021

```java
class battleship {
    private int locationX, locationY;
    
    void setup(int x, y){
        locationX = x;
        locationY = y;
        alive = true;
    }
    
    boolean isHit(int x, y){
        if (x == locationX && y == locationY){
            return true;
        }
    }
}

class rand {
    private int max = 6;
    private int min = 0;

    public static int get{
        return Math.random() * (max - min + 1) + min;
    }
}

class diskBoard {
    private battleship[] ships;
    private int no_of_ships;

    void setup{
        int i;
        // random number generator
        ships = new battleship[3]
        for (i = 0; i < no_of_ships; i++) {
            ships[i] = new battleship();
        	ships[i].setup(rand.get(), rand.get())
        }
    }
    
    void strike(int x, y){
        // check battleship isHit
        int i;
        boolean down;
        for (i = 0; i < ships.length; i++) {
            // accessing each element of array 
            down = ships[i].isHit(x, y); 
            if (down){
                // pop from array
                // too abit extra effort to write one...
                break;
            }
        } 
    }
    
    int getAlive{
        return ships.length;
    }
}

public class Game {
    public static void main(String[] args){
        // create new game
        diskBoard game = new diskBoard();
        game.setup();
        // play
        while (game.getAlive != 0){
            Scanner in = new Scanner(System.in);
            System.out.println("type x coor");
            int x = in.nextInt();
            Scanner in = new Scanner(System.in);
            System.out.println("type y coor");
            int y = in.nextInt();
            game.strike(x, y)
        }
        System.out.println("you win")
    }
}
```

after writing in IDE, it works but some parts might be redundant and others are just simply lazy

```java
import org.apache.commons.lang3.ArrayUtils;

import java.util.Scanner;

class battleship {
    private int locationX, locationY;
    boolean alive;

    void setup(int x, int y){
        locationX = x;
        locationY = y;
        alive = true;
    }

    boolean isHit(int x, int y){
        return x == locationX && y == locationY;
    }
}

class rand {

    public static int get(){
        int min = 0;
        int max = 6;
        return (int) (Math.random() * (max - min + 1) + min);
    }
}

class diskBoard {
    private battleship[] ships;

    void setup(){
        int i, coorX, coorY;
        // random number generator
        ships = new battleship[3];
        int no_of_ships = 3;
        for (i = 0; i < no_of_ships; i++) {
            ships[i] = new battleship();
            coorX = rand.get();
            coorY = rand.get();
            // print all coordinate for ease of testing
            System.out.println("coor x: " + coorX + " coor y: " + coorY);
            ships[i].setup(coorX, coorY);
        }
    }

    void strike(int x, int y){
        // check battleship isHit
        int i;
        boolean down;
        for (i = 0; i < ships.length; i++) {
            // accessing each element of array
            down = ships[i].isHit(x, y);
            if (down){
                // pop from array
                // too abit extra effort to write one...
                ships = ArrayUtils.remove(ships, i);
                break;
            }
        }
    }

    int getAlive(){
        return ships.length;
    }
}

public class Game {
    public static void main(String[] args){
        // create new game
        diskBoard game = new diskBoard();
        game.setup();
        // play
        while (game.getAlive() != 0){
            Scanner in = new Scanner(System.in);
            System.out.println("type x coor");
            int x = in.nextInt();
            in = new Scanner(System.in);
            System.out.println("type y coor");
            int y = in.nextInt();
            game.strike(x, y);
        }
        System.out.println("you win");
    }
}
```

## extreme programming (XP)

1. Make small, but frequent, releases.
2. Develop in iteration cycles.
3. Don’t put in anything that’s not in the spec (no matter how tempted you are to put in functionality “for the future”).
4. Write the test code first. No killer schedules; work regular hours.
5. Refactor (improve the code) whenever and wherever you notice the opportunity.
6. Don’t release anything until it passes all the tests.
7. Set realistic schedules, based around small releases.
8. Keep it simple.
9. Program in pairs, and move people around so that everybody knows pretty much everything about the code

## BufferedReader vs Scanner

scanner if called with nextLine() after the nextXXX() method, it does not read value from console and cursor will not come into console - it will skip that step. bufferedreader don't have this problem. this issues arises due to nextXXX method ignore newline character and nextLine only reads till first newline character. to "address" this we could call another nextLine to consume the newline character or use next() instead.

bufferedreader is synchronous and should always be used if we are working with threads. however it has significantly larger buffer memory (1kB vs 8kB). bufferedreader is faster due to no parsing involved but simply read sequence of characters.

## advanced for loop

```java
for (int i = 0; i < ships.length; i++) {}
// or
for (int i : ships.length){}
```

both should work the same.

## self initiating

```java
class cat {
    public static void main(String [] args) {
        cat c = new cat();
        c.create();
    }
    void create() {
    }
}
```

