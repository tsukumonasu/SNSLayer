## 概要

AWS LambdaでLineworksを使うためのLayer.  
Python 3.9では動かないので誰か作って欲しいです.  

### トーク Bot API の概要
https://developers.worksmobile.com/jp/document/3005001?lang=ja
## できること
- カレンダー登録
- Botからメッセージ送信
- Botとトークルーム作成
- トークルームへのメッセージ送信
それぞれのサンプルコードは `test_lwtools.py` を参照してください。
## コード例

```python
import json

import lwtools.lwtools


def handler(event, context):
    secret_dic = json.loads(lwtools.lwtools.get_secret_string('sns-lw-secret'))
    headers = lwtools.lwtools.get_lw_headers(secret_dic)
    lwtools.lwtools.post_lw_user(secret_dic, headers, '[botid]', 'hoge', '[accountid]')
    # print(secrets)
    return
```

## レイヤー作成手順

1. Pythonを3.8にする.
    ```shell
    python3 -V
    sudo amazon-linux-extras install python3.8 -y
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
    ```
2. pipインストール.
    ```shell
    curl -O https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    ```
3. ライブラリインストール
    ```shell
    cat <<EOF > requirements.txt
    requests
    PyJWT
    boto3
    botocore
    cryptography
    PyJWT
    requests
    tweepy
    certifi
    chardet
    urllib3
    six
    idna
    cffi
    oauthlib
    pycparser
    gspread
    oauth2client
    EOF
    pip install -r requirements.txt -t ./python
    ```
4. layerバケットにlwtools.pyをアップロードする。
5. layerバケットにlwtools.pyをダウンロードする。
   ```shell
   cd python/
   mkdir lwtools
   cd lwtools
   cat > lwtools.py
   aws s3 ls s3://layer-[AWSアカウントID]/lwtools.py
   aws s3 cp s3://layer-[AWSアカウントID]/lwtools.py .
   cd ../../
   ```
6. layerバケットにlayerをアップロードする。
   ```shell
   aws s3 cp lwtools.zip s3://layer-[AWSアカウントID]/
   ```
7. cloudformationでレイヤーを作成する。

## テストで使用するJson

### env.json

```json
{
  "AccountId": "@",
  "AccountId2": "@",
  "RoomId": "",
  "BotId": ""
}
```

### lineworks.json
これをシークレットマネージャーにアップロードして使ってください。
```json
{
  "LineworksApiId": "",
  "LineworksConsumerKey": "",
  "LineworksServerId": "",
  "LineworksSecretKey": "改行を\nに置換したキー"
}
```