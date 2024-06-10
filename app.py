from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging
import pymongo
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)
import os

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:

                    # query to search for images
                    query = request.form['content'].replace(" ","")

                            # directory to store downloaded images
                    save_dir = "image/"
                    if not os.path.exists(save_dir):
                          os.makedirs(save_dir)



                            # fake user agent to avoid getting blocked by Google
                    
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
                            # fetch the search results page
                    response = requests.get(f"https://www.google.com/search?q={query}&sca_esv=23275d10bb72eb94&sca_upv=1&udm=2&biw=1536&bih=695&sxsrf=ADLYWIIctTXENEZfoIRDbPZj02_eFB-v3g%3A1717955944430&ei=aO1lZvOBGorz4-EPvZ7h2A0&oq=faces+and+emot&gs_lp=Egxnd3Mtd2l6LXNlcnAiDmZhY2VzIGFuZCBlbW90KgIIADIFEAAYgAQyBRAAGIAEMgYQABgFGB4yBhAAGAgYHkj2T1CuCVijRnAJeACQAQGYAaoCoAGDHqoBBjAuMTguMrgBA8gBAPgBAZgCEqAC-hWoAgrCAgcQIxgnGOoCwgILEAAYgAQYsQMYgwHCAggQABiABBixA8ICChAAGIAEGEMYigXCAg0QABiABBixAxhDGIoFmAMHkgcINC4xMi4xLjGgB7ZG&sclient=gws-wiz-serp")

                            # parse the HTML using BeautifulSoup
                    soup = BeautifulSoup(response.content, "html.parser")

                            # find all img tags
                    images_tags = soup.find_all("img")

                            # download each image and save it to the specified directory
                    del images_tags[0]
                    img_data_mongo = []
                    for i in images_tags:
                            image_url = i['src']
                            image_data = requests.get(image_url).content
                            mydict = {"index": image_url , "image":image_data}
                            img_data_mongo.append(mydict)
                            with open(os.path.join(save_dir,f"{query}_{images_tags.index(i)}.jpg"),"wb") as f :
                                    f.write(image_data)


    
                    
                    client = pymongo.MongoClient("mongodb+srv://pwskills:pwskills@cluster0.9unxk7e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
                    db = client['ayush_image_scrap']
                    coll_image = db["ayush_image_scrap"]
                    coll_image.insert_many(img_data_mongo)          

                    return "image laoded"
                except Exception as e:
                    logging.info(e)
                    return 'something is wrong'
            # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
