import os
import tempfile
import shutil
import time
import signal
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== CONFIGURATION =====
original_user_data_dir = "/Users/chhailengtim/Library/Application Support/Google/Chrome"
profile_directory = "Person 1"
chromedriver_path = "/Users/chhailengtim/Desktop/generate veo2/chromedriver-mac-arm64/chromedriver"
image_path = "/Users/chhailengtim/Desktop/generate veo2/images/sample.jpg"
prompt_text = "Static camera, fixed angle, no zoom or pan. Framing stays constant, animate 2 character drinking hot coffee and reading book, realistic style, high detail, 4k"
download_dir = "/Users/chhailengtim/Desktop/generate veo2/videos"

driver = None
temp_user_data_dir = None

# ===== CLEANUP FUNCTION =====
def cleanup_and_exit(signum=None, frame=None):
    print("\n[INFO] Caught exit signal. Cleaning up...")
    try:
        if driver:
            driver.quit()
            print("[INFO] Browser closed.")
    except:
        pass
    try:
        if temp_user_data_dir and os.path.exists(temp_user_data_dir):
            shutil.rmtree(temp_user_data_dir)
            print("[INFO] Temporary profile deleted.")
    except:
        pass
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup_and_exit)

# ===== STEP 1: VERIFY DRIVER =====
try:
    service = Service(chromedriver_path)
    test_driver = webdriver.Chrome(service=service)
    print("✅ ChromeDriver version matches Chrome browser version")
    test_driver.quit()
except Exception as e:
    print(f"❌ Version mismatch error: {e}")
    exit()

# ===== STEP 2: TEMPORARY PROFILE =====
temp_user_data_dir = tempfile.mkdtemp()
try:
    shutil.copytree(
        os.path.join(original_user_data_dir, profile_directory),
        os.path.join(temp_user_data_dir, profile_directory)
    )
except FileNotFoundError:
    print("[WARNING] Profile directory not found, using fresh profile")

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={temp_user_data_dir}")
options.add_argument(f"profile-directory={profile_directory}")
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
# options.add_argument(f"--headless=new")  # Run headless in background
prefs = {"download.default_directory": download_dir}
options.add_experimental_option("prefs", prefs)

# ===== STEP 3: OPEN SITE =====
try:
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    driver.get("https://aistudio.google.com/prompts/new_video")
    wait = WebDriverWait(driver, 30)
    print("[INFO] Waiting 10 seconds for page load...")
    time.sleep(10)

    # ===== CLOSE POPUP IF PRESENT =====
    try:
        close_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//mat-dialog-actions//button[.//span[text()='close']]"))
        )
        driver.execute_script("arguments[0].click();", close_btn)
        print("[INFO] Popup closed.")
    except:
        print("[INFO] No popup to close.")

    # ===== CLICK note_add AND UPLOAD IMAGE =====
    for attempt in range(5):
        try:
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.cdk-overlay-backdrop-showing"))
            )
            note_add = driver.find_element(By.XPATH, "//span[contains(@class,'ms-button-icon') and text()='note_add']")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", note_add)
            driver.execute_script("arguments[0].click();", note_add)
            print("[INFO] note_add clicked.")
            break
        except Exception as e:
            print(f"[WARNING] note_add not clickable, retrying... ({e})")
            time.sleep(2)

    # Upload image
    try:
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(image_path)
        print("[INFO] Image uploaded.")
    except Exception as e:
        print(f"[ERROR] Could not upload image: {e}")

    # Click Acknowledge if exists
    try:
        ack_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Acknowledge')]"))
        )
        driver.execute_script("arguments[0].click();", ack_btn)
        print("[INFO] Acknowledge clicked.")
    except:
        print("[INFO] No Acknowledge button.")

    # Enter prompt
    try:
        textarea = driver.find_element(By.XPATH, "//textarea[@formcontrolname='prompt']")
        textarea.clear()
        textarea.send_keys(prompt_text)
        print("[INFO] Prompt entered.")
        time.sleep(3)
    except Exception as e:
        print(f"[ERROR] Could not enter prompt: {e}")

    # ===== CLICK RUN AND MONITOR =====
    def click_run():
        try:
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.cdk-overlay-backdrop-showing"))
            )
            run_button = driver.find_element(By.XPATH, "//span[contains(@class,'label') and text()='Run']")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", run_button)
            driver.execute_script("arguments[0].click();", run_button)
            print("[INFO] Run button clicked.")
            time.sleep(2)

            # Optional confirmation
            try:
                option_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Run']]"))
                )
                driver.execute_script("arguments[0].click();", option_btn)
                print("[INFO] Confirmed Run option.")
            except:
                print("[INFO] No extra Run dialog.")
        except Exception as e:
            print(f"[ERROR] Could not click Run button: {e}")
            return False
        return True

    stable = False
    while not stable:
        click_run()
        print("[INFO] Monitoring generation...")
        start_time = None
        while True:
            try:
                running_label = driver.find_element(By.XPATH, "//span[contains(@class,'label') and contains(text(),'Running')]")
                running_text = running_label.text.strip()
                if running_text.startswith("Running"):
                    if start_time is None:
                        start_time = time.time()
                        print("[INFO] Detected generation start.")
                    else:
                        elapsed = time.time() - start_time
                        print(f"[INFO] Elapsed time: {elapsed:.1f}s")
                        if elapsed >= 40:
                            print("✅ Generation stable (40s passed).")
                            stable = True
                            break
            except:
                if start_time is not None:
                    print("[WARNING] Generation stopped before 40s. Retrying Run...")
                    break
            time.sleep(2)

    # ===== DOWNLOAD VIDEO =====
    try:
        print("[INFO] Waiting 20 seconds after generation completes before downloading...")
        time.sleep(20)  # wait to ensure video is ready

        # Find the button that contains the <span> with text 'download'
        download_btn = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='download']]"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", download_btn)
        driver.execute_script("arguments[0].click();", download_btn)
        print(f"✅ Download button clicked. Video should start downloading to: {download_dir}")

    except Exception as e:
        print(f"[ERROR] Could not click download: {e}")


    print("[INFO] Script finished. Press CTRL+C to exit.")
    while True:
        time.sleep(5)

except Exception as e:
    print(f"❌ An error occurred: {e}")
    cleanup_and_exit()
