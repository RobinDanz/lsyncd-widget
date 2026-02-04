# lsyncd-widget
Little PyQt6 widget that analyses the [lsyncd](https://github.com/lsyncd/lsyncd) logfile and shows the sync status based on the logs in real time.

![insync](images/widget_insync.PNG)  

![processing](images/widget_processing.PNG)

## Features
* Realtime log reading based on filesystem events
* Minimal interface

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

## Test
Follow the next steps to test the widget without having an lsyncd setup:
1. Create an empty text file somewhere
2. Point the `LOG_FILE` variable in the .env to that text file
3. Run the widget: `python main.py`
4. Insert `Normal: Calling rsync` into the text file and save it
5. Insert `Normal: Finished` into the text file and save it

You should see the widget interface change accordingly !

