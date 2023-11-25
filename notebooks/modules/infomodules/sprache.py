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
        result = self.translator.detect(text)
        print(f"Sprache: {result.lang}\nSo sicher wurde die Sprache erkannt: {result.confidence * 100:.0f}%")
        return result.lang, result.confidence

if __name__ == "__main__":
    sprachuebersetzer = sprache()

    sprachuebersetzer.uebersetzen('Wir alle lieben Informatik!', zielsprache='fr')

    text_to_detect = 'Hagebutte'
    sprachuebersetzer.erkennen(text_to_detect)