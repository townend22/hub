from flask import Flask, render_template, request
import requests
app = Flask(__name__)
from bs4 import BeautifulSoup
import re
def replace_non_image_hostnames(input_string, new_hostname):
    # Define a regular expression to match image URLs (e.g., .png, .jpg, .gif, .jpeg)
    image_url_pattern = r"\bhttps?://\S+\.(png|jpe?g|gif|bmp)\b"

    # Find all image URLs in the input string
    image_urls = re.findall(image_url_pattern, input_string)

    # Replace hostnames in URLs that are not images
    def replace_non_image_urls(match):
        url = match.group(0)
        if url not in image_urls:
            return re.sub(r'https?://[^/]+', new_hostname, url)
        return url

    # Use re.sub to replace non-image URLs with the new hostname
    output_string = re.sub(r'https?://\S+', replace_non_image_urls, input_string)

    return output_string

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def home(path):
    param_value = request.args.get('s')
    

    url = path
    # Send a GET request
    if param_value != None:
        response = requests.get(f'https://moviesverse.vip/?s={param_value}')
    if param_value == None:
        response = requests.get(f'https://moviesverse.vip/{path}')
    

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # You can access the content of the response
        response_content = response.text
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response_content, 'html.parser')
        print(soup.title)
        title = 'TopFilmHub - Top Film - Hindi Dubbed Dual Audio Movie'
        try:
            title = soup.title.text.replace('Movies Verse', 'Top Film').replace('MoviesVerse', 'TopFilmHub')
        except:
            pass

        metatags = soup.find_all('meta', {'content': True})
        newmeta = ''
        for meta in metatags:  
            meta= str(meta)
            if('meta' in meta and 'link' not in meta.lower() and 'style' not in meta.lower()):
                try:
                    meta = meta.replace('MoviesVerse','TopFilmHub').replace('Movies Verse','Top Film').replace('moviesverse.vip','topfilmhub.xyz').replace('moviesverse','topfilmhub')
                    newmeta += f'{meta}\n'
                except:
                    pass

        # Find the div element with the specific id attribute
        div_with_id_page = soup.find('div', id='page')
        for a_tag in div_with_id_page.find_all('a'):
            if('download' in a_tag['href']):
                continue
            a_tag['href'] = a_tag['href'].replace('https://moviesverse.vip','http://127.0.0.1:5000')
        # response_content = response_content.replace('moviesverse.vip','127.0.0.1:5000')
        return render_template('index.html', data=div_with_id_page,meta = newmeta,title=title)
    else:
        return "<h1>Error in Backend</h1>",500

    # Render the HTML template named 'index.html' in the 'templates' folder

if __name__ == '__main__':
    app.run(debug=True)
