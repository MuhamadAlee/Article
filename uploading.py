import time
import pyautogui
import parameters as para
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class Upload:

    def __init__(self):
        self.driver = webdriver.Chrome("./driver/chromedriver")
        self.driver.get('https://www.noborderz.com/nblogin/')
        self.driver.maximize_window()

    def login(self):
        try:
            #setting login credential
            self.driver.find_element_by_id('wp-submit').click()
            time.sleep(5)
            username = self.driver.find_element_by_id("user_login")
            username.send_keys(para.username)
            password = self.driver.find_element_by_id("user_pass")
            password.send_keys(para.password)

            #login
            self.driver.find_element_by_id("wp-submit").click()
            time.sleep(5)

        except:
            self.driver.close()
    def create_blog(self,my_tittle,my_para,my_img):
        try:
            # select posts class from menus
            menus = self.driver.find_elements_by_css_selector("div[class='wp-menu-name']")
            menus[1].click()
            time.sleep(2)

            # make a new post  
            menus = self.driver.find_elements_by_css_selector("ul[class='wp-submenu wp-submenu-wrap']")[0].find_elements_by_css_selector('li')
            menus[-1].click()
            time.sleep(2)


            #select category            
            category_div = self.driver.find_element_by_css_selector("div[id='category-all']")
            self.driver.execute_script("arguments[0].scrollTop = (0,300)", category_div)
            category = self.driver.find_element_by_id("in-category-214").click()
            time.sleep(2)

           
            #moving to down position
            self.driver.execute_script("scroll(0, 450);")
            time.sleep(2)

            # select type of blog
            select = Select(self.driver.find_element_by_id('page_template'))
            select.select_by_visible_text('news announcement')
            time.sleep(2)

            #uploading image
            self.driver.find_element_by_id("set-post-thumbnail").click()
            time.sleep(2)
            self.driver.find_element_by_id("menu-item-upload").click()
            time.sleep(2)
            self.driver.find_element_by_id("__wp-uploader-id-1").click()
            time.sleep(2)
            pyautogui.press("esc")

            
            image = '/home/alee/Documents/MuhammadAlee/TextPreProcessing/ParaPhrasing/images/'+my_img
            input_file = "//input[starts-with(@id,'html5_')]"
            self.driver.find_element_by_xpath(input_file).send_keys(image)

            time.sleep(5)
            self.driver.find_elements_by_css_selector('button[class="button media-button button-primary button-large media-button-select"]')[0].click()
            time.sleep(2)


            #moving to down position
            self.driver.execute_script("scroll(0, 1200);")

            #setting seo title 
            seo_title=self.driver.find_elements_by_css_selector('div[class="public-DraftStyleDefault-block public-DraftStyleDefault-ltr"]')[0]
            seo_title.send_keys(Keys.CONTROL, 'a')
            seo_title.send_keys(Keys.DELETE)
            seo_title.send_keys(my_tittle)



             # place title here
            top_title = self.driver.find_element_by_id("title")
            top_title.send_keys(my_tittle)

            #place paragraph here
            self.driver.switch_to.frame(self.driver.find_element_by_id("content_ifr"))
            para_body = self.driver.find_element_by_id("tinymce")
            para_body.send_keys(my_para)

            #back to main content 
            self.driver.switch_to.default_content()

            #again moving to top
            self.driver.execute_script("scroll(0, 0);")
            time.sleep(2)
            #finally publish Blog here
            self.driver.find_element_by_css_selector("input[id='publish']").click()
            time.sleep(5)
            self.driver.close()
        except Exception as e:
            print(e)
            self.driver.close()

# if __name__=="__main__":
#     up=Upload()
#     up.login()
#     up.create_blog("akjk","akkh","160.jpg")



    
    