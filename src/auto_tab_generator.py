#---------------------------------> importing
import librosa
import random
import os
import json

#---------------------------------> math dance
def generate_tabs(audio_path, lane_count=4, complexity=0.2, sensitivity=1.0, min_interval=0.1):
    print(f"🎧 Processing: {audio_path}")

    try:
        y, sr = librosa.load(audio_path, mono=True)
    except Exception as e:
        print(f"❌ Error loading {audio_path}: {e}")
        return None

    # Detect BPM
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(tempo)

    # Detect onsets
    onset_times = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True, units='time')
    onset_times = onset_times.tolist()

    # Filter too-close onsets
    filtered_onsets = []
    last_time = -999
    for t in onset_times:
        if t - last_time > min_interval:
            filtered_onsets.append(t)
            last_time = t
    tabs = []
    for t in filtered_onsets:
        if random.random() < complexity:
            count = random.randint(2, 3)
            lanes = random.sample(range(lane_count), count)
        else:
            lanes = [random.randint(0, lane_count - 1)]

        tabs.append({
            "time": round(float(t), 3),
            "lanes": lanes
        })

    print(f"✅ {os.path.basename(audio_path)} — BPM: {bpm:.1f}, notes: {len(tabs)}")

    return {
        "song_name": os.path.splitext(os.path.basename(audio_path))[0],
        "bpm": bpm,
        "tabs": tabs
    }

#---------------------------------> load tabs
def generate_all_tabs_from_folder(folder_path="music", output_folder="tmp"):
    folder_path = os.path.abspath(folder_path)
    output_folder = os.path.abspath(output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    supported_formats = (".mp3", ".wav", ".ogg", ".flac")
    songs = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_formats)]

    if not songs:
        print(f"⚠️ No audio files found in {folder_path}")
        return

    for song in songs:
        full_path = os.path.join(folder_path, song)
        result = generate_tabs(full_path)
        if result:
            out_path = os.path.join(output_folder, f"{result['song_name']}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved: {out_path}")

    print("\n✅ All songs processed!")