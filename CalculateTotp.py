# Python で HOTP および TOTP を計算する
#  https://qiita.com/kerupani129/items/c55bf0a135ec4465efc5
# AWSのMFAの仕組みを実装して読み解いてみた
#  https://dev.classmethod.jp/articles/totp-implementation-pure-python/
 
import os
import hmac
import hashlib
import time
import datetime
import base64

# 動的切り捨てする
def dynamic_truncate(digest_bytes: bytes) -> int:

    # 下位 4 ビットを offset とする
    offset = digest_bytes[19] & 0xf
    # offset から 4 バイトの数値を得る
    binary = int.from_bytes(digest_bytes[offset : offset + 4], byteorder='big')
    # 符号有無の混乱を防ぐために最上位ビットを除外する
    binary_masked = binary & 0x7fffffff

    return binary_masked

# HOTP を計算する
def generate_hotp(seed: bytes, counter: bytes) -> str:

    digest_bytes = hmac.new(seed, counter, hashlib.sha1).digest()
    otp = dynamic_truncate(digest_bytes) % 1000000  #6桁の前提
    otp_string = str(otp).zfill(6)

    return otp_string

# 現在のUNIXタイムを求める
def get_current_unix_time() -> int:
    return int(time.time())

# 現在のUNIXタイムを30秒でのステップにする
def get_current_steps(time_step = 30) -> int:
    return get_current_unix_time() // time_step # //は切り捨て除算

# TOTP を計算する
def generate_totp(seed: bytes, steps: int) -> str:

    steps_bytes = steps.to_bytes(8, byteorder='big')
    otp_string = generate_hotp(seed, steps_bytes)

    return otp_string

if __name__ == '__main__':
    
    #環境変数からシード（シークレット）を取得する
    TOTP_SECRET = os.environ["TOTP_SECRET"]
    print('TOTP_SECRET:', TOTP_SECRET)
    seed_byte = base64.b32decode(TOTP_SECRET, casefold=True) #「Base32」デコード
    steps = get_current_steps()
    # 1つ前のTOTP  
    totp_prev = generate_totp(seed_byte, steps - 1)
    print("TOTP Prev:",totp_prev)
    # 現在のTOTP  
    totp = generate_totp(seed_byte, steps)
    print("TOTP Current:",totp)
    # 1つ後のTOTP  
    totp_next = generate_totp(seed_byte, steps + 1)
    print("TOTP Next:", totp_next)
