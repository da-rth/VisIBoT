import json
from analysis import perform_analysis


def lambda_handler(event, _):
    try:
        url = event['queryStringParameters'].get("url", None)
        if url:
            return perform_analysis(url)
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Please include 'url' query parameter.")
        }
