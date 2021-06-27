import numpy as np
from scipy.io import wavfile
from scipy.signal import resample as rs
import matplotlib.pyplot as plt


def read_file(filename):
    samplerate, data = wavfile.read(filename)
    data = pad_data(data, samplerate)
    return samplerate, data


def pad_data(data, modulo):
    ext = modulo - (len(data) % modulo)
    return np.append(data, np.zeros(ext))


def resample(data, current_rate, target_rate):
    target_sample_count = len(data) // current_rate * target_rate
    return pad_data(rs(data, target_sample_count), target_rate)


def filter(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def draw(data):
    # og size: 1040
    # good size: 1791
    width = 2388
    rows = pad_data(data, width)
    rows = np.reshape(rows, (-1, width))

    plt.matshow(rows, cmap=plt.cm.gray)
    plt.show()


input_file = "./test.wav"

samplerate, data = read_file(input_file)

resampled_9600 = resample(data, samplerate, 9600)
instantaneous_4800 = [(data[i] ** 2 + data[i + 1] ** 2) ** (1 / 2) for i in range(0, len(resampled_9600), 2)]
result_4160 = resample(instantaneous_4800, 4800, 4160)
filtered = filter(result_4160) * 255

draw(filtered)
