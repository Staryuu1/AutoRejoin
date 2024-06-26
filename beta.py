import requests


url = 'https://raw.githubusercontent.com/Staryuu1/Rejoin-main/main/rejoin-beta.py'

response = requests.get(url)
script_content = response.text


exec(script_content)
