from ping3 import ping

file = open('websites.txt', 'r')
Line = file.readlines()

count = 0


def pingwebsite(host):
    response = ping(host)

    if response == False:
        return False
    else:
        return True


for line in Line:
    count += 1
    # print(count)
    web = format(line.strip())

    response = pingwebsite("https://" + web + "/")
    print(response)
    # print((pingwebsite(web)))
    # print("http://" + web + "/")
