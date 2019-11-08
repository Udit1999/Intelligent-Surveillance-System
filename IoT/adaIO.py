# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony Dicola, Justin Cooper

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed
import json

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'd62261bab11e4ae0a8e9ef9e368a4472'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'UDAI'

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

alarm = aio.feeds("alarm")
door = aio.feeds("door")

def playAlarm():
	aio.send_data(alarm.key,"1")

def openDoor():
	aio.send_data(door.key,"1")

def aiofeed():
    # List all of your feeds
    feeds = aio.feeds()
    print(feeds)

    # Create a new feed
    feed = Feed(name="PythonFeed")
    response = aio.create_feed(feed)
    print(response)

    # List a specific feed
    feed = aio.feeds(response.key)
    print(feed)



# Delete a feed
# aio.delete_feed(response.key)
