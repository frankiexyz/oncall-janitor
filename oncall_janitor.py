import click
import requests
import time
import six
import os
from rich.console import Console


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


def fetch_alertmanager(ALERTMGR_URL):
    try:
        alert_results = requests.get(ALERTMGR_URL).json()
        return alert_results, [alert["fingerprint"] for alert in alert_results]
    except Exception as e:
        if "console" in globals():
            console.log("Fail to access Alertmanager endpoint: {}".format(repr(e)))


console = Console()


@click.command()
@click.option("--alertmanager", required=True)
@click.option("--speak", default="speak", help="espeak or say")
@click.option("--sleep", default=30, help="Sleep interval")
def main(alertmanager, speak, sleep):
    ALERTMGR_URL = alertmanager
    SPEAKER = speak
    SLEEP_TIME = sleep
    alert_fingerprints = []
    console.log(":pray: Starting...")
    console.log(f"Alertmanager end-point {ALERTMGR_URL}")
    _, alert_fingerprints = fetch_alertmanager(ALERTMGR_URL)
    console.log(f":fire: There are {len(alert_fingerprints)} firing alerts")
    console.log(f":zzz: Sleep {SLEEP_TIME} seconds...")
    time.sleep(SLEEP_TIME)
    while True:
        try:
            alert_results, new_alert_fingerprints = fetch_alertmanager(ALERTMGR_URL)
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
                    message = get_alert_details(diff_fingerprint, alert_results)
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


if __name__ == "__main__":
    main()
