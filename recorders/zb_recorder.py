# encoding: UTF-8
from zb_lib import *

def record(coin_pair): # example btc_usdt
    api = ZB_Sub_Spot_Api()
    api.connect_Subpot('apiKey', 'secretKey', coin_pair, True)

if __name__ == "__main__":
    record('eos_usdt')
