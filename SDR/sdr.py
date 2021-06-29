from rtlsdr import RtlSdr

sdr = RtlSdr()


def listen(frequency, duration):
    # configure device
    sample_rate = 11025
    sdr.sample_rate = sample_rate  # Hz
    sdr.center_freq = frequency * 1e6  # Hz
    sdr.bandwidth = 60e3  # Hz
    sdr.gain = 'auto'

    samples = sdr.read_samples(sample_rate * duration)
    sdr.close()

    return samples, sample_rate
