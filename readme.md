# **Ping-Status App Documentation**

## **Overview**

The Ping-Status App is a web application that fetches and displays information about the online status of hostnames within a specified DNS zone. The app allows users to view the hostnames that were never online, hostnames created today, and the ping status of all hostnames in the DNS zone.

## **Features**

1. Display a list of hostnames that have never been online.
2. Show hostnames created today.
3. Show the ping status of hostnames within the specified DNS zone, including their IPv4 addresses, status, and timestamps.

## **Technical Implementation**

The Ping-Status App is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python. The app uses the **`dnspython`** library to query DNS records and retrieve the required information.

### **Dependencies**

- dnspython==2.3.0
- fastapi==0.94.1
- Jinja2==3.1.2
- uvicorn==0.21.1

### **Directory Structure**

```
.
├── app
│   ├── main.py
│   ├── templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── navbar.html
│   │   ├── never_online.html
│   │   └── today.html
│   └── util
│       └── dns_helper.py
├── requirements.txt
└── README.md
```

### **Usage**

1. Install the required dependencies using the **`requirements.txt`** file:

```bash
pip install -r requirements.txt
```

1. Run the application using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

1. Access the application at **[http://localhost:8000/](http://localhost:8000/)**.

### **Application Structure**

The application consists of the following components:

- **`main.py`**: The main file that sets up the FastAPI app and handles routing.
- **`dns_helper.py`**: Contains the **`HostARecords`** class, which fetches the DNS records.
- **`templates/`**: A directory containing the Jinja2 HTML templates for each page:
    - **`base.html`**: The base layout template that other templates extend.
    - **`index.html`**: The template that shows the ping status of hostnames in the DNS zone.
    - **`navbar.html`**: Navigation
    - **`never_online.html`**: The template that displays hostnames that have never been online.
    - **`today.html`**: The template that displays hostnames created today.

## **Customization**

To customize the application for a specific DNS server and zone, modify the following values in the **`dns_helper.py`** file:

```python
dns_server = "your_dns_server_address"
zone_name = "your_zone_name"
```

Replace **`your_dns_server_address`** with the IP address or hostname of your DNS server, and **`your_zone_name`** with the name of the DNS zone you want to query.

## **Future Improvements**

1. Add authentication and user management to restrict access to authorized users.
2. Provide support for IPv6 addresses.
3. Implement pagination for displaying large sets of hostnames.
4. Add filtering and sorting functionality to the hostname tables.
5. Extend the application to support additional record types and DNS zones.
