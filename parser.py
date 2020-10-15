import os
import pathlib
import fire
import bs4
import json
import re
import gzip


class Parser(object):

    data_dir = pathlib.Path('data') / 'dates'
    
    def format_header(self, header):
        return re.sub('[^0-9a-zA-Z]+', '', header.strip().replace(' ', '_').lower())

    def parse(self, date):
        """
        Print json objects for each record in the downloaded page
        """

        filename = self.data_dir / f"{date}.html.gz"
        if not os.path.exists(filename):
            raise ValueError(f"No downloaded page for {date}")
        with gzip.open(filename, 'r') as f:
            data = f.read()
            soup = bs4.BeautifulSoup(data, features="html.parser")
            table_wrapper = soup.find(attrs={'id': 'table'})
            table = table_wrapper.table
            rows = table.find_all('tr')
            header_row = rows[0]
            data_rows = rows[1:]
            headers = [self.format_header(th.text) for th in header_row.find_all('th')]
            for row in data_rows:
                data = [td.text.strip() for td in row.find_all('td')]
                parsed_data = dict(zip(headers, data))
                parsed_data.update(date=date)
                print(json.dumps(parsed_data))


if __name__  == "__main__":
    fire.Fire(Parser)