import os
import pathlib
import requests
import fire


class Scraper(object):

    boxofficemojo_url_template = "https://www.boxofficemojo.com/date/{date}/"
    data_dir = pathlib.Path('data') / 'dates'
    
    def scrape(self, date):
        """
        Pull data for a specific date and write to the data/dates directory
        """

        url = self.boxofficemojo_url_template.format(date=date)
        resp = requests.get(url)
        if resp.ok:
            filename = self.data_dir / f"{date}.html"
            with open(filename, 'wb')  as o:
                o.write(resp.content)
            print(f"Okay: {date}")
        else:
            print(f"Fail: {date}")


if __name__  == "__main__":
    fire.Fire(Scraper)