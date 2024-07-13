from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# タグを取得
def getTag(
        parent,
        target, 
        getBy = By.CSS_SELECTOR, 
        waitForDisplay = False, 
        waitTime = 3
    ):
    try:
        if waitForDisplay:
            WebDriverWait(parent, waitTime).until(
                EC.visibility_of_element_located((getBy, target))
            )
        return parent.find_element(getBy, target)
    
    except NoSuchElementException:
        return None