# fedex_zone_scraper
Modular webscraper that pulls zip-to-zip parcel shipping zones.

# Instructions
0. ```virtualenv venv```
1. ```source venv/Scripts/activate``` or ```venv\Scripts\activate```
2. ```pip install -r requirements.txt```
3. ```mkdir tmp```
4. drop file with unique zip-to-zip lanes in tmp.
5. update *main.py* ```FILENAME```, ```ZONE_TYPE```, ```ORIGIN_COL```, and ```DEST_COL``` with the name of the lanes file, the name of the origin zip column, and the name of the destination zip column.
6. ```python main.py```
7. result: ```tmp/output.csv```

## Notes
- ```.xlsx``` files are assumed to have one sheet named *Sheet1*.
- Assumes only US lanes.