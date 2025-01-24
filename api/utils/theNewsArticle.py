from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

class TheNewsArticle:
    def scrape_news(date, city):
        articles_data = []
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")  # Start Chrome maximized
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Navigate to the website
        url = f"https://e.thenews.com.pk/{city}/{date}/page1"
        driver.get(url)

        # Set an explicit wait with increased timeout
        wait = WebDriverWait(driver, 10)
        time.sleep(3)  # Ensure page has loaded

        try:
            # Retry mechanism for dropdown if not found
            retries = 3
            while retries > 0:
                try:
                    # Locate and click the dropdown menu
                    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.nav__item.dd")))
                    dropdown.click()
                    time.sleep(2)
                    break
                except Exception as e:
                    retries -= 1
                    print(f"Dropdown not clickable, retrying... {retries} attempts left.")
                    time.sleep(2)  # Wait before retrying
                    if retries == 0:
                        print("Failed to click the dropdown after multiple attempts.")
                        return articles_data  # Exit if unable to click

            # Locate all the options inside the dropdown
            options = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.dropdown-content.dropDouble > a")))
            print("Dropdown options:")

            clickedArticles = []

            for i in range(len(options)):
                try:
                    # Check if dropdown is visible again
                    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.nav__item.dd")))
                    dropdown.click()
                    time.sleep(2)

                    options = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.dropdown-content.dropDouble > a")))
                    option = options[i]

                    article_type = option.text

                    if option.text == 'Advertisement':
                        continue  # skip advertisement 

                    page_href = option.get_attribute("href")
                    if len(clickedArticles) > 0:
                        time.sleep(2)
                        clickedArticles = []

                    print(f"Clicking on option: {option.text}")
                    driver.execute_script(f"window.open('{page_href}', '_blank');")
                    driver.switch_to.window(driver.window_handles[-1])
                    time.sleep(2)

                    try:
                        areas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "area")))
                    except Exception as e:
                        print("No areas found, skipping to next option.")
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        continue  # Continue to the next option

                    for j in range(len(areas)):
                        try:
                            areas = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "area")))
                            area = areas[j]
                            href = area.get_attribute('href')
                            coords = area.get_attribute("coords")
                            print(f"Area {j + 1}: href={href}, coords={coords}")

                            if href not in clickedArticles and 'id' in href:
                                clickedArticles.append(href)
                                print(f"Opening Area {j + 1}: href={href}")
                                driver.execute_script(f"window.open('{href}', '_blank');")
                                driver.switch_to.window(driver.window_handles[-1])

                                retries = 3
                                while retries > 0:
                                    try:
                                        details_inner = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.detailsInner")))
                                        details_heading = details_inner.find_element(By.CSS_SELECTOR, 'div.detailsHeading')
                                        title = details_heading.find_element(By.CSS_SELECTOR, 'h1')
                                        print(title.text)

                                        story_details = details_inner.find_element(By.CSS_SELECTOR, 'div.story-detail')
                                        articles = story_details.find_elements(By.CSS_SELECTOR, 'p')
                                        article_text = "\n".join(article.text for article in articles)
                                        article_date = details_inner.find_element(By.CSS_SELECTOR, 'div.detail-left-tittle > div.category-date')

                                        articles_data.append({
                                            'title': title.text,
                                            'article': article_text,
                                        })
                                        print(f"Current article count: {len(articles_data)}")
                                        time.sleep(2)
                                        break

                                    except Exception as e:
                                        retries -= 1
                                        print(f"Retrying to fetch details_inner, remaining attempts: {retries}")
                                        time.sleep(2)  # Wait before retrying

                                if retries == 0:
                                    print(f"Failed to load details for {href} after multiple attempts.")
                                driver.close()
                                driver.switch_to.window(driver.window_handles[-1])

                        except Exception as e:
                            print(f"Error processing area {j + 1}: {e}")
                            continue  # Skip to next area if an error occurs

                    time.sleep(2)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[-1])

                except Exception as e:
                    print(f"An error occurred while processing option '{option.text}': {e}")
                    continue  # Skip to next dropdown option if an error occurs

            print("All areas processed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            driver.quit()
            return articles_data
