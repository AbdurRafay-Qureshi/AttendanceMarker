import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options

print("Starting Edge with detach: True...")
options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Edge(options=options)
driver.get("http://example.com")
print("Page loaded. Active handles:", len(driver.window_handles))

print("Stopping driver service natively to simulate _cleanup()...")
try:
    driver.service.stop()
except Exception as e:
    print(e)

print("Service stopped. Check if browser is still running. Sleeping 5s before script exit.")
time.sleep(5)
print("Script terminating. Python GC will fire.")
