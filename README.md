# 💬 WhatsApp Chat Analyzer

A powerful **WhatsApp Chat Analysis Dashboard** built with **Python and Streamlit** that transforms exported WhatsApp conversations into interactive insights.

Analyze messages, users, activity patterns, emojis, links, common words, and shared media including **images, videos, audio, and documents**.

---

## 🚀 Live Demo

🔗 **Live App:** `YOUR_STREAMLIT_APP_URL`

---

## 📌 Features

### 📊 Chat Overview

- Total messages
- Total words
- Media messages
- Links shared
- User-wise message statistics

### 👥 User Analysis

- Most active users
- Individual user analysis
- Percentage contribution of each user
- User activity comparison

### 📈 Activity Analysis

- Monthly message timeline
- Daily message timeline
- Most active days
- Most active months
- Weekly activity heatmap

### 💬 Message Analysis

- Word cloud
- Most commonly used words
- Hinglish stop-word filtering
- Emoji analysis
- Emoji frequency distribution

### 📸 Media Center

Analyze actual media files from WhatsApp exports containing:

- 🖼️ Images
- 🎥 Videos
- 🎵 Audio
- 📄 Documents

The Media Center provides:

- Total media count
- Images count
- Videos count
- Audio count
- Media type distribution
- Image gallery
- Video playback
- Audio playback
- File information and size
- Media filtering

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Interactive web application |
| Pandas | Data processing |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| WordCloud | Word-frequency visualization |
| URLExtract | URL extraction |
| Emoji | Emoji analysis |
| Regular Expressions | WhatsApp chat parsing |

---

## 📂 Project Structure

```text
WhatsApp-Chat-Analyzer/
│
├── app.py
├── helper.py
├── preprocessor.py
├── stop_hinglish.txt
├── requirements.txt
├── .gitignore
└── README.md
