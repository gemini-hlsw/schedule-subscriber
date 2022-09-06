# Subscriber for the Scheduler service

This is an auxiliary service for the [Gemini Automated Scheduler]().
Handles changes on the ODB and other services that could trigger a new schedule.


## Install 

```shell
$ pip install -r requirements.txt
```

## Run
```shell
$ python main.py
```

__Important__: This needs a version of the Scheduler core running alongside (either locally or remote) and the ODB endpoint. The path needs to be setup as a environment variable in `$ODB_ENDPOINT_URL` and `$CORE_ENDPOINT_URL`.
