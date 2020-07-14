import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pymongo
import threading, time


async def get_html(url, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            html = await resp.text()
            return html
        return False


myclient = pymongo.MongoClient("mongodb+srv://apiuser:gFnQX2F7gfrbe1RS@nz-snow-api.68ddg.azure.mongodb.net/<dbname>?retryWrites=true&w=majority")


mydb = myclient["nzsnowapi"]

async def deleteCard():
    mycol = mydb["cardrona_data"]
    x = mycol.delete_many({})
    return(x.deleted_count, " documents deleted.") 


async def cardrona(session):

    mycol = mydb["cardrona_data"]

    await deleteCard()

    url = "https://www.cardrona.com/winter/snow-report/"
    html = await get_html(url, session)
    soup = BeautifulSoup(html, "lxml")
    site_status_data = {"data": []}
    mes_data_data = {"data": []}
    wind_status_data_data = {"data": []}
    open_status_data_data = {"data": []}

    for report in soup.find_all("div", {"class": "c-snow-report__site"}):
        site_status = report.find("span", {"class": "c-snow-report__site-status"}).get_text()
        site_status_data["data"].append(site_status)

    for weather in soup.find_all("div", {"class": "c-snow-report__weather-header"}):
        weather_desc = weather.find("div", {"class": "c-snow-report__current-desc"}).get_text()

    outlook = soup.find("div", {"class": "c-snow-report__info-wrapper"})
    outlook_desc = outlook.find("div", {"class": "c-snow-report__info"}).get_text()

    for mes in soup.find_all("span", {"class": "c-snow-report__measurement-value"}):
        mes_data = mes.get_text()
        mes_data_data["data"].append(mes_data)

    for wind_status in soup.find_all("span", {"class": "c-snow-report__wind-status"}):
        wind_stats_data = wind_status.get_text()
        wind_status_data_data["data"].append(wind_stats_data)

    for snow_condition in soup.find_all("div", {"class": "c-snow-report__info-wrapper truncate-print u-mt"}):
        snow_condition_data = snow_condition.find("div", {"class": "c-snow-report__info"}).get_text()

    for open_status in soup.find_all("td", {"class": "c-snow-report__table-status"}):
        open_status_data = open_status.get_text()
        open_status_data_data["data"].append(open_status_data)
    
    import_data = { 
        "serivce_open": [
            {
                "service_name": "Resort", "status": site_status_data["data"][0]
            }, 
            {
                "service_name": "Lifts", "status": site_status_data["data"][1]
            }, 
            {
                "service_name": "Road", "status": site_status_data["data"][2]
            }
        ],
        "weather": weather_desc,
        "outlook": outlook_desc,
        "todays_temp": [
            {
                "position": "Upper 1860m", "temp": mes_data_data["data"][0]
            },
            {
                "position": "Mid 1640m", "temp": mes_data_data["data"][1]
            },
            {
                "position": "Lower 1260m", "temp": mes_data_data["data"][2]
            }
        ],
        "snow_level": [
            {
                "position": "Upper 1860m", "snow_level": mes_data_data["data"][3]
            },
            {
                "position": "Mid 1640m", "snow_level": mes_data_data["data"][4]
            },
            {
                "position": "Lower 1260m", "snow_level": mes_data_data["data"][5]
            }
        ],
        "snowfall_last_7_days": mes_data_data["data"][6],
        "wind_status": [
            {
                "position": "Upper 1860m", "wind_level": wind_status_data_data["data"][0]
            },
            {
                "position": "Mid 1640m", "snow_level": wind_status_data_data["data"][1]
            },
            {
                "position": "Lower 1260m", "snow_level": wind_status_data_data["data"][2]
            }
        ],
        "snow_condition": snow_condition_data,
        "open_status": [
            {
                "lift": "McDougall's Chondola", "status": open_status_data_data["data"][0]
            },
            {
                "lift": "Whitestar Express", "status": open_status_data_data["data"][1]
            },
            {
                "lift": "Captain's Express", "status": open_status_data_data["data"][2]
            },
            {
                "lift": "Learner Conveyors", "status": open_status_data_data["data"][3]
            },
            {
                "lift": "Kindy Conveyor", "status": open_status_data_data["data"][4]
            },
            {
                "food": "Mezz Café", "status": open_status_data_data["data"][5]
            },
            {
                "food": "The Lounge", "status": open_status_data_data["data"][6]
            },
            {
                "food": "Noodle Bar", "status": open_status_data_data["data"][7]
            },
            {
                "food": "F&B Base Bar", "status": open_status_data_data["data"][8]
            },
            {
                "food": "Captain's Café", "status": open_status_data_data["data"][9]
            },
            {
                "food": "Vista Bar", "status": open_status_data_data["data"][10]
            },
            {
                "food": "F&B Base Café", "status": open_status_data_data["data"][11]
            },
            {
                "food": "Stag Lane", "status": open_status_data_data["data"][12]
            },
            {
                "food": "Antlers Alley", "status": open_status_data_data["data"][13]
            },
            {
                "food": "Lil' Bucks", "status": open_status_data_data["data"][14]
            },
            {
                "food": "Sightseeing", "status": open_status_data_data["data"][15]
            },
        ]
    }
    x = mycol.insert_one(import_data)
    id_data = x.inserted_id
    return id_data


WAIT_TIME_SECONDS = 3600
ticker = threading.Event()

async def run_def():
    async with aiohttp.ClientSession() as session:
        print((await cardrona(session)))


if __name__ == "__main__":
    while not ticker.wait(WAIT_TIME_SECONDS):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_def())
