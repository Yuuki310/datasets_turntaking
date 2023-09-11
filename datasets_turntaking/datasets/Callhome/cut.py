import os 
import soundfile as sf
import json

from utils import load_data, get_speaker_num, load_utterances
from datasets_turntaking.utils import (
    read_txt,
    read_json,
    repo_root,
)

def cut_audio(path, start, end):
    newpath = os.path.join(os.path.dirname(os.path.dirname(path)), "data", os.path.basename(path))
    data, sr = sf.read(path)
    sf.write(newpath, data[int(start*sr/1000) : int(end*sr/1000)], sr)


if __name__ == "__main__":
    dataset = "Callhome"
    lang = "jpn"

    audio_dir = os.path.join(repo_root(), "data", dataset, lang, "up16k_data")
    out_dir = os.path.join(repo_root(), "data", dataset, lang, "data")
    text_dir = os.path.join(repo_root(), "data", dataset, lang, "original/transcript")
    paths = load_data(audio_dir, text_dir)

    os.makedirs(out_dir, exist_ok=True)
    datalist = {}
    for path in paths:
        if get_speaker_num(path["text"]) > 2: 
            print(f"Number of speakers is greater than 3 :  {path}")
            continue

        try:        
            start, end, utterances = load_utterances(path["text"])
            audio_path = path["audio_path"]
            cut_audio(audio_path, start, end)

        except:
            continue
        
        