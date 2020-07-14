#!/usr/bin/env python3
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pymongo
import threading, time
from datetime import datetime


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

async def deleteTC():
    mycol = mydb["treble_cone_data"]
    x = mycol.delete_many({})
    return(x.deleted_count, " documents deleted.")


async def cardrona(session):

    print(await treblecone(session))

    mycol = mydb["cardrona_data"]

    await deleteCard()

    url = "https://www.cardrona.com/winter/snow-report/"
    html = await get_html(url, session)
    soup = BeautifulSoup(html, "lxml")
    site_status_data = {"data": []}
    mes_data_data = {"data": []}
    wind_status_data_data = {"data": []}
    open_status_data_data = {"data": []}

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

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
        "data_updated": current_time,
        "serivce_open": [
            {
                "Resort": site_status_data["data"][0]
            }, 
            {
                "Lifts": site_status_data["data"][1]
            }, 
            {
                "Road": site_status_data["data"][2]
            }
        ],
        "weather": weather_desc,
        "outlook": outlook_desc,
        "todays_temp": [
            {
                "Upper 1860m": mes_data_data["data"][0]
            },
            {
                "Mid 1640m": mes_data_data["data"][1]
            },
            {
                "Lower 1260m": mes_data_data["data"][2]
            }
        ],
        "snow_level": [
            {
                "Upper 1860m": mes_data_data["data"][3]
            },
            {
                "Mid 1640m": mes_data_data["data"][4]
            },
            {
                "Lower 1260m": mes_data_data["data"][5]
            }
        ],
        "snowfall_last_7_days": mes_data_data["data"][6],
        "wind_status": [
            {
                "Upper 1860m": wind_status_data_data["data"][0]
            },
            {
                "Mid 1640m": wind_status_data_data["data"][1]
            },
            {
                "Lower 1260m": wind_status_data_data["data"][2]
            }
        ],
        "snow_condition": snow_condition_data,
        "open_status": [
            {
                "McDougall's Chondola": open_status_data_data["data"][0]
            },
            {
                "Whitestar Express": open_status_data_data["data"][1]
            },
            {
                "Valley View Quad": open_status_data_data["data"][2]
            },
            {
                "Captain's Express": open_status_data_data["data"][3]
            },
            {
                "Learner Conveyors": open_status_data_data["data"][4] 
            },
            {
                "Kindy Conveyor": open_status_data_data["data"][5]
            },
            {
                "Mezz Café": open_status_data_data["data"][6]
            },
            {
                "The Lounge": open_status_data_data["data"][7]
            },
            {
                "Noodle Bar": open_status_data_data["data"][8]
            },
            {
                "F&B Base Bar": open_status_data_data["data"][9]
            },
            {
                "Captain's Café": open_status_data_data["data"][10]
            },
            {
                "Vista Bar": open_status_data_data["data"][11]
            },
            {
                "F&B Base Café": open_status_data_data["data"][12]
            },
            {
                "Stag Lane": open_status_data_data["data"][13]
            },
            {
                "Antlers Alley": open_status_data_data["data"][14]
            },
            {
                "Lil' Bucks": open_status_data_data["data"][15]
            },
            {
                "Sightseeing": open_status_data_data["data"][16]
            },
        ]
    }
    x = mycol.insert_one(import_data)
    id_data = x.inserted_id
    return id_data

async def treblecone(session):

    mycol = mydb["treble_cone_data"]

    await deleteTC()

    url = "https://www.treblecone.com/mountain/snow-report/"
    html = await get_html(url, session)
    soup = BeautifulSoup(html, "lxml")
    data_tc = {"data": []}

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    for data in soup.find_all("div", {"class": "table__cell"}):
        tc_data = data.get_text().replace("\n", "").strip()
        data_tc["data"].append(tc_data)

    import_data_tc = {
        "data_updated": current_time,
        "ski_field_status": data_tc["data"][1],
        "snowfall": [
                {
                    "overnight_snowfall": data_tc["data"][5]
                },
                {
                    "snowfall_24_hours": data_tc["data"][7]
                },
                {
                    "snowfall_last_7_days": data_tc["data"][9]
                },
                {
                    "last_snowfall_date": data_tc["data"][11]
                },
                {
                    "last_snowfall_amount": data_tc["data"][13]
                },
            ],
            "basin_snow_depth": data_tc["data"][15],
            "saddle_snow_depth": data_tc["data"][17],
            "live_temp": data_tc["data"][19],
            "overnight_temp": data_tc["data"][21],
            "open_status": [
                {
                    "home_basin_express": data_tc["data"][23]
                },
                {
                    "saddle_quad_chair": data_tc["data"][25]
                },
                {
                    "nice_n_easy_platter": data_tc["data"][27]
                },
                {
                    "magic_carpet": data_tc["data"][29]
                },
                {
                    "home_basin": data_tc["data"][31]
                },
                {
                    "saddle_basin": data_tc["data"][33]
                },
                {
                    "matukituki_basin": data_tc["data"][35]
                },
                {
                    "motatapu_chutes": data_tc["data"][37]
                },
                {
                    "summit_slopes": data_tc["data"][39]
                },
            ],
            "grommed_status": [
                {
                    "easy_rider": data_tc["data"][41]
                },
                {
                    "nice_n_easy": data_tc["data"][43]
                },
                {
                    "big_skite": data_tc["data"][45]
                },
                {
                    "raffills_run": data_tc["data"][47]
                },
                {
                    "petes_treat": data_tc["data"][49]
                },
                {
                    "tims_table": data_tc["data"][51]
                },
                {
                    "high_street": data_tc["data"][53]
                },
                {
                    "saddle_track": data_tc["data"][55]
                }
            ],
            "road_status": data_tc["data"][57],
            "chain_status": data_tc["data"][59],
            "food_status": [
                {
                    "saddle_track": data_tc["data"][61]
                },
                {
                    "grab_and_go": data_tc["data"][62]
                },
                {
                    "the_southern_bbq": data_tc["data"][65]
                },
                {
                    "allpress_at_altitued": data_tc["data"][67]
                },
            ]
        }
    x = mycol.insert_one(import_data_tc)
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
