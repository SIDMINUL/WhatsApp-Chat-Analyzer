import re
import pandas as pd

# Supports common WhatsApp exports such as:
# 12/08/26, 8:42 pm - Name: message
# 12/08/26, 20:42 - Name: message
PATTERNS = [
    re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s?(am|pm)? - (.*?): (.*)$', re.IGNORECASE),
    re.compile(r'^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s?(am|pm)? - (.*)$', re.IGNORECASE),
]

def preprocess(data):
    dates, users, contents = [], [], []
    current = None

    for line in data.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        matched = None
        for pattern in PATTERNS:
            matched = pattern.match(line)
            if matched:
                break

        if matched:
            groups = matched.groups()
            date, time, ampm = groups[0], groups[1], groups[2]
            rest = groups[3:]
            if len(rest) == 2:
                user, message = rest
            else:
                user, message = 'group_notification', rest[0]
            date_string = f'{date} {time}' + (f' {ampm}' if ampm else '')
            current = {'date': date_string, 'user': user, 'message': message}
            dates.append(date_string)
            users.append(user)
            contents.append(message)
        elif current is not None and line.strip():
            # Preserve WhatsApp multiline messages.
            contents[-1] += '\n' + line

    df = pd.DataFrame({'date': dates, 'user': users, 'message': contents})
    if df.empty:
        return pd.DataFrame(columns=['date','user','message','year','month_num','month','day','day_name','hour','minute','only_date','period'])

    df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=False)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['period'] = df['hour'].apply(lambda x: f'{int(x):02d}-{(int(x)+1)%24:02d}' if pd.notna(x) else '')
    df['message'] = df['message'].fillna('').astype(str).str.strip()
    return df
