from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import configparser
import time

cfg = configparser.ConfigParser()
cfg.read("config.ini")
username = cfg.get("AUTH", "USERNAME")
password = cfg.get("AUTH", "PASSWORD")
base_url = cfg.get("IG_URLS", "base")
login_url = cfg.get("IG_URLS", "login")
search_tags_path = cfg.get("IG_URLS", "search_tags")


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()
        self.action = ActionChains(self.driver)
        self.driver.implicitly_wait(5)
        self.login()

    def login(self):
        self.driver.get(f"{login_url}")
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)
        self.driver.find_element_by_xpath("//div[text()='Log In']/parent::button").click()
        time.sleep(3)

    def nav_user(self, user):
        if self.driver.current_url not in f"{base_url}/{user}":
            self.driver.get(f"{base_url}/{user}")

    def is_following(self):
        try:
            self.driver.find_element_by_xpath("//span[@aria-label='Following']")
            return True
        except Exception:
            return False

    def follow_user(self, user):
        self.nav_user(user)
        if not self.is_following():
            try:
                follow_button = self.driver.find_element_by_xpath(
                    f"//h2[text()='{user}']/parent::div/div/div/div/div/span/span/button[text()='Follow']"
                )
                follow_button.click()
                print(f"Following {user}!")
                return
            except :
                pass
            try:
                follow_back_button = self.driver.find_element_by_xpath("//button[text()='Follow Back']")
                follow_back_button.click()
                print(f"Following {user}!")
                return
            except:
                print("You are not on a user profile!")
        else:
            print("You already follow this user!")

    def like_first_nine(self):
        thumbnails = self.driver.find_elements_by_xpath("//article/div/div/div/div/a")
        thumbnails[0].click()
        for i in range(10):
            like_button = self.driver.find_elements_by_xpath("//article[@role='presentation']/div/section/span/button")[
                0]
            right_arrow = self.driver.find_element_by_xpath("//a[text()='Next']")
            heart_icon = like_button.find_element_by_xpath("div/span/*[local-name()='svg']")
            time.sleep(1)
            if heart_icon.get_attribute("aria-label") == "Like":
                like_button.click()
            if i < 9:
                right_arrow.click()


if __name__ == '__main__':
    ig_bot = InstagramBot(username, password)

