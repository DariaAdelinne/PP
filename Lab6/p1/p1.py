import os
import struct
from abc import ABC, abstractmethod


class GenericFile(ABC):
    @abstractmethod
    def get_path(self):
        pass

    @abstractmethod
    def get_freq(self):
        pass

    @staticmethod
    def compute_frequencies(content):
        freq = {i: 0 for i in range(256)}
        for byte in content:
            freq[byte] += 1
        return freq


class TextASCII(GenericFile):
    def __init__(self, path, content):
        self.path_absolut = path
        self.frecvente = GenericFile.compute_frequencies(content)

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class TextUNICODE(GenericFile):
    def __init__(self, path, content):
        self.path_absolut = path
        self.frecvente = self.compute_frequencies(content)

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class Binary(GenericFile):
    def __init__(self, path, content):
        self.path_absolut = path
        self.frecvente = GenericFile.compute_frequencies(content)

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class XMLFile(TextASCII):
    def __init__(self, path, content):
        super().__init__(path, content)
        self.first_tag = self.get_first_tag(content)

    def get_first_tag(self, content):
        try:
            text = content.decode('ascii', errors='ignore')
            start = text.find('<')
            end = text.find('>', start)
            if start != -1 and end != -1 and '</' in text:
                return text[start:end + 1]
        except:
            return None
        return None


class BMP(Binary):
    def __init__(self, path, content):
        super().__init__(path, content)
        self.width, self.height, self.bpp = self.extract_info(content)

    def extract_info(self, content):
        if len(content) >= 30 and content[:2] == b'BM':  # primii 2 arata ca este BMP
            width = struct.unpack('<I', content[18:22])[0]  # latimea imaginii
            height = struct.unpack('<I', content[22:26])[0]  # inaltimea
            bpp = struct.unpack('<H', content[28:30])[0]  # biti per pixel
            return width, height, bpp
        return None, None, None

    def show_info(self):
        return f'BMP File: {self.get_path()} - Width: {self.width}, Height: {self.height}, BPP: {self.bpp}'


def identify_file_type(path, content):
    # 1. Verifică BMP
    if len(content) >= 30 and content[:2] == b'BM':
        return BMP(path, content)

    # 2. Frecvențe de caractere
    freq = GenericFile.compute_frequencies(content)
    total_chars = sum(freq.values())
    if total_chars == 0:
        return None

    ascii_ratio = sum(freq[i] for i in range(9, 128)) / total_chars
    unicode_zero_ratio = freq[0] / total_chars

    if ascii_ratio > 0.9 and unicode_zero_ratio < 0.01:
        try:
            text = content.decode('ascii')
            if '<' in text and '>' in text and '</' in text:
                return XMLFile(path, content)
            return TextASCII(path, content)
        except:
            pass

    if content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff'):
        return TextUNICODE(path, content)

    try:
        content.decode('utf-8')
        return TextUNICODE(path, content)
    except UnicodeDecodeError:
        pass

    return Binary(path, content)



def scan_directory(directory):
    results = {
        'xml': [],
        'unicode': [],
        'bmp': [],
        'text_ascii': [],
        'binary': []
    }

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                    identified_file = identify_file_type(file_path, content)

                    if identified_file:
                        frecvente = identified_file.get_freq()
                        print(f"[DEBUG] Frequencies for {identified_file.get_path()}:")
                        print({k: v for k, v in frecvente.items() if v > 0})

                    if isinstance(identified_file, XMLFile):
                        results['xml'].append(identified_file.get_path())
                    elif isinstance(identified_file, TextUNICODE):
                        results['unicode'].append(identified_file.get_path())
                    elif isinstance(identified_file, BMP):
                        results['bmp'].append(identified_file.show_info())
                    elif isinstance(identified_file, TextASCII):
                        results['text_ascii'].append(identified_file.get_path())
                    elif isinstance(identified_file, Binary):
                        results['binary'].append(identified_file.get_path())

    return results

directory_to_scan = "C:\\Users\\Infoscop\\PycharmProjects\\PythonProject\\fisier_texte"
scan_results = scan_directory(directory_to_scan)

print("\nRezultate:")
print("XML Files:", scan_results['xml'])
print("UNICODE Files:", scan_results['unicode'])
print("BMP Files:", scan_results['bmp'])
print("Text ASCII Files:", scan_results['text_ascii'])
print("Binary Files:", scan_results['binary'])
