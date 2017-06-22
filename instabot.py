import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from keys import ACCESS_TOKEN

BASE_URL = 'https://api.instagram.com/v1'

'''
Function for getting the owner info (yourself)
'''


def self_info():

    request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    my_info = requests.get(request_url).json()
    if my_info['meta']['code'] == 200:
        if len(my_info['data']):
            print 'Username : %s' % (my_info['data']['username'])
            print 'Full Name : %s' % (my_info['data']['full_name'])
            print 'No. of followers are : %s ' % (my_info['data']['counts']['followed_by'])
            print 'No. of peoples you are following : %s' % (my_info['data']['counts']['follows'])
            print 'No of posts : %s' % (my_info['data']['counts']['media'])
        else:
            print 'User does not exist'
    else:
        print 'Received Meta Code is other then 200'


'''
Function definition to get a user id using Instagram username
'''


def get_user_id(insta_username):

    request_url = BASE_URL + '/users/search?q=%s&access_token=%s' % (insta_username, ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Received Meta Code is other then 200'


'''
Function to get the user information
'''


def user_info(insta_username):

    user_id = get_user_id(insta_username)
    if user_id is None:
        print 'User does not exit'
        exit()
    else:
        request_url = BASE_URL + '/users/%s/?access_token=%s' % (user_id, ACCESS_TOKEN)
        print 'GET request url : %s' % request_url
        user_info = requests.get(request_url).json()
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                print 'Username : %s' % (user_info['data']['username'])
                print 'Full Name :%s' % (user_info['data']['full_name'])
                print 'He/She is following : %s peoples.' % (user_info['data']['counts']['followed_by'])
                print 'No. of peoples following him/her are: %s' % (user_info['data']['counts']['follows'])
                print 'No of posts : %s' % (user_info['data']['counts']['media'])
            else:
                print 'User have no data!'
        else:
            print 'Received Meta Code is other then 200'

'''
Function to get the recent post of the owner
'''


def get_own_post():

    request_url = BASE_URL+'/users/self/media/recent/?access_token=%s' % (ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Your recent post is downloaded'
            return 'Here is your post id '+own_media['data'][0]['id']
        else:
            return 'Hmm!! looks like you do not have any post'
    else:
        print 'Received Meta Code is other then 200'

'''
Function definition to get the recent post of the user 
'''


def get_user_post(insta_username):

    user_id = get_user_id(insta_username)
    if user_id is None:
        print 'User does not exit !'
        exit()
    else:
        request_url = BASE_URL + '/users/%s/media/recent/?access_token=%s' % (user_id, ACCESS_TOKEN)
        print 'GET request url : %s' % request_url
        user_media = requests.get(request_url).json()
        print user_media
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                image_name = user_media['data'][0]['id'] + '.jpeg'
                image_url = user_media['data'][0]['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)
                print 'User\'s recent post is downloaded'
                return 'Here is the post id '+ user_media['data'][0]['id']
            else:
                return 'He/She does not have any post !'
        else:
            print 'Received Meta Code is other then 200'

'''
Function to get the user's recent post id 
'''


def get_user_post_id(insta_username):

    user_id = get_user_id(insta_username)
    if user_id is None:
        print 'User does not exit'
        exit()
    else:
        request_url = BASE_URL + '/users/%s/media/recent/?access_token=%s' % (user_id, ACCESS_TOKEN)
        print 'GET request url : %s' % request_url
        user_media = requests.get(request_url).json()
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                return user_media['data'][0]['id']
            else:
                print 'User does not have any post!'
                exit()
        else:
            print 'Received Meta Code is other then 200'


'''
Function to like a post
'''


def like_a_post(insta_username):

    media_id = get_user_post_id(insta_username)
    request_url = BASE_URL+'/media/%s/likes' % (media_id)
    print 'POST request url : %s' % request_url
    payload = {"access_token": ACCESS_TOKEN}
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Hurray Post Liked'
    else:
        print 'Like Unsuccessful Try Again!'

'''
Function to get the comment list from a post
'''


def get_comment_list(insta_username):

    media_id = get_user_post_id(insta_username)
    request_url = BASE_URL+'/media/%s/comments?access_token=%s' % (media_id, ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    comments = requests.get(request_url).json()
    if comments['meta']['code'] == 200:
        if len(comments['data']['text']):
            print 'Here are the comments :'
            for x in range(0, len(comments['data'])):
                print comments['data'][x]['text']
        else:
            print 'There are no comments on this post'
    else:
        print 'No media available !'

'''
Function to comment on a post
'''


def comment_on_post(insta_username):

    media_id = get_user_post_id(insta_username)
    comment = raw_input('Add a comment...')
    request_url = BASE_URL+'/media/%s/comments' % (media_id)
    print 'POST request url : %s' % request_url
    payload = {'access_token': ACCESS_TOKEN, 'text': comment}
    post_comment = requests.post(request_url, payload).json()
    if post_comment['meta']['code'] == 200:
        print 'Commented Successful'
    else:
        print 'Unable to comment please try agin !'

'''
Function to get the recent media liked by owner
'''


def own_media_liked():

    request_url = BASE_URL+'/users/self/media/recent/?access_token=%s' % (ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    recent_media = requests.get(request_url).json()
    if recent_media['meta']['code'] == 200:
        if len(recent_media['data']):
            print recent_media['data'][0]['id']
        else:
            print 'You have not liked any media'
    else:
        print 'Meta Code Error!'

'''
Function to get the recent media like d by other user
'''


def user_media_liked(insta_username):

    user_id = get_user_id(insta_username)
    if user_id is None:
        print ' No such user'
        exit()
    request_url = BASE_URL+'/users/%s/media/recent/?access_token=%s' % (user_id, ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    recent_media = requests.get(request_url).json()
    if recent_media['meta']['code'] == 200:
        if len(recent_media['data']):
            return recent_media['data'][0]['id']
        else:
            return None
    else:
        print 'Meta Code Error!'

'''
Function to delete negative comments from a post
'''


def del_negative_comment(insta_username):

        media_id = get_user_post_id(insta_username)
        request_url = (BASE_URL + '/media/%s/comments/?access_token=%s') % (media_id, ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        comment_info = requests.get(request_url).json()

        if comment_info['meta']['code'] == 200:
            if len(comment_info['data']):
                for x in range(0, len(comment_info['data'])):
                    comment_id = comment_info['data'][x]['id']
                    comment_text = comment_info['data'][x]['text']
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                    if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                        print 'Negative comment : %s' % (comment_text)
                        delete_url = BASE_URL + '/media/%s/comments/%s/?access_token=%s' % (media_id,comment_id,ACCESS_TOKEN)
                        print 'DELETE request url : %s' % (delete_url)
                        delete_info = requests.delete(delete_url).json()

                        if delete_info['meta']['code'] == 200:
                            print 'Comment successfully deleted!\n'
                        else:
                            print 'Unable to delete comment!'
                    else:
                        print 'Positive comment : %s\n' % (comment_text)
            else:
                print 'There are no existing comments on the post!'
        else:
            print 'Status code other than 200 received!'


def promotional_comments(tag_name):
    request_url = BASE_URL+'/tags/%s/media/recent?access_token=%s' % (tag_name,ACCESS_TOKEN)


'''
The main function
'''


def start():

    print 'Welcome to Instagram PhotoBot'
    print 'Menu:'
    print 'a. Get your own details'
    print 'b. Get your friend\'s details'
    print 'c. Download your recent post'
    print 'd. Download your friend\'s recent post'
    print 'e. Like a post'
    print 'f. Comment on a post'
    print 'g. Find out what you have liked recently'
    print 'h. Find out what your friend have liked recently'
    print 'i. Delete the negative comments from your post'
    print 'j. Get the comment list on post'
    print 'k. Search by Hastag'
    print 'Exit'
    option = raw_input('Enter your choice : ')

    if option == 'a':
        print 'Here is your information :'
        self_info()

    elif option == 'b':
        username = raw_input('Enter your friends name :')
        user_info(username)

    elif option == 'c':
        get_own_post()

    elif option == 'd':
        username = raw_input('Enter your friends name :')
        get_user_post(username)

    elif option == 'e':
        query = raw_input('Do you want to like your own post? y/n')
        if query.upper() == 'Y':
            request_url = BASE_URL+'/users/self/?access_token=%s' % (ACCESS_TOKEN)
            username = requests.get(request_url).json()
            like_a_post(username['data']['username'])
        elif query.upper() == 'N':
            print 'Enter the friend\'s name who\'s post you wanna like'
            username = raw_input()
            like_a_post(username)
        else:
            print 'Wrong choice !'

    elif option == 'f':
        query = raw_input('Do you want to comment on your own post? y/n')
        if query.upper() == 'Y':
            request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
            username = requests.get(request_url).json()
            comment_on_post(username['data']['username'])
        elif query.upper() == 'N':
            print 'Enter the friend\'s name on who\'s post you wanna comment'
            username = raw_input()
            comment_on_post(username)
        else:
            print 'Wrong choice !'

    elif option == 'g':
        own_media_liked()

    elif option == 'h':
        username = raw_input('Enter your friends name')
        user_media_liked(username)

    elif option == 'i':
        query = raw_input('Do you want to delete comments from your own post? y/n')
        if query.upper() == 'Y':
            request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
            username = requests.get(request_url).json()
            del_negative_comment(username['data']['username'])
        elif query.upper() == 'N':
            print 'Enter the friend\'s name who\'s post from you wanna delete comments :'
            username = raw_input()
            del_negative_comment(username)
        else:
            print 'Wrong choice !'

    elif option == 'j':
        query = raw_input('Do you want to get the comments from your own post? y/n')
        if query.upper() == 'Y':
            request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
            username = requests.get(request_url).json()
            get_comment_list(username['data']['username'])
        elif query.upper() == 'N':
            print 'Enter the friend\'s name who\'s post from you wanna get the comments :'
            username = raw_input()
            get_comment_list(username)
        else:
            print 'Wrong choice !'

start()