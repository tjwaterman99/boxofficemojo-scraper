import time
import pathlib
import requests
import fire
import gzip


class Scraper(object):

    boxofficemojo_url_template = "https://www.boxofficemojo.com/date/{date}"
    data_dir = pathlib.Path('data') / 'dates'
    max_retries = 6

    def scrape(self, date, retries=max_retries):
        """
        Pull data for a specific date and write to the data/dates directory
        """

        if retries <= 0:
            raise AttributeError(f"Fail: Max retries exceeded when scraping {date}.")

        url = self.boxofficemojo_url_template.format(date=date)
        resp = requests.get(url)
        if resp.ok:
            filename = self.data_dir / f"{date}.html.gz"
            with gzip.open(filename, 'wb')  as o:
                o.write(resp.content)
            print(f"Okay: {date}")
        else:
            time_to_sleep = 2 ** (self.max_retries - retries)
            print(f"Fail: {date} [status_code={resp.status_code}]. Retries left: {retries}. Waiting {time_to_sleep} seconds until retrying.")
            time.sleep(time_to_sleep)
            self.scrape(date, retries=retries-1)


if __name__  == "__main__":
    fire.Fire(Scraper)