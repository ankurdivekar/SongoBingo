from pydub import AudioSegment
import pandas as pd


# Refer to https://github.com/jiaaro/pydub
def get_time_in_milliseconds(time_str):
    # print(time_str)
    ftr = [60000, 1000, 1]
    fragments = time_str.split('.')
    msec = 0
    for idx, fragment in enumerate(fragments):
        msec += int(fragment)*ftr[idx]

    return msec


def generate_audio_clips(params):

    # Get the parameters
    input_dir = params['input_dir']
    output_dir = params['output_dir']
    xlsx_path = params['xlsx_path']
    backspin_path = params['backspin_path']
    overwrite = params['overwrite']

    # Read the xlsx
    df = pd.read_excel(xlsx_path, converters={'In': str, 'Out': str})
    # print(df)

    # Get backspin sample
    backspin = AudioSegment.from_mp3(backspin_path)

    # Cut the clip from the song and append the backspin
    for index, row in df.iterrows():
        # print(row['FileName'], row['In'], row['Out'])
        song_path = input_dir / row['FileName']

        tmp_song = row['Song'].strip().title()
        tmp_artist = row['Artiste'].strip().title()
        tmp_filename = tmp_song + " - " + tmp_artist + ".mp3"
        clip_path = output_dir / tmp_filename

        if not overwrite and clip_path.exists():
            print('File exists :', clip_path)
        else:
            start = get_time_in_milliseconds(row['In'])
            end = get_time_in_milliseconds(row['Out'])
            # print(row['FileName'], ': Clip from', start, 'seconds to', end, 'seconds - Duration:', end-start, 'seconds')

            # Read in song
            song = AudioSegment.from_mp3(song_path)

            # Extract the clip
            extract = song[start:end]
            # print(len(extract))

            # Append the backspin
            clip = extract + backspin

            clip.export(clip_path, format="mp3")
            print('Saved :', clip_path)
