# pylama:ignore=E402:ignore=E702
import sys; sys.path.append("..")
import os
import time
import requests
import database as db


vtapi = VirusTotalURLProcessor(os.getenv("VIRUSTOTAL_API_KEY"))


def process_payloads(payload_ids):
    total_scans = len(payload_ids)
    scans_still_processing = []

    for i, payload_id in enumerate(payload_ids):
        print(f"Payload VirusTotal scans still processing: {i+1}/{total_scans}", end="\r")
        payload = db.Payload(id=payload_id)
        payload.vt_result = vtapi.process_url(payload.url)
        payload.save()

        if payload.vt_result['processing'] == True:
            scans_still_processing.append(payload)

    # Sleep 60 seconds to let payload scans process
    print("Waiting 60 seconds for VirusTotal Scans to process...\n")
    time.sleep(60)
    print("Time up! Checking processing status for pending scans...")

    while scans_still_processing:
        print(f"Payload VirusTotal scans still processing: {len(scans_still_processing)}", end="\r")

        for payload in scans_still_processing:
            payload_idx = scans_still_processing.index(payload)
            vt_result = vtapi.process_url(payload.url)

            if vt_result['processing'] == False:
                payload.vt_result = vt_result
                payload.save()
                del scans_still_processing[payload_idx]

        print("Waiting an additional 30 seconds...", end="\r")
        time.sleep(30)


