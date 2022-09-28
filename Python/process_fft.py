import os

import pandas as pd
import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpck
import numpy

SAMPLE_FILE_DIR = "../speaker_samples"
OUTPUT_DIR = "../fft_data"


# s_rate, single = wavfile.read("./speaker_samples/center/0_degrees_18:27:15.513170.wav")
#
# FFT = abs(fftpck.fft(single))
# freqs = fftpck.fftfreq(len(FFT), 1.0 / s_rate)
#
# xs = freqs[range(len(FFT) // 2)][1:]
# ys = FFT[range(len(FFT) // 2)][1:]
#
# print(type(xs))


def get_speaker_type_sub_dirs() -> list[str]:
    """gets all speakers in SAMPLE_FILE_DIR """
    return [folder for folder in os.listdir(SAMPLE_FILE_DIR) if os.path.isdir(os.path.join(SAMPLE_FILE_DIR, folder))]


def get_all_samples_for_speaker_type(speaker_sub_dir: str) -> list[str]:
    """gets all off-axis samples for speaker type"""
    return [file for file in os.listdir(os.path.join(SAMPLE_FILE_DIR, speaker_sub_dir)) if file[-3:] == "wav"]


def get_sample_name(sample_file: str) -> str:
    """gets the name of the sample"""
    return sample_file.split('_')[0]


def preform_fft(sample_file: str, speaker_sub_dir: str) -> numpy.ndarray:
    """runs fft on sample_file"""
    s_rate, single = wavfile.read(os.path.join(SAMPLE_FILE_DIR, speaker_sub_dir, sample_file))
    sample_fft = abs(fftpck.fft(single))
    return sample_fft[range(len(sample_fft) // 2)][1:]


def get_frequency_range(sample_file: str, speaker_sub_dir: str) -> numpy.ndarray:
    """returns frec range of sample"""

    s_rate, single = wavfile.read(os.path.join(SAMPLE_FILE_DIR, speaker_sub_dir, sample_file))

    sample_fft = abs(fftpck.fft(single))
    freqs = fftpck.fftfreq(len(sample_fft), 1.0 / s_rate)

    return freqs[range(len(sample_fft) // 2)][1:]


def save_df_as_csv(df: pd.DataFrame, save_file: str):
    """saves a dataframe to csv file"""
    df.to_csv(path_or_buf=os.path.join(OUTPUT_DIR, save_file))


def solve_aal_fft_for_speaker(speaker_sub_dir):
    """solves all ffts for each speaker"""
    samples = get_all_samples_for_speaker_type(speaker_sub_dir=speaker_sub_dir)
    if not samples:
        return

    to_df_dict = {'freq': get_frequency_range(sample_file=samples[0], speaker_sub_dir=speaker_sub_dir)}

    for sample in samples:
        name = get_sample_name(sample_file=sample)
        fft_result = preform_fft(sample_file=sample, speaker_sub_dir=speaker_sub_dir)
        to_df_dict[name] = fft_result

    df = pd.DataFrame.from_dict(to_df_dict)
    df.sort_values('freq')
    save_df_as_csv(df=df, save_file=f"{speaker_sub_dir}_speaker.csv")


def run_fft():
    """runs fft on all speaker samples"""
    for speaker in get_speaker_type_sub_dirs():
        solve_aal_fft_for_speaker(speaker_sub_dir=speaker)


if __name__ == '__main__':
    run_fft()
