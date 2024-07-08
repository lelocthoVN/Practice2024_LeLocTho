from typing import Callable
from process import Optional
from process import read_audio


class ExtractorLSB:
    def __init__(self, audio_file: str) -> None:
        self.samples, _ = read_audio(audio_file)
        if self.samples is None:
            raise ValueError("Failed to read audio samples.")

    def extract_lsb(self, length: int, method: str) -> str:
        match method:
            case 'replace':
                extract_func: Callable[[int], int] = lambda sample: sample & 1
            case 'xor':
                extract_func = lambda sample: sample & 1
            case 'negate_xor':
                extract_func = lambda sample: ~sample & 1
            case _:
                raise ValueError(f"Unknown method: {method}")

        watermark = []
        for i in range(length):
            bit = extract_func(self.samples[i])
            watermark.append(bit)
        return ''.join(map(str, watermark))

    def extract_watermark(self, length: int, method: str) -> Optional[str]:
        if self.samples is not None:
            return self.extract_lsb(length, method)
        else:
            return None


if __name__ == "__main__":
    files_methods = [
        ('output_replace.wav', 'replace'),
        ('output_xor.wav', 'xor'),
        ('output_negate_xor.wav', 'negate_xor')
    ]
    watermark_length = 84
    for file, method in files_methods:
        extractor = ExtractorLSB(file)
        extracted_watermark = extractor.extract_watermark(watermark_length, method)
        if extracted_watermark is not None:
            print(f'Extracted watermark ({method}): {extracted_watermark}')
        else:
            print(f'Failed to extract watermark from {file}')
