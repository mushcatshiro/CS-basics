[TOC]

# Event handling

event handling by implementing an listener interface that bridges the listener and event source (imagine a button).

```java
import java.util.*;

// An interface to be implemented by everyone interested in "Hello" events
interface HelloListener {
    void someoneSaidHello();
}

// Someone who says "Hello"
class Initiater {
    private List<HelloListener> listeners = new ArrayList<HelloListener>();

    public void addListener(HelloListener toAdd) {
        listeners.add(toAdd);
    }

    public void sayHello() {
        System.out.println("Hello!!");

        // Notify everybody that may be interested.
        for (HelloListener hl : listeners)
            hl.someoneSaidHello();
    }
}

// Someone interested in "Hello" events
class Responder implements HelloListener {
    @Override
    public void someoneSaidHello() {
        System.out.println("Hello there...");
    }
}

class Test {
    public static void main(String[] args) {
        Initiater initiater = new Initiater();
        Responder responder = new Responder();

        initiater.addListener(responder);

        initiater.sayHello();  // Prints "Hello!!!" and "Hello there..."
    }
}
```

the usual steps to implement will be implementing the interface, register the event source and provide the event handling as a listener.

on contrast, an event source will accept registrations, get events and call the listener's event-handling method.

lastly the event object carries date back and forth between listener and event.

## inner classes

when we wanted to implement multiple action events for different purpose (eg buttons) what can be done?

- implement two action performed methods which is impossible since the method name collides
- register to same listener with all source then filter / query which event is being called, works but not OO where a single event handler doing many different things
- create two separate action listener class, but these classes will not have access to the supposed superclass or main client (difference between this option with inner class is that here we will be having at least 3 classes and multiple getter / setter methods)
- inner class

```java
public class TwoButtons {
    JFrame frame;
    JLabel label;

    public static void main (String[] args) {
        TwoButtons gui = new TwoButtons ();
        gui.go();
    }
    public void go() {
        frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        JButton labelButton = new JButton(“Change Label”);
        labelButton.addActionListener(new LabelListener());
        JButton colorButton = new JButton(“Change Circle”);
        colorButton.addActionListener(new ColorListener());
        label = new JLabel(“I’m a label”);
        MyDrawPanel drawPanel = new MyDrawPanel();

        frame.getContentPane().add(BorderLayout.SOUTH, colorButton);
        frame.getContentPane().add(BorderLayout.CENTER, drawPanel);
        frame.getContentPane().add(BorderLayout.EAST, labelButton);
        frame.getContentPane().add(BorderLayout.WEST, label);
        frame.setSize(300,300);
        frame.setVisible(true);
    }

    class LabelListener implements ActionListener {
        public void actionPerformed(ActionEvent event) {
        	label.setText(“Ouch!”);
    	}
    } // close inner class
    class ColorListener implements ActionListener {
        public void actionPerformed(ActionEvent event) {
        	frame.repaint();
    	}
    } // close inner class

}
```

with inner class we can implement the same interface / method more than once in a class

