import csv
import gdax
import time


class myWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com/"
        self.products = ["BTC-USD"]
        self.message_count = 0
        self.open_count = 0
        self.received_count = 0
        self.done_count = 0
        self.match_count = 0
        self.price = 0
        self.size = 0
        self.time = None

    def on_message(self, msg):
        self.message_count += 1
        self.time = msg['time']
        if 'done' in msg['type']:
            self.done_count += 1
        elif 'received' in msg['type']:
            self.received_count += 1
        elif 'open' in msg['type']:
            self.open_count += 1
        if 'match' in msg['type']:
            self.match_count += 1
            self.price = msg['price']
            self.size = msg['size']

    def on_close(self):
        print("-- Goodbye! --")


with open('mycsvfile.csv', 'w') as f:
    f.write('time,message_count,open_count,received_count,'
            + 'done_count,open_count,match_count,price,size\n')


wsClient = myWebsocketClient()
wsClient.start()
while True:
    with open('trade_history.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([wsClient.time,
                         wsClient.message_count,
                         wsClient.open_count,
                         wsClient.received_count,
                         wsClient.done_count,
                         wsClient.open_count,
                         wsClient.match_count,
                         wsClient.price,
                         wsClient.size])

    wsClient.message_count = 0
    wsClient.open_count = 0
    wsClient.received_count = 0
    wsClient.done_count = 0
    wsClient.match_count = 0

    time.sleep(1)
wsClient.close()
