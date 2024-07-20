from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
op = Options()
op.headless = True
class Scraper:
    def __init__(self):
        self.path = "chromedrivers\chromedriver.exe"
        self.driver = webdriver.Chrome(self.path,options = op)
        self.main_link = "https://webstream.sastra.edu/sastraparentweb/"
        self.driver.get(self.main_link)
        self.driver.maximize_window()
        self.form = self.driver.find_element(By.XPATH,"//form[@id ='frmLogin']")
        self.link = "https://webstream.sastra.edu/sastraparentweb/usermanager/home.jsp"
    def getcaptcha(self):
        img = self.form.find_element(By.ID,"imgCaptcha")
        self.driver.save_screenshot("static/captcha.png")
        location = img.location
        location = img.location
        size = img.size
        ax = location['x']
        ay = location['y']
        width = location['x']+size['width']
        height = location['y']+size['height']
        cropImage = Image.open('static/captcha.png')
        cropImage = cropImage.crop((int(ax), int(ay), int(width), int(height)))
        cropImage.save('static/captcha1.png')
    def login(self,regno,pwd,captcha):
        number = self.form.find_element(By.ID,"txtRegNumber")
        dob = self.form.find_element(By.ID,"txtPwd")
        cap = self.form.find_element(By.ID,"answer")
        number.send_keys(regno)
        dob.send_keys(pwd)
        cap.send_keys(captcha)
        # time.sleep(10)
        button = self.form.find_element(By.XPATH,"//input[@type = 'button']")
        button.click()
        try:
            self.driver.get(self.link)
            return True
        except:
            time.sleep(1)
            return False
    def get_details(self):
        try:
            print("logged in")
            time.sleep(10)
            form1 = self.driver.find_element(By.XPATH,"//form[@id ='frmStudentMain']")
            link = self.driver.find_elements(By.TAG_NAME,"a")
            for i in link:
                if(i.text.lower() == "timetable"):
                    i.click()
                    break
            time.sleep(5)
            details = self.driver.find_elements(By.CLASS_NAME,"leftnavlinks01")
            details = details[0].text.split("\n")
            name = details[0]
            course = details[1]
            form2 = form1.find_element(By.XPATH,"//form[@id='frmStudentTimetable']")
            table = form2.find_elements(By.CLASS_NAME,"tablecontent01")
            section = table[68].text
            return (name,course,section)
        except:
            return None
    def get_timetable(self):
        try:
            link = self.driver.find_elements(By.TAG_NAME,"a")
            for i in link:
                if(i.text.lower() == "timetable"):
                    i.click()
                    break
            time.sleep(5)
            form2 = self.driver.find_element(By.XPATH,"//form[@id ='frmStudentTimetable']")
            table = form2.find_elements(By.CLASS_NAME,"tablecontent01")
            table = [i.text for i in table[:55]]
            timetable = []
            for i in range(0,55,11):
                timetable.append(table[i:i+11])
            for i in range(len(timetable)):
                timetable[i] = timetable[i][:8]
            return timetable
        except:
            return None
    def logout(self):
        link = self.driver.find_elements(By.TAG_NAME,"a")
        for i in link:
            if(i.text.lower() == "logout"):
                i.click()
                break
        self.driver.get(self.main_link)
        time.sleep(1)
        self.form = self.driver.find_element(By.XPATH,"//form[@id ='frmLogin']")
        
# s = Scraper()
# s.login("125003358","02012004","")
# print(s.get_details())
