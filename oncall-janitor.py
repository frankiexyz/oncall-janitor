import requests
import time
import six
import os
from rich.console import Console


PROM_URL = "https://<ALERTMANAGER_URL>/api/v2/alerts?silenced=false&inhibited=false&active=true"
SLEEP_TIME = 30
SPEAKER = "espeak"
# SPEAK="say" For mac user


def get_alert_details(fingerprint, firing_alerts):
    for alert in firing_alerts:
        if fingerprint == alert["fingerprint"]:
            if (
                "instance" in alert["labels"]
                or "device" in alert["labels"]
                or "colo_name" in alert["labels"]
            ):
                label = " ".join(
                    [
                        f"{k} {v}"
                        for k, v in six.iteritems(alert["labels"])
                        if k
                        in ["instance", "device", "port", "description", "colo_name"]
                    ]
                )
                return f"{alert['labels']['alertname']} in {label} summary {alert['annotations']['summary']}"
            else:
                return f"{alert['labels']['alertname']} summary {alert['annotations']['summary']}"


alert_fingerprints = []


console = Console()
console.log(":pray: Starting...")
console.log(f"Prometheus end-point {PROM_URL}")
prom_results = requests.get(PROM_URL).json()
for alert in prom_results:
    alert_fingerprints.append(alert["fingerprint"])
console.log(f":fire: There are {len(alert_fingerprints)} firing alerts")
console.log(":zzz: Sleep 30 seconds...")
time.sleep(30)

while True:
    try:
        prom_results = requests.get(PROM_URL).json()
        new_alert_fingerprints = []
        for alert in prom_results:
            new_alert_fingerprints.append(alert["fingerprint"])

        diff_fingerprints = set(new_alert_fingerprints) - set(alert_fingerprints)

        diff_fingerprints = [
            i for i in diff_fingerprints if "Interface_State_Changed_to" not in i
        ]
        if diff_fingerprints:
            if len(diff_fingerprints) == 1:
                message = "There is"
            else:
                message = "There are"
            message = f"{message} {len(diff_fingerprints)} new firing alerts"
            console.log(f":pile_of_poo: {message}")
            count = 1
            os.system(f"{SPEAKER} '{message}' 2>/dev/null ")
            time.sleep(1)
            for diff_fingerprint in diff_fingerprints:
                message = get_alert_details(diff_fingerprint, prom_results)
                console.log(message)
                os.system(f"{SPEAKER} 'alert {count} {message}' 2>/dev/null")
                time.sleep(1)
                if SPEAKER == "espeak":
                    os.system(f"notify-send -u critical '{message}'")
                count += 1
        else:
            console.log(":thumbs_up: There is no new firing alerts")
        alert_fingerprints = new_alert_fingerprints
        console.log(f":zzz: Sleep {SLEEP_TIME} seconds...")
        time.sleep(SLEEP_TIME)
    except Exception as e:
        console.log("Error: {}".format(repr(e)))
        if SPEAKER == "espeak":
            os.system(f"notify-send -u critical '{repr(e)}'")
        time.sleep(SLEEP_TIME * 2)
