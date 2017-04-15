import requests
App_Access_token = "2247652388.61a4075.a8ace6f81850450683de586106907181" #access_token
BASE_URL = "https://api.instagram.com/v1/" #common url


def info_owner():  # using get to collect owner information
    url_owner = BASE_URL + "users/self/?access_token=" + App_Access_token
    owner_info = requests.get(url_owner).json()
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OWNER INFORMATION:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("owner id is " + owner_info["data"]['id'])
    print ("owner full name is " + owner_info["data"]["full_name"])
    print ("owner bio is " + owner_info["data"]["bio"])
    print ("owner usename is " + owner_info["data"]["username"])
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
