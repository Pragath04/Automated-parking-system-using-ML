import re
import requests

def send_message(message, number):
    url = "https://www.fast2sms.com/dev/bulkV2"
    
    querystring = {
        "authorization": "CD1rsoVcqH0ROQgafUhPlA9xwMpSWTyXub7I2Nn6tKzkiLdejBu6YyQgJEskzrnwl7ZdxKe8W4a0cLAb",
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": number
    }

    headers = {
        'cache-control': "no-cache"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def entry_message(name, slot_number, number):
    mylist = [
        "https://drive.google.com/file/d/1SuQV8Vg9uMrtebObak42b_uvX-SwZVTP/view?usp=sharing",
        "https://drive.google.com/file/d/1YUz0wOotahjK8OrcQztcP3zi5a3MDvYK/view?usp=sharing",
        # ... add more URLs as needed
    ]
    url2 = mylist[slot_number]
    message = f"Hello {name}, Your allocated parking slot is {slot_number}. To see the map, visit: {url2}"
    send_message(message, number)

def exit_message(amount, upi_id, number):
    upi_url = f"https://upayi.ml/{upi_id}/{amount}"
    message = f"Your parking fee is {amount}. Please pay it using the link: {upi_url}"
    send_message(message, number)

def main():
    # Example usage:
    name = "Adam"
    slot_number = 3
    number = 9945848007
    entry_message(name, slot_number, number)

    amount = 35
    upi_id = "sumukhjadhav007@okaxis"
    exit_message(amount, upi_id, number)

if __name__ == "__main__":
    main()
