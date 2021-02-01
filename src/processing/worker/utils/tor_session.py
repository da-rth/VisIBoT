import os
import requests

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

    print("[Tor Session] Proxy set to", session.proxies['http'])
    try:
        if "Congratulations" in session.get("https://check.torproject.org").text:
            print("[Tor Session] Proxy successfully connected to Tor network.")
        else:
            print("[Tor Session] Proxy test failed. Is tor running?")
    except Exception:
        raise SystemExit("[Tor Session] Could not reach test website using tor session. Is tor running?")
