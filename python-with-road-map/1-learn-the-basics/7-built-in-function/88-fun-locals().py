def localsNotPresent():
    return locals()


def localsPresent():
    present = True
    return locals()


print('localsNotPresent:', localsNotPresent())
print('localsPresent:', localsPresent())
