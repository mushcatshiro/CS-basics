[TOC]

# encoding and decoding

[Pragmatic Unicode, or, How do I stop the pain?](https://www.youtube.com/watch?v=sgHbC6udIqc&ab_channel=NextDayVideo) - Ned Batchelder

five facts of life

1. IO is always bytes
2. we need more than 256 symbols
3. we will need to deal with both unicode and bytes
4. we cant infer encodings
5. declared encoding can be wrong

three pro tips

1. unicode sandwich
2. know what you have / what is your variable's type
3. test (with kool character generator)

## unicode and utf-8

unicode is code points. 0 - 0x10FFFF

> U+0041 hex maps to "A"

utf-8 is a variable width character encoding and is capable to encode all unicodes. the variable width here refers to it can encode using 1 - 4 bytes. a 1 byte utf-8 is mapped to ascii with the first byte starts with a 0. 2 byte and beyond the first byte will start differently (110, 1110, 11110) and the subsequent byte always starts with 10.

conversion from unicode to utf-8 in short is to find the most significant bit and fit just nice into 1 - 4 bytes and left trim all zeros.

## python 3

in python encoding refers to the process of  converting unicode to bytes and decoding refers to the opposite process.

## references

[unicode-and-character-sets](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)
