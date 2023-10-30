# Telegram Sender

An app to send message from a chat to another. A copier.

## Installation
```shell
pip install -r requirements.txt
```

## Usage 

Modify the this [file](connections.csv).
It has to be like:
```text
https://t.me/canale1,https://t.me/chat1
https://t.me/242wex2,https://t.me/dsisdos
```

where the first is the copied, the second the target. Then
```shell
python main.py
```

the first time on the device it should ask the code sent by telegram.

If you want to run in background:
```shell
nohup python main.py &
```