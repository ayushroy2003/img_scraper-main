# 🌟 Image Scraper

This is an **Image Scraper** project that fetches images from the web based on user queries. The project is deployed at: 🚀 [Project Demo](https://img-scraper-main.onrender.com).

---

## ✨ Features
✅ Scrapes images based on user input  
✅ Stores images in a local directory  
✅ Logs scraping activities  
✅ Uses **MongoDB** to store image IDs and metadata  
✅ Web-based UI using **Flask**  

---

## 🔧 Installation and Setup

### 📌 Prerequisites
Ensure you have Python installed (>=3.7). Install dependencies using:

```bash
pip install -r requirements.txt
```

### ▶ Running the Project
Start the application with:

```bash
python app.py
```

Then, access the web interface at:  
🌐 `http://127.0.0.1:5000/`

---

## 🗄️ Database (MongoDB) Usage
This project uses **MongoDB** to store image metadata, including:
- **🆔 _id**: Unique identifier for each image
- **🔗 index**: URL of the image
- **🖼️ image**: Binary data of the image stored in Base64 format

📌 Example MongoDB document:
```json
{
  "_id": "67d3f09f9b0fd084ac85356f",
  "index": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPHtlHfYMJAgcVf…",
  "image": "Binary.createFromBase64('iVBORw0KGgoAAAANSUhEUgAAAKIAAABUCAMAAAA25xwtAAAAY1BMVEX///8AAAD6+vqAgIC2traWlpaGhoZqamq')"
}
```

---

## 📁 Project Structure
```
img_scraper-main-main/
│-- app.py                 # Main Flask application
│-- requirements.txt       # Dependencies
│-- scrapper.log           # Log file for monitoring
│-- image/                 # Downloaded images
│-- templates/             # HTML templates for UI
```

---

## 🎯 Usage Guide
1️⃣ Enter a search query.  
2️⃣ Click submit to scrape images.  
3️⃣ Download the fetched images.  

---

## 🚀 Deployment
The project is hosted on **Render**. To deploy manually:
1. Push the code to a **Git repository**.
2. Connect the repository to **Render**.
3. Deploy with the required **environment settings**.

---

## 📜 License
This project is **open-source** and free to use. 💡

