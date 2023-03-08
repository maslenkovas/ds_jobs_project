from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import re

#author: Kenarapfaik
#url: https://github.com/arapfaik/scraping-glassdoor-selenium

def get_jobs(keyword_job, keyword_location, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    if keyword_location=='Bahrain':
        loc_id = '21'
    if keyword_location=='Qatar':
        loc_id = '199'
    if keyword_location=='Kuwait':
        loc_id = '137'
    if keyword_location=='Oman':
        loc_id = '167'
    if keyword_location=='Saudi Arabia':
        loc_id = '207'
    if keyword_location=='United Arab Emirates':
        loc_id = '6'

    url = "https://www.glassdoor.com/Search/results.htm?keyword=" + keyword_job + "&locId="+ loc_id +"&locT=N&locName=" + keyword_location


    print(url)
    driver.get(url)
    jobs = []

    try:
        # clicking to the "See All Jobs" button.
        driver.find_element(
            By.XPATH, '/html/body/div[2]/div/div/div[1]/div[1]/div[3]/a/strong').click()
        # print('  "See All Jobs"  worked')
    except NoSuchElementException:
        # print('  "See All Jobs" failed')
        pass
    
    num_jobs = int(re.findall(r'\d+', \
                          driver.find_element(By.XPATH, './/h1[@data-test="jobCount-H1title"]').text)[0])
    
    # If true, should be still looking for new jobs.
    while len(jobs) < num_jobs:

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        time.sleep(.1)

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(
            By.XPATH, '//li[@class="react-job-listing css-wp148e eigr9kq3"]')
        # print('job_buttons DONE, length=', len(job_buttons))
        job_count = 0

        for job_button in job_buttons:

            print("Progress: {}".format(
                "" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()
            time.sleep(1)
            collected_successfully = False

            try:
                # clicking to the X.
                driver.find_element(By.XPATH, '//span[@alt="Close"]').click()
                # print(' x out worked')
            except NoSuchElementException:
                # print(' x out failed')
                pass

            # clicking the "Show More" button
            try:
                driver.find_element(By.XPATH, './/div[@class="css-t3xrds e856ufb4"][text()="Show More"]').click()
                print("'Show More' button' is clicked")
            except NoSuchElementException:
                pass

            while not collected_successfully:
                try:
                    company_name = driver.find_element(
                        By.XPATH, './/div[@data-test="employerName"]').text
                    location = driver.find_element(
                        By.XPATH, './/div[@data-test="location"]').text
                    job_title = driver.find_element(
                        By.XPATH, './/div[@data-test="jobTitle"]').text
                    all_children = driver.find_elements(By.XPATH, './/div[@class="jobDescriptionContent desc"]//*')
                    if len(all_children)>0:
                        job_description_l = []
                        for i, child in enumerate(all_children):
                            if child.text not in job_description_l:
                                job_description_l.append(child.text)
                        job_description = " ".join(job_description_l)
                    else:
                        job_description = driver.find_element(By.XPATH, './/div[@class="jobDescriptionContent desc"]').text

                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = job_button.find_element(
                    By.XPATH, './/span[@data-test="detailSalary"]').text
                # print('SALARY INFO-------->', salary_estimate)
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."
                # print('SALARY INFO-------->', salary_estimate)

            try:
                rating = job_button.find_element(
                    By.XPATH, './/span[@class=" css-2lqh28 e1cjmv6j1"]').text
                # print('RATING INFO-------->', rating)
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."
                # print('RATING INFO-------->', rating)

            try:
                job_age = job_button.find_element(
                    By.XPATH, './/div[@class="d-flex align-items-end pl-std css-1vfumx3"]').text
                # print('RATING INFO-------->', rating)
            except NoSuchElementException:
                job_age = -1  # You need to set a "not found value. It's important."
                # print('RATING INFO-------->', rating)

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
                print("job_age: {}".format(job_age))

            try:
                size = driver.find_element(
                    By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Size"]//following-sibling::*').text
                # print('Found the size of the company')
            except NoSuchElementException:
                size = -1
                # print('Didnt find the size of the company')

            try:
                founded = driver.find_element(
                    By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Founded"]//following-sibling::*').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element(
                    By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Type"]//following-sibling::*').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element(
                    By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Industry"]//following-sibling::*').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element(
                    By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Sector"]//following-sibling::*').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element(
                    By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Revenue"]//following-sibling::*').text
            except NoSuchElementException:
                revenue = -1

            try:
                competitors = driver.find_element(
                    By.XPATH, './/div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]//span[text()="Competitors"]//following-sibling::*').text
            except NoSuchElementException:
                competitors = -1

            if verbose:
                # print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "job_age": job_age,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "Competitors": competitors})

            # add job to jobs
            job_count += 1
            # print('job_count = ', job_count)

        # Clicking on the "next page" button
        try:
            next_button = driver.find_element(By.XPATH, './/button[@class="nextButton css-1hq9k8 e13qs2071"]')
            if next_button.is_enabled():
                next_button.click()
                print('NEXT button is clicked')
            else:
                print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                    num_jobs, len(jobs)))
                break
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(
                num_jobs, len(jobs)))
            break

    # This line converts the dictionary object into a pandas DataFrame.
    return pd.DataFrame(jobs)
