import re
import pandas as pd
from datetime import datetime
# Function to clean and convert to 24-hour format
def convert_to_24_hour(dates):
    converted_dates = []
    for date in dates:
            # Remove the Unicode narrow no-break space (\u202f) and trailing characters
        clean_date = date.replace('\u202f', '').strip(' -')
        try:
                # Try parsing with the 24-hour format
            datetime.strptime(clean_date, "%d/%m/%Y, %H:%M")
                # If successful, append without changes
            converted_dates.append(clean_date)
            continue
        except ValueError:
            pass
            # Parse the date and time
        parsed_date = None
        try:
            # Try with 4-digit year format
            parsed_date = datetime.strptime(clean_date, "%d/%m/%Y, %I:%M%p")
        except ValueError:
            try:
                    # Try with 2-digit year format
                parsed_date = datetime.strptime(clean_date, "%d/%m/%y, %I:%M%p")
            except ValueError:
                raise ValueError(f"Date format not recognized: {clean_date}")

            # Format it back to 24-hour format
        converted_dates.append(parsed_date.strftime("%d/%m/%Y, %H:%M"))


    return converted_dates

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s?[apAP][mM]\s-\s|\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)


    # Convert the list
    dates_24_hour = convert_to_24_hour(dates)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates_24_hour})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df