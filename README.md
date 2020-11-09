# oncall-janitor
Let the company speak your alerts!


```
pip install -r Requirements.txt
>python oncall-janitor.py --help
Usage: oncall-janitor.py [OPTIONS]

Options:
  --alertmanager TEXT  [required]
  --speak TEXT         espeak or say
  --sleep INTEGER      Sleep interval
  --help               Show this message and exit.
>python oncall-janitor.py  --alertmanager "https://127.0.0.1/api/v2/alerts?silenced=false&inhibited=false&active=true" --sleep 5
[17:05:00] 🙏 Starting...                                                                                                                                                                        oncall-janitor.py:40
           Prometheus end-point https://127.0.0.1/api/v2/alerts?silenced=false&inhibited=false&active=true                                                 oncall-janitor.py:41
[17:05:02] 🔥 There are 87 firing alerts                                                                                                                                                         oncall-janitor.py:45
           💤 Sleep 30 seconds...             


```


