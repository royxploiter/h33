from flask import Flask, request
from requests import get, post
from bs4 import BeautifulSoup as bs
import json, base64, random

app = Flask(__name__)

@app.route('/')
def home():
    a = {
    'Contoh-Penggunaan':{'lirik': 'sdsd', 'facebook-downloader':'sadsd', 'nulis-bot':'sdsdsd', 'instagram-downloader': 's'}
    }
    return a

@app.route('/bot', methods=['GET'])
def fb():
    url = request.args.get('url')
    req = requests.get(url)
    sd = re.search('sd_src:"(.+?)"', req.text).group(1)
    hd = re.search('hd_src:"(.+?)"', req.text).group(1)
    js = {
    "results-hd": hd,
    "results-sd": sd
    }
    return js

@app.route('/nulis', methods=['GET', 'POST'])
def tulis():
    from nulis import tulis
    text = request.args.get('text')
    tulis=tulis(text)
    for i in tulis.tulis():
        i.save('gambar.jpg')
        image = open('gambar.jpg', 'rb')
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)
        url = 'https://api.imgbb.com/1/upload'
        par = {
         'key':'bfb879871c22df49a0694b4fb9ef6f9d',
         'image':image_64_encode,
         'name':'nulis',
         'expiration': 60
         }
        headers = {
         'Accept': 'application/json'
         }
        req = requests.post(url,data=par, headers=headers)
        p = req.json()['data']['display_url']
        js = {
         "results":p
         }
        return js

@app.route('/ig', methods=['GET'])
def ig():
    url = request.args.get('video_id')
    req = requests.get('https://instagram.com/p/'+url+'?__a=1')
    jss = req.json()['graphql']['shortcode_media']['video_url']
    js = {
    "results":jss
    }
    return js

@app.route('/lirik')
def lirik():
    par= request.args.get('search')
    from lirik import search
    a = search(par)
    b = {
    'results': a.result()
    }
    return b

@app.route('/v1/randomquotes', methods=['GET','POST'])
def quotes():
	quotes_file = json.loads(open('quotes.json').read())
	result = random.choice(quotes_file)
	print(result)
	return {
		'status': 200,
		'author': result['author'],
		'quotes': result['quotes']
	}

if __name__ == '__main__':
    app.run()