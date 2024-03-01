# shazam
Unsere Anwendung kann in folgende Hauptpunkte aufgeteilt werden.
Fingerabdruck: Die Erstellung eines Fingerabdrucks beginnt mit der Berechnung des Spektrogramms des Songs oder Audios. Anschließend werden Spitzen im Spektrogramm identifiziert, die die lautesten Frequenzen repräsentieren. Diese Spitzen werden gepaart, um einzigartige Hashes zu erstellen, die den Fingerabdruck des Songs bilden. Diese Hashes werden dann in der Datenbank gespeichert.
Erkenner: Der Erkenner berechnet zunächst einen Fingerabdruck des eingegebenen Audio-Samples. Anschließend sucht er nach übereinstimmenden Hashes in der Datenbank und gruppiert diese nach Song. Die Übereinstimmung jedes potenziellen Songs wird anhand der zeitlichen Ausrichtung der Hashes bewertet. Der Song mit der höchsten Übereinstimmung wird als wahrscheinlichste Identifizierung des Audio-Samples ausgewählt.
Streamlit-Benutzeroberfläche: Die Streamlit-Benutzeroberfläche wurde entwickelt, um die Anwendung nutzerfreundlich zu gestalten. Sie ermöglicht es Benutzern, Audio-Samples aufzunehmen und mit dem Erkenner zu interagieren. Die Benutzeroberfläche zeigt die Ergebnisse der Song-Identifizierung an und erleichtert die Navigation durch die Anwendung.
Datenbank: Die Datenbank dient zur effizienten Speicherung von Fingerabdrücken und zugehörigen Metadaten. Sie ist so strukturiert, dass Fingerabdrücke schnell und effizient abgerufen werden können. Die Datenbank unterstützt Funktionen wie das Hinzufügen, Aktualisieren und Löschen von Fingerabdrücken und gewährleistet die Skalierbarkeit und Leistungsfähigkeit für den Betrieb mit großen Datenmengen.
Hiermit werden die Grundvoraussetzungen für das Projekt erfüllt. Neben diese haben wir das Projekt noch mit folgenden Punkten erweitert:

1.	Erstellung von Links
Wenn ein gesuchter Song gefunden wird, werden in Streamlit zwei Links angezeigt. Einer führt den Nutzer auf den gefundenen Song auf Spotify und der andere führt zum gefundenen Song auf YouTube.

2.	Albumcover
Wenn man in Streamlit einen Song sucht, kann man wählen, ob ein Cover angezeigt werden soll oder nicht. Wenn man dies will, wird mit Hilfe von DuckDuckGo ein Song-Cover angezeigt, wenn der Song gefunden wird.

3.	Waveform hinzugefügt
In Streamlit wird die Waveform des hochgeladenen Songs geplottet und grafisch dargestellt.

4.	Gesuchten Song abspielen
Der gesuchte Song, den man auf Streamlit in der Tab2 hochgeladen hat, kann nun auch abgespielt werden, wie der Hochgeladene in der Tab1.

