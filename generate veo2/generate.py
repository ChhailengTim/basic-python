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

signal.signal(signal.SIGINT, cleanup_and_exit)  # Handle Ctrl+C on Mac/Linux

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
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")

# ===== STEP 3: OPEN SITE =====
try:
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
        """
    })

    driver.get("https://aistudio.google.com/prompts/new_video")
    wait = WebDriverWait(driver, 30)

    print("[INFO] Waiting 60 seconds for manual steps (or page load)...")
    time.sleep(60)

    # Function to click Run button
    def click_run():
        try:
            run_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'label') and text()='Run']"))
            )
            run_button.click()
            print("[INFO] Run button clicked.")
            time.sleep(3)

            # Optional confirmation dialog
            try:
                option_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Run']]"))
                )
                option_btn.click()
                print("[INFO] Confirmed Run option.")
            except:
                print("[INFO] No extra Run dialog.")
        except Exception as e:
            print(f"[ERROR] Could not click Run button: {e}")
            return False
        return True

    # ===== MAIN LOOP: KEEP TRYING UNTIL STABLE RUN =====
    print("[INFO] Starting generation attempts...")
    stable = False

    while not stable:
        click_run()

        print("[INFO] Monitoring generation for stability...")
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
                # No "Running" detected yet or generation stopped
                if start_time is not None:
                    print("[WARNING] Generation stopped before 40s. Retrying...")
                    break
            time.sleep(2)

    print("[INFO] Video is generating. Press CTRL+C to stop the program and cleanup.")

    while True:
        time.sleep(5)  # Keep the script alive

except Exception as e:
    print(f"❌ An error occurred: {e}")
    cleanup_and_exit()
