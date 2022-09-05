import requests


def createLoggedInSession(url: str, username: str, password: str):

    # headers copied from firefox
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

    credentials = {
        "username": username,
        "password": password,
        "submit": "login"
    }

    # create session to store cookies
    session = requests.Session()

    # post to login
    session.post(url,
                 data=credentials, headers=headers)
    return session
