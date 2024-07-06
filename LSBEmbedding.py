import wave
import numpy as np


def convert_to_mono(input_file, output_file):
    """
    Convert a stereo audio file to mono.
    :param input_file: Input stereo audio file.
    :param output_file: Output mono audio file.
    :return: None
    """
    try:
        with wave.open(input_file, 'rb') as stereo_wave:
            params = stereo_wave.getparams()
            n_channels, sampwidth, framerate, n_frames = params[:4]
            frames = stereo_wave.readframes(n_frames)
            stereo_data = np.frombuffer(frames, dtype=np.int16)
            if n_channels == 2:
                left_channel = stereo_data[0::2]
                right_channel = stereo_data[1::2]
                mono_data = ((left_channel.astype(np.int32) + right_channel.astype(np.int32)) // 2).astype(np.int16)
            else:
                raise ValueError("The audio file is not stereo.")

        with wave.open(output_file, 'wb') as mono_wave:
            mono_wave.setnchannels(1)
            mono_wave.setsampwidth(sampwidth)
            mono_wave.setframerate(framerate)
            mono_wave.writeframes(mono_data.tobytes())
        print(f"Converted '{input_file}' to mono and saved as '{output_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_audio(file):
    try:
        with wave.open(file, 'rb') as wav:
            params = wav.getparams()
            frames = wav.readframes(params.nframes)
            samples = np.frombuffer(frames, dtype=np.int16)
        return samples, params
    except Exception as e:
        print(f"Error reading the wave file: {e}")


class EmbeddingLSB:
    def __init__(self, audio_path, secret_bits, algorithm):
        self.audio_path = audio_path
        self.secret_bits = secret_bits
        self.algorithm = algorithm
        self.audio_data, self.params = read_audio(self.audio_path)
        if self.audio_data is None:
            raise ValueError("Failed to read audio data.")

    def embed_bits(self):
        n = len(self.secret_bits)
        samples = np.array(self.audio_data)
        for i in range(n):
            bit = int(self.secret_bits[i])
            if self.algorithm == 'replace':
                samples[i] = (samples[i] & ~1) | bit
            elif self.algorithm == 'xor':
                samples[i] = samples[i] ^ bit
            elif self.algorithm == 'negate_xor':
                samples[i] = samples[i] ^ bit
                samples[i] = ~samples[i]
        return samples

    def save_audio(self, file):
        try:
            embedded_samples = self.embed_bits()
            with wave.open(file, 'wb') as wav:
                wav.setparams(self.params)
                wav.writeframes(embedded_samples.tobytes())

            print(f"Algorithm '{self.algorithm}' successfully executed!")
            print(f"The file has been saved as '{file}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        """
        bit_index = 0
        for i in range(len(audio_data)):
            if bit_index < len(self.secret_bits):
                audio_data[i] = (audio_data[i] & 0xFE) | int(self.secret_bits[bit_index])
                bit_index += 1
            else:
                break
        self.audio = (audio_data, params)

    def embed_bits_xor(self):
        audio_data, params = self.audio
        bit_index = 0
        for i in range(len(audio_data)):
            if bit_index < len(self.secret_bits):
                audio_data[i] = audio_data[i] ^ int(self.secret_bits[bit_index])
                bit_index += 1
            else:
                break
        self.audio = (audio_data, params)

    def embed_bits_xor_neg(self):
        audio_data, params = self.audio
        bit_index = 0
        for i in range(len(audio_data)):
            if bit_index < len(self.secret_bits):
                audio_data[i] = audio_data[i] ^ int(self.secret_bits[bit_index])
                audio_data[i] = ~audio_data[i] & 0xFF
                bit_index += 1
            else:
                break
        self.audio = (audio_data, params)

    def embed(self):
        if self.algorithm_variant == 'replace':
            self.embed_bits_replace()
        elif self.algorithm_variant == 'xor':
            self.embed_bits_xor()
        elif self.algorithm_variant == 'xor_neg':
            self.embed_bits_xor_neg()
        else:
            raise ValueError(f"Unknown algorithm variant: {self.algorithm_variant}")
        print(f"Algorithm '{self.algorithm_variant}' successes!")
"""


if __name__ == "__main__":
    input_file = "input_audio.wav"
    mono_file = "mono_audio.wav"
    output_file = 'embed_audio.wav'
    bits = '101010001110'
    algorithm_variant = 'replace'  # algorithm: 'replace', 'xor', 'xor_neg'

    convert_to_mono(input_file, mono_file)
    algorithms = ['replace', 'xor', 'negate_xor']
    output_files = ['output_replace.wav', 'output_xor.wav', 'output_negate_xor.wav']

    for algorithm, output_file in zip(algorithms, output_files):
        lsb_embedder = EmbeddingLSB(mono_file, bits, algorithm)
        lsb_embedder.save_audio(output_file)
