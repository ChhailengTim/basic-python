from ping3 import ping
import gspread

sa = gspread.service_account()
sh = sa.open("របាយការវែបសាយ")

wks = sh.worksheet("Sheet1")

# print("Rows: ", wks.row_count)
# print("Cols: ", wks.col_count)

# print(wks.acell("B9").value)
# print(wks.cell(3, 4).value)

# print(wks.get_all_records())


file = open('websites-3.txt', 'r')
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
    web = format(line.strip())
    count += 1
    print(count)
    response = pingwebsite(web)
    # print(pingwebsite("{}".format(line.strip())))
    print(response)
