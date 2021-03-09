import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()

class Indiegogo(object):

    def __init__(self,url,num_pages):
        self.url=url
        self.num_pages=num_pages

    def get_phone_number(self,selection):
        try:
            phone = selection.find_element_by_css_selector("span.section-result-info.section-result-phone-number")
            phone_number=phone.text
        except:
            phone_number="NA"
        return phone_number

    def get_title(self,selection):
        try:
            title = selection.find_element_by_class_name("section-result-title").text
        except:
            title="NA"
        return title

    def get_location(self,selection):
        try:
            location = selection.find_element_by_class_name("section-result-location").text
        except:
            location="NA"
        return location

    def _get_sigle_page_data(self,data,url):
        ls_of_dict=[]

        for ind_data in data:
            dict_data = {}

            # print (ind_data.text)
            phone_number = self.get_phone_number(ind_data)
            dict_data['phone'] = phone_number
            # opening_hours = ind_data.find_element_by_css_selector("span.section-result-info.section-result-opening-hours")
            # print("opening_hours",opening_hours.text)
            # dict_data['opening_hours'] = opening_hours.text
            title = self.get_title(ind_data)
            dict_data['title'] = title

            location = self.get_location(ind_data)
            dict_data['location'] = location

            dict_data['category'] = url.split("/")[5]
            dict_data['url'] = url
            ls_of_dict.append(dict_data)
        single_page_df=pd.DataFrame(ls_of_dict)
        return single_page_df

    def new(self):
        error_counter=5
        delay=5
        df_list=[]
        for url in self.url:
            pages_counter = 0
            final_data=[]
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
            options.add_argument("--no-sandbox")  # Bypass OS security model
            options.add_argument('window-size=1920x1080')
            options.add_argument("--disable-extensions")

            browser = webdriver.Chrome(executable_path='Z:/Kamal/study/python/tools/google_data_downloader/chromedriver.exe')
            browser.get(url)
            myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//*[@id='n7lv7yjyC35__section-pagination-button-next']/img")))

            # titles_element = browser.find_element_by_xpath("//*[@id='n7lv7yjyC35__section-pagination-button-next']/span")
            titles_element=browser.find_element_by_xpath("//*[@id='n7lv7yjyC35__section-pagination-button-next']/img")
            print(titles_element)

            # data=browser.find_elements_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[4]")
            # print (data[0].title)

            for i in range(num_pages):
                browser.implicitly_wait(3)

                data=browser.find_elements_by_class_name("section-result")
                #
                # data=browser.find_elements_by_xpath("//*[@id='pane']/div/div[1]/div/div/div[4]/div[1]")

                single_page_df=self._get_sigle_page_data(data,url)


                try:
                    browser.implicitly_wait(10)
                    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located(
                        (By.XPATH, "//*[@id='n7lv7yjyC35__section-pagination-button-next']/img")))
                    titles_element = browser.find_element_by_xpath(
                        "//*[@id='n7lv7yjyC35__section-pagination-button-next']/img")
                    titles_element.click()

                    pages_counter =pages_counter+1

                except:
                    logging.info("Breaking Loop as cant find click next button")

                single_page_df["page_counter"] = pages_counter
                df_list.append(single_page_df)



            logging.info("dataframe for {} is :".format(url))
            browser.quit()
        logging.info("Number of dataframe {}".format(len(df_list)))
        df_combined = pd.concat(df_list)
        df_combined.to_csv("google_result.csv",index=False)



