import os
import json
import datetime
import urllib.request
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import openai

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]
SLACK_BOT_ID = os.environ["SLACK_BOT_ID"]
client = WebClient(token=SLACK_BOT_TOKEN)

def query_completion(prompt, model='text-davinci-003', temperature=0.9, max_tokens=1500, top_p=1, frequency_penalty=0.4, presence_penalty=0.2):
    estimated_prompt_tokens = int(len(prompt.split()) * 1.6)
    estimated_answer_tokens = 2049 - estimated_prompt_tokens
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=min(4096-estimated_prompt_tokens, max_tokens),
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    return response

def query_chat_completion(prompt, model='gpt-3.5-turbo', temperature=0.9, frequency_penalty=0.3):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        frequency_penalty=frequency_penalty
    )
    return response
    
def image_create(prompt):
    trans_req = 'Translate the following text to English:'+prompt
    trans_resp = query_chat_completion(trans_req)
    prompt = trans_resp['choices'][0]['message']['content'].strip()
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response
    
def post_slack_basic(response_message_ko):
    message = response_message_ko
    send_data = {
        "text": message,
        "challenge": message
    }
    send_text = json.dumps(send_data)
    request = urllib.request.Request(
        SLACK_WEBHOOK_URL, 
        data=send_text.encode('utf-8'), 
    )

    with urllib.request.urlopen(request) as response:
        slack_message = response.read()
    
welcome_text = "A) chatMST에 오신걸 환영합니다.\n사용법을 확인하려면 `help` 라고 쳐보세요."
help_text = "A) 사용법에 대해 알려 드리겠습니다.\n\n*[공통]*\n*chatMST를 사용하기 위해서는 저를 꼭 멘션해주세요* -> *`@chatMST`*\n\n*[QnA]*\n묻고 싶은 글을 자유롭게 작성해 주세요. 최대한 자세히 작성할수록 좋아요.```@chatMST 질문글```\n만약 저의 훈련 모델을 변경하고 싶다면 질문 글 제일 앞에 [model=davinch] 를 넣어주세요.(default model=gpt-3.5-turbo)\n```@chatMST [model=davinch] 질문글\n한글이 깨진다면 기본 모델에 글 복사하여 한국어로 번역을 요청해 보세요.```\n\n*[이미지 생성]*\n생성하고자 하는 이미지에 대한 설명 제일 앞에 [image=create] 를 넣어주세요.\n```@chatMST [image=create] 생성 이미지에 대한 설명글```\n\n*[이미지 편집]*\n-"

def lambda_handler(event, context):
    retry_num = '1'
    print(f"Init: {datetime.datetime.now()}")
    print(f"Event: {event}")
        
    openai.api_key = OPENAI_API_KEY
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
        # ,'body': ''
    }
    
    try:
        body = json.loads(event['body'])
        channel = body['event']['channel']
        
        if SLACK_CHANNEL == channel:
            if event['headers'].get('x-slack-retry-num') != 'None':
                retry_num = event['headers']['x-slack-retry-num']
            type = body['event']['type']
            prompt = body['event']['text']
            btype = body['type']
            print(f"retry num: {retry_num} /event type: {type} / body type: {btype}")
                
            max_tokens = 1500
            
            if type=='app_mention' and 'user' in body['event'] and re.match("^<@"+SLACK_BOT_ID+">", prompt) and 'A)' not in prompt and retry_num == '1':
                print(f"prompt1: {prompt}")
                prompt = prompt.replace("^<@"+SLACK_BOT_ID+">","")
                print(f"prompt2: {prompt}")
                
                if '[model=davinci]' in prompt:
                    prompt = prompt.replace("[model=davinci]","")
                    answer = query_completion(prompt)
                    answer_text = 'A) '+answer['choices'][0]['text'].strip() # davinci(completion)
                elif '[image=create]' in prompt:
                    prompt = prompt.replace("[image=create]","")
                    answer = image_create(prompt)
                    answer_text = answer['data'][0]['url']
                else:
                    answer = query_chat_completion(prompt)
                    answer_text = 'A) '+answer['choices'][0]['message']['content'].strip() # gpt-turbo(chat completion)
                print(f"answer_text: {answer_text}")
                response['body'] = json.dumps({'message': answer_text})
                post_slack_basic(answer_text)
            elif '에 참여했습니다.' in prompt and 'chatmst' in prompt:
                post_slack_basic(welcome_text)
            elif 'help' == prompt:
                post_slack_basic(help_text)
    except Exception as e:
        response['statusCode'] = 500
        response['body'] = json.dumps({'error': str(e)})
    
    return response