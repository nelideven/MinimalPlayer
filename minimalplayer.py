#* This file is part of MinimalPlayer.
#*
#* MinimalPlayer is free software: you can redistribute it and/or modify either this part (minimalplayer.py) of the software and/or this whole software under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#* 
#* MinimalPlayer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#*
#* You should have received a copy of the GNU General Public License (LICENSE) along with this project. If not, see <https://www.gnu.org/licenses/>.
#*
#* You should also have a copy of the mp_autocomplete script, which is required for the file name input in this software (if you downloaded the source code). 

import subprocess
import os
import argparse
import sys

def get_filename_from_bash():
    try:
        # Get the path to the prompt.sh script
        if getattr(sys, 'frozen', False):
            script_path = os.path.join(sys._MEIPASS, 'mp_autocomplete')
        else:
            script_path = os.path.join(os.path.dirname(__file__), 'prompt.sh')

        # Run the bash script and capture the output
        subprocess.run(['bash', script_path], check=True)

        # Read the output from the temporary file
        with open('/tmp/filename_output.txt', 'r') as file:
            filename = file.read().strip()
        return filename
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def check_binary(binary):
    return subprocess.call(['which', binary], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def calculate_sample_rate(speed_factor, pipe_path=None):
    original_rate = 44100
    if pipe_path:
        return int(original_rate / speed_factor)
    else:
        return int(original_rate * speed_factor)

def play_audio(player, file_path, new_sample_rate, pipe_path=None, ffmpeg_exist=True, out_format='s16le'):
    if pipe_path:
        if ffmpeg_exist:
            print(f'Piping converted file {file_path} with format {out_format} to {pipe_path}. Press q to exit')
            if pipe_path == "-":
                command = f'ffmpeg -i "{file_path}" -ar {new_sample_rate} -f {out_format} -loglevel warning -stats - '
            else:
                command = f'ffmpeg -i "{file_path}" -ar {new_sample_rate} -f {out_format} -loglevel warning -stats {pipe_path} -y'
        else:
            ncvconfirm = input(f'It is NOT recommended to continue, since this software would pipe the original (UNCONVERTED) audio to {pipe_path}!!. Do you REALLY want to continue? (unless you want to hear pacat/pw-cat (possibly) making weird noises so..) (y/n): ')
            if ncvconfirm == "y":
                print(f'Piping original file {file_path} to {pipe_path} without speed modifications. Press CTRL+C to exit')
                if pipe_path == "-":
                    command = f'cat "{file_path}"'
                else:
                    command = f'cat "{file_path}" > "{pipe_path}"'
            else:
                print('User aborted. Exiting..')
                exit(0)
    else:
        if ffmpeg_exist:
            print(f'Playing audio file {file_path}. Press q to exit')
            if player == "pacat":
                command = f'ffmpeg -i "{file_path}" -ar 44100 -f s16le -loglevel warning -stats - | pacat --rate={new_sample_rate} --latency=1'
            elif player == "pw-play":
                command = f'ffmpeg -i "{file_path}" -ar 44100 -f s16le -loglevel warning -stats - | pw-play --rate={new_sample_rate} -'
            elif player == "pw-cat":
                command = f'ffmpeg -i "{file_path}" -ar 44100 -f s16le -loglevel warning -stats - | pw-cat --rate={new_sample_rate} -p -'
            elif player == "paplay":
                command = f'ffmpeg -i "{file_path}" -ar 44100 -f s16le -loglevel warning -stats - | paplay --rate={new_sample_rate} --latency=1'
        else:
            print(f'Playing audio file {file_path} without speed modifications. Press CTRL+C to exit')
            if player == "paplay":
                command = f'cat "{file_path}" | paplay'
            elif player == "pw-play":
                command = f'pw-play "{file_path}"'
    subprocess.run(command, shell=True)

def main():
    parser = argparse.ArgumentParser(description='MinimalPlayer: A CLI-based audio player based on FFmpeg and audio players (pacat/pa-play/paplay/pw-play)')
    parser.add_argument('-p', '--pipe', nargs='?', const=True, default=False, help='Enable pipe mode. Optionally provide the pipe path or "-" for stdout')
    parser.add_argument('-f', '--file', type=str, help='Audio file path')
    parser.add_argument('-s', '--speed', type=float, default=0.0, help='Speed factor (e.g., 0.5 for half speed, 2.0 for double speed)')
    parser.add_argument('-o', '--output', type=str, help='Output file format (only for pipe mode)')
    parser.add_argument('--extm', action="store_true", help='You might not want to mess with this...')

    args = parser.parse_args()
    pipe_mode = args.pipe
    file_path = args.file
    speed_factor = args.speed
    out_format = args.output
    
    if args.output and not args.pipe:
        parser.error("-o/--output requires -p/--pipe to be specified")

    # Checking if FFmpeg exists
    if check_binary("ffmpeg"):
        ffmpeg_exist = True
    else:
        ffmpeg_exist = False
    
    # Determine which player to use
    player = ""
    if ffmpeg_exist:
        if check_binary("pacat") & check_binary("pw-cat"):
            if pipe_mode:
                player = None
            elif args.extm:
                player = "pw-cat"
            else:
                player = input("You have pw-cat and pacat. Choose one to use: ").strip()
        elif check_binary("pw-cat"):
            player = "pw-cat"
        elif check_binary("pacat"):
            player = "pacat"
        else:
            print("Neither pacat nor pw-cat detected! Falling back to paplay/pw-play")
            if check_binary("paplay") & check_binary("pw-play"):
                if pipe_mode:
                    player = None
                elif args.extm:
                    player = "pw-play"
                else:
                    player = input("You have pw-play and paplay. Choose one to use: ").strip()
            elif check_binary("pw-play"):
                player = "pw-play"
            elif check_binary("paplay"):
                player = "paplay"
            else:
                print("Neither pacat, paplay, pw-cat, nor pw-play detected! Exiting..")
                exit(127)
    else:
        print("FFmpeg does not exist! Audio file would be played without modifications (now relies on paplay/pw-play)")
        if check_binary("paplay") & check_binary("pw-play"):
            if pipe_mode:
                player = None
            elif args.extm:
                player = "pw-play"
            else:
                player = input("You have pw-play and paplay. Choose one to use: ").strip()
        elif check_binary("pw-play"):
            player = "pw-play"
        elif check_binary("paplay"):
            player = "paplay"
        else:
            print("Neither paplay nor pw-play detected! Exiting..")
            exit(127)
    
    # Handle pipe mode and arguments
    if pipe_mode:
        if pipe_mode == True:
            pipe_path = input("Enter the named pipe (or input a '-' to output via stdout): ").strip()
        else:
            pipe_path = pipe_mode
        if not file_path:
            file_path = get_filename_from_bash()
        if not out_format:
            out_format = input('Enter the output format (default; s16le. See ffmpeg -formats for more info): ')
            if not out_format:
                out_format = "s16le"
        if speed_factor == 0.0:
            if ffmpeg_exist:
                if args.extm:
                    zen_in = subprocess.run(["zenity", "--entry", "--title=Speed factor", "--text=Enter the speed factor (e.g., 0.5 for half speed, 2.0 for double speed)"], capture_output=True, text=True)
                    speed_factor = float(zen_in.stdout.strip())
                else:
                    speed_factor = float(input("Enter the speed factor (e.g., 0.5 for half speed, 2.0 for double speed): ").strip())
            else:
                print("FFmpeg does not exist! Piped audio will not have any speed adjustments!")
    else:
        if not file_path:
            file_path = get_filename_from_bash()
        if speed_factor == 0.0:
            if ffmpeg_exist:
                if args.extm:
                    zen_in = subprocess.run(["zenity", "--entry", "--title=Speed factor", "--text=Enter the speed factor (e.g., 0.5 for half speed, 2.0 for double speed)"], capture_output=True, text=True)
                    speed_factor = float(zen_in.stdout.strip())
                else:
                    speed_factor = float(input("Enter the speed factor (e.g., 0.5 for half speed, 2.0 for double speed): ").strip())
            else:
                print("FFmpeg does not exist! Played audio will not have any speed adjustments!")

    new_sample_rate = calculate_sample_rate(speed_factor, pipe_path if pipe_mode else None)
    print(f'Sample rate: {new_sample_rate}')
    play_audio(player, file_path, new_sample_rate, pipe_path if pipe_mode else None, ffmpeg_exist, out_format)

if __name__ == '__main__':
    main()
