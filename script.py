import time
from selenium import webdriver
import pandas as pd
import glob, os
from selenium.webdriver.support.ui import Select

url = 'https://www.nseindia.com/products/content/equities/indices/historical_index_data.htm'

options = webdriver.ChromeOptions()

# Add the directory where you want to save the files
save_dir = 'C:/Stock_data/...'

prefs = {'download.default_directory': save_dir}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

s_key1 = '01-01-'
s_key2 = '30-12-'

# Add the starting year and the index
year_end = 2008
index = 'NIFTY Realty'

while True:

    select = Select(driver.find_element_by_id('indexType'))
    select.select_by_visible_text(index)
    field = driver.find_element_by_id('fromDate')
    field.send_keys(s_key1+str(year_end))

    field2 = driver.find_element_by_id('toDate')
    field2.send_keys(s_key2+str(year_end))

    python_button = driver.find_element_by_id('get')
    python_button.click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    down = driver.find_element_by_link_text('Download file in csv format')
    down.click()

    time.sleep(2)
    os.rename(save_dir + '/data.csv', save_dir + '/nse_{}_{}.csv'.format(index, year_end))

    year_end += 1

# Last year
    if year_end == 2019:
        driver.close()
        break
    else:
        driver.refresh()
        driver.execute_script("window.scrollTo(0, 0)")



## Merge all the files into one

os.chdir(save_dir)
dframe = pd.DataFrame()

for file in glob.glob("nse*"):
    data_sheet = pd.read_csv(file, skiprows=0, usecols=[0,4]) # Columns 0 and 4 are the date and the close price
    dframe = dframe.append(data_sheet)

dframe.to_csv(save_dir + "/nse_final.csv", index=False)