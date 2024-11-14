from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
from bs4 import BeautifulSoup
import requests
import os
from io import BytesIO
from zipfile import ZipFile

app = Flask(__name__)

# Scrape images from the provided URL
def scrape_images(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    
    image_urls = []
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            if img_url.startswith('//'):
                img_url = 'http:' + img_url
            elif not img_url.startswith('http'):
                img_url = url.rstrip('/') + '/' + img_url.lstrip('/')
            image_urls.append(img_url)

    return image_urls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            images = scrape_images(url)
            return render_template('index.html', url=url, images=images)
    return render_template('index.html')

# Route for downloading a single image
@app.route('/download_image')
def download_image():
    image_url = request.args.get('image_url')
    if not image_url:
        return "Image URL not provided", 400
    
    response = requests.get(image_url)
    if response.status_code != 200:
        return "Failed to retrieve image", 404
    
    image_data = BytesIO(response.content)
    filename = image_url.split("/")[-1]
    return send_file(image_data, as_attachment=True, download_name=filename)

# Route for downloading multiple images as a ZIP file
@app.route('/download_all')
def download_all():
    image_urls = request.args.getlist('image_urls')
    if not image_urls:
        return "No images selected", 400
    
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for image_url in image_urls:
            response = requests.get(image_url)
            if response.status_code == 200:
                filename = image_url.split("/")[-1]
                zip_file.writestr(filename, response.content)
    
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name="images.zip", mimetype="application/zip")

if __name__ == '__main__':
    app.run(debug=True)
