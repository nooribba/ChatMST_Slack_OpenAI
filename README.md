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
  ![slack app setting](./imgs/Slack_App_Setting_1.PNG)

</div>
</details>

<details open>
<summary><font size="3em">AWS Lambda</font></summary>
<div markdown="1">

> * Lambda Layer 생성 및 추가
> * Lambda Function 생성
>   * Runtime: python3.9
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
>   * Lambda Layer 추가
>  * Lambda Code 작성
  
## Usage
* Slack 채널 내에서 <font size='3em' color="orange">help</font> 입력하면 사용법 안내
  ![help](./imgs/help.PNG)
* QnA
  * Default Model: gpt-3.5-turbo
  * Slack 채널에 추가한 Bot App을 멘션 후 질문글 작성
  ![help](./imgs/sample_qna1.PNG)
    * text-davinci-003 model로 변경 가능
      * Bot 멘션 후 <font color="orange">[model=davinci]</font> 뒤에 질문글 작성
* 이미지 생성
  * Model: DALL·E
  * Bot 멘션 후 <font color="orange">[image=create]</font> 뒤에 생성하고자 하는 이미지에 대한 설명글 작성
  ![help](./imgs/sample_qna2.PNG)
    * 내부적으로 [한글->영어로 번역 요청] + [이미지 생성 요청] 2번 요청에 의한 응답 처리
      * 영어로 요청 시 더 정확한 결과