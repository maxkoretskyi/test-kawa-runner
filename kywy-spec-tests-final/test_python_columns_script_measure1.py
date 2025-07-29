import pandas as pd

from kywy.client.kawa_decorators import kawa_tool
from slack_sdk import WebClient
import requests

def get_todo_title(todo_id: int) -> str:
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"
    response = requests.get(url)

    if response.ok:
        return response.json().get("title", "No title found")
    else:
        raise Exception(f"Failed to fetch todo (status code {response.status_code})")

@kawa_tool(inputs={'measure1': float}, outputs={'message': str})
def execute_new_decorator(df: pd.DataFrame):
    print('run: simple_join_script')
    print('[1]: Data from KAWA')
    print(df)
    title = get_todo_title(1)
    df['message'] = title
    print('[2]: Data after script operation')
    print(df)
    return df
