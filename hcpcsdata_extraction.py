import requests
import pandas as pd
import lxml.html as LH

site_url = "https://www.hcpcsdata.com"  # main URL to get data
url = 'https://www.hcpcsdata.com/Codes'  # first url to get the HCPCS Codes and  Category
page = requests.get(url)

# to get CODE from first URL
sub_code_master = LH.fromstring(page.content).xpath('//tr/td/a/@href')
sub_code = sub_code_master[0]

#  to replace the code as GROUP
code = sub_code.replace('/Codes/', '')
code = f"HCPS '{code}' Codes"

# to get Category
category = LH.fromstring(page.content).xpath('//tr/td[3]')
desc = [x.text.strip() for x in category]

second_url = f"{site_url}{sub_code_master[0]}"  # second url to get CODE and Long Description
page_2 = requests.get(second_url)
leaf_links = LH.fromstring(page_2.content).xpath('//tr/td/a/@href')

# to clean the code as required CODE
clean_code = []
for code_data in leaf_links:
    cleansed_code = code_data.replace('/Codes/A/', '')
    clean_code.append(cleansed_code)

# to get long description
leaf_desc = LH.fromstring(page_2.content).xpath('//tr/td[2]')
leaf_desc1 = [x.text.strip() for x in leaf_desc]

# to get short desc
all_shrt = []
for i in leaf_links[0:10]:
    third_url = f"{site_url}{i}"
    page_3 = requests.get(third_url)
    short_desc = LH.fromstring(page_3.content).xpath('//tr[1]/td[2]')
    leaf_short_desc = [x.text.strip() for x in short_desc]
    all_shrt.extend(leaf_short_desc)

# to convert all scraped data to Dataframe to write to CSV
a = pd.DataFrame({'Group': pd.Series(code), "Category": pd.Series(desc[0]), "Code": pd.Series(clean_code),
                  "Long Desc": pd.Series(leaf_desc1), "Short Desc": pd.Series(all_shrt)})

a.fillna(method='ffill', inplace=True)
a.to_csv('output.csv', index=False)
