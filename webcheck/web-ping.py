from ping3 import ping

file = open('websites.txt', 'r')
Lines = file.readlines()

count = 0
# Strips the newline character



def pingwebsite(host):
    response = ping(host)

    if response == False:
        return False
    else:
        return True


for line in Lines:
    count += 1
    print(pingwebsite("{}".format(line.strip())))

