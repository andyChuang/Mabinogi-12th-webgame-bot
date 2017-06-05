# Mabinogi-12th-webgame-bot

瑪奇十二週年樂園(https://tw.event.beanfun.com/mabinogi/e20170511/index.aspx)

因為這大概只有台版才有吧，我也不曉得為什麼突然冒出個網頁小遊戲，所以Readme直接用中文寫也沒關係吧XD

目前功能有（皆支援多帳號）：
1. 登入，停三秒後就換下一帳號
2. 擲骰子，每次都幫你登入然後每隔2~5秒幫你玩一次直到沒錢

若有想要什麼其他的或功能請留issue，不過寫完時大概活動也結束了XD

## Quick Start
0. 首先你要有裝python
1. Clone this repository to wherever you want
2. `cd Mabinogi-12th-webgame-bot`
2. `pip install -r requirement.txt`
3. 同目錄下建立`account.json`，格式如下：
```
[
    {
        "account": "帳號1",
        "password": "密碼1",
        "game_account": "遊戲帳號1"
    },
    {
        "account": "帳號2",
        "password": "密碼2",
        "game_account": "遊戲帳號2"
    },
    .
    .
    .
    {
        "account": "帳號N",
        "password": "密碼N",
        "game_account": "遊戲帳號N"
    }
]
```
5. python play.py 
    - --game_type login => 登入簽到
    - --game_type dice => 骰子遊戲

## To-do
1. 補完所有小遊戲
2. 多帳號同時進行 (20170520 done)

## License
See the LICENSE file for license rights and limitations (MIT).
