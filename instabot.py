#import requests library
import requests

#Import termcolor library
from termcolor import colored

APP_ACCESS_TOKEN = '2996685060.904631f.97cd5e6d8298465b9e6b668aa4a0c711'
#Token Owner : Sabha_11_
#Sandbox Users : friends usernames

BASE_URL = 'https://api.instagram.com/v1/'

#Function for getting own info

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Error due to Status code other than 200 received!'


# Function for getting the ID of a user


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

'''
Function declaration to get the info of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print colored('---There is no data for this user!---', 'red')
    else:
        print colored('---Status code other than 200 received!---', 'red') #error in code

def start_bot():
    while True:
        print '\n'
        print colored('Hello! ---Welcome to InstaBot---!','green')
        print colored('Menu options are:','blue')
        print colored("1.Get your own details\n",'blue')
        print colored("2.Get details of a user by username\n", 'blue')
        print colored("3.Exit", 'blue')

        choice=raw_input(colored("Enter you choice: ",'blue'))
        if choice=="1":
            self_info()
        elif choice=="2":
            insta_username = raw_input(colored("Enter the username of the user: ", 'blue'))
            get_user_info(insta_username)
        elif choice=="3":
            exit()
        else:
            print colored("Invalid choice", 'red')  #selected choice is wrong

start_bot()