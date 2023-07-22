# SEC API Wrapper in Python

This repository contains a Python wrapper for interacting with the SEC (Securities and Exchange Commission) API. The SEC API provides access to various financial data related to companies registered with the SEC.
This code allows downloading the JSON file provided by the SEC and formatting to a Pandas DataFrame.

## Methods

### get_companytickers

Get the company CIK, tickers and company title from the SEC.

```python
  SEC_API.get_companytickers()
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `parse_cik` | `bool` | Get CIK in CIK########## format if True instead as integer numbers. |

#### Returns:
- `pd.DataFrame`: A DataFrame containing the company ticker data.


### get_submissions

Get entity’s current filing history for a specific SEC company.

```python
  SEC_API.get_companysubmissions(cik: str, header_email: str)
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `cik` | `string` | The CIK (Central Index Key) of the company. Format: CIK##########. |
| `header_email` | `string` | The email to be used as a User-Agent header in the HTTP request. |


### get_companyconcepts

Get company concepts (a taxonomy and tag) for a specific SEC company.

```python
  SEC_API.get_companyconcept(cik: str, header_email: str, taxonomy: str, tag: str)
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `cik` | `string` | The CIK (Central Index Key) of the company. Format: CIK##########. |
| `header_email` | `string` | The email to be used as a User-Agent header in the HTTP request. |
| `taxonomy` | `string` | The taxonomy of the frames (e.g. "us-gaap"). |
| `tag` | `string` | The tag of the frame (e.g. "Assets"). |

#### Returns:
- `pd.DataFrame`: A DataFrame containing frames data.


### get_companyfacts

Get concepts facts data for a specific SEC company.

```python
  SEC_API.get_companyfacts(cik: str, header_email: str)
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `cik` | `string` | The CIK (Central Index Key) of the company. Format: CIK##########. |
| `header_email` | `string` | The email to be used as a User-Agent header in the HTTP request. |

#### Returns:
- `pd.DataFrame`: A DataFrame containing frames data.


### get_frames

Get facts for each reporting entity that is last filed that most closely fits the calendrical period requested. Supports for annual, quarterly and instantaneous data.

```python
  SEC_API.get_frames(header_email: str, taxonomy: str, tag: str, units: str, period: str)
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `header_email` | `string` | The email to be used as a User-Agent header in the HTTP request. |
| `taxonomy` | `string` | The taxonomy of the frames (e.g. "us-gaap"). |
| `tag` | `string` | The tag of the frame (e.g. "Assets"). |
| `units` | `string` | The units of the frames (e.g. "USD" or "shares"). |
| `period` | `string` | The period of the frames (e.g. ""CY2019Q1I""). |

#### Returns:
- `pd.DataFrame`: A DataFrame containing frames data.

## Usage/Examples

```python
from SEC_API import SEC_API

# Get all company tickers
df_tickers = SEC_API.get_companytickers(parse_cik = True)
df_tickers.to_csv("./Tickers.csv", index=False)

# Get filing history from Apple Inc. (CIK0000320193)
df_submissions = SEC_API.get_companysubmissions(cik="CIK0000320193, header_email="youremail@email.com")
df_submissions.to_csv("./AccountsPayable Concepts.csv", index=False)

# Get all AccountsPayableCurrent from Apple Inc. (CIK0000320193)
df_concepts = SEC_API.get_companyconcepts(cik="CIK0000320193", header_email="youremail@email.com", taxonomy="us-gaap", tag="AccountsPayableCurrent")
df_concepts.to_csv("./AccountsPayable Concepts.csv", index=False)

# Get all company facts from Apple Inc. (CIK0000320193)
df_facts = SEC_API.get_companyfacts(cik="CIK0000320193", header_email="youremail@email.com")
df_facts.to_csv("./CIK0000320193 Facts.csv", index=False)

# Get all Assets for every company in 2023 Q1
df_frames = SEC_API.get_frames(header_email="youremail@email.com", taxonomy="us-gaap", tag="Assets", units="USD", period="CY2023Q1I")
df_frames.to_csv("./Assets 2023 Q1.csv", index=False)
```

## More
More details can be found on the official SEC API documentation: https://www.sec.gov/edgar/sec-api-documentation
