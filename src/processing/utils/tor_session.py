import os
import requests
import logging

logger = logging.getLogger('tor-session')


def get_session():
    use_tor = os.getenv("TOR_SESSION_ENABLE", None)
    proxy_url = os.getenv("TOR_PROXY_URL", None)

    session = requests.session()
    session.proxies = {}

    if proxy_url and use_tor.lower() == "true":
        session.proxies['http'] = proxy_url
        session.proxies['https'] = proxy_url

    return session


def check_session():
    try:
        session = get_session()
        proxyless_ip = session.get('https://api.ipify.org').text

        if session.proxies:
            print("[Tor Session] Proxy set to", session.proxies['http'])

            try:
                proxy_ip = session.get('https://api.ipify.org').text
                if proxy_ip == proxyless_ip:
                    print("[Tor Session] Proxy test successful. Proxy IP:", proxy_ip)
                else:
                    msg = "[Tor Session] Proxy test failed: proxy session IP address has not changed."
                    logger.error(msg)
                    raise SystemExit(msg)
            except Exception:
                msg = "[Tor Session] Could not reach test website using tor session. Is the tor service running and proxy URL correct?"
                logger.error(msg)
                raise SystemExit(msg)

        else:
            print("[Tor Session] Proxy session disabled. Using a proxyless (unprotected) session instead.")
    except Exception:
        raise SystemExit("[Tor Session] Session failed to connect to test server. Is the tor service running and proxy URL correct?")
