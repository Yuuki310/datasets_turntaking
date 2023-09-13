import os
import re
import json
import torch
import matplotlib.pyplot as plt
from datasets_turntaking.utils import (
    read_txt,
    read_json,
    repo_root,
    load_waveform
)
from plot_utils import (
    plot_waveform,
    plot_vad,
)


REL_AUDIO_PATH = os.path.join(
    repo_root(), "datasets/Switchboard/files/relative_audio_path.json"
)
JSON_PATH = os.path.join(repo_root(), "datasets/Switchboard/files")

vad_dir = "/data/group1/z40351r/datasets_turntaking/data/Switchboard/vad"

def plot_audio_vad(
    waveform: torch.Tensor,
    vad: torch.Tensor,
    plot: bool = True,
    figsize=(9, 6),
    downsample: int = 10,
    sample_rate: int = 16000,
):
    assert (
        waveform.shape[0] == 2
    ), f"Expected waveform of shape (2, n_samples) got {waveform.shape}"

    fig, ax = plt.subplots(3, 1, figsize=figsize)
    _ = plot_waveform(waveform=waveform[0], ax=ax[0], downsample=downsample, sample_rate=sample_rate)
    _ = plot_waveform(waveform=waveform[1], ax=ax[0], color="orange", downsample=downsample, sample_rate=sample_rate)
    ax[0].set_xticks([])

    _ = plot_vad_zone(waveform=waveform[0], vad=vad[0], ax=ax[1], color="lightblue", downsample=downsample, sample_rate=sample_rate)
    _ = plot_vad_zone(waveform=waveform[1], vad=vad[1], ax=ax[1], color="orange", downsample=downsample, sample_rate=sample_rate)
    # ax[0].set_xticks([])
    return fig, ax


def plot_vad_zone(waveform, vad, ax, 
    color="b", 
    downsample: int = 10,
    sample_rate: int = 16000
):
    x = waveform[..., ::downsample]
    new_rate = sample_rate / downsample
    x_time = torch.arange(x.shape[-1]) / new_rate

    for zone in vad:
        print(zone)
        ax.axvspan(zone[0], zone[1], color=color, alpha=0.7)
        ax.set_xlim([0, x_time[-1]])

    return ax

def load_vad(vad_path):  
    with open(vad_path) as f:
        d = json.load(f)
    return d



if __name__ == "__main__":
    dataset = "Callhome/eng"
    audio_dir = os.path.join(repo_root(), "data", dataset, "data")
    vad_dir = os.path.join(repo_root(), "data", dataset, "vad")

    session = "4065"
    audio_path = os.path.join(audio_dir, session + ".wav")
    vad_path = os.path.join(vad_dir, session + ".json")
    
    waveform, sr = load_waveform(audio_path)
    print(waveform)
    vad = load_vad(vad_path)
    print(len(vad[0]))
    fig, ax = plot_audio_vad(
        waveform.cpu(), vad, plot=True, figsize=(100,50)
    )
    figpath = os.path.join("/data/group1/z40351r/datasets_turntaking/plot", session + ".png")
    fig.savefig(figpath)



    

