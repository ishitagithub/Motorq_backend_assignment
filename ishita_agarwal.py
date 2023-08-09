'''import requests
import json
import os
import time
while (True):
    t=requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").text
    t=json.loads(t)
    price=int(t["bitcoin"]["usd"])
    os.system(f"notify-send -t 10000 \"Price is {price} \"")
    time.sleep(60)
print(t)'''




from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app)

# Set rate limits
limiter.limit("100 per day")(app)
limiter.limit("10 per minute")(app)

@app.route('/get_coin_price')
@limiter.limit("5 per minute")
def get_coin_price():
    # Your code to fetch coin price
    coin_price = fetch_coin_price()
    return jsonify({"coin_price": coin_price})

if __name__ == "__main__":
    app.run()
