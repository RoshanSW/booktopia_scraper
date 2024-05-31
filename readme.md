# Booktopia Scraper

## Overview

This project involves creating a web scraper to extract book information from the Booktopia website using a list of ISBNs as input. The objective is to gather specific details about each book and save the data in a CSV file.

## Requirements

### Tools and Packages

1. **Python 3.x** - Ensure you have Python installed on your machine.
2. **Scrapy** - An open-source and collaborative web crawling framework for Python.
3. **pandas** - A powerful data manipulation and analysis library for Python.
4. **latest_user_agents** - A package to get the latest user agents.
5. **pip** - Python package installer.

### Installation

You can install the necessary packages using `pip`. Open a terminal and run the following commands:

```bash
pip install add_above_packages 
```

## Input File
Ensure you have the input CSV file (input_list.csv) containing the list of ISBNs.The file should be formatted as follows:
```bash
ISBN13
9781234567890
9780987654321
...
```

## Steps to Run the Code

1. Clone the repository or download the project files.

2. Navigate to the project directory:
    ```bash
    cd booktopia_scraper
    ```
3. Run the Scrapy spider:
   ```bash
   scrapy crawl booktopia   
    ```
   #### Example :
   **To extra save file**
   ```bash
   scrapy crawl booktopia -o scrap_data.csv      
   ```
4. **Output:** The scraped data will be saved in output.csv in the project directory.


## Acknowledgments

All acknowledgments provided in this README file are made for educational purpose from the respective individuals and projects. We express our sincere gratitude for their contributions to the development community.
