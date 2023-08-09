from flask import Flask, request, jsonify
import pyairtable
import redis

app = Flask(__name__)

# Airtable API configuration
BASE_ID = "app5cSBI0IZXXqghU"
TABLE_NAME = "Cryptocurrencies"
# Redis cache configuration
REDIS_HOST = "localhost"  
REDIS_PORT = 6379         
CACHE_TTL = 600           # Cache time-to-live in seconds (10 minutes)

# Initialize Airtable and Redis
airtable = pyairtable.Table(BASE_ID, TABLE_NAME, API_KEY)
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# GET /coins endpoint
@app.route('/coins', methods=['GET'])
def get_coins():
    # Fetch coins and their information from Airtable
    coins_data = airtable.get_all()
    coins_info = []
    
    for record in coins_data:
        coin_info = {
            "name": record["fields"]["Name"],
            "symbol": record["fields"]["Symbol"],
            "market_cap": record["fields"]["MarketCap"],  
            # Add more fields based on your Airtable setup
        }
        coins_info.append(coin_info)
    
    return jsonify(coins_info)

# GET /coins/price/:coinId endpoint
@app.route('/coins/price/<coinId>', methods=['GET'])
def get_coin_price(coinId):
    # Check if the price is available in the cache
    cached_price = cache.get(coinId)
    if cached_price:
        return jsonify({"Current price": cached_price.decode('utf-8')})
    
    # Fetch coin details from Airtable
    coin_data = airtable.find_by_field("Coin Symbol", coinId)  
    if coin_data:
        coin_price = coin_data["Current Price"]["PriceUSD"]  
        cache.setex(coinId, CACHE_TTL, coin_price)  # Cache the price
        return jsonify({"coin_price": coin_price})
    else:
        return jsonify({"error": "Coin not found"}), 404

if __name__ == "__main__":
    app.run()
