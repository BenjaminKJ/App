import streamlit as st
import pandas as pd
import requests

st.title("Adresseopslag")

st.write("Søg efter en adresse via Dataforsyningen API")

vejnavn = st.text_input("Vejnavn", "Eliasgade")
husnr = st.text_input("Husnummer", "2B")
postnr = st.text_input("Postnummer", "2300")
etage = st.text_input("Etage", "st")
side = st.text_input("Side", "tv")

if st.button("Søg adresse"):
    url = "https://api.dataforsyningen.dk/adresser"

    params = {
        "vejnavn": vejnavn,
        "husnr": husnr,
        "postnr": postnr
    }

    if etage:
        params["etage"] = etage

    if side:
        params["dør"] = side

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        if data:
            df = pd.json_normalize(data)

            st.success(f"Fandt {len(df)} adresse(r)")
            st.dataframe(df)

            if "adressebetegnelse" in df.columns:
                st.subheader("Adresse")
                st.write(df["adressebetegnelse"].iloc[0])

            if "adgangsadresse.adgangspunkt.koordinater" in df.columns:
                st.subheader("Koordinater")
                st.write(df["adgangsadresse.adgangspunkt.koordinater"].iloc[0])
        else:
            st.warning("Ingen adresser fundet")
    else:
        st.error(f"Fejl fra API: {response.status_code}")
