import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup


async def get_html(url, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            html = await resp.text()
            return html
        return False


async def get_json(url, session):
    async with session.get(url) as resp:
        if resp.status == 200:
            data = await resp.json()
            return data
        return False


async def cardrona(session):
    url = "https://www.cardrona.com/winter/snow-report/"
    html = await get_html(url, session)
    soup = BeautifulSoup(html, "lxml")
    data = ""
    for report in soup.find_all("div", {"class": "c-snow-report__site"}):
        site_name = report.find("span", {"class": "c-snow-report__site-name"}).get_text()
        site_status = report.find("span", {"class": "c-snow-report__site-status"}).get_text()
        data += "Site_name: " + site_name + "\n" + "Site_status: " + site_status + "\n"
    for weather in soup.find_all("div", {"class": "c-snow-report__weather-header"}):
        weather_desc = weather.find("div", {"class": "c-snow-report__current-desc"}).get_text()
        data += "Weather: " + weather_desc + "\n"
    outlook = soup.find("div", {"class": "c-snow-report__info-wrapper"})
    outlook_desc = outlook.find("div", {"class": "c-snow-report__info"}).get_text()
    data += "Outlook: " + outlook_desc + "\n"
    return data

async def run_def():
    async with aiohttp.ClientSession() as session:
        print((await cardrona(session)))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_def())
    loop.close()
