import numpy as np
from scipy.io import wavfile
from scipy.signal import resample as rs


def read_file(filename):
    samplerate, data = wavfile.read(filename)
    data = pad_data(data, samplerate)
    return samplerate, data


def pad_data(data, modulo):
    ext = modulo - (len(data) % modulo)
    return np.append(data, np.zeros(ext))


def resample(data, current_rate, target_rate):
    # print(f"Sample rate cutoff, 0 expected: {len(data) % current_rate}")
    target_sample_count = len(data) // current_rate * target_rate
    return pad_data(rs(data, target_sample_count), target_rate)


def filter(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data)) * 255
