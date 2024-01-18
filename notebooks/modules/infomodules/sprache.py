#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sprache modules
"""
from googletrans import Translator
from num2words import num2words
import random

class sprache:
    def __init__(self):
        self.translator = Translator()

    def uebersetzen(self, satz, zielsprache='en'):
        translation = self.translator.translate(satz, dest=zielsprache)
        print(translation.origin, ' -> ', translation.text)

    def erkennen(self, text):
        normalized_text = self.normalisiere_umlaut(text)
        result = self.translator.detect(normalized_text)
        print(f"Sprache: {result.lang}\nSo sicher wurde die Sprache erkannt: {result.confidence * 100:.0f}%")
        return result.lang, result.confidence

    def normalisiere_umlaut(self, text):
        umlaute_dict = {
            'ae': 'ä', 'Ae': 'Ä', 'AE': 'Ä',
            'oe': 'ö', 'Oe': 'Ö', 'OE': 'Ö',
            'ue': 'ü', 'Ue': 'Ü', 'UE': 'Ü'
        }
        for key, value in umlaute_dict.items():
            text = text.replace(key, value)
        return text

if __name__ == "__main__":
    sprachuebersetzer = sprache()

    sprachuebersetzer.uebersetzen('Wir alle lieben Informatik!', zielsprache='fr')

    text_to_detect = 'Hagebutte'
    sprachuebersetzer.erkennen(text_to_detect)