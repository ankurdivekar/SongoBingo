import glob
import pandas as pd
from pathlib import Path


# Define the path for song cutting XLS
xlsx_path = Path('Assets/Index.xlsx').absolute()

# New songs folder path
full_songs_dir = Path('Files/FullSongs').absolute()

# Create dataframe
df = pd.DataFrame(columns=['FileName', 'Artiste', 'Song', 'In', 'Out'])

# Get a list of all files and assign to the dataframe column
df['FileName'] = [Path(f).stem for f in glob.glob(str(full_songs_dir) + '/*.mp3')]

# Write out to xlsx
df.to_excel(xlsx_path, index=0, sheet_name='FileList')