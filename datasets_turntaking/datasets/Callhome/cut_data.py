import glob
import os 
from os.path import join, exists, basename
from datasets_turntaking.utils import read_txt
import json as json
from sklearn.model_selection import train_test_split
import numpy as np
from datasets_turntaking.dataset.callhome.utils import load_utterances
import soundfile as sf
from datasets_turntaking.utils import read_txt
import re


def load_data(lang):
    audio_path = os.path.join("/data/group1/z40351r/datasets_turntaking/data", "Callhome", lang, "data_full")
    text_path = "/data/group1/z40351r/datasets_turntaking/data/Callhome/" + lang + "/transcript"

    if not exists(text_path):
        raise FileNotFoundError(f"text_path not found: {text_path}")

    dataset = []
    for file in os.listdir(audio_path):
        if file.endswith(".wav"):
            sample = {"audio_path": join(audio_path, file)}
            txt = join(text_path, file.replace(".wav", ".cha"))
            if exists(txt):
                sample["text"] = txt
            dataset.append(sample)
    return dataset


def get_member_num(filepath):
    member = 0
    for row in read_txt(filepath):
        if row.startswith("@ID"):
            member += 1
        elif row[0]=="*":
            break
    return member

def preprocess_utterance(filepath):
    """
    Load filepath and preprocess the annotations

    * Omit empty rows
    * join utterances spanning multiple lines
    """
    data = []
    speak = False
    print(read_txt(filepath))
    for row in read_txt(filepath):
        # omit empty rows and rows starting with '#' (global file info)
        if row == "" or row.startswith("#"):
            continue

        # Some utterances span multiple rows:
        # i.e. evaltest/en_6467.txt
        #
        # 462.58 468.59 B: That's were, that's where I guess, they would, %um, they
        # get involved in initial public offering, stock offerings
        #if row[0].isdigit():
        if row.startswith("@"):
            continue
        elif row.startswith("%"):
            continue
        elif row[0]=="*":
            speak = True
            data.append(row)
        else:
            if speak == True:
                data[-1] += " " + row
    return data


def load_utterances(filepath, clean=True):
    #try:
    data = preprocess_utterance(filepath)

    last_speaker = None
    utterances = []
    script_start = -1
    script_end = -1
    member = 0

    for row in data:
        split = row.split(" ")
        time_stamp = re.findall(r"\x15(.\d*)_(.\d*)", row)
        if time_stamp == []:
            continue
        else:
            start, end = list(map(int, list(time_stamp[0])))
            #開始時間の調整
            if script_start == -1:
                script_start = start
            start = (start - script_start) / 1000
            end = (end - script_start)  / 1000

        speaker = re.findall(r"\*(.):", row)[0]
        re.sub(r"\*(.):", "", row)
        speaker = 0 if speaker == "A" else 1
        text = " ".join(split[1:])
        if last_speaker is None:
            utterances.append(
                {"start": start, "end": end, "speaker": speaker, "text": text}
            )
        elif last_speaker == speaker:
            utterances[-1]["end"] = end
            utterances[-1]["text"] += " " + text
        else:
            utterances.append(
                {"start": start, "end": end, "speaker": speaker, "text": text}
            )
        last_speaker = speaker
    script_end = list(map(int, list(time_stamp[0])))[1]
    return script_start, script_end, utterances

    # except:
    #     print(f"ERROR on split {filepath}")
    #     raise(aa)

if __name__ == "__main__":
    paths = load_english()
    dic = {}
    datalist = []

    time = 0
    count = 0

    for path in paths:
        member_num = get_member_num(path["text"])
        if member_num > 2: 
            print(f"Number of speakers is greater than 3 :  {path}")
            continue
        print(path["audio_path"])

        try:        
            start, end, utterances = load_utterances(path["text"])
        except:
            continue
        newpath = os.path.join("/data/group1/z40351r/datasets_turntaking/data/Callhome/jpn/data", os.path.basename(path["audio_path"]))
        data, sr = sf.read(path["audio_path"])
        time += end - start
        count += 1
        sf.write(newpath, data[int(start*sr/1000) : int(end*sr/1000)], sr)
        print(path["audio_path"],start,end,sr)
        print(data[int(start*sr/1000) : int(end*sr/1000)])
        
        