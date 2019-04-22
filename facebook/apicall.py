import facebook
import requests
from fbchat import Client
from fbchat.models import *
client = Client('FoodFriendEmail','FoodFriendPassword')

token = '339457186920319|7XyqpNHlCSlzdCXFGxfEZLPyQU0'
graph = facebook.GraphAPI(access_token=token, version = 3.1)
users = 'https://graph.facebook.com/v3.1/app/accounts/test-users?access_token='+token
users = requests.get(users)
users = users.json()
users_data=[]



for u in range(len(users['data'])):
    attributes=['id','name','location','friends']
    user_token=users['data'][u]['access_token']
    call_me="https://graph.facebook.com/v2.11/me?fields=name&access_token="+user_token
    call_location="https://graph.facebook.com/v2.11/me?fields=location&access_token="+user_token
    call_friends="https://graph.facebook.com/v2.11/me?fields=friends&access_token="+user_token
    id =requests.get(call_me).json()['id']
    name=requests.get(call_me).json()['name']
    location=requests.get(call_location).json()
    raw_friends=requests.get(call_friends).json()
    raw_friends=raw_friends['friends']['data']
    friends=[]
    for f in raw_friends:
        friends.append(f['id'])
    values=[id, name, location, friends]
    user=dict(zip(attributes, values))
    users_data.append(user)


users = client.searchForUsers('YourFriend')
#print('users:', users)
user = users[0]
user_id = user.uid
print("User's ID: {}".format(user.uid))
print("User's name: {}".format(user.name))
print("User's profile picture url: {}".format(user.photo))
print("User's main url: {}".format(user.url))
client.send(Message(text='Hi! Lets eat!'), thread_id=user_id, thread_type=ThreadType.USER)
client.logout()