# Image Scraper

An image scraper web application built with Flask that allows users to enter a URL, scrape images from the provided URL, and download them individually or in bulk. The app also includes a responsive and visually enhanced frontend.

## Features

- Scrape images from any provided website URL.
- Display scraped images in a grid layout with options to:
  - Download images individually.
  - Select multiple images and download them as a ZIP file.
- Responsive design with animations and interactive UI elements.
- "Select All" and "Deselect All" options for bulk image management.


## Technologies Used

- **Flask** - Backend framework for handling routes and server logic.
- **Requests** - Library for making HTTP requests to retrieve web pages.
- **BeautifulSoup** - HTML parser used to scrape images from the webpage.
- **HTML, CSS, and JavaScript** - Frontend for building a responsive, interactive user interface.

## Setup and Installation

### Prerequisites

- **Python 3.x**: Make sure Python is installed on your system. You can check by running `python --version`.
- **pip**: The Python package installer.

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/image-scraper.git
   cd image-scraper
