#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crypto modules
"""

def caesar_verschlüsseln(text, key):
    if isinstance(key,str): key = ord(key.upper()) - ord('A')
    return ''.join(chr((ord(char) - ord('A' if char.isupper() else 'a') + key) % 26 + ord('A' if char.isupper() else 'a')) if char.isalpha() else char for char in text)

def caesar_entschlüsseln(cipher, key):
    if isinstance(key,str): key = ord(key.upper()) - ord('A')
    return caesar_verschlüsseln(cipher, -key)


if __name__ == "__main__":
    caesar_verschlüsseln('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'D')

    caesar_entschlüsseln('LJMJNRSFHMWNHMY', 'F')