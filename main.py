import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def scrape_company(driver, company_url):
    """Scrape required fields from LinkedIn Company URL"""
    driver.get(company_url + "about/")

    company_name = driver.find_element(By.CSS_SELECTOR, "h1 span").get_attribute("innerText")

    # Get company about container
    about_section = driver.find_element(By.CSS_SELECTOR, "section.org-page-details-module__card-spacing").get_attribute("innerHTML").strip()
    about_section = about_section.replace("\n", "")

    # Remove extra double spaces
    while True:
        if about_section.find("  ") > 0:
            about_section = about_section.replace("  ", " ")
        else:
            break

    # Scrape Website URL
    if about_section.find('Website </dt>') > 0:
        company_website = about_section.split('Website </dt>')[1]
        company_website = company_website.split('</dd>')[0]

        if company_website.find('href="') > 0:
            company_website = company_website.split('href="')[1]
            company_website = company_website.split('"')[0]
        else:
            company_website = ""

    # Scrape Company Industry
    if about_section.find('Industry </dt>') > 0:
        company_industry = about_section.split('Industry </dt>')[1]
        company_industry = company_industry.split('</dd>')[0]
        company_industry = company_industry.split('">')[1].strip()
    else:
        company_industry = ""

    # Scrape Company headquarter
    if about_section.find('Headquarters </dt>') > 0:
        company_headquarter = about_section.split('Headquarters </dt>')[1]
        company_headquarter = company_headquarter.split('</dd>')[0]
        company_headquarter = company_headquarter.split('">')[1].strip()
    else:
        company_headquarter = ""


    print("Company Name: {}".format(company_name))
    print("Website: {}".format(company_website))
    print("Industry: {}".format(company_industry))
    print("Headquarter: {}".format(company_headquarter))


def scrape_profile(driver, profile_url):
    """Scrape required fields from LinkedIn company URL"""
    driver.get(profile_url)

    profile_name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").get_attribute("innerText")
    profile_title = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").get_attribute("innerText")
    profile_location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline").get_attribute("innerText")

    # Click on Contact Info link
    driver.find_element(By.ID, "top-card-text-details-contact-info").click()
    time.sleep(1)
    profile_email = driver.find_element(By.CSS_SELECTOR, "a.pv-contact-info__contact-link[href^='mailto:']").get_attribute("innerText")

    print("Profile Name: {}".format(profile_name))
    print("Title: {}".format(profile_title))
    print("Location: {}".format(profile_location))
    print("Email: {}".format(profile_email))


def scrape_jobs(driver, jobs_url):
    """Scrape required fields from LinkedIn job page"""
    driver.get(jobs_url)

    for job in driver.find_elements(By.CSS_SELECTOR, "ul#jobs-home-vertical-list__entity-list li"):
        try:
            job_title = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title").get_attribute("innerText")
            company_name = job.find_element(By.CSS_SELECTOR, "span.job-card-container__primary-description").get_attribute("innerText")
            company_location = job.find_element(By.CSS_SELECTOR, "li.job-card-container__metadata-item").get_attribute("innerText")
        except:
            continue

        print("Job title: {}".format(job_title))
        print("Company name: {}".format(company_name))
        print("Company location: {}".format(company_location))


if __name__ == "__main__":
    driver = webdriver.Chrome(service=Service(r"your chromedriver path"))

    # Log in LinkedIn
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys("<your username>")

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("<your password>")

    sign_in_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    sign_in_btn.click()

    scrape_profile(driver, "https://www.linkedin.com/in/veekekv-chuhna-077aa0126/")
    scrape_company(driver, "https://www.linkedin.com/company/microsoft/")
    scrape_jobs(driver, "https://www.linkedin.com/jobs/")

    driver.close()
    driver.quit()
