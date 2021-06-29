from wx2img.utils import *
import io
from matplotlib import pyplot as plt


def sample_steps(data, samplerate):
    resampled_9600 = resample(data, samplerate, 9600)
    instantaneous_4800 = [(data[i] ** 2 + data[i + 1] ** 2) ** (1 / 2) for i in range(0, len(resampled_9600), 2)]
    result_4160 = resample(instantaneous_4800, 4800, 4160)
    return filter(result_4160)


def histogram(data):
    histogram = np.zeros(256, dtype=int)
    for e in data:
        histogram[round(e)] += 1
    return histogram


def cumsum(histogram):
    cumsum = np.zeros(256, dtype=int)
    cumsum[0] = histogram[0]
    for i, e in enumerate(histogram[1:]):
        cumsum[i + 1] = cumsum[i] + e
    return cumsum


def histogram_normalise(data):
    cs = cumsum(histogram(data))
    mapping = np.zeros(256, dtype=int)
    grey_levels = 256
    for i in range(grey_levels):
        mapping[i] = max(0, round((grey_levels * cs[i]) / len(data)) - 1)

    for i, e in enumerate(data):
        data[i] = mapping[round(data[i])]

    return data


def cutoff(data):
    low_tresh = 0.03
    high_tresh = 0.97

    cs = cumsum(histogram(data))

    lower_bound = len(data) * low_tresh
    upper_bound = len(data) * high_tresh

    min_gray = 0
    while cs[min_gray] < lower_bound:
        min_gray += 1

    max_gray = 255
    while cs[max_gray] > upper_bound:
        max_gray -= 1

    data = (data - min_gray) / (max_gray - min_gray) * 255
    return np.clip(data, 0, 255)


def align(rows, factor):
    for i, e in enumerate(rows):
        rows[i] = np.roll(e, int(factor * i))
    return rows


def data_to_img(data, ext="png"):
    # og size: 1040
    # good size: 1791
    # width = 2388
    width = 2388
    rows = pad_data(data, width)
    rows = np.reshape(rows, (-1, width))

    # img1 -17/40
    rows = align(rows, -3/4)

    plt.matshow(rows, cmap=plt.cm.gray)
    plt.axis('off')
    plt.show()
    buf = io.BytesIO()
    plt.savefig(buf, format=ext, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    return buf


input_file = "./test3-1.wav"
samplerate, data = read_file(input_file)
data_to_img(cutoff(sample_steps(data, samplerate)))
