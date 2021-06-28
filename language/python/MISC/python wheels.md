[TOC]

# python wheels

keywords: packing and distribution, ELF, ABIs, Dynamic linking

## the eggs, the wheel

early packaging approach, no guiding PEP, no standard, designed to be directly importable (might include .pyc files), and thus leads to the invention of the wheel (PEP 427, PEP 426 and PEP 376)

- pure wheels
  - only python code
  - might specific to certain python version
- universal wheels
  - compatible to python 2 and 3
- extension wheels

## extensions 

### without binary distributions

when we install some packages that requires other binary eg gcc we might run into some errors. this is because the required binary distribution is not available.

> addressing this we can just install a few more packages including python-dev, libffi-dev and libssl-dev

### with binary distributions

no problem.

## python native extensions

python code is more than python, c dependencies is one of the main component. c is compiled language, gcc compiles it into a ELF file. so an alternate approach on packaging package with c, we could bundle pre-compiled binaries dependencies inside python wheel.

## manylinux and auditwheel

PEP 513 and 571 define a set of permitted libraries and their symbol versions for linux systems. we can check if the symbol policies if enforced with auditwheel.

___

## reference

[youtube](https://www.youtube.com/watch?v=02aAZ8u3wEQ&ab_channel=PyCon2019)