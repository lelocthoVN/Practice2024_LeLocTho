import wave
import numpy as np


def read_audio(file_audio):
    try:
        with wave.open(file_audio, 'rb') as wav:
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            samples = np.frombuffer(frames, dtype=np.int16)
        return samples, params
    except Exception as e:
        print(f"Error reading the wave file: {e}")
        return None, None


def extract_lsb(samples, length, methods):
    watermark = []
    for i in range(length):
        if methods == 'replace':
            bit = samples[i] & 1
        elif methods == 'xor':
            bit = samples[i] & 1
        elif methods == 'negate_xor':
            bit = samples[i] & 1
            bit = ~bit & 1
        watermark.append(bit)
    return ''.join(map(str, watermark))


def extract_watermark(file, length, method):
    samples, _ = read_audio(file)
    if samples is not None:
        return extract_lsb(samples, length, method)
    else:
        return None


if __name__ == "__main__":
    files_methods = [
        ('output_replace.wav', 'replace'),
        ('output_xor.wav', 'xor'),
        ('output_negate_xor.wav', 'negate_xor')
    ]
    watermark_length = 12
    for file, method in files_methods:
        extracted_watermark = extract_watermark(file, watermark_length, method)
        if extracted_watermark is not None:
            print(f'Extracted watermark ({method}): {extracted_watermark}')
        else:
            print(f'Failed to extract watermark from {file}')
