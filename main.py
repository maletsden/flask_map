import tweepy
import hidden
import folium
from geopy.geocoders import Nominatim
import geopy.exc

# setup
oauth = hidden.oauth()
auth = tweepy.OAuthHandler(oauth['consumer_key'], oauth['consumer_secret'])
auth.set_access_token(oauth['token_key'], oauth['token_secret'])
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# create geolocator
geolocator = Nominatim()

# create Map
map = folium.Map()


# def initialize():
def define_coords(location):
    """
    (str) -> tuple

    Generate coordinates for given location

    :param location: the place where movie was filmed

    :return:
    (tuple) coordinates
    """
    try:
        result = geolocator.geocode(location, timeout=500000)
        if result:
            return result.latitude, result.longitude
        else:
            result = geolocator.geocode(location[location.find(',') + 1:],
                                        timeout=500000)
            if result:
                return result.latitude, result.longitude
    except geopy.exc.GeopyError as error:
        return


def read_friends(nickname, limit):
    return api.friends_ids(screen_name=nickname, count=limit)['ids']


def check_user(nickname):
    try:
        api.get_user(screen_name=nickname)
    except tweepy.error.TweepError:
        return 'unknown user'


def get_locations(friends_ids):
    lst = []
    for id in friends_ids:
        user = api.get_user(id)
        if user['location']:
            coords = define_coords(user['location'])
            if coords is None:
                continue
            dct = {"nickname": user['screen_name'],
                   "location": user['location'],
                   "coords": coords,
                   "img": user['profile_image_url_https']}
            lst.append(dct)
    return lst


popup = '''
<div style="display:flex;flex-direction:column;justify-content:center;">
  <img src="{}">
  <div>
    {},
  </div>
  <div>
    {}
  </div>
</div>'''


def create_markers(friends):
    for friend in friends:
        values = list(friend.values())
        values = values[-1:] + values[0:2]
        map.add_child(folium.Marker(location=friend['coords'],
                                    popup=popup.format(*values),
                                    icon=folium.Icon()))


def init(nickname, limit):
    check = check_user(nickname)
    if check:
        return check

    friends = read_friends(nickname, limit)
    friends = get_locations(friends)
    create_markers(friends)
    map.save('templates/Map.html')
