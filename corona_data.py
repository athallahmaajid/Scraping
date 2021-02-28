import pandas as pd
import requests
import re

source = requests.get('https://www.worldometers.info/coronavirus/').text
source = re.sub(r'<.*?>', lambda g: g.group(0).upper(), source)

html = pd.read_html(source)

now = html[0]
print(now.tail(59))
now.drop(columns=["#", "Unnamed: 0"], inplace=True)
now.to_csv('corona_data.csv')
