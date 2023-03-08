# Data Scientist salary prediction in UAE 📊&#128176; 🇦🇪 
As you probably saw, the job posters often do not provide the salary information in the job description. So it may be difficult to understand what salary range you should aim for when negotiating with recruiters. In this project we built a model, that can predict estimated average salary for a role, based on the information mentioned in the description for this role.

### This project is aimed to:
* analyze Data Scientist job market in UAE;
* provide a tool for predicting estimated average salary for Data Science and similar roles based on a job description;
* show the proccess of creating data science project scratch.

📲 You can check out the demo app of the project here: [➡️ Scientist salry prediction app ◀️](https://ds-salary-prediction.azurewebsites.net/)

<img src="https://github.com/maslenkovas/ds_jobs_project/blob/master/images/demo.png" width="600">

# Project structure 🗂 
If you want to replicate this project on your machine, you should run files in the following order:

1. Install the requirements using 
```sh
pip install -r requirements.txt
```
2. Run **_data_collection.py_**. This file contains the code for scraping jobs data from _glassdoor.com_ using Selenium webdriver.

_Note: don't forget to change **driver_path** and **save_to_path**, as well as the locations for job search._

3. **salary_extraction.ipynb** . In this file we make use of transformer model to extract the salary info from job descriptions. 
_Note: this file contains python notebook from google colab, so if you want to use it on your own gpu make sure you removed the unrelevant rows and changes the paths._

4. Run **data_cleaning.py** . This file contains the data cleaning & feature extraction code.
_Note: don't forget to change **curr_path** and **data_scraped_path**, as well as the locations for job search._

5. **eda.ipynb** contains exploratory data analysis for cleaned webscraped data.

6. **model_building.py** contains the code for developing of the machine learning model. 

_Note: The code contains several models for explaratory purposes. The best performing model is saved as **model_file.p**_

# EDA &#128202;
Since in UAE job posters often do not contain information about salary range for the position, we had to use additional tools to extract salary from the job description itself, such as question-answering transformer model. After collecting and clearning the data, we ended up with around 40 jobs. The most common job category was data analyst. According collected job descriptions, the topics such _experience, business, management, financial analysis, team work_ are commonly menationed by recruiters when they search for Data Science/ Data Analysis professionals.

The following wordcloud shows the most mentioned words in the scraped data jobs' descriptions:
<img src="https://github.com/maslenkovas/ds_jobs_project/blob/master/images/wc.png" width="350">


If you have any questions or suggestions, please send them to me via following email: maslenkova.lana@gmail.com

## Resources 📚

Glassdoor web-scraper code originating from Kenarapfaik: https://github.com/arapfaik/scraping-glassdoor-selenium

The transformer model for salary information extraction is taken from here: [🤗bert-large-uncased-whole-word-masking-finetuned-squad](https://huggingface.co/bert-large-uncased-whole-word-masking-finetuned-squad)

