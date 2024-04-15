import pandas as pd

def analyze_file(file_path):
    output = {
        'affiliations_count': 'No data',
        'participants_count': 'No data',
        'averages': {}
    }

    try:
        affiliations_df = pd.read_excel(file_path, sheet_name='affiliations')
        participants_df = pd.read_excel(file_path, sheet_name='participants')

        output['affiliations_count'] = f"Total entries in 'affiliations': {len(affiliations_df)}"
        output['participants_count'] = f"Total participants: {len(participants_df)}"

        # Calculate averages
        for col in ['Perc_Effort', 'Attendance', 'Perc_Academic', 'CompleteYears']:
            if col in participants_df.columns:
                output['averages'][col] = f"Average {col}: {participants_df[col].mean():.2f}"
            else:
                output['averages'][col] = f"{col} column not found"

    except Exception as e:
        output['error'] = f"Failed to process file: {str(e)}"

    return output