from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re


class Parser:
    def __init__(self) -> None:
        pass

    def SetOption(self):
        self.option = webdriver.FirefoxOptions()
        # self.option.add_argument('--headless')
        # self.option.add_argument('--window-size=1920,1080')

    def Driver(self, url):
        self.driver = webdriver.Firefox(
            executable_path=r'c:\geckodriver.exe', options=self.option)
        self.driver.get(url)
        time.sleep(5)

    def CloseDriver(self):
        self.driver.close()


class Elements():
    def __init__(self, driver):
        self.driver = driver

    def MoveMenuCity(self):  # Переход в меню местоположения
        self.CityMenu = self.driver.find_element(
            By.CLASS_NAME, 'city-select__text')
        self.CityMenu.click()
        time.sleep(3)
        self.CitySelect = self.driver.find_element(By.ID, 'select-city')

    def SerchFO(self):
        self.Districts = self.CitySelect.find_element(
            By.CLASS_NAME, 'districts')  # Получили все ФО
        self.ListDistricts = self.Districts.text.split('\n')
        return self.ListDistricts

    def SerchRegions(self, Districts):  # Получили список регионов.
        self.CitySelect.find_element(By.PARTIAL_LINK_TEXT, Districts).click()
        time.sleep(2)
        self.Regions = self.CitySelect.find_element(By.CLASS_NAME, 'regions')
        self.ListRegions = self.Regions.text.split('\n')
        return self.ListRegions

    # Получили Список городов Региона
    def SerchCity(self, Region):
        self.CitySelect.find_element(By.PARTIAL_LINK_TEXT, Region).click()
        time.sleep(2)
        self.Cities = self.CitySelect.find_element(By.CLASS_NAME, 'cities')
        self.ListCities = self.Cities.text.split('\n')
        return self.ListCities

    def SelectParam(self, District, Region, City):
        self.CitySelect.find_element(By.PARTIAL_LINK_TEXT, District).click()
        time.sleep(1.5)
        self.CitySelect.find_element(By.PARTIAL_LINK_TEXT, Region).click()
        time.sleep(1.5)
        self.CitySelect.find_element(By.PARTIAL_LINK_TEXT, City).click()

    def ShopsAvail(self):
        self.driver.find_element(
            By.CLASS_NAME, 'order-avail-wrap__link').click()  # Кнопка наличия
        time.sleep(4)
        self.shops = self.driver.find_element(
            By.CLASS_NAME, 'vue-shop-avail__content')  # Выбор поля
        CatalogShopNames = self.shops.find_elements(
            By.CLASS_NAME, 'shop-view__title-p')  # Получаем список магазинов
        CatalogProductAvails = self.shops.find_elements(
            By.CLASS_NAME, 'shop-choose-list__issue-date-text')  # Получаем наличие
        ShopName = []
        ProductAvail = []
        for i in CatalogShopNames:
            ShopName.append(i.text)
        for i in CatalogProductAvails:
            if re.search(r'\d+ шт', i.text) == None:
                ProductAvail.append('No')
            else:
                ProductAvail.append(re.search(r'\d+', i.text).group())
        self.CatalogsShopAvailProduct = dict(zip(ShopName, ProductAvail))
        print(self.CatalogsShopAvailProduct)

    def FindInfo(self):
        self.data = self.driver.find_element(By.CLASS_NAME, 'product-card-top')
        self.title = self.data.find_element(
            By.CLASS_NAME, 'product-card-top__title').text
        try:
            self.price = self.data.find_element(
                By.CLASS_NAME, 'product-buy__price_active').text
            self.price = self.price.replace(' ', '')
            self.price = re.search('\d+₽', self.price).group().replace('₽', '')
            print(self.title+'\n'+self.price)
        except:
            self.price = self.data.find_element(
                By.CLASS_NAME, 'product-buy__price').text
            self.price = self.price.replace(' ', '')
            self.price = re.search('\d+₽', self.price).group().replace('₽', '')
            print(self.title+'\n'+self.price)


url = 'https://www.dns-shop.ru/product/057676b27db03330/processor-amd-athlon-x4-950-oem/'
main = Parser()
main.SetOption()
main.Driver(url)
info = Elements(main.driver)
info.MoveMenuCity()
Districts = info.SerchFO()


for i in Districts:
    Regions = info.SerchRegions(i)
    for i2 in Regions:
        City = info.SerchCity(i2)
        for i3 in City:
            try:
                info.SelectParam(i, i2, i3)
            except:
                main.driver.refresh()
                time.sleep(3)
                info.SelectParam(i, i2, i3)
            info.FindInfo()
            info.ShopsAvail()
            main.driver.refresh()
            time.sleep(3)
            info.MoveMenuCity()
main.CloseDriver()
