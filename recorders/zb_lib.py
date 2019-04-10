from time import sleep
from threading import Thread
import websocket
from  datetime import datetime as dt
import sys

zb_usd_url = "wss://api.zb.com:9999/websocket"

class ZB_Sub_Spot_Api(object):
    '''API object based on Websocket'''
    def __init__(self):
        """Constructor"""
        self.apiKey = ''         # apiKey
        self.secretKey = ''      # secretKey
        self.ws_sub_spot = None  # websocket, for spot market
        self.coin_pair = ''

    def _parse_event(self, event):
        data = eval(event)
        if data.get('dataType', '') == 'depth':
            output = {"_exchange_":"zb","_instance_id_":"RECORDER"}
            output["snapshot"]=True
            output["_product_"] = data.get("channel").split('_')[0]
            output["_type_"] = "OrderBook"
            output["exchangeTimestamp"] = data.get("timestamp", 0)*1000
            output["timestamp"] = int(int(dt.now().strftime("%s%f"))/1000)
            output["asks"] = list(map(lambda x: {"price":x[0], "amount":x[1]}, data.get('asks', [])[::-1]))
            output["bids"] = list(map(lambda x: {"price":x[0], "amount":x[1]}, data.get('bids', [])))
            # directly print the parsing results
            print(str(output).replace("'",'"').replace("True", "true").replace(" ", ""))
            #print("Latency=%d"%(output["timestamp"] - output["exchangeTimestamp"]))

        if data.get('dataType', '') == 'trades':
            trades = data["data"]
            for trade in trades:
                output = {"_exchange_":"zb","_instance_id_":"RECORDER"}
                output["_product_"] = data.get("channel").split('_')[0]
                output["_type_"] = "Trade"
                output["exchangeTimestamp"] = trade["date"] * 1000
                output["timestamp"] = int(int(dt.now().strftime("%s%f"))/1000)
                output["amount"] = float(trade["amount"])
                output["id"] = trade["tid"]
                output["price"] = float(trade["price"])
                output["side"] = trade["type"]
                print(str(output).replace("'",'"').replace(" ", ""))
                #print("Latency=%d"%(output["timestamp"] - output["exchangeTimestamp"]))

    #----------------------------------------------------------------------
    def reconnect(self):
        sys.stderr.write("Close before reconnect.\n")
        self.close()
        # reconnection
        self.ws_sub_spot = websocket.WebSocketApp(self.host,
                                         on_message=self.onMessage,
                                         on_error=self.onError,
                                         on_close=self.onClose,
                                         on_open=self.onOpen)

        self.thread = Thread(target=self.ws_sub_spot.run_forever)
        self.thread.start()
        sys.stderr.write("Reconnected.\n")

        sleep(3)
        self._subscribeSpotTicker()
        self._subscribeSpotDepth()
        self._subscribeSpotTrades()
        sys.stderr.write("Data re-subscribed\n")

    def connect_Subpot(self, apiKey , secretKey , coin_pair,  trace = False):
        self.host = zb_usd_url
        self.apiKey = apiKey
        self.secretKey = secretKey
        self.coin_pair = coin_pair

        websocket.enableTrace(trace)

        self.ws_sub_spot = websocket.WebSocketApp(self.host,
                                             on_message=self.onMessage,
                                             on_error=self.onError,
                                             on_close=self.onClose,
                                             on_open=self.onOpen)

        self.thread = Thread(target=self.ws_sub_spot.run_forever)
        self.thread.start()
        sys.stderr.write("Connection Established\n")

        sleep(3)
        self._subscribeSpotTicker()
        self._subscribeSpotDepth()
        self._subscribeSpotTrades()
        sys.stderr.write("Data subsribed")

    def close(self):
        '''Close socket'''
        sys.stderr.write("Closing...\n")
        if self.thread and self.thread.isAlive():
            self.ws_sub_spot.close()
            try:
                self.thread.join()
            except:
                sys.stderr.write("Cannot join thread!\n")
        sys.stderr.write("Closed!\n")

    #----------------------------------------------------------------------
    def onMessage(self, event):
        '''reaction on market event message'''
        self._parse_event(event)

    def onError(self, event):
        '''Error push'''
        sys.stderr.write("Error Event!\n")
        sys.stderr.write(str(event) + "\n")
        self.reconnect()

    def onClose(self):
        '''Close connection'''
        sys.stderr.write("On Close!\n")

    def onOpen(self):
        '''Open Connection'''
        sys.stderr.write("On Open!\n")

    #----------------------------------------------------------------------
    def _subscribeSpotTicker(self):
        # Spot market ticker
        symbol_pair = self.coin_pair
        sys.stderr.write("Subscribing Spot Ticker\n")
        symbol_pair = symbol_pair.replace('_','')
        req = "{'event':'addChannel','channel':'%s_ticker'}" % symbol_pair
        self.ws_sub_spot.send(req)
        sys.stderr.write("Spot ticker %s subscribed\n"%(symbol_pair))

    def _subscribeSpotDepth(self):
        # Spot market depth
        symbol_pair = self.coin_pair
        symbol_pair = symbol_pair.replace('_','')
        req = "{'event':'addChannel','channel':'%s_depth'}" % symbol_pair
        self.ws_sub_spot.send(req)

    def _subscribeSpotTrades(self):
        symbol_pair = self.coin_pair
        symbol_pair = symbol_pair.replace('_','')
        req = "{'event':'addChannel','channel':'%s_trades'}" % symbol_pair
        self.ws_sub_spot.send(req)
