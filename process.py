import wave
import numpy as np
import logging
from typing import Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_to_mono(input_file: str, output_file: str) -> None:
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
        logger.info(f"Converted '{input_file}' to mono and saved as '{output_file}'.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def read_audio(file: str) -> Optional[Tuple[np.ndarray, wave._wave_params]]:
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
        logger.error(f"Error reading the wave file: {e}")