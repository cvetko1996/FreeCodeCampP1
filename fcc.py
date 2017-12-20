from flask import Flask, render_template,request
import feedparser
from confidental import apiweather
import json
import urllib
from urllib.request import urlopen

#za python2 obrisati gore i ubactiti
#import urllib2

from urllib.parse import quote

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

app = Flask(__name__)

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"
    query = quote(query)
    url = api_url.format(query,apiweather)
    data = urlopen(url).read()
    parsed = json.loads(data.decode('utf-8'))
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "icon":parsed["weather"][0]["icon"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather

def get_channel_info(query):
    fquery = str(query)
    api_url = 'https://wind-bow.glitch.me/twitch-api/users/'
    url = str(api_url+fquery)
    data = urlopen(url).read()
    parsed = json.loads(data.decode('utf-8'))
    channel_info = None
    if parsed.get("display_name"):
        channel_info = {"display_name": parsed['display_name'],
                   "info": parsed['bio'],
                   "logo": parsed["logo"]
                   }
    return channel_info


@app.route('/',methods=['GET','POST'])
def home():
    city = request.form.get('city')
    if city is None:
        city = 'London'
    weather = get_weather(city)
    icon = 'http://openweathermap.org/img/w/'+weather['icon']+'.png'
    feed = feedparser.parse(BBC_FEED)
    return render_template("bbc.html",articles=feed['entries'], weather=weather,icon=icon)

@app.route('/bbc',methods=['GET','POST'])
def bbc():
    city = request.form.get('city')
    if city is None:
        city = 'London'
    weather = get_weather(city)
    icon = 'http://openweathermap.org/img/w/' + weather['icon'] + '.png'
    feed = feedparser.parse(BBC_FEED)
    return render_template("bbc.html",articles=feed['entries'],weather=weather,icon = icon)

@app.route('/twitch',methods=['GET','POST'])
def twitch():

    twitch_channel = request.form.get("twitch_name")

    if twitch_channel is None:
        twitch_channel = "Monstercat"

    channel = get_channel_info(twitch_channel)
    print(channel)

    city = request.form.get('city')

    if city is None:
        city = 'London'

    weather = get_weather(city)

    icon = 'http://openweathermap.org/img/w/' + weather['icon'] + '.png'

    return render_template('twitch.html',weather=weather,icon=icon,channel=channel)



if __name__ == '__main__':
    app.run(port=5000,debug=True)
