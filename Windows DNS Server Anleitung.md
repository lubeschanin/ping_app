# Windows DNS Server Anleitung

Um unter Windows DNS Server eine IP-Adresse hinzuzufügen, damit der Zonentransfer erlaubt wird, müssen Sie die folgenden Schritte ausführen:

1. Öffnen Sie die DNS-Manager-Konsole auf Ihrem Windows-Server. Klicken Sie dazu auf das Windows-Logo in der Taskleiste, geben Sie "DNS-Manager" in die Suchleiste ein und klicken Sie auf das entsprechende Ergebnis.
2. Navigieren Sie zu der Zone, für die Sie den Zonentransfer erlauben möchten.
3. Klicken Sie mit der rechten Maustaste auf die Zone und wählen Sie "Eigenschaften" aus dem Kontextmenü aus.
4. Klicken Sie auf die Registerkarte "Zonentransfers".
5. Aktivieren Sie das Kontrollkästchen "Zulassen, dass Zone übertragen wird".
6. Wählen Sie "Nur zu bestimmten Servern" aus und klicken Sie auf die Schaltfläche "Hinzufügen".
7. Geben Sie die IP-Adresse des Servers ein, an den Sie die Zone übertragen möchten.
8. Klicken Sie auf "OK", um das Hinzufügen der IP-Adresse abzuschließen.
9. Wiederholen Sie diesen Vorgang für alle zusätzlichen Server, die die Zone empfangen sollen.
10. Klicken Sie auf "OK", um die Eigenschaften der Zone zu schließen und die Änderungen zu speichern.

Durch das Hinzufügen der IP-Adresse des Servers zum Zonentransfer erlauben Sie diesem Server, die DNS-Zonendaten Ihrer Domäne zu empfangen und zu aktualisieren. Beachten Sie jedoch, dass Sie die IP-Adresse nur Servern hinzufügen sollten, denen Sie vertrauen und die autorisiert sind, auf Ihre DNS-Server zuzugreifen.