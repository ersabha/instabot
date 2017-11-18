#import details file
import details

#import requests library
import requests

#import url library
import urllib

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


#Import termcolor library
from termcolor import colored, cprint

APP_ACCESS_TOKEN = '5699261293.09da3c1.b9271e354aab4544b08c07c2c16e81e6'
#Token Owner : rosetaylor1232
#Sandbox Users : saby_11_, im_mukeshdubey, simranbindal38, shreya1400, im_nikkimikki

BASE_URL = 'https://api.instagram.com/v1/'

#Function for getting own info

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:  #checking status code
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print colored('Error due to Status code other than 200 received!','red')


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


#Function declaration to get the info of a user by username

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200: #checking the status code
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people user is following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print colored('---There is no data for this user!---', 'red')
    else:
        print colored('---Status code other than 200 received!---', 'red') #error in code

#Function declaration to get your recent post
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','green')  # successfully downloaded image
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')


#Function declaration to get the recent post of a user by username
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!','red')
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','green')
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')


# function declaration to getting the post id
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()




#Function declaration to like the recent post of a user

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)

    #    passing the payloads
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:   #checking of status code
        print colored('Like was successful!','green')
    else:
        print colored('Your like was unsuccessful. Try again!','red')


# Defining the Function for getting like list
def get_like_list(insta_username):
    media_id = get_post_id(insta_username)  # Getting post id by passing the username
    request_url = BASE_URL + 'media/%s/likes?access_token=%s' % (media_id, APP_ACCESS_TOKEN)
    print colored('GET request url : %s', 'blue') % (request_url)
    like_list = requests.get(request_url).json()

    if like_list['meta']['code'] == 200:  # checking of status code
        if len(like_list['data']):
            position = 1
            print colored("List of people who Liked Your Recent post", 'blue')
            for users in like_list['data']:
                if users['username']!= None:
                    print position, colored(users['username'],'green')
                    position = position + 1
                else:
                    print colored('No one had liked Your post!', 'red')
        else:
            print colored("User Does not have any post",'red')
    else:
        print colored('Status code other than 200 recieved', 'red')


#Function declaration to Get the lists of comments on  the recent post of a user
def get_comment_list(insta_username):
    media_id = get_post_id(insta_username)  # Getting post id by passing the username
    request_url = BASE_URL + 'media/%s/comments?access_token=%s' % (media_id, APP_ACCESS_TOKEN)
    print colored('GET request url : %s\n', 'blue') % (request_url)
    comment_list = requests.get(request_url).json()

    if comment_list['meta']['code'] == 200:  # checking the status code .....
        if len(comment_list['data']):
            position = 1
            print colored("List of people who commented on Your Recent post", 'blue')
            for _ in range(len(comment_list['data'])):
                if comment_list['data'][position-1]['text']:
                    print colored(comment_list['data'][position-1]['from']['username'],'blue') +colored( ' said: ','blue') + colored(comment_list['data'][position-1]['text'],'blue')      #    Json Parsing ..printing the comments ..
                    position = position+1
                else:
                    print colored('No one had commented on Your post!\n', 'red')
        else:
            print colored("There is no Comments on User's Recent post.\n", 'red')
    else:
        print colored('Status code other than 200 recieved.\n', 'red')


#Function to make a comment on the recent post of the user
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")

    #    passing the payloads
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print colored("Successfully added a new comment!",'green')  # successfully addition of comment
    else:
        print colored("Unable to add comment. Try again!",'red')


#Function declaration to make delete negative comments from the recent post
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
# naive implementation to delete the negative comments
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print colored('There are no existing comments on the post!','red')
    else:
        print colored('Status code other than 200 received!','red')


# function for caption based comment - Extra Objective

# captions of a Token Owner posts = darshanraval, green, pizza

def get_post_by_caption(insta_username):
    caption = raw_input("Enter caption : ")
    user_id = get_user_id(insta_username)
    if user_id == None:
        cprint("This user doesn't exist in your sandbox list", 'red')
    request_url = BASE_URL + 'users/' + user_id + '/media/recent/?access_token=' + APP_ACCESS_TOKEN
    print('GET request url :', request_url)
    try:
        user_media = requests.get(request_url).json()
    except requests.exceptions.ConnectionError:
        cprint("Please check your internet connection",'red')
    item = 1
    if user_media['meta']['code'] == 200: # status code checking
        if len(user_media['data']):
            flag = False
            item = 1
            for post in user_media['data']:
                for sabha in post['tags']:
                    if sabha == caption:
                        flag = True
                        # counts the caption of existing posts and saves them
                        print item,colored("post Found and saved",'green')
                        image_name = str(item)+'.jpeg'
                        image_url = post['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        item +=1
            if (not flag):
                print colored("Caption not found",'red')
        else:
            print colored("User doesn't have any post\n", 'red')
    else:
        print(colored('Status code other than 200 received!\n', 'red'))


def start_bot():
    while True:
        print '\n'
        print colored('Hello! ---Welcome to InstaBot---!','green')
        print colored('Menu options are:','blue')
        print colored("1. To Get your own details\n",'blue')
        print colored("2. To Get details of a user by username\n", 'blue')
        print colored("3. To Get your own recent post\n",'blue')
        print colored("4. To Get the recent post of a user by username\n",'blue')
        print colored("5. To Get a list of people who have liked the recent post of a user\n",'blue')
        print colored("6. To Like the recent post of a user\n",'blue')
        print colored("7. To Get a list of comments on the recent post of a user\n",'blue')
        print colored("8. To Make a comment on the recent post of a user\n",'blue')
        print colored("9. To Delete negative comments from the recent post of a user\n",'blue')
        print colored("10. To Get post by particular caption-(EXTRA OBJECTIVE)",'green')
        print colored("11. To Exit The Menu", 'red')

# function calling according to the choice selection
        choice=raw_input(colored("Enter you choice: ",'blue'))
        if choice=="1":
            self_info()
        elif choice=="2":
            insta_username = raw_input(colored("Enter the username of the user: ", 'blue'))
            get_user_info(insta_username)
        elif choice == "3":
            get_own_post()
        elif choice == "4":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            get_user_post(insta_username)
        elif choice=="5":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice=="6":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="7":
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice=="8":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="9":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)
        elif choice == '10':
            insta_username = raw_input("Enter username : ")
            get_post_by_caption(insta_username)
        elif choice=="11":
            exit()
        else:
            print colored("Invalid choice", 'red')  #selected choice is wrong

start_bot()