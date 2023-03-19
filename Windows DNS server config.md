# Windows DNS server config

To add an IP address to a Windows DNS server to allow zone transfers, follow these steps:

1. Open the DNS Manager console on your Windows server. To do this, click the Windows logo in the taskbar, type "DNS Manager" in the search bar, and click the appropriate result.
2. Navigate to the zone for which you want to allow zone transfers.
3. Right-click the zone and select "Properties" from the context menu.
4. Click on the "Zone Transfers" tab.
5. Check the box for "Allow zone transfers."
6. Select "Only to specific servers" and click the "Add" button.
7. Enter the IP address of the server to which you want to transfer the zone.
8. Click "OK" to complete the addition of the IP address.
9. Repeat this process for any additional servers that should receive the zone.
10. Click "OK" to close the zone properties and save the changes.

By adding the server's IP address to the zone transfer, you allow this server to receive and update the DNS zone data of your domain. However, note that you should only add the IP address to servers you trust and are authorized to access your DNS servers.