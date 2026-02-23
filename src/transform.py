import pandas as pd

# Dim date
def create_dim_date(df):

    df["application_date"] = pd.to_datetime(df["application_date"])

    df["date_key"] = df["application_date"].dt.strftime("%Y%m%d").astype(int)

    dim_date = df[["date_key", "application_date"]].drop_duplicates().copy()

    dim_date["year"] = dim_date["application_date"].dt.year
    dim_date["month"] = dim_date["application_date"].dt.month
    dim_date["day"] = dim_date["application_date"].dt.day

    dim_date.rename(columns={"application_date": "full_date"}, inplace=True)

    dim_date = dim_date[["date_key", "month", "day", "year", "full_date"]]

    return dim_date


# Create dims seniority, country, technology
def create_dimension(df, column_name, key_name):

    dim = df[[column_name]].drop_duplicates().reset_index(drop=True)

    dim[key_name] = dim.index + 1

    dim = dim[[key_name, column_name]]

    return dim



# Dim candidate
def create_dim_candidate(df):

    dim_candidate = df[["first_name", "last_name", "email"]] \
        .drop_duplicates().reset_index(drop=True)

    dim_candidate["candidate_key"] = dim_candidate.index + 1

    dim_candidate = dim_candidate[
        ["candidate_key", "first_name", "last_name", "email"]
    ]

    return dim_candidate



# Fact table
def create_fact_table(df,
                      dim_country,
                      dim_seniority,
                      dim_technology,
                      dim_candidate):

    df = df.merge(dim_country, on="country", how="left")
    df = df.merge(dim_seniority, on="seniority", how="left")
    df = df.merge(dim_technology, on="technology", how="left")
    df = df.merge(dim_candidate,
                  on=["first_name", "last_name", "email"],
                  how="left")

    df["hired_flag"] = (
        (df["code_challenge_score"] >= 7) &
        (df["technical_interview_score"] >= 7)
    ).astype(bool)

    fact_application = df[[
        "code_challenge_score",
        "technical_interview_score",
        "yoe",
        "hired_flag",
        "country_key",
        "candidate_key",
        "technology_key",
        "seniority_key",
        "date_key"
    ]].copy()

    return fact_application


# Transform complete
def transform_data(df):

    dim_date = create_dim_date(df)

    dim_country = create_dimension(df, "country", "country_key")
    dim_seniority = create_dimension(df, "seniority", "seniority_key")
    dim_technology = create_dimension(df, "technology", "technology_key")

    dim_candidate = create_dim_candidate(df)

    fact_application = create_fact_table(
        df,
        dim_country,
        dim_seniority,
        dim_technology,
        dim_candidate
    )

    return {
        "dim_date": dim_date,
        "dim_country": dim_country,
        "dim_seniority": dim_seniority,
        "dim_technology": dim_technology,
        "dim_candidate": dim_candidate,
        "fact_application": fact_application
    }