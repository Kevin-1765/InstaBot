# Importing requests for accessing the web urls
import requests

# Importing matplotlib,numpy for plotting the pie graph
import matplotlib.pyplot as plt
import numpy as np

# Importing urllib to retrieve the image url
import urllib

# Importing TextBlob from textblob to analyze the text
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

# Importing the ACCESS TOKEN from keys.py file
from keys import ACCESS_TOKEN

# Defining the BASE URL
BASE_URL = 'https://api.instagram.com/v1'

'''
Function for getting the owner info (yourself)
'''


def self_info():

    request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    my_info = requests.get(request_url).json()
    # Checking if the return meta code is 200
    if my_info['meta']['code'] == 200:
        # If the data of user  exist
        if len(my_info['data']):
            print 'Username : %s' % (my_info['data']['username'])
            print 'Full Name : %s' % (my_info['data']['full_name'])
            print 'No. of followers are : %s ' % (my_info['data']['counts']['followed_by'])
            print 'No. of peoples you are following : %s' % (my_info['data']['counts']['follows'])
            print 'No of posts : %s' % (my_info['data']['counts']['media'])

        else:
            print 'User does not exist'
    else:
        print 'Received Meta Code is ' + my_info['meta']['code']


'''
Function definition to get a user id using Instagram username
'''


