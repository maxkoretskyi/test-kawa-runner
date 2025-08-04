import pandas as pd

from kywy.client.kawa_decorators import kawa_tool
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from msal import ConfidentialClientApplication

def get_todo_title(todo_id: int) -> str:
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    response = requests.get(url)

    if response.ok:
        return response.json().get("title", "No title found")
    else:
        raise Exception(f"Failed to fetch todo (status code {response.status_code})")


def send_teams_message(
    message="💬 Hello from Bot Assistant! This message was sent from a background Python script."
):
    # === App Registration Info ===
    TENANT_ID = "25b6f03d-f689-4c11-b93e-48feb473fa95"
    CLIENT_ID = "27679395-988e-4c4a-bea6-8dae982f5d03"

    part1 = "Rpq8Q"
    part2 = "~r6gfwSA3bejWbGlw"
    part3 = "TA-mHHL3WQOZ4"
    part4 = "OYaBL"

    CLIENT_SECRET = part1 + part2 + part3 + part4
    AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

    # === Bot user credentials ===
    BOT_USERNAME = "bot@indepthdev.onmicrosoft.com"
    BOT_PASSWORD = "M.430057270212az"

    # === Recipient user info ===
    RECIPIENT_ID = "43e8deb0-6a39-49c0-ad9b-ee665c8fa35f"  # Main user ID
    BOT_ID = "1aced1f7-efd0-4106-bc75-1eb16db237b5"        # Bot user ID

    # === Required delegated scopes ===
    SCOPES = ["Chat.ReadWrite", "Chat.Create", "User.Read"]

    # === Authenticate using username + password ===
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=AUTHORITY
    )

    result = app.acquire_token_by_username_password(
        username=BOT_USERNAME,
        password=BOT_PASSWORD,
        scopes=SCOPES
    )

    if "access_token" not in result:
        print("❌ Failed to acquire token:", result.get("error_description"))
        return

    access_token = result["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # === Step 1: Create a 1:1 chat ===
    chat_body = {
        "chatType": "oneOnOne",
        "members": [
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{RECIPIENT_ID}')"
            },
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{BOT_ID}')"
            }
        ]
    }

    chat_resp = requests.post(
        "https://graph.microsoft.com/v1.0/chats",
        headers=headers,
        json=chat_body
    )

    if chat_resp.status_code != 201:
        print(f"❌ Failed to create chat ({chat_resp.status_code}):")
        print(chat_resp.json())
        return

    chat_id = chat_resp.json()["id"]
    print(f"✅ Chat created: {chat_id}")

    # === Step 2: Send a message ===
    msg_body = {
        "body": {
            "content": message
        }
    }

    msg_resp = requests.post(
        f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages",
        headers=headers,
        json=msg_body
    )

    if msg_resp.status_code != 201:
        print(f"❌ Failed to send message ({msg_resp.status_code}):")
        print(msg_resp.json())
    else:
        print("✅ Message sent successfully!")


def send_message_to_user(slack__bot_token, msg):
    user_id = "U08UG5LUKFT"
    message_text = "Hi Max, Kawa welcomes you! " + msg

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


@kawa_tool(inputs={'measure1': float}, outputs={'message': str}, secrets={'token': 'slack__bot_token'}, parameters={'msg': {'type':str}})
def execute_new_decorator(df: pd.DataFrame, token, msg):
    print('run: simple_join_script')
    print('[1]: Data from KAWA')
    print(df)
    send_message_to_user(token, msg)
    # send_teams_message("📣 Hello from Kawa!")
    title = get_todo_title(1)
    df['message'] = "hardcore"
    print('[2]: Data after script operation')
    print(df)
    return df
