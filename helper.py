from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())
    
    words_count = len(words)

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    num_links = len(links)

    return num_messages, words_count, num_media_messages, num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, new_df

#def create_wordcloud(selected_user, df):
 #   stop_words = f.read()

   # if selected_user != 'Overall':
   #     df = df[df['user'] == selected_user]

   # temp = df[df['user'] != 'group_notification']
   # temp = temp[temp['message'] != '<Media omitted>\n']

   # def remove_stop_words(message):
    #    return " ".join([word for word in message.lower().split() if word not in stop_words.split()])

    #wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    #temp_copy = temp.copy()
    #temp_copy['message'] = temp_copy['message'].apply(remove_stop_words)
    #df_wc = wc.generate(temp_copy['message'].str.cat(sep=" "))
    #return df_wc
from wordcloud import WordCloud

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Remove group notifications and empty messages
    temp = df[df['message'] != '']
    temp = temp[temp['message'].notna()]

    text = temp['message'].str.cat(sep=" ")

    if not text or len(text.strip()) == 0:
        return None  # No words available

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(text)


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r', encoding='utf-8')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        words.extend([word for word in message.lower().split() if word not in stop_words.split()])

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    if not emojis:
        return pd.DataFrame()

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['month'].iloc[i]}-{timeline['year'].iloc[i]}")

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap