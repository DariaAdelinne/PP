import os
import struct
from abc import ABC, abstractmethod


class GenericFile(ABC):
    @abstractmethod
    def get_path(self): #pentru calea fisierului
        pass

    @abstractmethod
    def get_freq(self): #pentru a obtine frecventa caracterelor din fisier
        pass

    @staticmethod
    def compute_frequencies(content): #pentru frecventa fiecarui byte
        freq = {i: 0 for i in range(256)} #dictionar de frecvente
        for byte in content: #pentru fiecare byte ii creste frecventa
            freq[byte] += 1
        return freq


class TextASCII(GenericFile):  #fisiere text in fromat ascii
    def __init__(self, path, content): #constructor
        self.path_absolut = path #stocheaza calea fisierului
        self.frecvente = GenericFile.compute_frequencies(content)  #calculeaza frecventele

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class TextUNICODE(GenericFile):  #fisiere text in format Unicode, are 0 in cel putin 30% din continut
    def __init__(self, path, content):
        self.path_absolut = path
        self.frecvente = self.compute_frequencies(content)

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class Binary(GenericFile):   #fisiere binare
    def __init__(self, path, content):
        self.path_absolut = path
        self.frecvente = GenericFile.compute_frequencies(content)

    def get_path(self):
        return self.path_absolut

    def get_freq(self):
        return self.frecvente


class XMLFile(TextASCII): #fisiere XML, mosteneste TextASCII
    def __init__(self, path, content):
        super().__init__(path, content)
        self.first_tag = self.get_first_tag(content)

    def get_first_tag(self, content): #cauta si extrage primul tag xml
        try:
            text = content.decode('ascii', errors='ignore')
            start = text.find('<')
            end = text.find('>', start)
            if start != -1 and end != -1 and '</' in text:
                return text[start:end + 1]
        except:
            return None
        return None


class BMP(Binary): #fisiere BMP (imagine), extinde Binary
    def __init__(self, path, content):
        super().__init__(path, content)
        self.width, self.height, self.bpp = self.extract_info(content)

    def extract_info(self, content): #extrage informatiile
        if len(content) >= 30 and content[:2] == b'BM':  # primii 2 arata ca este BMP
            width = struct.unpack('<I', content[18:22])[0]  # latimea imaginii
            height = struct.unpack('<I', content[22:26])[0]  # inaltimea
            bpp = struct.unpack('<H', content[28:30])[0]  # biti per pixel
            return width, height, bpp
        return None, None, None

    def show_info(self): #returneaza informatiile fisierului BMP
        return f'BMP File: {self.get_path()} - Width: {self.width}, Height: {self.height}, BPP: {self.bpp}'


def identify_file_type(path, content): #analizeaza continutul fisierului pentru a determina tipul
    if len(content) >= 30 and content[:2] == b'BM': #verifica BMP
        return BMP(path, content)

    freq = GenericFile.compute_frequencies(content)     #frecvente de caractere
    total_chars = sum(freq.values()) #calculeaza nr tot de caractere
    if total_chars == 0:
        return None

    ascii_ratio = sum(freq[i] for i in range(9, 128)) / total_chars #calculeaza proportia de elem ASCII valide
    unicode_zero_ratio = freq[0] / total_chars #calculeaza proportia de byte uri 0

    if ascii_ratio > 0.9 and unicode_zero_ratio < 0.01: #daca nu e unicode continue sa verifice daca este un fisier XML sau ASCII
        try:
            text = content.decode('ascii')
            if '<' in text and '>' in text and '</' in text: #veriica daca este XML
                return XMLFile(path, content)
            return TextASCII(path, content)
        except:
            pass

    if content.startswith(b'\xff\xfe') or content.startswith(b'\xfe\xff'): #verifica daca este unicode
        return TextUNICODE(path, content)

    try:
        content.decode('utf-8')
        return TextUNICODE(path, content)
    except UnicodeDecodeError:
        pass

    return Binary(path, content)



def scan_directory(directory): #scaneaza un fisier pentru directoare
    results = {
        'xml': [],
        'unicode': [],
        'bmp': [],
        'text_ascii': [],
        'binary': []
    }

    for root, _, files in os.walk(directory): #parcurge toate fisierele din director
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path): #verifica daca calea se refera la un fisier si nu la un director
                with open(file_path, 'rb') as f: #dechide fisierul in mod binar pentru citire
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
