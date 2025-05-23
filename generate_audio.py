
import requests
from pydub import AudioSegment

FORWARD_AUDIO = "FART_1SEC_FORWARD.aif"
REVERSE_AUDIO = "FART_1SEC_REVERSE.aif"
OUTPUT_AUDIO = "daily_audio.mp3"

def fetch_btc_change():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    response = requests.get(url)
    data = response.json()
    return data['market_data']['price_change_percentage_24h']

def stretch_audio(input_path, output_path, stretch_factor):
    audio = AudioSegment.from_file(input_path)

    # Calculate new frame rate
    new_frame_rate = int(audio.frame_rate / stretch_factor)

    # Apply frame rate adjustment
    stretched = audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate})
    stretched = stretched.set_frame_rate(audio.frame_rate)

    # Export stretched file
    stretched.export(output_path, format="mp3")

def main():
    pct_change = fetch_btc_change()
    print(f"24h BTC Change: {pct_change}%")
    is_up = pct_change >= 0
    stretch_factor = 1 + abs(pct_change / 100)

    input_file = FORWARD_AUDIO if is_up else REVERSE_AUDIO
    stretch_audio(input_file, OUTPUT_AUDIO, stretch_factor)

if __name__ == "__main__":
    main()
