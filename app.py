from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
from bs4 import BeautifulSoup
import requests
import os
from io import BytesIO
from zipfile import ZipFile

# Initialize the Flask application
app = Flask(__name__)

# Function to scrape images from a given URL
def scrape_images(url):
    try:
        # Send an HTTP GET request to the specified URL
        response = requests.get(url)
        # Raise an error if the request was unsuccessful
        response.raise_for_status()
    except requests.RequestException as e:
        # Print error message if there's an issue with the request
        print(f"Error fetching {url}: {e}")
        return []  # Return an empty list if request fails

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <img> tags in the HTML
    img_tags = soup.find_all('img')
    
    # Initialize a list to store image URLs
    image_urls = []
    for img in img_tags:
        # Get the 'src' attribute of each <img> tag
        img_url = img.get('src')
        if img_url:
            # If the URL is relative, convert it to an absolute URL
            if img_url.startswith('//'):
                img_url = 'http:' + img_url
            elif not img_url.startswith('http'):
                img_url = url.rstrip('/') + '/' + img_url.lstrip('/')
            # Add the full image URL to the list
            image_urls.append(img_url)

    # Return the list of image URLs
    return image_urls

# Route for the main page, handles GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the URL entered by the user
        url = request.form.get('url')
        if url:
            # Scrape images from the specified URL
            images = scrape_images(url)
            # Render the index.html template, passing the URL and images
            return render_template('index.html', url=url, images=images)
    # For GET requests, just render the index.html template without images
    return render_template('index.html')

# Route for downloading a single image
@app.route('/download_image')
def download_image():
    # Get the image URL from the query parameters
    image_url = request.args.get('image_url')
    if not image_url:
        # Return an error if no image URL is provided
        return "Image URL not provided", 400
    
    # Send a GET request to retrieve the image content
    response = requests.get(image_url)
    if response.status_code != 200:
        # Return an error if the image could not be retrieved
        return "Failed to retrieve image", 404
    
    # Store the image content in a BytesIO object (in-memory file)
    image_data = BytesIO(response.content)
    # Extract the filename from the image URL
    filename = image_url.split("/")[-1]
    # Send the file to the client for download with the appropriate filename
    return send_file(image_data, as_attachment=True, download_name=filename)

# Route for downloading multiple images as a ZIP file
@app.route('/download_all')
def download_all():
    # Get a list of image URLs from the query parameters
    image_urls = request.args.getlist('image_urls')
    if not image_urls:
        # Return an error if no images were selected
        return "No images selected", 400
    
    # Create an in-memory ZIP file
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for image_url in image_urls:
            # Send a GET request to each image URL
            response = requests.get(image_url)
            if response.status_code == 200:
                # Use the last part of the URL as the filename
                filename = image_url.split("/")[-1]
                # Write the image content to the ZIP file
                zip_file.writestr(filename, response.content)
    
    # Move the buffer position to the beginning of the file
    zip_buffer.seek(0)
    # Send the ZIP file to the client for download
    return send_file(zip_buffer, as_attachment=True, download_name="images.zip", mimetype="application/zip")

# Run the Flask application
if __name__ == '__main__':
    # Enable debug mode for easier development and testing
    app.run(debug=True)
