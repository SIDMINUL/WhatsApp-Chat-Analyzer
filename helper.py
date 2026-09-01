from collections import Counter
from pathlib import Path

import emoji
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic", ".heif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".3gp", ".webm"}
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".aac", ".ogg", ".wav", ".opus"}
DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv", ".zip"}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | AUDIO_EXTENSIONS | DOCUMENT_EXTENSIONS


def media_type(extension):
    extension = extension.lower()
    if extension in IMAGE_EXTENSIONS:
        return "Images"
    if extension in VIDEO_EXTENSIONS:
        return "Videos"
    if extension in AUDIO_EXTENSIONS:
        return "Audio"
    if extension in DOCUMENT_EXTENSIONS:
        return "Documents"
    return "Other"


def media_statistics(media_files):
    counts = Counter(media_type(m["extension"]) for m in media_files)
    return {
        "total": len(media_files),
        "images": counts["Images"],
        "videos": counts["Videos"],
        "audio": counts["Audio"],
        "by_type": dict(counts),
    }


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    num_messages = df.shape[0]
    words_count = sum(len(message.split()) for message in df["message"].astype(str))
    num_media_messages = df["message"].str.strip().str.lower().isin({"<media omitted>", "image omitted", "video omitted", "audio omitted"}).sum()
    num_links = sum(len(extract.find_urls(message)) for message in df["message"].astype(str))
    return num_messages, words_count, int(num_media_messages), num_links


def most_busy_users(df):
    x = df["user"].value_counts().head()
    new_df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index()
    new_df.columns = ["name", "percent"]
    return x, new_df


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    temp = df[df["message"].notna() & (df["message"].str.strip() != "")]
    text = temp["message"].str.cat(sep=" ")
    if not text.strip():
        return None
    return WordCloud(width=500, height=500, min_font_size=10, background_color="white").generate(text)


def most_common_words(selected_user, df):
    try:
        stop_words = Path("stop_hinglish.txt").read_text(encoding="utf-8").split()
    except FileNotFoundError:
        stop_words = []

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    temp = df[(df["user"] != "group_notification") & (df["message"].str.strip() != "<Media omitted>")]
    words = []
    stop_set = set(stop_words)
    for message in temp["message"].astype(str):
        words.extend(word for word in message.lower().split() if word not in stop_set)
    return pd.DataFrame(Counter(words).most_common(20))


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    emojis = [c for message in df["message"].astype(str) for c in message if c in emoji.EMOJI_DATA]
    if not emojis:
        return pd.DataFrame()
    return pd.DataFrame(Counter(emojis).most_common())


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    timeline = df.groupby(["year", "month_num", "month"])["message"].count().reset_index()
    timeline["time"] = timeline.apply(lambda r: f"{r['month']}-{r['year']}", axis=1)
    return timeline


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    return df.groupby("only_date")["message"].count().reset_index()


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    return df["day_name"].value_counts()


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    return df["month"].value_counts()


def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]
    return df.pivot_table(index="day_name", columns="period", values="message", aggfunc="count").fillna(0)
