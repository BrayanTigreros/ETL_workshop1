# 📊 ETL WORKSHOP 01

## Project Overview

Build a dimensional model that represents candidate applications as a fact table and its associated dimensions (candidate, technology, seniority, country, and date). To perform an EDA on the raw data to determine the dataset size, data types, and null and duplicate values. Additionally, to determine the average score and the most common scores obtained by applicants in the coding test and technical interview.

To apply an ETL process to extract the applicant information. To transform the columns into dimensions, create the fact table based on granularity, and calculate, based on the coding test and technical interview scores, whether the applicant is eligible for the job. To create surrogate keys and relationships between the dimensions and the fact table. To load the information into the data warehouse and connect it to a key information visualization tool and generate KPIs from the transformed data.

---

## KPIs and requeriments

The KPIs from de dashboard show us important information about the Hirings by Years, Technology, Country over Years and Seniority, in addition the dashboard show also the top 10 average code and technology scores by technology and the hired by age ranges

About the requieriments, the KPIS meet the following requirements

- How many hirings are there for each of the technologies?
- How many hires are there for each year?
- How many hires are there according to the Seniority level?
- How many hirings are there for each country over the years?
- What is the average score obtained by the candidates in the Code Challenge and in the Technical Enterview by Technology?
- How many hiring are there per age range?

---

## Dimensional Model — Star Schema

This star schema dimensional model was designed because the core business objective is the application of candidates to a company. The fact table should contain information about the scores obtained on the company's tests, the years of experience of each applicant, and their suitability for the job.

The dimensions use surrogate keys to relate to the fact table. These dimensions are the descriptive attributes of each applicant. This allows us to know their personal information, country of origin, profession, seniority levels, and the date they applied to the company. Including a time dimension facilitates historical trend analysis using KPIs.


<img width="1203" height="781" alt="Captura de pantalla 2026-02-23 152605" src="https://github.com/user-attachments/assets/62551742-24b6-4657-8d9e-2e9ef0c140d1" />


---

## Grain Definition

> **One row represents an individual candidate's application to the company.**

Level of detail equals: 1 candidate
- With a first name, last name, and email address
- With a seniority level
- With a country of origin
- With a technology position
- With the day, month, and year they applied to the company, all in a single column and in three separate columns
- With a score on the company's tests
- With a number of years of experience

---

## ETL Logic

### Extract
We use a function to read the candidates' CSV files and store them in a staging area, in this case, pandas dataframes

### Transform
We calculate whether a candidate can be hired based on their coding test and technical interview scores. 
- We separate the first name, last name, and email address into a single dimension.
- We take the date and separate it into columns, creating a date key column where we combine the year, month, and day into a single value, all for the date or time dimension.
- For the remaining dimensions, we use a general function to separate these descriptive attributes into seniority level, technology role, and country.

Once we define the dimensions, we create the fact table where we will have the scores from the coding test and the technical interview, years of experience, a column indicating whether or not the candidate will be hired based on the decision rule, and the related surrogate keys for each dimension within the fact table

### Load
For data loading, we have two functions: 
- One that loads the transformed CSV data, which is useful for quick tests and verifying that the relationships between the fact table and the dimensions were correctly established, thus preventing the uploading of incorrect information to the data warehouse
- The other function that loads the transformed data frames from the staging area into the data warehouse, establishing the connection to the database engine we are using, in this case, MySQL.

---

## Data quality assumptions

Regarding data quality, we found no null, outlier, or negative data in the EDA. Therefore, we assume the following from the raw CSV data:

- First name, Last name, email, country, seniority, and technology are strings and are not null.

- Application date is a string, but it is converted to a date type during transformation and is not null.

- YOE, Code Challenge Score, and Technical Interview Score are integers and are not null.

- Hired flag is a boolean (true or false) calculated from the Code Challenge Score and Technical Interview Score.

---

##  How to run the project

To run this project, you must download the repository from GitHub. Inside the main folder, you will find a folder called sql. Inside this folder, there will be a script called create_tables.sql. This script creates the star schema data warehouse (DW). Ideally, it should be run in a MySQL environment.

