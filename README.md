# ChatMST_Slack_OpenAI ![Generic badge](https://img.shields.io/badge/OpenAI-blue.svg) ![Generic badge](https://img.shields.io/badge/python-AWS_Lambda-darkgreen.svg) ![Generic badge](https://img.shields.io/badge/Slack-purple.svg) 

## About
* OpenAI ChatGPT API를 활용한 Slack 챗봇

## Prerequisite
<details open>
<summary><font size="3em">OpenAI API</font></summary>
<div markdown="1">

> * API Key 생성
>   * https://platform.openai.com/account/api-keys
> * API Reference
>   * https://platform.openai.com/docs/introduction

</div>
</details>

<details open>
<summary><font size="3em">Slack</font></summary>
<div markdown="1">

> * Workspace 생성
> * App 생성
>   * https://api.slack.com/apps
> * Bot App 추가
> * App 세팅
>   * OAuth Token
>   * Incoming Webhooks
>   * Event Subscriptions
  ![slack app setting](https://user-images.githubusercontent.com/40586079/230657106-071a7f31-a3cf-4b2f-b5b6-eb61943b1366.png)

</div>
</details>

<details open>
<summary><font size="3em">AWS Lambda</font></summary>
<div markdown="1">

> * Lambda Layer 생성 및 추가
>   * OpenAI API 사용을 위한 python module(zip)
> * Lambda Function 생성
>   * Runtime: python 3.9
> * Lambda 세팅
>   * Time Limit(1분 이상)
>   * Memory(256MB 이상)
>   * 권한 IAM Role
>   * 환경변수
>     * SLACK_BOT_ID
>     * SLACK_BOT_TOKEN
>     * SLACK_WEBHOOK_URL
>     * SLACK_CHANNEL
>     * OPENAI_API_KEY
>  * Lambda Code 작성 배포
  
## Usage
* Slack 채널 내에서 <font size='3em' color="orange">help</font> 입력하면 사용법 안내
  ![help](https://user-images.githubusercontent.com/40586079/230657323-16037253-82ad-4e1b-9c57-cfe25431ef95.png)
* QnA
  * Default Model: gpt-3.5-turbo
  * Slack 채널에 추가한 Bot App을 멘션 후 질문글 작성
  ![help](https://user-images.githubusercontent.com/40586079/230658169-f7d820ad-9594-4de8-b425-6fcfdd2c57f2.png)
    * text-davinci-003 model로 변경 가능
      * Bot 멘션 후 <font color="orange">[model=davinci]</font> 뒤에 질문글 작성
* 이미지 생성
  * Model: DALL·E
  * Bot 멘션 후 <font color="orange">[image=create]</font> 뒤에 생성하고자 하는 이미지에 대한 설명글 작성
  ![help](https://user-images.githubusercontent.com/40586079/230657490-ab5652a5-c1f7-41fe-84dd-2a8c76f04fe8.png)
    * 내부적으로 [한글->영어로 번역 요청] + [이미지 생성 요청] 2번 요청에 의한 응답 처리
      * 영어로 요청 시 더 정확한 결과