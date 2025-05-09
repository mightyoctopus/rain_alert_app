import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

#--------------------------------- Kakao API Authorization -- To Get Access Token --------------------------------------------#

## STEP-BY-STEP PROCESS:
# 1. Get the authorization code via user login and consent
# 2. Exchange the authorization code for an access token
# 3. Call the Kakao Friends List API to retrieve friend UUIDs
# 4. Use the Send Message API to deliver a message to a specific friend

# url = "https://kauth.kakao.com/oauth/token"
# rest_api_key = "09a6494f5f986e27a017d180485f4ebe"
# redirect_url = "https://example.com/oauth"
# authorization_code = "t7nc9Akdf_WQfyb2jqRMt7FpYZlCEX-aHlzGVS1sSlfnlKSG-eIyeAAAAAQKFxKWAAABlrCJUu5Dz1szkZmFRA"
#
# params = {
#     'grant_type': 'authorization_code',
#     'client_id': rest_api_key,
#     'redirect_uri': redirect_url,
#     'code': authorization_code,
# }
#
# response = requests.post(url, params=params)
# tokens = response.json()
# print("KAKAO TOKENS: ", tokens)
#
#
# json_data_path = "./data/kakao_tokens.json"
# with open(json_data_path, "w") as fp:
#     json.dump(tokens, fp, indent=2)




# #------------------------------------- Kakao API Processing ------------------------------------------#

REST_API_KEY = os.getenv("REST_API_KEY")
TOKEN_FILE_PATH = "./data/kakao_tokens.json"

def refresh_access_token(tokens):
    print("Access token expired -- refreshing...")
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": REST_API_KEY,
        "refresh_token": tokens["refresh_token"]
    }
    response = requests.post(url, data=data)
    new_data = response.json()
    print("REFRESH RESPONSE: ", new_data)

    if "access_token" in new_data:
        tokens["access_token"] = new_data["access_token"]
        if "refresh_token" in new_data:
            tokens["refresh_token"] = new_data["refresh_token"]

        with open(TOKEN_FILE_PATH, "w") as file:
            json.dump(tokens, file, indent=2)

        print("Access token refreshed.")
        return tokens
    else:
        print("Failed to refresh token.")
        return None

# ### TESTING -- Refresh Access Token
# with open("./data/kakao_tokens.json") as file:
#     data = json.load(file)
#     refresh_access_token(data)


def get_friend_uuid():
    # Refresh the token everytime before the friend UUID retrieval process

    with open("./data/kakao_tokens.json") as token_file:
        data = json.load(token_file)
        tokens = refresh_access_token(data)

    ## Friend's UUID endpoint
    friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

    # Set the request headers to prove who you are
    headers = {"Authorization": "Bearer" + " " + tokens["access_token"]}
    print("HEADERS: ", headers)

    response = requests.get(friend_url, headers=headers)
    result = response.json()
    print("Friend API Response: ", result)

    friends_list = result.get("elements")

    if not friends_list:
        print("No friends found.")
        return None

    friend_id = friends_list[0].get("uuid")
    return friend_id

# uuid = get_friend_uuid()
# if uuid:
#     print("Friend UUID: ", uuid)


def send_message():
    friend_id = get_friend_uuid()

    with open("./data/kakao_tokens.json") as token_file:
        data = json.load(token_file)
        tokens = data["access_token"]

    headers = {"Authorization": "Bearer " + tokens}

    # Message-Sending API
    send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

    ## Convert dictionary to the json format again before requesting to the server
    data={
        "receiver_uuids": json.dumps([friend_id]),
        "template_object": json.dumps({
            "object_type":"text",
            "text":"앞으로 12시간 이내에 비가 옵니다🌧️🌧️. 우산을 챙기세요.☂️☂️☂️☂️",
            "link":{
                "web_url":"www.daum.net",
                "mobile_web_url":"www.naver.com"
            },
            "button_title": "바로 확인"
        })
    }

    response = requests.post(send_url, headers=headers, data=data)
    return response

send_message()