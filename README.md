# lsyncd-widget
Little PyQt6 widget to check lsyncd status.

Currently check if there is a sync running or not.


## Usage

1. Install requirements:

```
pip install -r requirements.txt
```

2. Rename the .env.example file to .env

3. Configure the  `LOG_FILE` variable in the .env file. The value should be the path to the Lsyncd logfile:

```
LOG_FILE=/path/to/lsyncd/logs
```

4. Launch the widget:

```
python main.py
```

