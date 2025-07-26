import pandas as pd
import os
from django.conf import settings
def searchAns(user):

    # Read the CSV file
    file = os.path.join(settings.BASE_DIR,'static/assets/data/datacollected2.csv')
    df=pd.read_csv(file)

    # Create a list to store filtered DataFrames
    arr = []

    # Check if 'head' column exists and search it
    if 'head' in df.columns:
        arr.append(df[df['head'].str.contains(user, case=False, na=False)])

    # Check if 'description' column exists and search it
    if 'description' in df.columns:
        arr.append(df[df['description'].str.contains(user, case=False, na=False)])

    # Concatenate and drop duplicates
    df = pd.concat(arr).drop_duplicates().reset_index(drop=False)
    return df

