from wx2img.utils import *


def sample_steps(data, samplerate):
    resampled_9600 = resample(data, samplerate, 9600)
    instantaneous_4800 = [(data[i] ** 2 + data[i + 1] ** 2) ** (1 / 2) for i in range(0, len(resampled_9600), 2)]
    result_4160 = resample(instantaneous_4800, 4800, 4160)
    return filter(result_4160)


def histogram(data):
    return data * 255


def data_to_img(data, ext="png"):
    # og size: 1040
    # good size: 1791
    width = 2388
    rows = pad_data(data, width)
    rows = np.reshape(rows, (-1, width))

    plt.matshow(rows, cmap=plt.cm.gray)
    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format=ext, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    return buf
