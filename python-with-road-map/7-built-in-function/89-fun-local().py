def localsPresent():
    present = True
    print(present)
    locals()['present'] = False;
    print(present)


localsPresent()
