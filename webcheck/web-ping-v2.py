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
    web = format(line.strip())

    response = pingwebsite("http://" + web + "/")
    print(response)
    # print("http://" + web + "/")
