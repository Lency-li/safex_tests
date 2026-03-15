from selenium.webdriver.common.by import By


#locators
class Locators:
    #Host page
    CREATE_SECRET_MESSAGE = (By.XPATH, '//*[@id="create-card"]/div/header/h1')
    TEXT_AREA = (By.XPATH, '//*[@id="secret-message"]')
    FILE_LABEL = (By.XPATH, '//*[@id="secret-file-dropzone"]')
    FILE_INPUT = (By.ID, "secret-file")
    PIN_INPUT = (By.XPATH, '//*[@id="pin-code"]')
    EXPIRY_VALUE = (By.XPATH, '//*[@id="expiry-value"]')
    SELECT_UNIT = (By.XPATH, '//*[@id="ttl_unit"]')
    SUBMIT_BUTTON = (By.XPATH, '//*[@id="create-submit"]')
    #ERROR = (By.XPATH, '//*[@id="create-result"]/div/div/div/span')

    #Reult Page
    LINK_RESULT = (By.XPATH, '//*[@id="create-result"]/div/div/div/div[1]/div')
    COPY_LINK = (By.XPATH, '//*[@id="create-result"]/div/div/div/div[2]/button')
    NEW_SECRET_BUTTON = (By.XPATH, '//*[@id="create-result"]/div/div/div/div[2]/a')

    #View page
    PIN_UNLOCK = (By.XPATH, '//*[@id="unlock-pin"]')
    BUTTON_RETRIEVE = (By.XPATH, '//*[@id="unlock-form"]/div[2]/button')
    MESSAGE_AREA = (By.XPATH, '//*[@id="message-content"]')
    COPY_BUTTON = (By.XPATH, '//*[@id="unlock-card"]/div/div[2]/button')
    FILE_NAME = (By.XPATH, '//*[@id="file-name"]')
    