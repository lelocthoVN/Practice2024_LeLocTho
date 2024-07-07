import wave
import numpy as np
import matplotlib.pyplot as plt


def read_audio(file):
    """
    Reads audio data from a .wav file.
    :param file: Path to the .wav file.
    :return: Tuple containing samples as a numpy array and wave file parameters.
    """
    try:
        with wave.open(file, 'rb') as wav:
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            samples = np.frombuffer(frames, dtype=np.int16)
        return samples, params
    except Exception as e:
        print(f"Error reading the wave file: {e}")
        return None, None


def plot_histogram(file, ax, title):
    """
    Plots the histogram of audio samples.
    :param file: Path to the audio file.
    :param ax: Matplotlib axis to plot on.
    :param title:
    :return:
    """
    samples, _ = read_audio(file)
    if samples is not None:
        ax.hist(samples, bins=256, range=(-32768, 32767), edgecolor='black')
        ax.set_title(title)
        ax.set_xlabel('Sample Value')
        ax.set_ylabel('Frequency')
    else:
        print(f"Could not plot histogram for {file}.")


def compare_histograms(original_file, stego_files, stego_titles):
    """
    Compares histograms of the original audio file and stego audio files.
    :param original_file: Path to the original audio file.
    :param stego_files: List of paths to stego audio files.
    :param stego_titles: List of titles for stego histograms.
    :return: None
    """
    fig, axes = plt.subplots(len(stego_files) + 1, 1, figsize=(10, 5 * (len(stego_files) + 1)))
    plot_histogram(original_file, axes[0], "Original Audio")
    for i, (stego_file, title) in enumerate(zip(stego_files, stego_titles)):
        plot_histogram(stego_file, axes[i + 1], title)

    plt.tight_layout()
    plt.show()


def plot_histogram_difference(original_hist, stego_hist, bins, ax, title):
    """
    Plots the difference between the histograms of original and stego audio files.
    :param original_hist: Histogram of the original audio samples.
    :param stego_hist: Histogram of the stego audio samples.
    :param bins: Bins used for the histograms.
    :param ax: Matplotlib axis to plot on.
    :param title: Title of the histogram difference plot.
    :return: None

    difference = stego_hist - original_hist
    ax.bar(bins[:-1], difference, width=1, edgecolor='Red')
    ax.set_title(title)
    ax.set_xlabel('Sample Value')
    ax.set_ylabel('Frequency Difference')
"""
    difference = stego_hist - original_hist
    ax.bar(bins[:-1], difference, width=1, edgecolor='Red', color='blue', alpha=0.9)
    ax.set_title(title)
    ax.set_xlabel('Sample Value')
    ax.set_ylabel('Frequency Difference')


def compare_histogram_differences(original_file, stego_files, stego_titles):
    """
    Compares the histogram differences between the original audio file and stego audio files.
    :param original_file: Path to the original audio file.
    :param stego_files: List of paths to stego audio files.
    :param stego_titles: List of titles for the difference plots.
    :return: None
    """
    fig, axes = plt.subplots(len(stego_files), 1, figsize=(15, 5 * len(stego_files)))

    original_samples, _ = read_audio(original_file)
    original_hist, bins = np.histogram(original_samples, bins=256, range=(-32768, 32767))

    for i, (stego_file, title) in enumerate(zip(stego_files, stego_titles)):
        stego_samples, _ = read_audio(stego_file)
        stego_hist, _ = np.histogram(stego_samples, bins=256, range=(-32768, 32767))
        plot_histogram_difference(original_hist, stego_hist, bins, axes[i], title)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    mono_file = "mono_audio.wav"

    output_files = ['output_replace.wav', 'output_xor.wav', 'output_negate_xor.wav']
    stego_titles = ['Replace LSB', 'XOR LSB', 'Negate XOR LSB']

    compare_histograms(mono_file, output_files, stego_titles)
    compare_histogram_differences(mono_file, output_files, stego_titles)
