# Smart Garden

## Getting Started

Run script to log sensor data to sqlite database.
```
python3 data_logger.py
```

Run script to water plants with button manually.
```
python3 button_moisture.py
```

Run web server.
```
authbind --deep python3 web_server.py
```

Use `crontab -e` to run python processes on start up.
```
@reboot cd smart-garden && python3 data_logger.py &
@reboot cd smart-garden && python3 button_moisture.py &
@reboot cd smart-garden && authbind --deep python3 web_server.py &
```

## Tools for debugging

```
i2cdetect -y 1
```