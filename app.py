from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import logging
import pymongo
import os

logging.basicConfig(
    filename="scrapper.log",
    level=logging.INFO
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def homepage():
    return render_template("index.html")


@app.route("/review", methods=["POST", "GET"])
def index():

    if request.method == "POST":

        try:

            # Search query
            query = request.form["content"].strip().replace(" ", "_")

            # Create image folder
            save_dir = "image"
            os.makedirs(save_dir, exist_ok=True)

            # Browser headers
            headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            }

            # Google Images URL
            url = f"https://www.google.com/search?tbm=isch&q={query}"

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(
                response.content,
                "html.parser"
            )

            images_tags = soup.find_all("img")

            # Prevent IndexError
            if len(images_tags) <= 1:
                return "No images found. Google may be blocking the scraper."

            # Remove Google's logo image
            images_tags = images_tags[1:]

            img_data_mongo = []

            for idx, img in enumerate(images_tags):

                image_url = img.get("src")

                if not image_url:
                    continue

                try:

                    image_response = requests.get(
                        image_url,
                        timeout=10
                    )

                    image_data = image_response.content

                    filename = f"{query}_{idx}.jpg"

                    filepath = os.path.join(
                        save_dir,
                        filename
                    )

                    with open(filepath, "wb") as f:
                        f.write(image_data)

                    img_data_mongo.append(
                        {
                            "query": query,
                            "image_url": image_url,
                            "filename": filename
                        }
                    )

                except Exception as img_error:
                    logging.warning(
                        f"Image Download Error: {img_error}"
                    )

            if not img_data_mongo:
                return "No valid images found."

            # MongoDB Connection
            mongo_uri = os.getenv(
                "MONGO_URI",
                "mongodb+srv://pwskills:pwskills@cluster0.9unxk7e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            )

            client = pymongo.MongoClient(mongo_uri)

            db = client["ayush_image_scrap"]

            collection = db["ayush_image_scrap"]

            collection.insert_many(img_data_mongo)

            client.close()

            return f"{len(img_data_mongo)} images downloaded and stored successfully."

        except Exception as e:

            logging.exception("Application Error")

            import traceback

            return f"<pre>{traceback.format_exc()}</pre>"

    return render_template("index.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )
```
