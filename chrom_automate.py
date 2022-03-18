
import webbrowser

url = ["https://xsmb.me", "https://xsmn.me","https://xsmb.co","https://xsmn.com","https://xsmn.info"]

chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

webbrowser.get("chrome").open(url[0])
webbrowser.get("chrome").open(url[1])
webbrowser.get("chrome").open(url[2])
webbrowser.get("chrome").open(url[3])
webbrowser.get("chrome").open(url[4])