def get_user_id(insta_username):

    request_url = BASE_URL + '/users/search?q=%s&access_token=%s' % (insta_username, ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    user_info = requests.get(request_url).json()
    # Checking if returned meta code is 200 or not
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            # Returning the user id
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Received Meta Code is ' + user_info['meta']['code']


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
        # Checking if meta code received is 200
        if user_info['meta']['code'] == 200:
            if len(user_info['data']):
                # Printing user info
                print 'Username : %s' % (user_info['data']['username'])
                print 'Full Name :%s' % (user_info['data']['full_name'])
                print 'No of peoples He/She is following : %s ' % (user_info['data']['counts']['follows'])
                print 'No. of peoples following him/her are: %s' % (user_info['data']['counts']['followed_by'])
                print 'No of posts : %s' % (user_info['data']['counts']['media'])
            else:
                print 'User have no data!'
        else:
            print 'Received Meta Code is ' + user_info['meta']['code']

'''
Function to get the recent post of the owner
'''


def get_own_post():

    request_url = BASE_URL+'/users/self/media/recent/?access_token=%s' % (ACCESS_TOKEN)
    print 'GET request url : %s' % request_url
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            # Getting the image name as same as the post id
            image_name = own_media['data'][0]['id'] + '.jpeg'
            # Getting the image url from instagram database
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            # Using urllib downloading the image from the url and saving it with image_name name
            urllib.urlretrieve(image_url, image_name)
            print 'Your recent post is downloaded'
            return 'Here is your post id '+own_media['data'][0]['id']
        else:
            return 'Hmm!! looks like you do not have any post'
    else:
        print 'Received Meta Code is' + own_media['meta']['code']

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
        if user_media['meta']['code'] == 200:
            if len(user_media['data']):
                # Providing search criteria
                print 'You can refine your search more precisely'
                print '1. Post with Minimum likes\n' \
                      '2. Post with Maximum likes\n' \
                      '3. Post with a certain Caption\n' \
                      '4. Just Recent one'
                option = int(raw_input('Enter the choice'))
                # Declaring a variable will be used as id of a post
                i = -1
                if option == 1:
                    like = ''
                    for x in range(0, len(user_media['data'])):
                        # Comparing likes on a post
                        if user_media['data'][x]['likes']['count'] < like:
                            like = user_media['data'][x]['likes']['count']
                            i = x

                elif option == 2:
                    like = -1
                    for x in range(0, len(user_media['data'])):
                        # Comparing likes on a post
                        if user_media['data'][x]['likes']['count'] > like:
                            like = user_media['data'][x]['likes']['count']
                            i = x

                elif option == 3:
                    caption = raw_input('Enter the caption')
                    for x in range(0, len(user_media['data'])):
                        text = user_media['data'][x]['caption']['text']
                        # Checking if the entered caption is present in all the captions
                        if caption.lower() in text.lower():
                            i = x

                    if i is -1:
                        print 'No such caption present'
                        exit()

                elif option == 4:
                    # Assigning 0 to i i.e id of recent post
                    i = 0

                else:
                    print 'Wrong choice made'
                if i >= 0:
                    # Getting the image name as same as the post id
                    image_name = user_media['data'][i]['id'] + '.jpeg'
                    # Getting the url of image from the instagram
                    image_url = user_media['data'][i]['images']['standard_resolution']['url']
                    # Downloading the image from image_url and saving it with image_name name.
                    urllib.urlretrieve(image_url, image_name)
                    print 'User\'s recent post is downloaded'
                    return user_media['data'][i]['id']
            else:
                return 'He/She does not have any post !'
        else:
            print 'Received Meta Code is' + user_media['meta']['code']

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
                # Returning the user's recent post id
                return user_media['data'][0]['id']
            else:
                print 'User does not have any post!'
                exit()
        else:
            print 'Received Meta Code is ' + user_media['meta']['code']


'''
Function to like a post
'''


def like_a_post(insta_username):

    media_id = get_user_post_id(insta_username)
    request_url = BASE_URL+'/media/%s/likes' % (media_id)
    print 'POST request url : %s' % request_url
    payload = {"access_token": ACCESS_TOKEN}
    # Setting a like on a user's recent post
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
    comment = requests.get(request_url).json()
    if comment['meta']['code'] == 200:
        if len(comment['data']):
            print 'Here are the comments :'
            for x in range(0, len(comment['data'])):
                # Printing the comment posted on a post
                print comment['data'][x]['text']
        else:
            print 'There are no comments on this post'
    else:
        print 'No media available !'

'''
Function to comment on a post
'''


def comment_on_post(insta_username):

    media_id = get_user_post_id(insta_username)
    print 'Comment length should not exceed by 300, Can not have more than 4 # tags and in all Capital letters\n'
    comment = raw_input('Add a comment...')
    request_url = BASE_URL+'/media/%s/comments' % (media_id)
    print 'POST request url : %s' % request_url
    payload = {'access_token': ACCESS_TOKEN, 'text': comment}
    # Posting a comment on post
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
            print 'Post id :'+recent_media['data'][0]['id']
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
            print 'Post id he/she liked recently'+ recent_media['data'][0]['id']
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
        neg = 0
        pos = 0
        if comment_info['meta']['code'] == 200:
            if len(comment_info['data']):
                for x in range(0, len(comment_info['data'])):
                    comment_id = comment_info['data'][x]['id']
                    comment_text = comment_info['data'][x]['text']
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                    if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                        neg = +1
                        print 'Negative comment : %s' % (comment_text)
                        delete_url = BASE_URL + '/media/%s/comments/%s/?access_token=%s' % (media_id,comment_id,ACCESS_TOKEN)
                        print 'DELETE request url : %s' % (delete_url)
                        delete_info = requests.delete(delete_url).json()

                        if delete_info['meta']['code'] == 200:
                            print 'Comment successfully deleted!\n'
                        else:
                            print 'Unable to delete comment!'
                    else:
                        pos = +1
                        print 'Positive comment : %s\n' % (comment_text)
                query = raw_input('Do you want to plot the data on a pie chart (y/n) ?')
                if query.upper() == 'Y':
                    labels = 'Positive', 'Negative'
                    sizes = [pos, neg]
                    explode = (0, 0)
                    fig1, ax1 = plt.subplots()
                    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
                    # Equal aspect ratio ensures that pie is drawn as a circle.
                    ax1.axis('equal')
                    plt.show()
            else:
                print 'There are no existing comments on the post!'
        else:
            print 'Received status code is ' + comment_info['meta']['code']


def search_by_hashtag(tag_name):

    request_url = BASE_URL+'/tags/search?q=%s&access_token=%s' % (tag_name, ACCESS_TOKEN)
    tag_info = requests.get(request_url).json()
    if tag_info['meta']['code'] == 200:
        label = []
        tags = []
        if len(tag_info['data']):
            # Getting the count of post with a particular Hashtag
            # NOTE Only 10 different Hash Tags will be displayed in Bar Chart
            for x in range(0, 10):
                label.insert(x, tag_info['data'][x]['name'])
                tags.insert(x, tag_info['data'][x]['media_count'])

            y_pos = np.arange(len(label))
            plt.bar(y_pos, tags, align='center', alpha=0.8)
            plt.xticks(y_pos, label)
            plt.ylabel('Number of posts shared with the Hashtag '+tag_name)
            plt.show()

    else:
        print 'There are no post with this tag'''
'''
The main function
'''


def start():

    while True:
        print '\nWelcome to Instagram PhotoBot'
        print 'Menu:'
        print '1.  Get your own details'
        print '2.  Get your friend\'s details'
        print '3.  Download your recent post'
        print '4.  Download your friend\'s post'
        print '5.  Like a post'
        print '6.  Comment on a post'
        print '7.  Find out what you have liked recently'
        print '8.  Find out what your friend have liked recently'
        print '9.  Delete the negative comments from your post'
        print '10. Get the comment list on post'
        print '11. Find out how many post are shared using a Hash Tag'
        print '12. Exit'
        option = int(raw_input('Enter your choice : '))

        if option == 1:
            print 'Here is your information :'
            self_info()

        elif option == 2:
            username = raw_input('Enter your friends name :')
            user_info(username)

        elif option == 3:
            get_own_post()

        elif option == 4:
            username = raw_input('Enter your friends name :')
            get_user_post(username)

        elif option == 5:
            query = raw_input('Do you want to like your own post (y/n) ?')
            if query.upper() == 'Y':
                request_url = BASE_URL+'/users/self/?access_token=%s' % (ACCESS_TOKEN)
                username = requests.get(request_url).json()
                like_a_post(username['data']['username'])
            elif query.upper() == 'N':
                print 'Enter the friend\'s name who\'s post you wanna like : '
                username = raw_input()
                like_a_post(username)
            else:
                print 'Wrong choice !'

        elif option == 6:
            query = raw_input('Do you want to comment on your own post (y/n) ?')
            if query.upper() == 'Y':
                request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
                username = requests.get(request_url).json()
                comment_on_post(username['data']['username'])
            elif query.upper() == 'N':
                print 'Enter the friend\'s name on who\'s post you wanna comment : '
                username = raw_input()
                comment_on_post(username)
            else:
                print 'Wrong choice !'

        elif option == 7:
            own_media_liked()

        elif option == 8:
            username = raw_input('Enter your friends name : ')
            user_media_liked(username)

        elif option == 9:
            query = raw_input('Do you want to delete comments from your own post (y/n) ?')
            if query.upper() == 'Y':
                request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
                username = requests.get(request_url).json()
                del_negative_comment(username['data']['username'])
            elif query.upper() == 'N':
                print 'Enter the friend\'s name who\'s post from you wanna delete comments : '
                username = raw_input()
                del_negative_comment(username)
            else:
                print 'Wrong choice !'

        elif option == 10:
            query = raw_input('Do you want to get the comments from your own post (y/n) ?')
            if query.upper() == 'Y':
                request_url = BASE_URL + '/users/self/?access_token=%s' % (ACCESS_TOKEN)
                userdata = requests.get(request_url).json()
                username = userdata['data']['username']
                get_comment_list(username)
            elif query.upper() == 'N':
                print 'Enter the friend\'s name who\'s post from you wanna get the comments : '
                username = raw_input()
                get_comment_list(username)
            else:
                print 'Wrong choice !'

        elif option == 11:
            tag_name = raw_input('Enter the name of tag for which you want to search : ')
            search_by_hashtag(tag_name)

        elif option == 12:
            exit()

        else:
            print 'Wrong Choice !'
            exit()

start()
