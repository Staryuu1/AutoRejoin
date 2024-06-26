import requests


url = 'https://raw.githubusercontent.com/Staryuu1/Rejoin-main/main/rejoin-beta.py'

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    script_content = response.text

    # Execute the script in a restricted namespace
    exec(script_content)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