Once the DW has been created, you will execute the entire ETL pipeline. You can do this using Visual Studio Code and select the folder if you downloaded it, or simply clone the repository. Once the folder is selected, you must change the paths on your computer and your database credentials (username and password).

Install dependencies:
```
pip install -r requirements.txt
```

Once everything is configured on your computer, you must run the main file, which orchestrates the entire project. Once executed, main will call the ETL process functions and execute the pipeline, from extraction and transformation to finally loading the data into the DW.


---

## Example Outputs

Fact table:
<img width="1893" height="742" alt="Captura de pantalla 2026-02-27 215459" src="https://github.com/user-attachments/assets/422672e6-1e8a-491b-b901-6d7b11650bde" />

Candidate dimension:
<img width="1151" height="737" alt="Captura de pantalla 2026-02-27 215542" src="https://github.com/user-attachments/assets/c0876365-d984-4f4e-a9aa-90b68f271fd3" />

 ### Some SQL queries from the DW

- Hired by Technology
 ```
SELECT 
    dt.technology AS cargo,
    COUNT(*) AS contratados
FROM fact_application fa
JOIN dim_technology dt ON fa.technology_key = dt.technology_key
WHERE fa.hired_flag = TRUE
GROUP BY dt.technology
ORDER BY contratados DESC;
```
<img width="1917" height="1021" alt="Captura de pantalla 2026-02-27 220016" src="https://github.com/user-attachments/assets/ef79f22b-111e-40ea-8c3d-c403acbe0b25" />


- Hired by Country over Years
```
SELECT 
    dc.country AS pais,
    COUNT(*) AS contratados
FROM fact_application fa
JOIN dim_country dc ON fa.country_key = dc.country_key
WHERE fa.hired_flag = TRUE
    AND dc.country IN ('Colombia', 'Brazil', 'United States of America', 'Ecuador')
GROUP BY dc.country
ORDER BY contratados DESC;
```
<img width="1913" height="770" alt="Captura de pantalla 2026-02-27 220225" src="https://github.com/user-attachments/assets/48b0ed02-39c5-46f3-b832-e3ddc9fea5eb" />

## How to connect Power BI file with the DW (ODBC Connection)

This project consumes the Data Warehouse from Power BI through an ODBC Data Source Name (DSN) configured with the MySQL ODBC driver.

- You must to download the NET and the Unicode Driver
- Open the Data Sources (64-bit) in Windows
- Go to the System DSN
- Click add
- Select MySQL Unicode Driver (9.6 in this case the most recently)
- Configure with this following steps:
  
    - Data source name: Workshop1
    - Port: 3306
    - TCP/IP Server: localhost
    - User: <your_MySQL_Workbench_user>
    - Password: <your_password>
    - Database: workshop1
  
- Click test
- Click OK to save DNS


The repository contains the PowerBI report to run in your PC. Follow the steps below to connect it to your local Data Warehouse after cloning the project.

Locate the file:
- etl_workshop_01/KPI_workshop1.pbix

Open it with Power BI and update Data Source Credentials
- In Power BI go to: Home → Transform Data → Data Source Settings
- Select the ODBC source
- Click Edit Permissions
- Enter your MySQL credentials if prompted
- Confirm that the DSN used is: Workshop1

Refresh the dataset and you will see:

- Hires by Technology
- Hires by Year
- Hires by Country over Years
- Hired by Seniority
- Top 10 Average code and technical score by Technology
- Hired by Age range

## KPI examples
<img width="1267" height="714" alt="Workshop KPI 1" src="https://github.com/user-attachments/assets/068d5301-5157-464e-bfbe-7bc8ca7a85d5" />

<img width="1267" height="711" alt="Workshop KPI 2" src="https://github.com/user-attachments/assets/c7d5ac06-a621-4424-8f39-a9219ef3a6c2" />

<img width="1270" height="712" alt="Workshop KPI 3" src="https://github.com/user-attachments/assets/5206fb38-2831-4044-808d-29f7bf017240" />

<img width="1270" height="712" alt="Workshop KPI 4" src="https://github.com/user-attachments/assets/909cf91e-aef7-4fd8-a251-ee659a3dc4d7" />

