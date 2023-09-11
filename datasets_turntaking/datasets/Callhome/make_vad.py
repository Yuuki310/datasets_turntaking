import os
import re
import glob
import json

from pathlib import Path
from tqdm import tqdm

from utils import (
    load_data,
    load_utterances,
    extract_vad,
)
from datasets_turntaking.utils import (
    repo_root,
    read_txt,
    read_json,
)

lang = "eng"
dataset = "Callhome"

if __name__ == "__main__":
    audio_dir = os.path.join(repo_root(), "data", dataset, lang, "data")
    text_dir = os.path.join(repo_root(), "data", dataset, lang, "original/transcript")
    vad_dir = os.path.join(repo_root(), "data", dataset, lang, "vad")


    paths = load_data(audio_dir, text_dir)

    for path in tqdm(paths):
        session = Path(path["audio_path"]).stem
        _, _, dialog = load_utterances(path["text"])
        vad = extract_vad(dialog)

        encode_data = json.dumps(vad, indent=4)
        with open(os.path.join(vad_dir, f"{session}.json"), "w") as f:
            json.dump(vad, f, indent=4)
        