import sys
import json

class Event:

    def __init__(self, event_string):
        '''parse event'''
        self.type = "unknown" # trade, update (for order book), snapshot (for order book)
        self.content = {} # a dictionary parsed from the strong

class OrderBook:
    def __init__(self):        
        self.bidbook = {} # design your own data structure for this
        self.askbook = {} # design your own data sturcture for this

    def parse_new_event(self, event):
        if event.type == "update":
            self._apply_update_(event)
        if event.type == "snapshot":
            self._apply_snapshot_(event)
        if event.type == "trade":
            self._apply_trade_(event)

    def _apply_update_(self, event):
        '''apply the orbook update to get a new orderbook'''
        self.bidbook["newentry"] = "newvalue" # add your own logic
        self.askbook["newentry"] = "newvalue"  # add your own logic

    def _apply_snapshot_(self, event):
        '''repalce the current bid/ask book using the latest snapshot'''
        self.bidbook = {} # add your own logic
        self.askbook = {} # add yoru own logic

    def __apply_trade_(self, event):
        '''update the orderbook using the latest trade info'''
        if trade['side'] == 'buy':
            self.askbook = {} # add your own logic
        if trade['side'] == 'sell':
            self.bidbook = {} # add your own logic

    def get_bid(self, size=0):
        '''return the best bid price after slicing "size" from the top of the bid book'''
        if size == 0:
            return (0, 0) # add your own logic here with (top_bid_price, top_bid_size)
        else:
            # first slice size from the order book
            return (0, 0) # add your own logic here with (top_bid_price_after_slicing, top_bid_size_after_slicing)

    def get_ask(self, size=0):
        '''return the best ask price after slicing "size" from the top of the ask book'''
        if size == 0:
            return (0, 0)
        else:
            return (0, 0)

    def is_fake_trade(self, trade_event):
        if trade_event['price'] < self.get_bid() and trade_event['price'] > self.get_ask():
            return True
        else:
            return False
        

            
    
            
        
        

        
