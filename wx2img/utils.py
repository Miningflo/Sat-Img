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
    print(f"current_rate: {current_rate}, target_rate: {target_rate} ")
    # print(f"Sample rate cutoff, 0 expected: {len(data) % current_rate}")
    #data = pad_data(data, current_rate)
    print(len(data) / current_rate * target_rate)
    target_sample_count = int(len(data) / current_rate * target_rate)
    value = rs(data, target_sample_count)
    print(len(value))
    return pad_data(value, target_rate)


def filter(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data)) * 255
