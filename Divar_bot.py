from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import  WebDriverWait
import os , csv

# put ur username account in your windows
user:str = ""
# you have to sing in into the Divar website with ur phone number to be able to excract the phone numbers 
user_profile = fr"--user-data-dir=C:\\Users\\{user}\AppData\\Local\\Google\\Chrome\\User Data"
op = webdriver.ChromeOptions()
op.add_argument("--start-maximize")
# op.add_argument("--incognito")
op.add_argument(user_profile)
op.add_argument('--profile-directory=Default')
driver = webdriver.Chrome(options=op)
city = "tehran"
buy_or_rent = "buy"
# make a list of all the city on tehran in order to select one 
location = "azari"
size = "65-200"
price = "300000000-5000000000"
driver.get(f"https://divar.ir/s/{city}/{buy_or_rent}-residential/{location}?size={size}&price={price}&has-photo=true")
articles = WebDriverWait(driver,100).until(EC.visibility_of_all_elements_located((By.TAG_NAME,"article")))

for article in articles:
    links = article.find_element(By.TAG_NAME,"a")
    link = links.get_attribute("href")
    name = article.find_element(By.TAG_NAME,"h2").text
    name = name.replace("/","-").replace("\\","-").replace("*","-")
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(link) # type: ignore
    # new page opens
    
    button = WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".kt-button.kt-button--primary.post-actions__get-contact")))
    button.click()
    tel_number = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div/main/article/div/div[1]/section[1]/div[3]/div[1]/div/div[2]/a')))
    tel = tel_number.get_attribute("href").replace("tel:","").strip()# type: ignore
    pic_element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div[1]/div/main/article/div/div[2]/section[1]')))
    pic_num = pic_element.find_element(By.TAG_NAME,"span").get_attribute("innerHTML")
    pic_num = int(pic_num[-1]) # type: ignore
    left_arrow = driver.find_element(By.TAG_NAME,"html")
    for i in range(pic_num):
        image = pic_element.find_element(By.TAG_NAME,'img')
        src = requests.get(image.get_attribute("src")) # type:ignore
        newpath = fr".\divar_data\{name}"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        with open(fr"{newpath}\{i}.jpg","wb") as f:
            f.write(src.content)
        left_arrow.send_keys(Keys.LEFT)
        
        sleep(3.5)
    with open(fr"{newpath}\{i}.csv",mode="a",newline="") as f: # type:ignore
        writer = csv.writer(f)
        writer.writerow(["Phone Number",tel])
    sleep(5)
    
    # new page closed
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


