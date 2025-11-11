import re
import pandas as pd

def preprocess(data):
    # Regex pattern for WhatsApp exported chat format
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s?(?:am|pm)? - (.*?): (.*)'

    messages = []
    dates = []
    users = []
    contents = []

    for line in data.split("\n"):
        match = re.match(pattern, line)
        if match:
            date = match.group(1) + " " + match.group(2)
            user_message = match.group(3)
            message = match.group(4)

            dates.append(date)
            users.append(user_message)
            contents.append(message)
            messages.append(line)

    df = pd.DataFrame({'date': dates, 'user': users, 'message': contents})

    # Convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Add extra columns
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date

    # Create period (e.g. 23-00)
    df['period'] = df['hour'].apply(lambda x: f"{x:02d}-{(x+1)%24:02d}")

    # 🔥 Ensure all messages are strings (fixes .str accessor error)
    df['message'] = df['message'].astype(str)

    return df
