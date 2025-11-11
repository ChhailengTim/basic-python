from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")

# Setup Chrome driver with webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Open login page
    driver.get("https://tube2fb.app/login.html")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))

    # Login
    driver.find_element(By.ID, "email").send_keys("channyy751@gmail.com")
    time.sleep(0.5)
    driver.find_element(By.ID, "password").send_keys("zkxjqTmEjxL5o223")
    time.sleep(0.5)
    driver.find_element(By.NAME, "login").click()

    # Wait for login success
    WebDriverWait(driver, 10).until(EC.url_contains("tube2fb.app"))

    # Navigate to Photos in Bulk
    driver.get("https://tube2fb.app/pages/photos-bulk.html")

    # Select account
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@class='fb-account-name' and text()='Tim Chhaileng']"))
    ).click()
    time.sleep(0.5)

    # Select page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='page-name' and text()='Kape Watch']"))
    ).click()
    time.sleep(0.5)

    # Click Upload tab
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@class='tab' and @data-val='photo-upload']"))
    ).click()
    time.sleep(0.5)

    print("Waiting for upload page to fully load...")
    time.sleep(120)  # Wait for image upload inputs to appear

    new_captions = [
    "Happiness in every bite!",
    "So good, no sharing!",
    "Cheese, please!",
    "Grill it, thrill it!",
    "Boom! Flavor blast!",
    "My burger obsession!",
    "Hot, fresh, wow!",
    "Dreaming in cheese!",
    "Pizza goals!",
    "Burger bliss!",
    "Slice, slice, baby!",
    "Fresh out the oven!",
    "Melted perfection!",
    "Stacked with love!",
    "Crispy on the edge!",
    "Cheese pull magic!",
    "Saucy & proud!",
    "Buns of glory!",
    "Golden & gooey!",
    "One bite, hooked!",
    "Sizzling hot!",
    "Pizza night, every night!",
    "Burger heaven!",
    "Thin crust thrills!",
    "Loaded & loved!",
    "Feast mode on!",
    "Topped to perfection!",
    "Melty, messy, mine!",
    "Savor the stack!",
    "Crust you can’t resist!",
    "Flavors that wow!",
    "Just one more bite!",
    "Cheese the day!",
    "Grilled just right!",
    "Dripping with flavor!",
    "Crunch into joy!",
    "Freshly stacked!",
    "Perfect pizza moment!",
    "Burger & chill!",
    "Say it with cheese!",
    "Crispy crust vibes!",
    "Patty perfection!",
    "Mozza magic!",
    "Full of flavor!",
    "Your slice awaits!",
    "All about that bite!",
    "Smash it & love it!",
    "Cheese lovers unite!",
    "From oven to heart!",
    "Patty goals!",
    "Thin, thick, perfect!",
    "Fresh, hot, wow!",
    "Buns, beef, bliss!",
    "Stack it high!",
    "Oven-fresh love!",
    "Gooey & glorious!",
    "Patty party!",
    "Slice made for you!",
    "Double the cheese!",
    "Hot, fresh, ready!",
    "Layers of love!",
    "Grilled to thrill!",
    "Crust heaven!",
    "Eat, smile, repeat!",
    "All stacked up!",
    "Pizza perfection!",
    "Mega melty moment!",
    "Say hello to flavor!",
    "Your burger, your rules!",
    "Golden crust dreams!",
    "Loaded with love!",
    "Perfect patty vibes!",
    "Slice of pure joy!",
    "Grilled greatness!",
    "Cheese it up!",
    "Stack & snack!",
    "Hot cheese hugs!",
    "Bite, love, repeat!",
    "Crust lovers’ club!",
    "Ultimate burger fix!",
    "Slice life best life!",
    "Freshly grilled love!",
    "Pizza party time!",
    "Patty packed!",
    "Crispy & cheesy!"
]



    start_time = datetime(2025, 8, 10, 0, 0, 0)
    interval = timedelta(hours=1)
    schedule_dates = [(start_time + i * interval).strftime("%d %b %Y %H:%M:%S") for i in range(len(new_captions))]

    for i in range(len(new_captions)):
        # Refresh elements each loop
        caption_textareas = driver.find_elements(By.CSS_SELECTOR, "textarea[name='caption[]'].caption.input-text")
        schedule_tabs = driver.find_elements(By.CSS_SELECTOR, "a.tab[data-val='schedule']")
        schedule_inputs = driver.find_elements(By.CSS_SELECTOR, "input[name='schedule-date[]'].schedule-date")

        if i >= len(caption_textareas) or i >= len(schedule_tabs) or i >= len(schedule_inputs):
            print(f"No more inputs or tabs at index {i}")
            break

        # Add caption
        try:
            caption_textareas[i].clear()
            time.sleep(0.5)
            caption_textareas[i].send_keys(new_captions[i])
            print(f"Photo {i+1} caption added.")
            time.sleep(0.5)
        except Exception as e:
            print(f"Error adding caption for photo {i+1}: {e}")
            continue

        # Click schedule tab for this photo to open calendar popup
        try:
            driver.execute_script("arguments[0].click();", schedule_tabs[i])
            time.sleep(0.5)
        except Exception as e:
            print(f"Failed to click schedule tab for photo {i+1}: {e}")
            continue

        # Clear and send schedule date/time
        try:
            schedule_input = schedule_inputs[i]
            schedule_input.clear()
            time.sleep(0.5)
            schedule_input.send_keys(schedule_dates[i])
            time.sleep(0.10)
            print(f"Photo {i+1} scheduled at {schedule_dates[i]}")
        except ElementNotInteractableException:
            print(f"Schedule input not interactable for photo {i+1}")
            continue

        # Click Apply button on calendar popup
        try:
            apply_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "applyBtn"))
            )
            driver.execute_script("arguments[0].click();", apply_button)
            print(f"Photo {i+1} schedule applied.")
            time.sleep(0.5)  # wait for popup to close
        except TimeoutException:
            print(f"No calendar popup Apply button found for photo {i+1}.")

    print("All photos processed. Browser will stay open for manual check.")

    # Keep browser open
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    driver.quit()
