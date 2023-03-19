import asyncio, sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from datetime import datetime
import multiprocessing
from util.dns_helper import HostARecords


app = FastAPI(
    title="Ping-API",
    description="""The Ping-Status App is a web application that fetches and displays 
              information about the online status of hostnames within a specified DNS zone. 
              The app allows users to view the hostnames that were never online, 
              hostnames created today, and the ping status of all hostnames in the DNS zone.
              """,
    contact={"Email": "vit@lij.de"},
    version="0.1.4",
    license_info={"name": "GNU General Public License version 2 (GPLv2) "},
)

app.config = {
    "server_ip": "127.0.0.1",
    "server_port": 8000,
    "database": "results.db",
    "dns_server": "10.0.60.203",
    "dns_zone": "nardini.rp",
    "semaphore": 499,
    "sleep": 300,
}
templates = Jinja2Templates(directory="templates")


def get_db():
    db = sqlite3.connect(app.config["database"])
    db.row_factory = sqlite3.Row
    return db


def close_connection(db):
    if db is not None:
        db.close()


def create_table():
    with sqlite3.connect(app.config["database"]) as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS hostnames (id INTEGER PRIMARY KEY, hostname TEXT UNIQUE, created_at TEXT)"
        )
        db.execute(
            "CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY, IPv4Address TEXT, hostname_id INTEGER, status TEXT, timestamp TEXT, FOREIGN KEY(hostname_id) REFERENCES hostnames(id))"
        )
        db.commit()


def insert_result(target, hostname, status):
    with get_db() as db:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = db.execute("SELECT id FROM hostnames WHERE hostname=?", (hostname,))
        hostname_id = cursor.fetchone()

        if not hostname_id:
            db.execute(
                "INSERT INTO hostnames (hostname, created_at) VALUES (?, ?)",
                (hostname, current_time),
            )
            db.commit()
            hostname_id = db.execute(
                "SELECT id FROM hostnames WHERE hostname=?", (hostname,)
            ).fetchone()[0]
        else:
            hostname_id = hostname_id[0]

        db.execute(
            "INSERT INTO results (IPv4Address, hostname_id, status, timestamp) VALUES (?, ?, ?, ?)",
            (target, hostname_id, status, current_time),
        )
        db.commit()


def query_results():
    results = []
    dns_count = len(read_dns())
    with get_db() as db:
        cursor = db.execute(
            f"SELECT r.IPv4Address, h.hostname, r.status, r.timestamp FROM results r JOIN hostnames h ON r.hostname_id = h.id ORDER BY r.timestamp DESC LIMIT {dns_count}"
        )
        for row in cursor.fetchall():
            results.append(
                {
                    "IPv4Address": row["IPv4Address"],
                    "hostname": row["hostname"],
                    "status": row["status"],
                    "timestamp": row["timestamp"],
                }
            )
    return results


def query_today_hostnames():
    hostnames = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    with get_db() as db:
        cursor = db.execute(
            "SELECT hostname, created_at FROM hostnames WHERE DATE(created_at) = ?",
            (current_date,),
        )
        for row in cursor.fetchall():
            hostnames.append(
                {"hostname": row["hostname"], "created_at": row["created_at"]}
            )
    return hostnames


def query_never_online_hostnames():
    hostnames = []
    with get_db() as db:
        cursor = db.execute(
            "SELECT h.hostname FROM hostnames h LEFT JOIN results r ON h.id = r.hostname_id WHERE r.status != 'online' GROUP BY h.hostname"
        )
        for row in cursor.fetchall():
            hostnames.append({"hostname": row["hostname"]})
    return hostnames


async def async_ping(semaphore, target):
    async with semaphore:
        command = "ping -c 1 " + target["IPv4Address"]
        response = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await response.communicate()

        return target, response.returncode


async def ping_targets(targets):
    semaphore = asyncio.Semaphore(app.config["semaphore"])
    tasks = [async_ping(semaphore, target) for target in targets]
    results = await asyncio.gather(*tasks)

    for target, returncode in results:
        if returncode == 0:
            insert_result(
                target["IPv4Address"],
                target["Hostname"],
                "online",
            )
        else:
            insert_result(
                target["IPv4Address"],
                target["Hostname"],
                "nicht erreichbar",
            )


def read_dns():
    host_a_records_instance = HostARecords(
        app.config["dns_server"], app.config["dns_zone"]
    )
    return host_a_records_instance.fetch_records()


async def main():
    data = read_dns()
    targets = [i for i in data]
    await ping_targets(targets)


@app.get("/api/results", tags=["json"])
async def get_results():
    results = query_results()
    return JSONResponse(content=results)


@app.get("/api/hosts/today", tags=["json"])
async def get_hosts_today():
    hosts = query_today_hostnames()
    return JSONResponse(content=hosts)


@app.get("/api/hosts/never_online", tags=["json"])
async def get_hosts_never_online():
    hosts = query_never_online_hostnames()
    return JSONResponse(content=hosts)


@app.get("/today", response_class=HTMLResponse, tags=["html"])
async def display_today_hostnames(request: Request):
    hostnames = query_today_hostnames()
    return templates.TemplateResponse(
        "today.html", {"request": request, "hostnames": hostnames}
    )


@app.get("/never_online", response_class=HTMLResponse, tags=["html"])
async def display_never_online_hostnames(request: Request):
    hostnames = query_never_online_hostnames()
    return templates.TemplateResponse(
        "never_online.html", {"request": request, "hostnames": hostnames}
    )


@app.get("/", response_class=HTMLResponse, tags=["html"])
async def display_results(request: Request):
    results = query_results()
    return templates.TemplateResponse(
        "index.html", {"request": request, "results": results}
    )


async def schedule_main():
    while True:
        print(f"Starting main at {datetime.now()}")
        await main()
        print(f"Finished main at {datetime.now()}")
        await asyncio.sleep(app.config["sleep"])


def run_uvicorn():
    uvicorn.run(app, host=app.config["server_ip"], port=app.config["server_port"])


if __name__ == "__main__":
    create_table()
    uvicorn_process = multiprocessing.Process(target=run_uvicorn)
    uvicorn_process.start()
    asyncio.run(schedule_main())
