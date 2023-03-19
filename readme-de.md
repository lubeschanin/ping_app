# **Ping-Status-App-Dokumentation**

## **Einleitung**

Die Ping-Status-App ist eine Webanwendung, die es Benutzern ermöglicht, den Ping-Status von Hosts innerhalb einer bestimmten Domain zu überprüfen. Die App bietet verschiedene Funktionen, um Informationen über Hosts und deren Verfügbarkeit zu erhalten.

## **Funktionalität**

Die Ping-Status-App besteht aus den folgenden Hauptkomponenten:

1. Startseite: Auf dieser Seite werden alle Hosts in der Domain und deren Ping-Status angezeigt. Benutzer können den Status jedes Hosts einsehen und Informationen über den Zeitpunkt der letzten Aktualisierung erhalten.
2. Hostnamen von heute: Diese Seite zeigt eine Liste der Hosts, die am aktuellen Tag erstellt wurden. Hier können Benutzer sehen, welche neuen Hosts hinzugefügt wurden und wann sie erstellt wurden.
3. Nie online: Auf dieser Seite werden Hosts angezeigt, die bisher noch nie online waren. Dies kann für Administratoren nützlich sein, um potenzielle Probleme mit der Konfiguration oder Infrastruktur zu identifizieren.

## **Technische Details**

Die Ping-Status-App wurde in Python entwickelt und verwendet das FastAPI-Framework für das Backend. Die Daten werden über das dnspython-Paket abgerufen und mit der Jinja2-Template-Engine für die Darstellung in HTML verarbeitet. Das Frontend verwendet Bootstrap 5 für das Styling und DataTables für erweiterte Tabellenfunktionen.

## **Installation und Setup**

1. Stellen Sie sicher, dass Python 3.7 oder höher auf Ihrem System installiert ist.
2. Klonen Sie das Repository oder laden Sie den Quellcode der App herunter.
3. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie:
    
    ```
    python -m venv venv
    source venv/bin/activate  # Für Windows: venv\Scripts\activate
    ```
    
4. Installieren Sie die erforderlichen Abhängigkeiten:
    
    ```
    pip install -r requirements.txt
    ```
    
5. Passen Sie die Konfiguration in der **`main.py`**Datei an, indem Sie die DNS-Server- und Zoneninformationen entsprechend Ihrem System eintragen.
6. Starten Sie die App, indem Sie den folgenden Befehl ausführen:
    
    ```
    uvicorn main:app --reload
    ```
    
7. Öffnen Sie einen Webbrowser und navigieren Sie zu **`http://localhost:8000`**, um die App zu verwenden.

## **Fazit**

Die Ping-Status-App bietet eine einfache und effektive Möglichkeit, den Ping-Status von Hosts innerhalb einer Domain zu überwachen. Durch den Einsatz moderner Webtechnologien und einer intuitiven Benutzeroberfläche ermöglicht die App Administratoren, den Überblick über die Verfügbarkeit ihrer Systeme zu behalten.
