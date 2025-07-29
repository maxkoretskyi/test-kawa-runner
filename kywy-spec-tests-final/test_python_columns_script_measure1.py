import pandas as pd

from kywy.client.kawa_decorators import kawa_tool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

def get_todo_title(todo_id: int) -> str:
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    response = requests.get(url)

    if response.ok:
        return response.json().get("title", "No title found")
    else:
        raise Exception(f"Failed to fetch todo (status code {response.status_code})")

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_message_to_user():
    part1 = "xoxb"
    part2 = "-8968190956241"
    part3 = "-9248869405735"
    part4 = "-9neb001gDIIPsNg8jcbyk0Yb"
    
    slack__bot_token = part1 + part2 + part3 + part4
    user_id = "U08UG5LUKFT"
    message_text = "Hi Max, Kawa welcomes you!"

    client = WebClient(token=slack__bot_token)

    try:
        dm_response = client.conversations_open(users=[user_id])
        dm_channel_id = dm_response["channel"]["id"]

        send_response = client.chat_postMessage(
            channel=dm_channel_id,
            text=message_text
        )

        print(f"✅ Message sent to user {user_id} in channel {dm_channel_id}: {send_response['ts']}")

    except SlackApiError as e:
        print(f"❌ Slack API error: {e.response['error']}")


@kawa_tool(inputs={'measure1': float}, outputs={'message': str})
def execute_new_decorator(df: pd.DataFrame):
    print('run: simple_join_script')
    print('[1]: Data from KAWA')
    print(df)
    send_message_to_user()
    title = get_todo_title(1)
    df['message'] = "hardcore"
    print('[2]: Data after script operation')
    print(df)
    return df
