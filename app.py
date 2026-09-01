import io
import zipfile
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import streamlit as st

import helper
import preprocessor

st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon="💬", layout="wide")
st.title("💬 WhatsApp Chat Analyzer")
st.caption("Analyze conversations, activity, links, emojis, and exported media.")


def read_upload(upload):
    """Read a WhatsApp TXT export or ZIP export with media."""
    if upload.name.lower().endswith(".txt"):
        raw = upload.getvalue()
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")
        return text, []

    media_files = []
    with zipfile.ZipFile(io.BytesIO(upload.getvalue())) as z:
        txt_names = [n for n in z.namelist() if n.lower().endswith(".txt") and not n.endswith("/")]
        if not txt_names:
            raise ValueError("No WhatsApp chat .txt file was found inside the ZIP.")
        txt_name = max(txt_names, key=lambda n: z.getinfo(n).file_size)
        raw = z.read(txt_name)
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("latin-1")

        for info in z.infolist():
            if info.is_dir() or info.filename == txt_name or info.filename.lower().endswith(".txt"):
                continue
            suffix = Path(info.filename).suffix.lower()
            if suffix in helper.MEDIA_EXTENSIONS:
                media_files.append({
                    "name": Path(info.filename).name,
                    "path": info.filename,
                    "extension": suffix,
                    "data": z.read(info.filename),
                    "size": info.file_size,
                })
    return text, media_files


st.sidebar.header("📁 WhatsApp Export")
uploaded_file = st.sidebar.file_uploader(
    "Upload .txt or .zip",
    type=["txt", "zip"],
    help="For actual media, export the WhatsApp chat with 'Include media' and upload the ZIP.",
)

if uploaded_file is None:
    st.info("👈 Upload a WhatsApp .txt export, or a .zip export with media.")
    st.stop()

try:
    data, media_files = read_upload(uploaded_file)
    df = preprocessor.preprocess(data)
except Exception as exc:
    st.error(f"Could not read this WhatsApp export: {exc}")
    st.stop()

if df.empty:
    st.error("No WhatsApp messages were detected. Please upload a standard WhatsApp export.")
    st.stop()

user_list = [u for u in df["user"].dropna().unique().tolist() if u != "group_notification"]
user_list.sort()
user_list.insert(0, "Overall")
selected_user = st.sidebar.selectbox("Analyze user", user_list)
section = st.sidebar.radio("📊 Section", ["Overview", "Media", "Messages", "Activity"])

if section == "Overview":
    num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Messages", f"{num_messages:,}")
    c2.metric("Total Words", f"{words:,}")
    c3.metric("Media Messages", f"{num_media_messages:,}")
    c4.metric("Links Shared", f"{num_links:,}")

    timeline = helper.monthly_timeline(selected_user, df)
    if not timeline.empty:
        st.subheader("📈 Monthly Timeline")
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"])
        ax.tick_params(axis="x", rotation=70)
        ax.set_ylabel("Messages")
        st.pyplot(fig)
        plt.close(fig)

    if selected_user == "Overall":
        st.subheader("👥 Most Active Users")
        x, new_df = helper.most_busy_users(df)
        c1, c2 = st.columns(2)
        with c1:
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values)
            ax.tick_params(axis="x", rotation=70)
            st.pyplot(fig)
            plt.close(fig)
        with c2:
            st.dataframe(new_df, use_container_width=True, hide_index=True)

elif section == "Media":
    st.header("📸 Media Center")
    st.write("For actual files, use WhatsApp **Export chat → Include media** and upload the resulting ZIP.")

    stats = helper.media_statistics(media_files)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Media Files", f"{stats['total']:,}")
    c2.metric("Images", f"{stats['images']:,}")
    c3.metric("Videos", f"{stats['videos']:,}")
    c4.metric("Audio", f"{stats['audio']:,}")

    if not media_files:
        st.info("No media files found. A .txt export contains media placeholders, not the actual files.")
    else:
        type_counts = pd.Series(stats["by_type"]).sort_values(ascending=False)
        st.subheader("📊 Media by Type")
        st.bar_chart(type_counts)

        media_type = st.selectbox("Filter", ["All", "Images", "Videos", "Audio", "Documents", "Other"])
        filtered = [m for m in media_files if media_type == "All" or helper.media_type(m["extension"]) == media_type]

        images = [m for m in filtered if helper.media_type(m["extension"]) == "Images"]
        if images:
            st.subheader(f"🖼️ Images ({len(images):,})")
            cols = st.columns(4)
            for i, media in enumerate(images[:100]):
                with cols[i % 4]:
                    try:
                        st.image(media["data"], caption=media["name"], use_container_width=True)
                    except Exception:
                        st.caption(media["name"])
            if len(images) > 100:
                st.info("Showing the first 100 images to keep the browser responsive.")

        others = [m for m in filtered if helper.media_type(m["extension"]) != "Images"]
        if others:
            table = pd.DataFrame([
                {"File": m["name"], "Type": helper.media_type(m["extension"]), "Size (KB)": round(m["size"] / 1024, 1)}
                for m in others
            ])
            st.subheader("📁 Files")
            st.dataframe(table, use_container_width=True, hide_index=True)

            for media in others[:50]:
                kind = helper.media_type(media["extension"])
                if kind == "Audio":
                    st.audio(media["data"])
                elif kind == "Videos":
                    st.video(media["data"])

elif section == "Messages":
    st.header("💬 Message Analysis")
    wc = helper.create_wordcloud(selected_user, df)
    if wc:
        st.subheader("Word Cloud")
        fig, ax = plt.subplots()
        ax.imshow(wc)
        ax.axis("off")
        st.pyplot(fig)
        plt.close(fig)

    common = helper.most_common_words(selected_user, df)
    if not common.empty:
        st.subheader("Most Common Words")
        fig, ax = plt.subplots()
        ax.barh(common[0], common[1])
        st.pyplot(fig)
        plt.close(fig)

    emoji_df = helper.emoji_helper(selected_user, df)
    if not emoji_df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.dataframe(emoji_df, use_container_width=True, hide_index=True)
        with c2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), autopct="%0.1f%%")
            st.pyplot(fig)
            plt.close(fig)

else:
    st.header("🗓️ Activity Analysis")
    daily = helper.daily_timeline(selected_user, df)
    if not daily.empty:
        st.subheader("Daily Timeline")
        fig, ax = plt.subplots()
        ax.plot(daily["only_date"], daily["message"])
        ax.tick_params(axis="x", rotation=70)
        st.pyplot(fig)
        plt.close(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Most Busy Day")
        st.bar_chart(helper.week_activity_map(selected_user, df))
    with c2:
        st.subheader("Most Busy Month")
        st.bar_chart(helper.month_activity_map(selected_user, df))

    heatmap = helper.activity_heatmap(selected_user, df)
    if not heatmap.empty:
        st.subheader("Weekly Activity Heatmap")
        fig, ax = plt.subplots(figsize=(12, 5))
        sns.heatmap(heatmap, ax=ax)
        st.pyplot(fig)
        plt.close(fig)
