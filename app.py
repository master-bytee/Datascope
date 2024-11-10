from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to analyze website for trackers
def analyze_website(url):
    trackers = {
        "Google Analytics": False,
        "Facebook Pixel": False,
        "Other Trackers": False
    }

    # Fetch the website content
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for Google Analytics
        if "analytics.js" in response.text or "gtag.js" in response.text:
            trackers["Google Analytics"] = True
        
        # Check for Facebook Pixel
        if "fbq('init'," in response.text:
            trackers["Facebook Pixel"] = True
        
        # Check for any other trackers (e.g., general trackers)
        if len(soup.find_all('script')) > 0:
            trackers["Other Trackers"] = True

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch the URL: {str(e)}"}

    return trackers

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form['url']
    if not url.startswith("http"):
        url = "http://" + url  # Ensure URL is correctly formatted
    result = analyze_website(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
