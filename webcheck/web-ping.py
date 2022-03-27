from ping3 import ping
import gspread

sa = gspread.service_account()
sh = sa.open("របាយការវែបសាយ")

# file = open('websites.txt', 'r')
# Lines = file.readlines()
#
# count = 0
# # Strips the newline character
#
#
#
# def pingwebsite(host):
#     response = ping(host)
#
#     if response == False:
#         return "មិនដំណើរការ"
#     else:
#         return "ដំណើរការ"
#
#
# for line in Lines:
#     count += 1
#     print(count)
#     print(pingwebsite("{}".format(line.strip())))
