import wave
import numpy as np
import random
from process import convert_to_mono
from process import read_audio
from process import logger


class EmbeddingLSB:
    def __init__(self, audio_path: str, secret_key: int, algorithm: str) -> None:
        self.audio_path = audio_path
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.audio_data, self.params = read_audio(self.audio_path)
        if self.audio_data is None:
            raise ValueError("Failed to read audio data.")

    def generate_secret_bits(self, length: int) -> str:
        """
        Generates a random sequence of bits based on the secret key.
        :param length: Length of the sequence.
        :return: Random sequence of bits as a string.
        """
        random.seed(self.secret_key)
        secret_bits = ''.join(str(random.randint(0, 1)) for _ in range(length))
        return secret_bits

    def get_embedding_function(self):
        match self.algorithm:
            case 'replace':
                return lambda sample, bit: (sample & ~1) | bit
            case 'xor':
                return lambda sample, bit: sample ^ bit
            case 'negate_xor':
                return lambda sample, bit: ~sample ^ bit
            case _:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def embed_bits(self) -> np.ndarray:
        """
        Embeds the secret bits into the audio data using the specified algorithm.
        :return: Numpy array of the audio samples with embedded secret bits.
        """
        secret_bits = self.generate_secret_bits(len(self.audio_data))
        samples = np.array(self.audio_data)
        embed_func = self.get_embedding_function()

        for i, bit in enumerate(secret_bits):
            samples[i] = embed_func(samples[i], int(bit))

        return samples

    def save_audio(self, file: str) -> None:
        """
        Saves the modified audio data with embedded bits to a new file.
        :param file: Path to the output audio file.
        :return: None
        """
        try:
            embedded_samples = self.embed_bits()
            with wave.open(file, 'wb') as wav:
                wav.setparams(self.params)
                wav.writeframes(embedded_samples.tobytes())

            logger.info(f"Algorithm '{self.algorithm}' successfully executed!")
            logger.info(f"The file has been saved as '{file}'.")
        except Exception as e:
            logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    input_file = "input_audio.wav"
    mono_file = "mono_audio.wav"
    key = 84
    convert_to_mono(input_file, mono_file)
    algorithms = ['replace', 'xor', 'negate_xor']
    output_files = ['output_replace.wav', 'output_xor.wav', 'output_negate_xor.wav']

    for algorithm, output_file in zip(algorithms, output_files):
        lsb_embedder = EmbeddingLSB(mono_file, key, algorithm)
        lsb_embedder.save_audio(output_file)
