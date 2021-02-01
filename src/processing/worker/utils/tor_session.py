import os
import requests
import time

USE_TOR = os.getenv("TOR_SESSION_ENABLE", False) == "True"
TOR_URL = "socks5h://tor:9050"


def get_session():
    session = requests.session()
    session.proxies = {}

    if USE_TOR:
        session.proxies['http'] = TOR_URL
        session.proxies['https'] = TOR_URL

    return session


def check_session():
    session = get_session()

    if USE_TOR:
        print("[Tor Session] Proxy set to", session.proxies['http'])
        try:
            if "Congratulations" in session.get("https://check.torproject.org").text:
                print("[Tor Session] Proxy successfully connected to Tor network.")
            else:
                print("[Tor Session] Proxy test failed. Is tor running?")
        except Exception:
            raise SystemExit("[Tor Session] Could not reach test website using tor session. Is tor running?")
    else:
        print("[Tor Session] Proxy session disabled. Using a proxyless (unprotected) session instead.")

