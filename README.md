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

## 🗂️ Dimensional Model — Star Schema

This star schema dimensional model was designed because the core business objective is the application of candidates to a company. The fact table should contain information about the scores obtained on the company's tests, the years of experience of each applicant, and their suitability for the job.

The dimensions use surrogate keys to relate to the fact table. These dimensions are the descriptive attributes of each applicant. This allows us to know their personal information, country of origin, profession, seniority levels, and the date they applied to the company. Including a time dimension facilitates historical trend analysis using KPIs.

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

## ⚙️ ETL Logic

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
In progress...

---

## 🚀 How to run the project

To run this project, you must download the repository from GitHub. Inside the main folder, you will find a folder called sql. Inside this folder, there will be a script called create_tables.sql. This script creates the star schema data warehouse (DW). Ideally, it should be run in a MySQL environment.

Once the DW has been created, you will execute the entire ETL pipeline. You can do this using Visual Studio Code and select the folder if you downloaded it, or simply clone the repository. Once the folder is selected, you must change the paths on your computer and your database credentials (username and password).

Once everything is configured on your computer, you must run the main file, which orchestrates the entire project. Once executed, main will call the ETL process functions and execute the pipeline, from extraction and transformation to finally loading the data into the DW.
