from flask import Flask, render_template

app = Flask(__name__)

# Sample product data — pore real affiliate link diye replace korbo
products = [
    {
        "name": "Wireless Earbuds",
        "price": "₹999",
        "image": "https://via.placeholder.com/200",
        "platform": "Amazon",
        "link": "#"
    },
    {
        "name": "Smart Watch",
        "price": "₹1499",
        "image": "https://via.placeholder.com/200",
        "platform": "Flipkart",
        "link": "#"
    },
    {
        "name": "Bluetooth Speaker",
        "price": "₹799",
        "image": "https://via.placeholder.com/200",
        "platform": "Amazon",
        "link": "#"
    }
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
