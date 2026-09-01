# 💬 WhatsApp Chat Analyzer

A powerful **WhatsApp Chat Analysis Dashboard** built with **Python and Streamlit** that transforms exported WhatsApp conversations into interactive insights.

Analyze messages, users, activity patterns, emojis, links, common words, and shared media including **images, videos, audio, and documents**.

---

## 🚀 Live Demo

🔗 **[Open the Live App](https://whatsapp-chat-analyzer-0808.streamlit.app/)**

---

## ✨ Features

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

Upload a WhatsApp chat exported with **Include Media** and explore the actual shared files.

Supported media:

- 🖼️ Images — JPG, JPEG, PNG, GIF, WEBP, BMP, HEIC/HEIF
- 🎥 Videos — MP4, MOV, AVI, MKV, 3GP, WEBM
- 🎵 Audio — MP3, M4A, AAC, OGG, WAV, OPUS
- 📄 Documents — PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX, CSV, TXT, ZIP

Media features:

- Total media count
- Images, videos and audio counts
- Media type distribution
- Image gallery
- Video playback
- Audio playback
- File name and size information
- Media filtering
- ZIP-based WhatsApp export support

> **Note:** A normal `.txt` export contains media placeholders such as `<Media omitted>` but does not contain the actual media files. Use **Export Chat → Include Media** and upload the resulting ZIP to use the Media Center.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming |
| Streamlit | Interactive web application |
| Pandas | Data processing and analysis |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization and heatmaps |
| WordCloud | Word-frequency visualization |
| URLExtract | URL extraction |
| Emoji | Emoji detection and analysis |
| Regular Expressions | WhatsApp chat parsing |
| ZIP / Pathlib | Export and media-file processing |

---

## 🧠 How It Works

```text
WhatsApp Export
      │
      ├── .txt ───────────────┐
      │                       │
      └── .zip + media ───────┤
                              ↓
                       Chat Preprocessor
                              │
                              ↓
                         Pandas DataFrame
                              │
                ┌─────────────┼─────────────┐
                ↓             ↓             ↓
            Messages       Activity       Media
                │             │             │
                ↓             ↓             ↓
             NLP &          Charts       Gallery /
           Word Analysis   & Heatmaps     Playback
                │             │             │
                └─────────────┼─────────────┘
                              ↓
                     Streamlit Dashboard
```

---

## 📥 WhatsApp Chat Export

### Without Media

For message and activity analysis:

```text
WhatsApp
   ↓
Open Chat
   ↓
Chat Info
   ↓
Export Chat
   ↓
Without Media
```

Upload the resulting `.txt` file.

### With Media

For the Media Center:

```text
WhatsApp
   ↓
Open Chat
   ↓
Chat Info
   ↓
Export Chat
   ↓
Include Media
```

Upload the resulting `.zip` file.

Example:

```text
WhatsApp Chat.zip
│
├── _chat.txt
├── IMG-20260825-WA001.jpg
├── IMG-20260825-WA002.jpg
├── VID-20260825-WA003.mp4
├── AUD-20260825-WA004.opus
├── DOC-20260825-WA005.pdf
└── ...
```

---

## 📊 Dashboard Sections

### 📊 Overview

Provides a high-level summary of the conversation:

- Total messages
- Total words
- Media messages
- Links shared
- Monthly timeline
- Most active users

### 📸 Media Center

Explore media extracted from a WhatsApp ZIP export.

```text
Media Center
├── 📊 Media Statistics
├── 📈 Media Type Distribution
├── 🖼️ Image Gallery
├── 🎥 Video Player
├── 🎵 Audio Player
└── 📁 File Information
```

### 💬 Messages

Analyze the content of the conversation using:

- Word Cloud
- Most Common Words
- Emoji Frequency

### 🗓️ Activity

Understand conversation patterns using:

- Daily Timeline
- Weekly Activity
- Monthly Activity
- Activity Heatmap

---

## 📈 Example Questions This Dashboard Answers

- 👤 Who sends the most messages?
- 📅 Which day is the conversation most active?
- 📆 Which month has the highest activity?
- 💬 How many messages were exchanged?
- 📝 How many words were exchanged?
- 🔗 How many links were shared?
- 😂 Which emojis are used most frequently?
- 🔤 What are the most common words?
- 🖼️ How many images were shared?
- 🎥 How many videos were shared?
- 🎵 How much audio was shared?
- 📁 Which type of media is shared most often?

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/SIDMINUL/WhatsApp-Chat-Analyzer.git
```

### 2. Enter the project directory

```bash
cd WhatsApp-Chat-Analyzer
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 📦 Dependencies

The project uses the following main Python packages:

```text
streamlit
pandas
numpy
matplotlib
seaborn
urlextract
wordcloud
emoji
```

See `requirements.txt` for the complete dependency list.

---

## 🔐 Privacy & Security

WhatsApp conversations can contain highly personal information.

- Do not upload private conversations to an unknown/public deployment.
- Use anonymized or sample data for portfolio demonstrations.
- Do not commit exported WhatsApp chats or media files to GitHub.
- Do not commit credentials, API keys, or secrets.

The application processes the uploaded export during the session and uses it to generate the dashboard.

---

## ⚠️ Limitations

### Media-to-message matching

WhatsApp exports do not always provide enough information to reliably associate every media file with its original sender and timestamp. The application avoids inventing metadata when an exact match cannot be determined.

### Large exports

Very large chat exports containing hundreds or thousands of media files may require additional memory and processing time.

### `.txt` vs `.zip`

A `.txt` export contains message text and media placeholders. The actual images, videos, audio and documents are available only when the chat is exported with media.

---

## 🎯 Future Improvements

- [ ] Sentiment analysis
- [ ] Conversation search
- [ ] Advanced media-to-message matching
- [ ] Media sharing timeline
- [ ] Interactive Plotly charts
- [ ] Message reaction analysis
- [ ] AI-powered conversation summaries
- [ ] User-wise word comparison
- [ ] PDF report generation
- [ ] CSV analysis export

---

## 👨‍💻 Author

**Abdul Momin Siddiqui**

GitHub: **[@SIDMINUL](https://github.com/SIDMINUL)**

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is available for educational and portfolio purposes.
