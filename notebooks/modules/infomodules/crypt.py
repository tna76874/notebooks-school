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

def buchstaben_haeufigkeiten(satz):
    _ = [print (f'{k[0]} : {k[1]*100:.2f}%') for k in sorted({buchstabe.lower(): satz.lower().count(buchstabe.lower()) / len(satz) for buchstabe in set(satz) if buchstabe.isalpha()}.items(), key=lambda x: x[1], reverse=True)]

if __name__ == "__main__":
    caesar_verschlüsseln('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'D')

    caesar_entschlüsseln('LJMJNRSFHMWNHMY', 'F')

    buchstaben_haeufigkeiten("""
    Die Caesar-Verschlüsselung (auch als Cäsar-Chiffre, Cäsar-Algorithmus, Caesar-Verschiebung, Verschiebechiffre oder als Einfacher Caesar bezeichnet)
    ist ein einfaches symmetrisches Verschlüsselungsverfahren, das auf der monographischen und monoalphabetischen Substitution basiert. Als eines der einfachsten
    und unsichersten Verfahren dient es heute hauptsächlich dazu, Grundprinzipien der Kryptologie anschaulich darzustellen. Der Einfachheit halber werden oftmals nur die 
    26 Buchstaben des lateinischen Alphabets ohne Unterscheidung von Groß- und Kleinbuchstaben als Alphabet für Klartext und Geheimtext verwendet und Sonderzeichen, Satzzeichen 
    usw. nicht beachtet.

    Wie alle monoalphabetischen Verschlüsselungsverfahren bietet auch die Verschiebechiffre keine hinreichende Sicherheit gegen unbefugte Entzifferung und kann sehr leicht „geknackt“
    werden. Die in der natürlichen Sprache ungleiche Verteilung der Buchstaben wird durch diese Art der Verschlüsselung nicht verborgen, so dass eine Häufigkeitsanalyse das Wirken einer
    einfachen monoalphabetischen Substitution enthüllt.

    Das folgende Diagramm zeigt die Häufigkeitsverteilung der Buchstaben in einem längeren Text in deutscher Sprache:

    Die Darstellung von Grafiken ist aktuell auf Grund eines Sicherheitsproblems deaktiviert.

    Wie zu erwarten, ist der häufigste Buchstabe E, gefolgt von N und I, wie es im Deutschen üblicherweise der Fall ist. Wird der Text mit dem Schlüssel 10
    (oder anders gesagt, mit dem Schlüsselbuchstaben J) chiffriert, erhält man einen Geheimtext, der folgende Häufigkeitsverteilung besitzt:

    Die Darstellung von Grafiken ist aktuell auf Grund eines Sicherheitsproblems deaktiviert.

    Der häufigste Buchstabe ist hier O, gefolgt von X und S. Man erkennt auf den ersten Blick die Verschiebung des deutschen „Häufigkeitsgebirges“
    um zehn Stellen nach hinten und besitzt damit den Schlüssel. Voraussetzung ist lediglich, dass man die Verteilung der Zeichen des Urtextes vorhersagen kann.

    Besitzt man diese Information nicht oder möchte man auf die Häufigkeitsanalyse verzichten, kann man auch die Tatsache ausnutzen, dass bei der Cäsar-Chiffre nur
    eine sehr kleine Anzahl möglicher Schlüssel in Frage kommt. Da die Größe des Schlüsselraums nur 25 beträgt, was einer „Schlüssellänge“ von nicht einmal 5 bit entspricht,
    liegt nach Ausprobieren spätestens nach dem 25. Versuch der Klartext vor. Eine erschöpfende Schlüsselsuche (Exhaustion) ist bei der Caesar-Verschlüsselung trivial realisierbar.
    Da dies auch ohne Computer oder Rechenmaschine mit geringem Aufwand möglich ist, bestand die Sicherheit der Caesar-Verschlüsselung schon zu ihren Anfängen nicht auf der
    Geheimhaltung des Schlüssels, sondern im Wesentlichen auf der Geheimhaltung des Verfahrens, und entspricht damit nicht dem im 19. Jahrhundert postulierten Prinzip von Auguste
    Kerckhoffs.

    """)