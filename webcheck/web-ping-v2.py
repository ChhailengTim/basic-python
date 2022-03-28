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

    response = pingwebsite(format(line.strip()))
    print(response)
    print(format(line.strip()))
