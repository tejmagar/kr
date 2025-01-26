from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

def save_snapshot(filename):
    """Save the current page as an HTML file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(driver.page_source)

def handle_alert():
    """Handle unexpected alerts."""
    try:
        alert = driver.switch_to.alert
        print(f"Unexpected alert detected: {alert.text}")
        alert.accept()  # Accept (click OK) the alert
        print("Alert accepted.")
    except Exception:
        pass  # No alert detected

def close_layer_popup():
    """Close the special notice layer popup if present."""
    try:
        popup = driver.find_element(By.ID, "layerSpecInfo")  # Look for popup by its ID
        if popup.is_displayed():
            print("Special notice popup detected. Closing it.")
            close_button = popup.find_element(By.XPATH, ".//a[contains(text(), '닫기')]")
            close_button.click()  # Click the close button
            print("Popup closed.")
    except Exception:
        print("No special notice popup detected.")

try:
    # Step 1: Open the login URL
    login_url = "https://www.g4k.go.kr/cipl/0100/login.do?koMber=Y"
    driver.get(login_url)
    save_snapshot("pages/login_page.html")
    print("Login page snapshot saved.")

    # Step 2: Detect URL change manually by checking driver.current_url
    current_url = driver.current_url
    while current_url == login_url:
        current_url = driver.current_url

    print(f"Login successful, current URL: {current_url}")
    save_snapshot("pages/post_login_page.html")

    # Step 3: Navigate to the target page
    target_url = "https://www.g4k.go.kr/ciph/0800/selectCIPH0801S1eng.do"
    driver.get(target_url)
    handle_alert()  # Handle potential alerts on navigation
    save_snapshot("pages/target_page.html")
    print("Target page snapshot saved.")

    # Step 4: Reload the page repeatedly and check for id="visitEmblAddr"
    while True:
        driver.refresh()  # Reload the page
        handle_alert()  # Handle potential alerts
        save_snapshot("pages/reloaded_page.html")
        print("Page reloaded and snapshot saved.")

        try:
            element = driver.find_element(By.ID, "visitEmblAddr")
            if element.text.strip():  # Check for any non-empty text
                print(f"Element found with text: {element.text}")
                break
        except Exception:
            pass  # Ignore if the element is not found

        time.sleep(0.1)  # Short delay between reloads

    # Step 5: Close popup if present and click the button with id="aftBtn"
    try:
        close_layer_popup()  # Close the popup if it's present
        aft_button = driver.find_element(By.ID, "aftBtn")
        aft_button.click()
        print("Button with ID 'aftBtn' clicked.")
        save_snapshot("after_button_click.html")
    except Exception as e:
        print(f"Failed to click button 'aftBtn': {e}")

    # Step 6: Monitor manual page changes
    print("Monitoring for manual page changes. Perform manual actions if necessary.")
    previous_url = driver.current_url

    while True:
        new_url = driver.current_url
        if new_url != previous_url:
            print(f"Page changed manually to: {new_url}")
            save_snapshot(f"manual_change_{int(time.time())}.html")
            previous_url = new_url

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Automation completed. The browser will remain open for manual tasks.")
