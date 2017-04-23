#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INSTABOT~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import requests # requests library added here
App_Access_token = "2247652388.61a4075.a8ace6f81850450683de586106907181" #access_token
BASE_URL = "https://api.instagram.com/v1/" #common url


# this func check the status
def going_right_or_wrong(data):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
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
    print ("owner usename is " + owner_info["data"]["username"])
    if owner_info["data"]["bio"] != "":
        print ("owner bio is " + owner_info["data"]["bio"])
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



def get_user_id_username(user_name):  # get user id
    url_user = BASE_URL + "users/search?q=" + str(user_name) + "&access_token=" + App_Access_token  # https://api.instagram.com/v1/users/search?q=jack&access_token=ACCESS-TOKEN
    user_info = requests.get(url_user).json()
    going_right_or_wrong(user_info)
    return user_info["data"][0]["id"]

# this func gets the post id
def get_user_post_id(username,choice=0):
    user_id1 = get_user_id_username(username)
    url_user1 = BASE_URL + "users/" + str(user_id1) + "/media/recent/?access_token=" + App_Access_token  # https://api.instagram.com/v1/users/{user-id}/media/recent/?access_token=ACCESS-TOKEN
    request_for_user_to_get_all_post = requests.get(url_user1).json()
    post_index = 0  # For most recent post
    like_list_on_each_post = []
    total_media=len(request_for_user_to_get_all_post["data"])
    if total_media == 0:
        print("\nThis User has no post!")
    else:
        for each_media in range(0, total_media):
            like_list_on_each_post.append(request_for_user_to_get_all_post['data'][each_media]['likes']['count'])
        if choice == 1:  # If we want least liked post to be liked
            least_count = min(like_list_on_each_post)
            post_index = like_list_on_each_post.index(least_count)
        if choice == 3:  # If we want most popular post to be liked
            most_count = max(like_list_on_each_post)
            post_index = like_list_on_each_post.index(most_count)
    print ("Link to the Media is ", request_for_user_to_get_all_post['data'][post_index]['link'])  # To print the link to a media.
    post_id = request_for_user_to_get_all_post["data"][post_index]['id']
    return post_id  # To return the particular media ID


# this func likes the post
def like_user_post(user_name,opt):
    post_id = get_user_post_id(user_name,opt)
    Access_token = {'access_token': App_Access_token}
    url_post_like = BASE_URL + "media/" + str(post_id) + "/likes"
    like = requests.post(url_post_like, Access_token).json()
    going_right_or_wrong(like)


# this func comments on the post
def comment_on_user_id(user_name):
    post_id = get_user_post_id(user_name,0)
    # post_id which is getting from  funn <<<user_post_id>>>
    print ("write your comment u want to post: ")
    entered_comment = input()  # getting comment which user want to write on post
    url_comment = BASE_URL + "media/" + str(post_id) + "/comments"
    Access_token_Plus_comment = {'access_token': App_Access_token, 'text': entered_comment}
    comment_result = requests.post(url_comment, Access_token_Plus_comment).json()  # posting comment on pic
    going_right_or_wrong(comment_result)


def search_comment(user_name):  # is using for searching a perticular comment of user choice
    post_id = get_user_post_id(user_name)
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
        return False, post_id, False
    else:  # Comment found!
        print ("Following are the comments that contains the word:")
        for i in range(len(comments_found)):
            print (comments_found[i])
        return comments_id_found, post_id, comments_found


# this func deletes the comment on the post
def delete_comment(user_name):
    comment_id, media_id, comment = search_comment(user_name)
    word_to_be_searched = input("Re-Enter the word you searched for so as to delete the comment containing it: ")
    if not comment_id:
        return False
    else:
        for each_item in range(len(comment_id)):
            url = BASE_URL + "media/" + str(media_id) + "/comments/" + str(
                comment_id[each_item]) + "/?access_token=" + App_Access_token
            info_to_delete = requests.delete(url).json()  # Delete call to delete comment.
            if info_to_delete['meta']['code'] == 200:
                print (comment[each_item] + " deleted")
                print ("Your task was successfully performed.")
                break
            elif info_to_delete['meta']['error_message'] == "You cannot delete this comment":  # By Default Error
                print (comment[each_item], " = ", info_to_delete['meta']['error_message'])
            else:
                print ("Sorry!!!\nYou faced an error while performing your task.\nTry again later!")


# this func finds the average word in all comments on a post
def find_average(username):
    post_id = get_user_post_id(username)
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


# this func is main working func
def main():
    info_owner()  # calling funn to print owner information
    Variable1 = "y"
    while Variable1 == "y" :
        print ("Type the username from following \n-> gabaishu7596  \n-> shivtaj21   ")
        user_name = input()
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("select what do you want to do \n1:like \n2:comment \n3:search a word \n4:delete a comment ")
        print ("5:average of words of comment on post")  # choice what user want to do
        choice = int(input("your option: "))
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        if choice == 1:
            print ("which post you want to like\n1.least popular\n2.recent media\n3.most popular")
            opt=int (input("your option: "))
            like_user_post(user_name,opt)  # for like a pic
        elif choice == 2:
            comment_on_user_id(user_name)  # comment on pic
        elif choice == 3:
            search_comment(user_name)  # searching commnet on pic
        elif choice == 4:
            delete_comment(user_name)  # deleting comment on pic
        elif choice == 5:
            find_average(user_name)  # finding average
        else:
            print ("you chose wrong")
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print (" press any key for exit or press y  to continue ")  # choice he want to do again or not
        Variable1 = input()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("_______________________________________________THANK YOU_________________________________________________")


main()

