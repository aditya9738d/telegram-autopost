import requests
from bs4 import BeautifulSoup
import schedule
import time

def send_telegram_message(bot_token, chat_id, message):
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(api_url, data=params)
    print(response.json())  # Print the Telegram API response for debugging purposes

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def extract_app_info(html_content):
    app_info_list = []

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all(['td', 'th'])
            if len(columns) == 2:
                app_name = columns[0].get_text(strip=True)
                app_url = columns[1].find('a').get('href') if columns[1].find('a') else ""
                app_info_list.append({'name': app_name, 'url': app_url})
    
    return app_info_list

def send_scheduled_posts():
    # Set your Telegram bot token and chat ID
    bot_token = "6489588208:AAG-fKULNFad3VVk6pe8n4iP7bben1GZlUw"  # Replace with your actual bot token
    chat_id = "@artistyaa_wallpapers"  # Replace with your actual channel or group ID

    # Specify the path to your HTML file
    html_file_path = "AllBetaApps.html"  # Replace with the actual path

    # Read content from the HTML file
    html_content = read_html_file(html_file_path)

    # Extract app information from the HTML file
    app_info_list = extract_app_info(html_content)

    # Get the last processed index from a file or another persistent storage
    try:
        with open("last_processed_index.txt", "r") as f:
            last_processed_index = int(f.read().strip())
    except FileNotFoundError:
        last_processed_index = 0

    # Send the next 5 posts
    for app_info in app_info_list[last_processed_index:last_processed_index + 5]:
        message = f"{app_info['name']}: {app_info['url']}\n\nMore: https://testflightcode.wixsite.com/testflight"
        send_telegram_message(bot_token, chat_id, message)

    # Update the last processed index
    last_processed_index += 5

    # Save the updated last processed index to a file or another persistent storage
    with open("last_processed_index.txt", "w") as f:
        f.write(str(last_processed_index))

# Schedule the posts
schedule.every().day.at("10:36").do(send_scheduled_posts)  # 10 AM
schedule.every().day.at("10:38").do(send_scheduled_posts)  # 7 PM

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)

