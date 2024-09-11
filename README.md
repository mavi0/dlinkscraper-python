# Dlinkscraper Python

[Dlinkscraper](https://github.com/mavi0/dlinkscraper) rewritten in python designed to print json to standard out and then consumed by Telegraf. 

See `telegraf.conf` snippet below:

```TOML
...
[[inputs.exec]]
  commands=["python /path/to/main.py"]
  interval = "20s"
  timeout = "10s"
  data_format = "json"
  name_override = "dlink"
...
  ```