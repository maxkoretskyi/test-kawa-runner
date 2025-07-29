import pandas as pd

from kywy.client.kawa_decorators import kawa_tool
from slack_sdk import WebClient

@kawa_tool(inputs={'measure1': float}, outputs={'message': str})
def execute_new_decorator(df: pd.DataFrame):
    print('run: simple_join_script')
    print('[1]: Data from KAWA')
    print(df)
    df['message'] = str(WebClient)
    print('[2]: Data after script operation')
    print(df)
    return df
