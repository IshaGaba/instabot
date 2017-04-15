import requests
App_Access_token = "2247652388.61a4075.a8ace6f81850450683de586106907181" #access_token
BASE_URL = "https://api.instagram.com/v1/" #common url

def going_right_or_wrong(data):
    right = data['meta']['code']
    if right == 200:
        print ("successfully found user id and fetched user's post id ")
    else:
        print ("unsuccessful plz check user name again")


def info_owner():  # using get to collect owner information
    url_owner = BASE_URL + "users/self/?access_token=" + App_Access_token
    owner_info = requests.get(url_owner).json()
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OWNER INFORMATION:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("owner id is " + owner_info["data"]['id'])
    print ("owner full name is " + owner_info["data"]["full_name"])
    print ("owner bio is " + owner_info["data"]["bio"])
    print ("owner usename is " + owner_info["data"]["username"])
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



def get_user_id_username(user_name):  # get user id
    url_user = BASE_URL + "users/search?q=" + str(user_name) + "&access_token=" + App_Access_token  # https://api.instagram.com/v1/users/search?q=jack&access_token=ACCESS-TOKEN
    user_info = requests.get(url_user).json()
    going_right_or_wrong(user_info)
    return user_info["data"][0]["id"]

def get_post_id(user_name):
    user_id = get_user_id_username(user_name)
    user_url = BASE_URL + "users/" + str(user_id) + "/media/recent/?access_token=" + App_Access_token  # https://api.instagram.com/v1/users/{user-id}/media/recent/?access_token=ACCESS-TOKEN
    request_for_post = requests.get(user_url).json()
    if len(request_for_post["data"]) == 0:
        print ("user has no post")
    else:
        print ('we have total ' + str(len(request_for_post)) + ' posts of :' + str(user_name) + '\nWhich post you want to choose?')
        post_no = int (input("Enter your choice:"))
        post_no= (post_no-1)
        going_right_or_wrong(request_for_post)
    return request_for_post["data"][post_no]['id']

def like_user_post(user_name):
    post_id = get_post_id(user_name)
    Access_token = {'access_token': App_Access_token}
    url_post_like = BASE_URL + "media/" + str(post_id) + "/likes"
    like = requests.post(url_post_like, Access_token).json()
    going_right_or_wrong(like)


def comment_on_user_id(user_name):
    post_id = get_post_id(user_name)
    # post_id which is getting from  funn <<<user_post_id>>>
    print ("write your comment u want to post: ")
    entered_comment = input()  # getting comment which user want to write on post
    url_comment = BASE_URL + "media/" + str(post_id) + "/comments"
    Access_token_Plus_comment = {'access_token': App_Access_token, 'text': entered_comment}
    comment_result = requests.post(url_comment, Access_token_Plus_comment).json()  # posting comment on pic
    going_right_or_wrong(comment_result)


def search_comment(user_name):  # is using for searching a perticular comment of user choice
    post_id = get_post_id(user_name)
    print ("Type the word you want to search comment")
    search = input()  # getting comment which user want to search on post
    search_comments = BASE_URL + "media/" + str(post_id) + "/comments?access_token=" + App_Access_token
    find_comments = requests.get(search_comments).json()
    list_comments_id = []
    list_comments = []
    user_name = []
    for each in find_comments['data']:
        list_comments.append(each['text'])
        list_comments_id.append(each['id'])
        user_name.append(each['from']['username'])
    comments_id_found = []
    comments_found = []
    user_found = []
    for each_item in range(len(list_comments)):  # Loop to look for the comment that contains the specified word
        if search in list_comments[each_item]:
            comments_found.append(list_comments[each_item])
            comments_id_found.append(list_comments_id[each_item])
            user_found.append(user_name[each_item])
    if len(comments_found) == 0:  # No comment Found
        print ("No comment have such word")
        return post_id, False
    else:  # Comment found!
        print ("Following are the comments that contains the word:")
        for i in range(len(comments_found)):
            print (comments_found[i])
        return post_id, comments_id_found


def delete_comment(user_name):
    media_id, comment_id = search_comment(user_name)
    word_to_be_searched = input("Re-Enter the word you searched for so as to delete the comment containing it: ")
    if not comment_id:
        return False
    else:
        for each_item in range(len(comment_id)):
            url = BASE_URL + "media/" + str(media_id) + "/comments/" + str(
                comment_id[each_item]) + "/?access_token=" + App_Access_token
            info_to_delete = requests.delete(url).json()  # Delete call to delete comment.
    going_right_or_wrong(info_to_delete)


def find_average(username):
    post_id = get_post_id(username)
    no_of_words = 0
    list_of_comments = []
    comment_id = []
    url = BASE_URL + "media/" + str(post_id) + "/comments/?access_token=" + App_Access_token
    data = requests.get(url).json()
    if len(data['data']) == 0:
        print("no comments on this post")
        return
    else:
        for comment in data['data']:
            list_of_comments.append(comment['text'])  # making a list if comments
            # print list_of_comments
            no_of_words += len(comment['text'].split())  # calculating words in comment without counting spaces
            # print no_of_words
        average_words = float(no_of_words) / len(list_of_comments)
        print("\nAverage on the post = %.2f" % average_words)
        return


def main():
    info_owner()  # calling funn to print owner information
    Variable1 = "y"
    while Variable1 == "y":
        print ("Type the username from following \n-> gabaishu7596  \n-> shivtaj21   ")
        user_name = input()
        print ("select what do you want to do \n1:like \n2:comment \n3:search a word \n4:delete a comment ")
        print ("5:average of words of comment on post")  # choice what user want to do
        choice = input("your option: ")
        if choice == "1":
            like_user_post(user_name)  # for like a pic
        elif choice == "2":
            comment_on_user_id(user_name)  # comment on pic
        elif choice == "3":
            search_comment(user_name)  # searching commnet on pic
        elif choice == '4':
            delete_comment(user_name)  # deleting comment on pic
        elif choice == '5':
            find_average(user_name)  # finding average
        else:
            print ("you chose wrong")
        print (" press any key for exit or press y to continue ")  # choice he want to do again or not
        Variable1 = input()
    print ("________________________THANK YOU_________________________")


main()

