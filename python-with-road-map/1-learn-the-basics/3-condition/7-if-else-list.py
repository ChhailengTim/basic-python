treepersqkm = {"Finland": 90652, "Taiwan": 69593, "Japan": 49894, "Russia": 41396, "Brazil": 39542, "Canada": 36388,
               "Bulgaria": 24987, "France": 24436, "Greece": 24323, "United States": 23513, "Turkey": 11126,
               "India": 11109, "Denmark": 6129, "Syria": 534, "Saudi Arabia": 1}


def moretrees(dict):
    lst = []
    for i in dict:
        if dict[i] > 20000:
            lst.append(i)
        else:
            pass
        return lst


print(moretrees(treepersqkm))
