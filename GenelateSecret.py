# Python で HOTP および TOTP を計算する
#  https://qiita.com/kerupani129/items/c55bf0a135ec4465efc5
# AWSのMFAの仕組みを実装して読み解いてみた
#  https://dev.classmethod.jp/articles/totp-implementation-pure-python/
 
# import os

import secrets
import base64

import urllib.parse
import qrcode

# 鍵（シード）を生成
seed = secrets.token_bytes(20)
print(seed)

# バイト列を「base32」エンコード
seed_byte = base64.b32encode(seed)          #「base32」エンコード
seed_string = seed_byte.decode()            #バイト列を文字列にする 
# os.environ["TOTP_SECRET"] = seed_string   #環境変数にセット → 「環境変数の追加や上書きによる変更はそのPythonプログラムの中でのみ有効」
                                            #                    手動でセットする。

print (seed_string)

# otpauth URI を生成する
issuer = urllib.parse.quote('kansai-it')
accountname = urllib.parse.quote('cu')
time_step = 30
type = 'totp'
label = f'{issuer}:{accountname}'
parameters = f'secret={seed_string}&issuer={issuer}&algorithm=SHA1&digits=6&period={time_step}' #algorithm以降は使われていないよう
otpauth_uri = f'otpauth://{type}/{label}?{parameters}'
print(otpauth_uri)

# otpauth URIをQRコードのイメージにする（スマホアプリで読み取れるようにするため）
img = qrcode.make(otpauth_uri)
img.save('GenelateSecret.png')
img.show()
