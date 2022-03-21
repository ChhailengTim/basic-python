import webbrowser


url = ["https://xsmb.me", "https://xsmn.me","https://xsmb.co","https://xsmn.com","https://xsmn.info"]

brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

webbrowser.register("brave", None, webbrowser.BackgroundBrowser(brave_path))

webbrowser.get("brave").open(url[0])
webbrowser.get("brave").open(url[1])
webbrowser.get("brave").open(url[2])
webbrowser.get("brave").open(url[3])
webbrowser.get("brave").open(url[4])



