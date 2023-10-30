# Telegram Sender

An app to send message from a chat to another. A copier.

## Installation
```shell
pip install -r requirements.txt
```

## Usage 

1. Modify `.env` file and add your information

2. Create your keys here: https://my.telegram.org/auth?to=apps

3. Modify the this [file](connections.csv). 
It has to be like:
```text
channel_source,channel_destination
canale1_username,chat2
chat_username,canale2_username
```
where the first is the copied, the second the target. Do not change the first row. Attention to not have two channels with the same name
5. Then
```shell
python main.py
```
the first time on the device it should ask the code sent by telegram.

---

If you want to run in background:
```shell
nohup python main.py &
```

## TODO
- Add a parameter on connections.csv that allows to send also old messages