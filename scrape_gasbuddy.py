from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.gasbuddy.com/home?search=boston")
    expect(page.locator("[id=\"\\34 3135\"]").get_by_role("link", name="Speedway")).to_be_visible()
    page.get_by_role("button", name="More boston Gas Prices").click()

    gas_station_names = [p.text_content() for p in page.get_by_role('heading').all()[2:-8]]
    # for e in gas_station_names:
    #     print(e)

    gas_station_addresses = [p.text_content() for p in page.get_by_text(',').all()[1:-2]
                 if p.text_content() != ','][:len(gas_station_names)]
    # for text in addresses:
    #     print(text)
    #
    # for i in range(len(gas_station_names)):
    #     print(f'{gas_station_names[i]}: {addresses[i]}')

    gas_station_prices = [p.text_content()
                          for p in page.get_by_text('$').all()][:len(gas_station_names)]

    out = {'name': gas_station_names, 'address': gas_station_addresses, 'price': gas_station_prices}
    df = pd.DataFrame(out)

    df.to_csv('gas_station_data/boston_gas_stations.csv', index=False)
    # gas station names will have some weird char, remove manually later

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
