from utils import *
import io
from matplotlib import pyplot as plt


def sample_steps(data, samplerate):
    resampled_9600 = resample(data, samplerate, 9600*2)
    instantaneous_4800 = [(resampled_9600[i] ** 2 + resampled_9600[i + 2] ** 2) ** (1 / 2) for i in range(0, len(resampled_9600)-2, 1)]
    result_16640 = resample(instantaneous_4800, 9600*2, 16640)
    #here syncing could happen
    #result_4160 = resample(instantaneous_4800, 4800, 4160)
    return filter(result_16640)


def histogram(data):
    histogram = np.zeros(256, dtype=int)
    for e in data:
        #print(e)
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
    #expected width 2080
    # og size: 1040
    # good size: 1791
    # width = 2388
    width = 2080
    rows = pad_data(data, width)
    rows = np.reshape(rows, (-1, width))

    # img1 -17/40
    print(rows.shape)
    #rows = align(rows, -3/4)
    print(rows.shape)

    plt.figure(figsize=tuple(reversed(rows.shape)), dpi=1, tight_layout=True)
    plt.imshow(rows, cmap=plt.cm.gray, interpolation=None)
    plt.axis('off')
    buf = io.BytesIO()
    # plt.savefig(buf, format=ext, bbox_inches='tight', pad_inches=0)
    plt.savefig("test.png", dpi=1)
    buf.seek(0)
    plt.show()
    return buf

import numpy as np
def sync(data, times=1):
    kernel = [-1,-1,1,1]*7 + [-1,-1,-1,-1,-1,-1,-1,-1]
    kernel = [val for val in kernel for _ in range(times)]

    print(data)
    print(kernel)
    kernel.reverse()
    print(kernel)
    convolution = np.convolve(data, kernel, mode="same")
    min_row_length = 2079*times
    normal_row_length = 2080*times
    max_row_length = 2500*times
    splits = [0]
    counter = 0
    max_value = -100000
    max_index = 0
    skipped_rows = 0
    index = 0
    treshold = 1300*times
    while index < len(convolution):
    #for index, value in enumerate(convolution):
        if counter >= max_row_length:
            #print(max_value)
            if max_value > treshold:
                #add max_index to list
                if(len(splits) == 1):
                    skipped_rows=0
                if(skipped_rows>0):
                    print(skipped_rows)
                splits.extend([round(x) for x in np.linspace(splits[-1],max_index,skipped_rows+2)][1:])
                skipped_rows = 0
                index = max_index + len(kernel)
            else:
                skipped_rows += 1
                index = splits[-1] + min_row_length*skipped_rows
                #add one to skipped rows
            #use the max value
            max_value = -100000
            counter = 0
            
        
        if convolution[index] > max_value:
            max_value = convolution[index]
            max_index = index

        counter += 1
        index += 1
    
    #image = np.zeros((len(splits),2080))
    result = []
    for i in range(len(splits)-1):
        row = data[splits[i]:splits[i]+normal_row_length]
        result.extend(row)
    
    return result

def lowpass(data, sample_rate):
    ## Compute Fourier Transform
    n = len(data)
    fhat = np.fft.fft(data, n) #computes the fft
    psd = fhat * np.conj(fhat)/n
    #freq = (1/(dt*n)) * np.arange(n) #frequency array
    fft_fre = np.fft.fftfreq(n=n, d=1/sample_rate)
    #idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32) #first half index

    ## Filter out noise
    threshold = 4800
    freq_pass = fft_fre <= threshold #array of 0 and 1
    #psd_clean = psd * psd_idxs #zero out all the unnecessary powers
    fhat_clean = freq_pass * fhat #used to retrieve the signal

    signal_filtered = np.real(np.fft.ifft(fhat_clean)) #inverse fourier transform
    return signal_filtered

def main():
    input_file = "./test3-1.wav"
    samplerate, data = read_file(input_file)
    data = lowpass(data, samplerate)
    #rows = sync(cutoff(sample_steps(data, samplerate)))
    rows = sync(cutoff(sample_steps(data, samplerate)), times=4)
    result_4160 = resample(rows, 16640, 4160)
    data_to_img(result_4160)

    #plt.figure(figsize=tuple(reversed(rows.shape)), dpi=1, tight_layout=True)
    #plt.imshow(rows, cmap=plt.cm.gray, interpolation=None)
    #plt.axis('off')
    #plt.savefig("test.png", dpi=1)


#import math
#def main2():
#    input_file = "./test3-1.wav"
#    samplerate, data = read_file(input_file)
#    resampled_20800 = resample(data, samplerate, 20800)
#    carrier_f = 2400
#    
#    phi = 2.0 * (carrier_f*2.0*math.pi)
#    #phi = 2*math.pi*(carrier_f/sampling_f)
#    #math.cos(phi)/math.sin(phi)
#    #math.sqrt(x[i-1]**2 + x[i]**2 - x[i-1]*x[i]*2*math.cos(phi))/math.sin(phi)


if __name__ == "__main__":
    main()