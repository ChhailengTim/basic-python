import urllib
from urllib.request import urlopen

url = ["https://xsmb.me", "https://xsmn.me", "https://xsmb.co", "https://xsmn.com", "https://xsmn.info"]


def is_internet():
    """
    Query internet using python
    :return:
    """
    try:
        urlopen(url[1], timeout=1)
        return True
    except urllib.error.URLError as Error:
        print(Error)
        return False


if is_internet():
    print("This web is active")
else:
    print("This web in disconnected")
