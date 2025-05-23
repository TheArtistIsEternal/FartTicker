
import requests
import subprocess
import os

FORWARD_AUDIO = "FART_1SEC_FORWARD.aif"
REVERSE_AUDIO = "FART_1SEC_REVERSE.aif"
TEMP_AUDIO = "temp.wav"
OUTPUT_AUDIO = "daily_audio.mp3"

def fetch_btc_change():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    data = response.json()
    return data['market_data']['price_change_percentage_24h']

def convert_to_wav(source, output):
    subprocess.run(["ffmpeg", "-y", "-i", source, output], check=True)

def apply_stretch(input_wav, output_mp3, stretch_factor):
    if stretch_factor < 0.5:
        # chain atempo filters if needed
        subprocess.run([
            "ffmpeg", "-y", "-i", input_wav,
            "-filter:a", f"atempo=0.5,atempo={stretch_factor / 0.5}",
            output_mp3
        ], check=True)
    else:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_wav,
            "-filter:a", f"atempo={stretch_factor}",
            output_mp3
        ], check=True)

def main():
    pct_change = fetch_btc_change()
    print(f"24h BTC Change: {pct_change}%")
    is_up = pct_change >= 0
    stretch_factor = 1 / (1 + abs(pct_change / 100))  # Inverse for slowing down

    source_aif = FORWARD_AUDIO if is_up else REVERSE_AUDIO

    # Convert to wav
    convert_to_wav(source_aif, TEMP_AUDIO)

    # Apply time-stretching
    apply_stretch(TEMP_AUDIO, OUTPUT_AUDIO, stretch_factor)

    # Cleanup temp file
    if os.path.exists(TEMP_AUDIO):
        os.remove(TEMP_AUDIO)

if __name__ == "__main__":
    main()