if __name__=="__main__":
    num_pages=20
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    url = ['https://www.google.com/maps/search/personal+trainer+in+bangalore/@12.9728325,77.6536063,12z/data=!3m1!4b1']
    url=["https://www.google.com/maps/search/personal+trainer+in+bangalore/@12.9728325,77.6536063,12z/data=!3m1!4b1"
,"https://www.google.com/maps/search/dietician+in+bangalore/@3.2516778,101.3661252,3z/data=!3m1!4b1"
,"https://www.google.com/maps/search/nutritionist+in+bangalore/@12.9584069,77.5735823,12z/data=!3m1!4b1"]
    url=["https://www.google.com/maps/search/personal+trainer+in+bangalore/@12.9728325,77.6536063,12z/data=!3m1!4b1"
,"https://www.google.com/maps/search/dietician+in+bangalore/@3.2516778,101.3661252,3z/data=!3m1!4b1"
,"https://www.google.com/maps/search/nutritionist+in+bangalore/@12.9584069,77.5735823,12z/data=!3m1!4b1"
,"https://www.google.com/maps/search/physiotherapist+in+Bangalore,+Karnataka/@12.9535483,77.3507267,10z/data=!3m1!4b1"
,"https://www.google.com/maps/search/massage+therapist+in+Bangalore,+Karnataka/@12.953249,77.3507229,10z/data=!3m1!4b1"
,"https://www.google.com/maps/search/photographer+in+Bangalore,+Karnataka/@12.9529496,77.350719,10z/data=!3m1!4b1"
,"https://www.google.com/maps/search/makeup+artist+in+bangalore/@12.9373757,77.5553892,12z/data=!3m1!4b1"
,"https://www.google.com/maps/search/boutique+in+Bangalore,+Karnataka/@12.937357,77.5553889,12z/data=!3m1!4b1"
,"https://www.google.com/maps/search/tailor+in+Bangalore,+Karnataka/@12.9702474,77.6481257,16z/data=!3m1!4b1"
,"https://www.google.com/maps/search/jewellery+designers+in+Bangalore,+Karnataka/@12.970245,77.6174832,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/interior+designers+in+Bangalore,+Karnataka/@12.9702403,77.6174832,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/life+coach+in+Bangalore,+Karnataka/@12.9702356,77.6174831,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/tutor+in+Bangalore,+Karnataka/@12.9702309,77.6174831,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/gym+in+Bangalore,+Karnataka/@12.9702263,77.617483,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/spa+in+Bangalore,+Karnataka/@12.9674882,77.6361475,15z/data=!3m1!4b1"
,"https://www.google.com/maps/search/salon+in+Bangalore,+Karnataka/@12.9702216,77.6174829,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/hair+stylist+bangalore/@12.9316535,77.6214979,17z/data=!3m1!4b1"
,"https://www.google.com/maps/search/chartered+accountant+in+Bangalore,+Karnataka/@12.9903701,77.5191062,12z/data=!3m1!4b1"
,"https://www.google.com/maps/search/real+estate+agents+in+Bangalore,+Karnataka/@12.9718216,77.6455088,16z/data=!3m1!4b1"
,"https://www.google.com/maps/search/financial+advisors+in+Bangalore,+Karnataka/@12.9718192,77.6148664,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/event+venues+in+bangalore/@12.9718146,77.6148663,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/event+planner+in+Bangalore,+Karnataka/@12.9718099,77.6148663,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/caterers+in+Bangalore,+Karnataka/@12.9718052,77.6148662,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/event+decorators+bangalore/@12.9717958,77.6148661,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/motor+training+school+bangalore/@12.9717911,77.614866,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/Packers+and+Movers+In+Bangalore/@12.9219686,77.6115036,15z/data=!3m1!4b1"
,"https://www.google.com/maps/search/UI+UX+Designer+bangalore/@12.9361315,77.62131,15z/data=!3m1!4b1"
,"https://www.google.com/maps/search/logo+Designer+bangalore/@12.9361291,77.595045,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/digital+marketing+bangalore/@12.9361197,77.5950449,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/digital+marketing+freelancers+bangalore/@12.9361104,77.5950447,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/video+shooting+services+bangalore/@12.9361057,77.5950447,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/video+editing+services+near+Bangalore,+Karnataka/@12.936101,77.5950446,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/music+composers+bangalore/@12.936073,77.5950443,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/music+audio+companies+in+bangalore/@12.9360637,77.5950442,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/music+classes+near+Bangalore,+Karnataka/@12.9360683,77.5950442,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/music+%26+audio+bangalore/@12.9360777,77.5950443,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/software+developers+in+bangalore/@12.9360964,77.5950446,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/freelance+software+developers+in+bangalore/@12.9360917,77.5950445,13z/data=!3m1!4b1"
,"https://www.google.com/maps/search/lawyers+in+Bangalore,+Karnataka/@12.9360824,77.5950444,13z/data=!3m1!4b1"]
    logging.info("Step 1 : Initiating Process with input config {}".format(url))
    obj = Indiegogo(url,num_pages)
    obj.new()


