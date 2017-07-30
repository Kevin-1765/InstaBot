# Project Instagram Bot
This project is using the APIs of Instagram.

# To genrate the ACCESS_TOKEN
Follow these steps to genrate your own access key to use Instagram API :-
1. Goto https://instagram.com/developer

2. Click on Manage Clients tab in the header.
3. If not already logged in, login in using your existing instagram account.
4. Click on Register a new client, the green colored button just below the header on the right.
5. Fill out the form with the valid url in the Valid redirect URIs field. The url can be different but try to use only one url.

    Ex: www.google.com, https://facebook.com, https://www.acadview.com 
6. Click on register.
7. Uncheck the “Disable implicit OAuth” under under the security tab.
8. Copy the client-id.
9. Replace CLIENT-ID and REDIRECT-URI, do not use the url directly, it won’t work. Run this in the browser:
    1. https://api.instagram.com/oauth/authorize/?
    2. client_id=CLIENT-ID
    3. &redirect_uri=REDIRECT-URI
    4. &response_type=token
    5. &scope=basic+public_content+likes+comments

		    Ex: https://api.instagram.com/oauth/authorize/?client_id=1234567890&redirect_uri=https://www.acadview.com&response_type=token&scope=basic+public_content+likes+comments
10. You will be redirected to: http://your-redirect-uri/#access_token=ACCESS-TOKEN

      Ex: https://www.acadview.com#access_token=596179601.03af553.4c01fa27c9014e84940a4ea6f59189af
11. Save the access token from the url in the python file. Name it as 'keys.py'

# Command for setup 
After you get your access key run the following commands in the terminal to install the python-libraries :-
1. pip install requests
2. pip install urllib
3. pip install matplotlib
4. pip install textblob

# To Run 
Write the following command in terminal :-

python instabot.py
