from binaryornot.check import is_binary
from floss import strings
from floss import main
import re
import os
import json
import utils
import requests


def perform_analysis(url):
    try:
        with requests.get(url) as r:
            try:
                filename = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            except (IndexError, KeyError):
                filename = "unknown_binary"

            open(filename, 'wb').write(r.content)

            if is_binary(filename):
                file_buf = main.get_file_as_mmap(filename)
                static_ascii_strings = strings.extract_ascii_strings(file_buf, 4)
                static_unicode_strings = strings.extract_unicode_strings(file_buf, 4)
                all_strings = utils.parse_floss_output(static_ascii_strings) + utils.parse_floss_output(static_unicode_strings)
                os.remove(filename)
                return {
                    'statusCode': 200,
                    'body': json.dumps(utils.ip_url_strings(all_strings))
                }
            else:
                os.remove(filename)
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        "msg": "The given URL does not lead to a binary file. Static Analysis cannot be performed."
                    })
                }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                "msg": str(e)
            })
        }
