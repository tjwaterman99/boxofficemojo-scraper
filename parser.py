import os
import pathlib
import fire
import bs4
import json
import re
import gzip
import datetime


class Parser(object):

    data_dir = pathlib.Path('data') / 'dates'
    
    def format_header(self, header):
        return re.sub('[^0-9a-zA-Z]+', '', header.strip().replace(' ', '_').lower())

    def _parse_date(self, date):
        """
        Parse a single downloaded page into a stream of JSON objects
        """

        filename = self.data_dir / f"{date}.html.gz"
        if not os.path.exists(filename):
            raise ValueError(f"No downloaded page for {date}")
        with gzip.open(filename, 'r') as f:
            data = f.read()
            soup = bs4.BeautifulSoup(data, features="html.parser")
            table_wrapper = soup.find(attrs={'id': 'table'})
            if table_wrapper is None:
                return
            table = table_wrapper.table
            rows = table.find_all('tr')
            header_row = rows[0]
            data_rows = rows[1:]
            headers = [self.format_header(th.text) for th in header_row.find_all('th')]
            for row in data_rows:
                data = [td.text.strip().replace('"', '') for td in row.find_all('td')]
                parsed_data = dict(zip(headers, data))
                parsed_data.update(date=date)
                print(json.dumps(parsed_data) + '\n', end='')

    def parse(self, start_date, end_date=None):
        """
        Print json objects  each record in the downloaded page
        """
        
        if end_date is None:
            self._parse_date(start_date)
        else:
            start = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            current = start
            while current <= end:
                self._parse_date(str(current))
                current = current + datetime.timedelta(days=1)
    
    def parse_all(self):
        """
        Parse all files saved in the data/dates directory
        """
        for filepath in self.data_dir.iterdir():
            date = filepath.name.replace('.html.gz', '')
            try:
                self.parse(date)
            except:
                raise AttributeError(f"Invalid parsing for {date}")


if __name__  == "__main__":
    fire.Fire(Parser)