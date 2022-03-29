import webbrowser

file = open('websites-2.txt', 'r')
Line = file.readlines()

count = 0

# url = ["https://xsmb.me", "https://xsmn.me","https://xsmb.co","https://xsmn.com","https://xsmn.info"]

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

webbrowser.register("brave", None, webbrowser.BackgroundBrowser(brave_path))

# webbrowser.get("brave").open(url[0])
# webbrowser.get("brave").open(url[1])
# webbrowser.get("brave").open(url[2])
# webbrowser.get("brave").open(url[3])
# webbrowser.get("brave").open(url[4])
for line in Line:
    count += 1
    web = format(line.strip())
    # webbrowser.get("brave").open(web)
    webbrowser.get("brave").open("http://" + web + "/")
    # webbrowser.get("chrome").open("https://"+web+"/")
