import webbrowser

# url = ["https://xsmb.me", "https://xsmn.me","https://xsmb.co","https://xsmn.com","https://xsmn.info"]

chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

file = open('websites.txt', 'r')
Lines = file.readlines()
count = 0

for line in Lines:
    count += 1
    web = format(line.strip())
    webbrowser.get("chrome").open(web)
    # webbrowser.get("chrome").open("http://" + web + "/")
    # webbrowser.get("chrome").open("https://"+web+"/")
