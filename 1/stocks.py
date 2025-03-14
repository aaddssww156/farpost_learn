import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


async def fetch_exchange_rate(session):
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    async with session.get(url) as response:
        xml_text = await response.text()
        tree = ET.fromstring(xml_text)
        # Ищем элемент с кодом валюты "USD"
        for valute in tree.findall("Valute"):
            if valute.find("CharCode").text == "USD":
                value = float(valute.find("Value").text.replace(",", "."))
                nominal = float(valute.find("Nominal").text)
                return value / nominal
    return None


async def fetch_main_table(session):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    url = "https://markets.businessinsider.com/index/components/s&p_500"

    result = []

    async with session.get(url, headers=headers) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        table = soup.find("table")
        table_body = table.find("tbody")
        table_rows = table_body.findAll("tr")

        for row in table_rows:
            name = row.find("a").text
            href = row.find("a").get("href")
            price = float(row.findAll("td")[1].text.split("\n")[1])
            growth = float(row.findAll("td")[7].findAll("span")[0].text)

            result.append(
                {
                    "name": name,
                    "url": "https://markets.businessinsider.com" + href,
                    "price": price,
                    "growth": growth,
                }
            )

    return result


async def fetch_table(session, row):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    async with session.get(row["url"], headers=headers) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        code = (
            soup.find("span", {"class": "price-section__category"})
            .text.split(",")[1]
            .strip()
        )
        full_table = soup.find("div", {"class": "snapshot"})
        pe = ""
        try:
            pe = float(full_table.findAll("div")[51].text.split("P/E Ratio")[0].strip())
        except ValueError:
            pe = 0

        low = float(full_table.findAll("div")[37].text.split("52 Week Low")[0].strip())
        high = float(
            full_table.findAll("div")[39].text.split("52 Week High")[0].strip()
        )

        if low and high and low > 0:
            row["potential_profit"] = ((high / low) - 1) * 100
        else:
            row["potential_profit"] = 0

        row["code"] = code
        row["P/E"] = pe

    return row


async def to_rubles(row, exchange_rate):
    row["price"] = row["price"] * exchange_rate
    return row


async def process_expensive(rows):
    expensive_list = [
        {"code": row["code"], "name": row["name"], "price": row["price"]}
        for row in rows
    ]
    result = sorted(
        expensive_list,
        key=lambda x: x["price"] if x["price"] is not None else 0,
        reverse=True,
    )[:10]

    write(result, "expensive")


async def process_low_pe(rows):
    low_pe_list = [
        {"code": row["code"], "name": row["name"], "P/E": row["P/E"]} for row in rows
    ]
    result = sorted(
        low_pe_list,
        key=lambda x: x["P/E"] if x["P/E"] is not None else float("inf"),
    )[:10]

    write(result, "low_pe")


async def process_growth(rows):
    growth_list = [
        {"code": row["code"], "name": row["name"], "growth": row["growth"]}
        for row in rows
    ]
    result = sorted(
        growth_list,
        key=lambda x: x["growth"] if x["growth"] is not None else float("-inf"),
        reverse=True,
    )[:10]

    write(result, "growth")


async def process_profit(rows):
    potential_profit_list = [
        {
            "code": row["code"],
            "name": row["name"],
            "potential profit": row["potential_profit"],
        }
        for row in rows
    ]
    result = sorted(
        potential_profit_list,
        key=lambda x: x["potential profit"] if x["potential profit"] is not None else 0,
        reverse=True,
    )[:10]

    write(result, "potential_profit")


def write(data, name):
    with open(f"top_10_{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


async def main():
    async with aiohttp.ClientSession() as session:
        exchange_rate = await fetch_exchange_rate(session)

        table_rows = await fetch_main_table(session)

        tasks = [to_rubles(row, exchange_rate) for row in table_rows]
        table_rows = await asyncio.gather(*tasks)

        tasks = [fetch_table(session, row) for row in table_rows]
        table_rows = await asyncio.gather(*tasks)

        await asyncio.gather(
            process_expensive(table_rows),
            process_low_pe(table_rows),
            process_growth(table_rows),
            process_profit(table_rows),
        )

        print("Данные успешно сохранены в JSON файлах.")


if __name__ == "__main__":
    asyncio.run(main())
