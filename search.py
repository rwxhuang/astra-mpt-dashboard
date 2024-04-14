from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from difflib import SequenceMatcher
import pandas as pd
import csv
import boolean_search

class Search():

    def __init__(self, search_phrase):
        csv_filename = './data/techport_all.csv'
        with open(csv_filename, encoding="utf8") as f:
            reader = csv.reader(f)
            self.data = list(reader)
        self.reorganize_data()
        self.search_phrase = search_phrase 

    def reorganize_data(self):
        labels = self.data[0]
        self.data.pop(0)
        reorganized_data = []
        for data in self.data:
            new_data = {labels[i]: data[i] for i in range(len(labels))}
            reorganized_data.append(new_data)
        self.data = reorganized_data
    
    def search_bar_tech_port(self):
        #Go to the homepage
        self.driver.get("https://techport.nasa.gov/home")

        #self.driver.implicitly_wait(0.5)

        #Enter into the search bar the 'self.search_phrase'
        text_box = self.driver.find_element(by=By.NAME, value="searchVO.searchCriteria.searchOptions[0].input")
        submit_button = self.driver.find_element(by=By.CLASS_NAME, value="button-search")

        text_box.send_keys(self.search_phrase)
        submit_button.click()

        counts = self.driver.find_element(by=By.CLASS_NAME, value="data-count")
        value = int(counts.text.replace(",", ""))

        #Extract ids from the page
        article_ids = []
        while(len(article_ids) < int(value)):
            elems = self.driver.find_elements(By.TAG_NAME, "a")
            for elem in elems:
                s = elem.get_attribute("href")
                if s and "https://techport.nasa.gov/view/" in s:
                    id = s[s.index("view/") + 5:]
                    if id.isdigit():
                        article_ids.append(int(s[s.index("view/") + 5:]))
            if len(article_ids) < int(value):
                next_btn = self.driver.find_element(by=By.CLASS_NAME, value="table-pagination-fwd ")
                next_btn.click()
        return article_ids

    def scrape_data(self):
        chrome_options = Options()
        chrome_options.add_argument("headless")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install(), options=chrome_options ))

        parsed_infos = []
        article_ids = self.search_bar_tech_port()
        self.driver.quit()

        for d in self.data:
            if int(d['Techport ID']) in article_ids:
                parsed_infos.append(dict(d))
        res = pd.DataFrame(parsed_infos)
        return res.to_csv().encode('utf-8')

        # self.get_sbir_scrape_data()

    def get_data(self):
        with open('./boolean_query/query.txt', 'w') as file:
            file.write(self.search_phrase)
        boolean_search.search("./boolean_query/dict_file.txt", "./boolean_query/post_file.txt", "./boolean_query/query.txt", './boolean_query/output.txt')
        with open("./boolean_query/output.txt") as file:
            first_line = file.read()
            ids = list(int(id) for id in first_line.split())
        all_techport_df = pd.read_csv('./data/techport_all.csv')

        selected_techport = all_techport_df[all_techport_df['Techport ID'].isin(ids)]
        
        return selected_techport

    def get_sbir_boolean_data(self):
        csv_filename = './data/sbir_all.csv'
        with open(csv_filename, encoding="utf8") as f:
            sbir = csv.reader(f)
            with open('./data/' + self.search_phrase + '_tp_boolean.csv', newline="", encoding="utf8") as to_read_fp, open('./data/' + self.search_phrase + '_tp_sbir.csv', "w", newline="", encoding="utf8") as to_write_fp:
                reader = csv.reader(to_read_fp)
                writer = csv.writer(to_write_fp)

                for count1, row1 in enumerate(reader):
                    added = False
                    for count2, row2 in enumerate(sbir):
                        if count1 == 0 and count2 == 0:
                            added = True
                            writer.writerow(row1 + row2)
                            break
                        if len(row1[2]) >= 1 and len(row2[-1]) >= 1 and SequenceMatcher(None, row1[2], row2[-1]).ratio() >= 0.1:
                            added = True
                            writer.writerow(row1 + row2)
                            break
                    if not added:
                        writer.writerow(row1)

    def get_sbir_scrape_data(self):
        csv_filename = './data/sbir_all.csv'
        with open(csv_filename, encoding="utf8") as f:
            sbir = csv.reader(f)
            with open('./data/' + self.search_phrase + '_tp.csv', newline="", encoding="utf8") as to_read_fp, open('./data/' + self.search_phrase + '_tp_sbir.csv', "w", newline="", encoding="utf8") as to_write_fp:
                reader = csv.reader(to_read_fp)
                writer = csv.writer(to_write_fp)

                for count1, row1 in enumerate(reader):
                    added = False
                    for count2, row2 in enumerate(sbir):
                        if count1 == 0 and count2 == 0:
                            added = True
                            writer.writerow(row1 + row2)
                            break
                        if len(row1[2]) >= 1 and len(row2[-1]) >= 1 and SequenceMatcher(None, row1[2], row2[-1]).ratio() >= 0.2:
                            added = True
                            writer.writerow(row1 + row2)
                            break
                    if not added:
                        writer.writerow(row1)
