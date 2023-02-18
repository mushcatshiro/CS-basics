import time

text =\
"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at interdum
lectus. Proin quis magna in sem faucibus congue vitae sit amet dui. Etiam
rutrum euismod ex et ultricies. Phasellus at dui orci. Mauris egestas quam
libero, sed rhoncus massa dignissim nec. Fusce est leo, scelerisque non augue
at, elementum imperdiet urna. Curabitur fringilla tortor ac velit consectetur
tincidunt. Praesent ultricies interdum sodales. Sed sed dolor vel elit dapibus
aliquet. Sed ut magna vel ipsum tincidunt elementum. Aenean quis est sit amet
nulla aliquam volutpat. In hac habitasse platea dictumst. Ut ac lacus eu elit
fermentum volutpat. Curabitur in mauris ex. Sed ornare nec nisi ac tristique.
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere
cubilia curae; Nam facilisis neque ac vestibulum interdum. Donec volutpat diam
et elit mollis, vitae vehicula est laoreet. Etiam ante nunc, eleifend ac nunc
a, placerat lacinia ipsum. Phasellus id arcu risus. Sed sit amet nisi faucibus,
tempus nunc quis, pellentesque ipsum. Pellentesque consequat felis eros, at
condimentum ex sollicitudin eget. Nullam quis imperdiet felis. Morbi eu posuere
erat. Sed vehicula dolor condimentum, imperdiet arcu non, rutrum eros. Etiam et
semper ante, id efficitur felis. Mauris sed finibus nulla, at lacinia lectus.
Aliquam fringilla metus vel diam elementum, quis porttitor sem aliquam. Fusce
elementum sapien eget odio vehicula, eget lacinia mi aliquam. Cras ac dictum
quam. Duis tellus eros, fringilla ut auctor at, vehicula nec lacus. Phasellus
ullamcorper rutrum nunc, ut dignissim purus molestie in. Suspendisse vitae
posuere ligula. Quisque sed erat nisl. Aenean lobortis dictum magna vel semper.
Morbi semper malesuada elit id feugiat. Aenean vel nibh sit amet magna bibendum
condimentum. Interdum et malesuada fames ac ante ipsum primis in faucibus.
Nullam in mi et purus fringilla commodo in at lorem. Quisque dui est,
consectetur a ligula in, efficitur vulputate velit. Phasellus malesuada
pharetra urna vel ultrices. Nunc leo felis, venenatis nec mattis aliquet,
efficitur eu augue. Quisque vitae lacus eu metus feugiat sodales. Integer
venenatis eros libero, sit amet aliquet orci ultricies eget. Duis ut vulputate
lorem. Proin tincidunt urna sed dui bibendum, a gravida magna malesuada. Cras
massa arcu, aliquet et tellus mollis, ornare sodales felis. Aliquam erat
volutpat. In hac habitasse platea dictumst. Maecenas laoreet orci at erat
aliquet, sit amet lacinia augue egestas. Mauris turpis orci, gravida eget
iaculis nec, dignissim fringilla orci. Ut gravida justo nec odio accumsan
fringilla. Aliquam est lorem, vestibulum quis nisi sed, vulputate dignissim
nibh."""


def bichar(target):
    paragraph = text.\
        replace("\n", " ").\
        replace(",", "").\
        replace(".", "").\
        lower().\
        split(" ")
    d = {}
    for word in paragraph:
        if len(word) == 1:
            continue
        if len(word) == 2:
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
        else:
            ctr = 0
            while ctr < len(word):
                slice = word[ctr:ctr+2]
                if slice in d:
                    d[slice] += 1
                else:
                    d[slice] = 1
                ctr += 1
    time.sleep(5)
    if target in d:
        cnt = d[target]
        print(f"found {cnt} of {target}.")
        return {target: cnt}
    else:
        print("target not found.")
        return {target: 0}
