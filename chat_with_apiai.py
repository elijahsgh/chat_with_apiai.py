#!/usr/bin/env python3

import sys
import credentials
import uuid
import json
import requests
import simpleaudio as sa
from io import BytesIO

def text_query(q):
    headers = {
        "Authorization": "Bearer {}".format(credentials.apikey),
        "Content-Type": "application/json"
    }

    params = {
        "v": "20150910",
        "sessionId": sessionid,
        "lang": lang,
        "query": query
    }

    r = requests.post("https://api.api.ai/v1/query",
                      headers=headers,
                      data=json.dumps(params))

    return r.json() if r.status_code == 200 else None


def response_to_speech(speech):
    query = { "text": speech,
              "v": "20150910"}

    headers = {"Authorization": "Bearer {}".format(credentials.apikey),
               "Accept-Language": "en-US" }

    r = requests.get("https://api.api.ai/v1/tts", headers=headers, params=query)

    if r.status_code == 200:
        with BytesIO(r.content) as rfp:
            sa.WaveObject.from_wave_file(rfp).play().wait_done()


if __name__ == '__main__':
    print('Starting...\n> ', end="")

    sessionid = uuid.uuid4().hex
    lang = "en-US"
    query = sys.stdin.readline().strip()

    while query:
        print("Query: {}".format(query))

        decoded_response = text_query(query)

        print("Full response: {}".format(decoded_response))

        if decoded_response['status']['errorType'] == 'success':
            speech = decoded_response['result']['speech']
            if not speech:
                print("Response: {}".format(speech))
            else:
                response_to_speech(speech)
        else:
            print("Could not process request: {}".format(
                    decoded_response['status']['errorDetails']))

        print("\n> ", end="")
        query = sys.stdin.readline().strip()
