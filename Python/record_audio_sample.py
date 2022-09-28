import os
import sys
import datetime
from enum import Enum, auto
from multiprocessing import Process
from pathlib import Path

import numpy as np
import pyaudio
import simpleaudio
import soothingsounds
import wave

OUT_FILE_DIR = "../speaker_samples"
WHITE_NOISE_FILE = Path("white_noise.wav")
CHUNK = 1024
FORMAT = pyaudio.paInt16
BIT_DEPTH = 16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = SAMPLE_DURATION = 1
p = pyaudio.PyAudio()


class SpeakerOptions(Enum):
    """options for what speaker is being testing"""
    center = auto()
    right = auto()


class OffAxisOptions(Enum):
    """options for what off-axis is being tested"""
    zero = auto()
    fifteen = auto()
    thirty = auto()
    forty_five = auto()


OFF_AXIS_OPTIONS_TO_DEGREES = {
    "zero": "0",
    "fifteen": "15",
    "thirty": "30",
    "forty_five": "45"
}


def generate_white_noise_file() -> None:
    """builds a white noise WAV file"""
    np_white_noise: np = soothingsounds.computenoise(ntype="white", fs=RATE, nsec=SAMPLE_DURATION, nbitfloat=BIT_DEPTH, nbitfile=1, verbose=True)
    soothingsounds.savenoise(samps=np_white_noise, nhours=0, fs=RATE, nsec=SAMPLE_DURATION, wavapi="scipy", ofn=WHITE_NOISE_FILE)


def check_white_noise_file_present() -> None:
    """checks if the while noise file is present. If not then make one"""

    if not WHITE_NOISE_FILE.exists():
        print("generating white noise file ...")
        generate_white_noise_file()
        print(f"... done. Saved at {str(WHITE_NOISE_FILE)}")


def record_sample(save_file: str) -> None:
    """records the sample"""
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * SAMPLE_DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(save_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_white_noise() -> None:
    """plays white noise"""

    # wave_obj = simpleaudio.WaveObject.from_wave_file(str(WHITE_NOISE_FILE))
    # play_obj = wave_obj.play()
    # play_obj.wait_done()

    # if system is not happy with output source then this is a simple workaround. Will play to your system default output speakers.
    # tested on Mac. Not sure if it will work for Windows.
    os.system(f'open {str(WHITE_NOISE_FILE)}')


def display_options(option_enum_class: type(Enum), message: str = ""):
    """displays options from an Enum class - assumes all values are auto"""
    print(f"Please select an option number {message}:")

    for option in option_enum_class:
        print(f"{option.value}: {option.name}")

    user_input = input("_____\nYour Section: ")
    try:
        return option_enum_class(int(user_input)).name
    except ValueError:
        print("Selected a non valid option. Try again.")
        return display_options(option_enum_class=option_enum_class)
    except RecursionError:
        print("Bad input too many times. Program exiting.")
        sys.exit()


def ask_user_what_speaker() -> str:
    """ask user what speaker is being tested"""
    return display_options(option_enum_class=SpeakerOptions, message="for speaker section")


def ask_user_off_axis() -> str:
    """asks the user what off-axis degree is being tested"""
    off_axis = display_options(option_enum_class=OffAxisOptions, message="for off-axis section")
    return OFF_AXIS_OPTIONS_TO_DEGREES[off_axis]


def set_output_file_name(speaker_section: str, off_axis_section: str) -> str:
    """returns the path to the sample will be saved to"""
    return os.path.join(OUT_FILE_DIR, speaker_section, f"{off_axis_section}_degrees_{datetime.datetime.now().time()}.wav")


def get_user_options() -> str:
    """asks user to define the test and solves output file name"""
    speaker: str = ask_user_what_speaker()
    off_axis: str = ask_user_off_axis()
    return set_output_file_name(speaker_section=speaker, off_axis_section=off_axis)


def ask_yes_no_question(message: str) -> bool:
    try:
        print(f"{message} (yes/no)")
        user_input = input("\n -> ")

        if user_input == "yes" or user_input[0] == "y":
            return True
        elif user_input == "no" or user_input[0] == "n":
            return False
        else:
            print("I did not understand that. Please try again.")
            return ask_yes_no_question(message=message)

    except RecursionError:
        print("Bad input too many times. Program exiting.")
        sys.exit()


def generate_sample() -> None:
    """generates a sample of speaker output"""
    print("Gathering Data for new sample.")
    check_white_noise_file_present()
    output_file_name = get_user_options()
    print(f"... output file will be saved to {output_file_name}")
    print("... begin measurement")

    play = Process(target=play_white_noise, args=())
    record = Process(target=record_sample, args=(output_file_name,))

    play.start()
    record.start()
    play.join()
    record.join()

    print(" ... done")


def run():
    """runs sampling program"""
    print("Sample Gathering Program is starting. Press Ctrl+C to exit at any time.")
    run_program = True

    try:
        while run_program:
            generate_sample()
            run_program = ask_yes_no_question(message="\nWould you like to collect another sample")
    except KeyboardInterrupt:
        pass

    print("Program now exiting. Goodbye.")


if __name__ == '__main__':
    run()
