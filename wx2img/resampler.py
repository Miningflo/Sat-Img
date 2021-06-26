import numpy as np
from scipy.io import wavfile
from scipy.signal import resample as rs
import math
import matplotlib.pyplot as plt


def pad_data(data, modulo):
    ext = modulo - (len(data) % modulo)
    return np.append(data, np.zeros(ext))


def resample(data, current_rate, target_rate):
    target_sample_count = len(data) // current_rate * target_rate
    return pad_data(rs(data, target_sample_count), target_rate)


input_file = "./test.wav"

samplerate, data = wavfile.read(input_file)

data = pad_data(data, samplerate)
resampled_9600 = resample(data, samplerate, 9600)
instantaneous_4800 = [(data[i] ** 2 + data[i + 1] ** 2) ** (1 / 2) for i in range(0, len(resampled_9600), 2)]
result_4160 = resample(instantaneous_4800, 4800, 4160)
print(len(result_4160))
filtered = (result_4160 - np.min(result_4160)) / (np.max(result_4160) - np.min(result_4160)) * 255
print(filtered)

# og size: 1040
# good size: 1791
width = 2388
rows = pad_data(filtered, width)
rows = np.reshape(rows, (-1, width))

plt.matshow(rows, cmap=plt.cm.gray)
plt.show()
