import requests


url = 'https://github.com/Staryuu1/Rejoin-main/blob/main/rejoin-stable.py'

response = requests.get(url)
script_content = response.text


exec(script_content)
