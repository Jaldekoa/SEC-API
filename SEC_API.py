import pandas as pd
import numpy as np
import requests


class SEC_API:
    """
    Class for interacting with the SEC (Securities and Exchange Commission) API.
    For more information, about SEC's API visit https://www.sec.gov/edgar/sec-api-documentation.
    """

    def __init__(self):
        pass

    @classmethod
    def get_companytickers(cls, parse_cik: bool = True) -> pd.DataFrame:
        """
        Get the company CIK, tickers and company title from the SEC.

        Args:
            parse_cik (bool): Get CIK in CIK########## format instead as integer numbers.

        Returns:
            pd.DataFrame: A DataFrame containing the company ticker data.
        """
        url = f"https://www.sec.gov/files/company_tickers.json"
        raw_json = requests.get(url).json()

        df = pd.DataFrame.from_records(raw_json).transpose().reset_index(drop=True)
        df.columns = ["cik", "ticker", "title"]

        if parse_cik:
            df["cik"] = "CIK" + df["cik"].astype("str").str.pad(10, fillchar='0')

        return df

    @classmethod
    def get_submissions(cls, cik: str, header_email: str) -> pd.DataFrame:
        """
        Get entity’s current filing history for a specific SEC company.

        Args:
            cik (str): The CIK (Central Index Key) of the company. Format: CIK##########
            header_email (str): The email to be used as a User-Agent header in the HTTP request.


        Returns:
            pd.DataFrame: A DataFrame containing the company concepts data.

        """
        url = f"https://data.sec.gov/submissions/{cik}.json"
        headers = {"User-Agent": header_email}
        raw_json = requests.get(url, headers=headers).json()

        df_list = raw_json["filings"]["recent"]

        return pd.DataFrame.from_records(df_list)

    @classmethod
    def get_companyconcept(cls, cik: str, header_email: str, taxonomy: str, tag: str) -> pd.DataFrame:
        """
        Get company concepts (a taxonomy and tag) for a specific SEC company.

        Args:
            cik (str): The CIK (Central Index Key) of the company. Format: CIK##########
            header_email (str): The email to be used as a User-Agent header in the HTTP request.
            taxonomy (str): The taxonomy of the concepts.
            tag (str): The tag of the concept.

        Returns:
            pd.DataFrame: A DataFrame containing the company concepts data.
        """
        url = f"https://data.sec.gov/api/xbrl/companyconcept/{cik}/{taxonomy}/{tag}.json"
        headers = {"User-Agent": header_email}
        raw_json = requests.get(url, headers=headers).json()

        df_list = [{
            "cik": raw_json["cik"],
            "taxonomy": raw_json["taxonomy"],
            "tag": raw_json["tag"],
            "label": raw_json["label"],
            "description": raw_json["description"],
            "entityName": raw_json["entityName"],
            "units": key_units,
            "end": row_list.get("end", np.nan),
            "val": row_list.get("val", np.nan),
            "accn": row_list.get("accn", np.nan),
            "fy": row_list.get("fy", np.nan),
            "fp": row_list.get("fp", np.nan),
            "form": row_list.get("form", np.nan),
            "filed": row_list.get("filed", np.nan),
            "frame": row_list.get("frame", np.nan)
        }
            for key_units, value_units in raw_json["units"].items()
            for row_list in value_units
        ]

        return pd.DataFrame.from_records(df_list)

    @classmethod
    def get_companyfacts(cls, cik: str, header_email: str) -> pd.DataFrame:
        """
        Get concepts facts data for a specific SEC company.

        Args:
            cik (str): The CIK (Central Index Key) of the company. Format: CIK##########
            header_email (str): The email to be used as a User-Agent header in the HTTP request.

        Returns:
            pd.DataFrame: A DataFrame containing the company facts data.
        """
        url = f"https://data.sec.gov/api/xbrl/companyfacts/{cik}.json"
        headers = {"User-Agent": header_email}
        raw_json = requests.get(url, headers=headers).json()

        df_list = [{
            "cik": raw_json["cik"],
            "entityName": raw_json["entityName"],
            "taxonomy": key_taxonomy,
            "tag": key_tag,
            "label": value_tag["label"],
            "description": value_tag["description"],
            "units": key_units,
            "end": row_list.get("end", np.nan),
            "val": row_list.get("val", np.nan),
            "accn": row_list.get("accn", np.nan),
            "fy": row_list.get("fy", np.nan),
            "fp": row_list.get("fp", np.nan),
            "form": row_list.get("form", np.nan),
            "filed": row_list.get("filed", np.nan),
            "frame": row_list.get("frame", np.nan)
        }
            for key_taxonomy, value_taxonomy in raw_json["facts"].items()
            for key_tag, value_tag in value_taxonomy.items()
            for key_units, value_units in value_tag["units"].items()
            for row_list in value_units
        ]

        return pd.DataFrame.from_records(df_list)

    @classmethod
    def get_frames(cls,  header_email: str, taxonomy: str, tag: str, units: str, period: str) -> pd.DataFrame:
        """
        Get frames for each reporting entity that is last filed that most closely fits the calendrical period requested.
        Supports for annual, quarterly and instantaneous data.

        Args:
            header_email (str): The email to be used as a User-Agent header in the HTTP request.
            taxonomy (str): The taxonomy of the frames.
            tag (str): The tag of the frame.
            units (str): The units of the frames.
            period (str): The period of the frames.

        Returns:
            pd.DataFrame: A DataFrame containing frames data.
        """
        url = f"https://data.sec.gov/api/xbrl/frames/{taxonomy}/{tag}/{units}/{period}.json"
        headers = {"User-Agent": header_email}
        raw_json = requests.get(url, headers=headers).json()

        df_list = [{
            "taxonomy": raw_json["taxonomy"],
            "tag": raw_json["tag"],
            "ccp": raw_json["ccp"],
            "uom": raw_json["uom"],
            "label": raw_json["label"],
            "description": raw_json["description"],
            "accn": row_list.get("accn", np.nan),
            "cik": row_list.get("cik", np.nan),
            "entityName": row_list.get("entityName", np.nan),
            "loc": row_list.get("loc", np.nan),
            "end": row_list.get("end", np.nan),
            "val": row_list.get("val", np.nan)
        }
            for row_list in raw_json["data"]
        ]

        return pd.DataFrame.from_records(df_list)
