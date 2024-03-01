# Softwaredesign Abschlussprojekt

## Inhalt

1. [Intro](#intro)
2. [Funktionsweise](#funktionsweise)
3. [Erweiterungen](#erweiterungen)
4. [Installation](#installation)
5. [UML Diagramm](#uml-diagramm)

## Intro
In diesem Programm wird eine beispielhafte Programmierung von Shazam nachgestellt. Dabei können ganze Songtitel hochgeladen werden. Aus diesen hochgeladenen Songs können dann in einem weiteren Tab kürzere Songsequenzen hochgeladen werden, die dann über den song-spezifischen Fingerabdruck erkannt werden.  
## Funktionsweise
Das Programm gliedert sich in mehrere Abschnitte. Zunächst wird beim Hochladen eines Songs ein Fingerprint erstellt. Die Erstellung des Fingerprints beginnt mit der Berechnung des Spektrogramms des Songs. Anschließend werden die Peaks im Spektrogramm identifiziert, die die lautesten Frequenzen repräsentieren. Diese Peaks werden gepaart, um eindeutige Hashes zu erstellen, die den Fingerabdruck des Songs bilden. Diese Hashes werden in der Datenbank gespeichert.

Die Datenbank dient nicht nur der effizienten Speicherung von Fingerabdrücken und zugehörigen Metadaten. Sie ist so strukturiert, dass Fingerprints schnell und effizient abgerufen werden können. Die Datenbank unterstützt Funktionen wie das Hinzufügen, Aktualisieren und Löschen von Fingerabdrücken und gewährleistet die Skalierbarkeit und Leistungsfähigkeit für den Betrieb mit großen Datenmengen.

Wird nun im zweiten Tab eine kürzere Song-Sequenz hochgeladen, wird diese in den Recognicer eingelesen und die Funktion erstellt einen Fingerabdruck für diese Sequenz. Anschließend sucht der Recognicer in der Datenbank nach übereinstimmenden Hashes und gruppiert diese nach Songs. Die Übereinstimmung jedes potentiellen Songs wird anhand der zeitlichen Ausrichtung der Hashes bewertet. Der Song mit der höchsten Übereinstimmung wird als wahrscheinlichste Identifikation des Audiosamples ausgewählt.

Mit Hilfe von Streamlit wurde eine Benutzeroberfläche erstellt. Die Streamlit-Benutzeroberfläche wurde entwickelt, um die Anwendung benutzerfreundlich zu gestalten. Sie ermöglicht es dem Benutzer, Audiosamples aufzunehmen und mit dem Erkenner zu interagieren. Die Benutzeroberfläche zeigt die Ergebnisse der Song-Identifikation an und erleichtert die Navigation durch die Anwendung.

## Erweiterungen
Neben den genannten Mindestanforderungen wurden weitere Ergänzungen implementiert. Als erste Erweiterung wurde eine Funktion hinzugefügt, die zu den erkannten Songs entsprechende Links für Spotify und Youtube ausgibt.

Eine weitere Erweiterung ist die Erstellung eines Covers des erkannten Songs. Dies wurde mit Hilfe von DuckDuckGo umgesetzt. Über Streamlit kann man dann auswählen, ob das Cover angezeigt werden soll oder nicht. Dies kann über eine Checkbox aktiviert oder deaktiviert werden.

Als nächste zusätzliche Implementierung wird noch die Waveform erstellt und ebenfalls über ein Auswahlkästchen grafisch dargestellt oder nicht. Die Waveform ist der Lautstärkeverlauf eines Songs.

In beiden Tabs können die Songs, die hochgeladen wurden, abgespielt werden und sorgen so für eine angenehmere und interessantere Bedienung des Interfaces.

Außerdem wurde eine Song-History hinzugefügt. Diese kann über einen Button angezeigt werden. Es werden die letzten fünf erkannten Songs angezeigt.

## Installation

1. Klonen Sie dieses Repository:

    ```bash
    git clone https://github.com/J0n1lu5/shazam
    ```

2. Wechseln Sie in das Verzeichnis:

    ```bash
    cd shazam
    ```

3. Installieren Sie die erforderlichen Pakete:

    ```bash
    pip install -r requirements.txt
    ```

4. Starten sie Streamlit um die Benutzeroberfläche zu starten:

    ```bash
    streamlit run user_interface.py
    ```


# UML Diagramm
![UML-Diagramm](https://github.com/timhornikel/shazam/UML-1.png)