#!/usr/bin/env python3
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pymongo
import threading, time
from datetime import datetime
import json


with open("config.json") as json_data_file:
    config = json.load(json_data_file)

async def get_html(url, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            html = await resp.text()
            return html
        return False


myclient = pymongo.MongoClient(config["mongodb"]["URI"])


mydb = myclient[config["mongodb"]["mongodb"]]

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
    try:
        if len(site_status_data["data"]) == 4:
            import_data = {
            "data": "True",
            "data_updated": current_time,
            "Resort": site_status_data["data"][0],
            "Lifts": site_status_data["data"][1],
            "Road": site_status_data["data"][3],
            "weather": weather_desc,
            "outlook": outlook_desc,
            "Upper_1860m_Temp": mes_data_data["data"][0],
            "Mid_1640m_Temp": mes_data_data["data"][1],
            "Lower_1260m_Temp": mes_data_data["data"][2],
            "Upper_1860m_Snow": mes_data_data["data"][3],
            "Mid_1640m_Snow": mes_data_data["data"][4],
            "Lower_1260m_Snow": mes_data_data["data"][5],
            "snowfall_last_7_days": mes_data_data["data"][6],
            "Upper_1860m_Wind": wind_status_data_data["data"][0],
            "Mid_1640m_Wind": wind_status_data_data["data"][1],
            "Lower_1260m_Wind": wind_status_data_data["data"][2],
            "snow_condition": snow_condition_data,
            "McDougalls_Chondola": open_status_data_data["data"][0],
            "Whitestar_Express": open_status_data_data["data"][1],
            "Valley_View_Quad": open_status_data_data["data"][2],
            "Captains_Express": open_status_data_data["data"][3],
            "Learner_Conveyors": open_status_data_data["data"][4],
            "Kindy_Conveyor": open_status_data_data["data"][5],
            "Mezz_Cafe": open_status_data_data["data"][6],
            "The_Lounge": open_status_data_data["data"][7],
            "Noodle_Bar": open_status_data_data["data"][8],
            "FB_Base_Bar": open_status_data_data["data"][9],
            "Captains_Cafe": open_status_data_data["data"][10],
            "Vista_Bar": open_status_data_data["data"][11],
            "FB_Base_Cafe": open_status_data_data["data"][12],
            "Stag_Lane": open_status_data_data["data"][13],
            "Antlers_Alley": open_status_data_data["data"][14],
            "Lil_Bucks": open_status_data_data["data"][15],
            "Sightseeing": open_status_data_data["data"][16]
            }
        else:
            import_data = {
            "data": "True",
            "data_updated": current_time,
            "Resort": site_status_data["data"][0],
            "Lifts": site_status_data["data"][1],
            "Road": site_status_data["data"][2],
            "weather": weather_desc,
            "outlook": outlook_desc,
            "Upper_1860m_Temp": mes_data_data["data"][0],
            "Mid_1640m_Temp": mes_data_data["data"][1],
            "Lower_1260m_Temp": mes_data_data["data"][2],
            "Upper_1860m_Snow": mes_data_data["data"][3],
            "Mid_1640m_Snow": mes_data_data["data"][4],
            "Lower_1260m_Snow": mes_data_data["data"][5],
            "snowfall_last_7_days": mes_data_data["data"][6],
            "Upper_1860m_Wind": wind_status_data_data["data"][0],
            "Mid_1640m_Wind": wind_status_data_data["data"][1],
            "Lower_1260m_Wind": wind_status_data_data["data"][2],
            "snow_condition": snow_condition_data,
            "McDougalls_Chondola": open_status_data_data["data"][0],
            "Whitestar_Express": open_status_data_data["data"][1],
            "Valley_View_Quad": open_status_data_data["data"][2],
            "Captains_Express": open_status_data_data["data"][3],
            "Learner_Conveyors": open_status_data_data["data"][4],
            "Kindy_Conveyor": open_status_data_data["data"][5],
            "Mezz_Cafe": open_status_data_data["data"][6],
            "The_Lounge": open_status_data_data["data"][7],
            "Noodle_Bar": open_status_data_data["data"][8],
            "FB_Base_Bar": open_status_data_data["data"][9],
            "Captains_Cafe": open_status_data_data["data"][10],
            "Vista_Bar": open_status_data_data["data"][11],
            "FB_Base_Cafe": open_status_data_data["data"][12],
            "Stag_Lane": open_status_data_data["data"][13],
            "Antlers_Alley": open_status_data_data["data"][14],
            "Lil_Bucks": open_status_data_data["data"][15],
            "Sightseeing": open_status_data_data["data"][16]
            }
        x = mycol.insert_one(import_data)
        id_data = x.inserted_id
        return id_data
    except IndexError:
        pass
    

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

    if data_tc["data"][40] == "No trails are currently groomed.":
        try:
            import_data_tc = {
            "data_updated": current_time,
            "ski_field_status": data_tc["data"][3],
            "overnight_snowfall": data_tc["data"][5],
            "snowfall_24_hrs": data_tc["data"][7],
            "snowfall_7_days": data_tc["data"][9],
            "last_snowfall_data": data_tc["data"][11],
            "last_snowfall_amount": data_tc["data"][13],
            "home_basin_snow_depth": data_tc["data"][15],
            "saddle_basin_depth": data_tc["data"][17],
            "live_temp": data_tc["data"][19],
            "overnight_temp": data_tc["data"][21],
            "home_basin_chair_status": data_tc["data"][23],
            "saddle_quad_chair_status": data_tc["data"][25],
            "nice_n_easy_status": data_tc["data"][27],
            "magic_carpet_status": data_tc["data"][29],
            "home_basin_status": data_tc["data"][31],
            "saddle_basin_status": data_tc["data"][33],
            "matukituki_basin_status": data_tc["data"][35],
            "motatapu_chutes_status": data_tc["data"][37],
            "summit_slopes_status": data_tc["data"][39],
            "main_street_groomed":"No data available.",
            "easy_rider_groomed": "No data available.",
            "nice_n_easy_grommed": "No data available.",
            "raffils_run_grommed": "No data available.",
            "petes_treat_groomed": "No data available.",
            "side_saddle_groomed": "No data available.",
            "south_ridge_wide_guid": "No data available.",
            "tims_table_groomed": "No data available.",
            "saddle_back_groomed": "No data available.",
            "high_street_groomed": "No data available.",
            "saddle_track_groomed": "No data available.",
            "road_status": data_tc["data"][43],
            "chain_status": data_tc["data"][45],
            "bar_status": data_tc["data"][47],
            "grab_and_go_status": data_tc["data"][49],
            "the_southern_bbq": data_tc["data"][51],
            "allpress_at_altitude": data_tc["data"][53],
            }
        except IndexError:
            pass
    else:
        try:
            import_data_tc = {
            "data_updated": current_time,
            "ski_field_status": data_tc["data"][3],
            "overnight_snowfall": data_tc["data"][5],
            "snowfall_24_hrs": data_tc["data"][7],
            "snowfall_7_days": data_tc["data"][9],
            "last_snowfall_data": data_tc["data"][11],
            "last_snowfall_amount": data_tc["data"][13],
            "home_basin_snow_depth": data_tc["data"][15],
            "saddle_basin_depth": data_tc["data"][17],
            "live_temp": data_tc["data"][19],
            "overnight_temp": data_tc["data"][21],
            "home_basin_chair_status": data_tc["data"][23],
            "saddle_quad_chair_status": data_tc["data"][25],
            "nice_n_easy_status": data_tc["data"][27],
            "magic_carpet_status": data_tc["data"][29],
            "home_basin_status": data_tc["data"][31],
            "saddle_basin_status": data_tc["data"][33],
            "matukituki_basin_status": data_tc["data"][35],
            "motatapu_chutes_status": data_tc["data"][37],
            "summit_slopes_status": data_tc["data"][39],
            "easy_rider_groomed": data_tc["data"][41],
            "nice_n_easy_grommed": data_tc["data"][43],
            "raffils_run_grommed": data_tc["data"][45],
            "tims_table_groomed": data_tc["data"][47],
            "petes_treat_groomed": data_tc["data"][49],
            "side_saddle_groomed": data_tc["data"][51],
            "south_ridge_wide_guid": data_tc["data"][53],
            "saddle_back_groomed": data_tc["data"][57],
            "high_street_groomed": data_tc["data"][59],
            "saddle_track_groomed": data_tc["data"][61],
            "road_status": data_tc["data"][63],
            "chain_status": data_tc["data"][6],
            "bar_status": data_tc["data"][65],
            "grab_and_go_status": data_tc["data"][67],
            "the_southern_bbq": data_tc["data"][69],
            "allpress_at_altitude": data_tc["data"][71],
            }
        except IndexError:
            pass
    x = mycol.insert_one(import_data_tc)
    id_data = x.inserted_id
    return id_data

WAIT_TIME_SECONDS = 900
ticker = threading.Event()

async def run_def():
    async with aiohttp.ClientSession() as session:
        print((await cardrona(session)))


if __name__ == "__main__":
    while not ticker.wait(WAIT_TIME_SECONDS):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_def())
