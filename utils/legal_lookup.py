import pandas as pd

def search_ipc_section(user_input):
    try:
        df = pd.read_csv("data/ipc_sections.csv")
        user_input = user_input.lower()
        matches = df[df.apply(lambda row: user_input in str(row['Title']).lower() or user_input in str(row['Details']).lower(), axis=1)]
        return matches
    except Exception as e:
        print(f"Error reading IPC CSV: {e}")
        return pd.DataFrame()
