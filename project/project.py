import json
import matplotlib.pyplot as plt
import numpy as np
import os
import re

from chat_downloader import ChatDownloader
from scipy.signal import find_peaks, savgol_filter

cd = ChatDownloader()


def main():
    link = check_link(input("VOD link: "))
    download_chat(link)
    bins, smooth_counts, peaks = get_highlights()
    print_graph(bins, smooth_counts, peaks)


def check_link(link):
    patterns = [
        r"(?:https?://)?(?:www\.)?twitch\.tv/videos/\d+",
        r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+"       
    ]

    link = link.strip()
    while True:
        if any(re.fullmatch(p, link) for p in patterns):
            return link
        
        link = input("Please, insert a valid URL: ").strip()


def download_chat(link):
    out_path = os.path.join(os.getcwd(), "chat.jsonl")

    with open(out_path, "w", encoding="utf-8") as f:
        try:
            for message in cd.get_chat(link):
                # message is a dict; write one JSON object per line
                json.dump(message, f, ensure_ascii=False)
                f.write("\n")
            
        except KeyboardInterrupt:
            # partial file saved
            pass

    return out_path


def get_highlights():
    BIN_SIZE = 120          # 2 minutos por bin
    SMOOTH_WINDOW = 3       # janela mínima (3 bins = 6 min de contexto)
    POLY_ORDER = 2          # polinômio leve para suavizar forma
    PEAK_THRESHOLD = 1.8    # picos acima de 1.8x a média = destaque
    MIN_PEAK_DISTANCE = 1   # evita múltiplos picos muito próximos

    timestamps = []

    # Read JSONL file
    with open("chat.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            timestamps.append(data["time_in_seconds"])

    max_time = max(timestamps)
    bins = np.arange(0, max_time + BIN_SIZE, BIN_SIZE)

    # Count messagens and filter noise
    counts, _ = np.histogram(timestamps, bins=bins)

    if len(counts) > SMOOTH_WINDOW:
        smooth_counts = savgol_filter(counts, SMOOTH_WINDOW, POLY_ORDER)
    else:
        smooth_counts = counts


    # Detect activity peaks
    avg_height = np.mean(smooth_counts)
    peaks, properties = find_peaks(
        smooth_counts,
        height=avg_height * PEAK_THRESHOLD,
        distance=MIN_PEAK_DISTANCE
    )

    # Print results
    print("Highlights detected:")
    for p in peaks:
        time = bins[p]
        score = smooth_counts[p]
        print(f" → {time/60:.1f} minutes (score: {score:.0f})")

    return bins, smooth_counts, peaks


def print_graph(bins, smooth_counts, peaks):
    plt.figure(figsize=(11, 5))
    plt.plot(bins[:-1]/60, smooth_counts, label="Chat activity (smoothed)", color="blue")
    plt.scatter(bins[peaks]/60, smooth_counts[peaks], color="red", label="Highlights", zorder=5)
    plt.title("Best moments detection")
    plt.xlabel("Time (minutes)")
    plt.ylabel("Messagens per bin (2 minutes)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
