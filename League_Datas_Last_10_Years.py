# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:09:32 2024

@author: DTYYILDIZ
"""

import requests
import pandas as pd
from pandas import json_normalize
import json

def get_token(auth_url, username, password):
    
    payload = {
        'grant_type': 'password',
        'username': username,
        'password': password,
    }
    try:
        response = requests.post(auth_url, data=payload)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Token alınamadı: {e}")
        return None
    
def get_fixture(token, url):
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Veri alınamadı: {e}")
        return None

def main():
    auth_url = 'XXXXXXXXX'
    username = 'XXXXXXXXX'
    password = 'XXXXXXXXX'
    fixture_url = 'https://XXXXX/api/fixture/organizationid/130/seasonid/1109'
    
   
    token = get_token(auth_url, username, password)
    if token:
        
        data = get_fixture(token, fixture_url)
        if data:
            print("Yanıt Verisi:", data)
            
            
            df_fixture = json_normalize(data['data'], sep='_')
            
           
            for key, value in data.items():
                if key != 'data':
                    df_fixture[key] = value

            
            columns_to_keep = [
                'round', 'awayTeam_id', 'awayTeam_name', 'homeTeam_id', 'homeTeam_name',
                'score_homeScoreHalf', 'score_awayScoreHalf', 'score_homeScore', 'score_awayScore',
                'season_organization_id', 'season_organization_name', 'season_name'
            ]

            
            df_fixture = df_fixture[columns_to_keep]

            
            print("Sonuç DataFrame'i:")
            print(df_fixture)
            
            
            result=df_fixture
            result.to_excel('C:/Users/DTYYILDIZ/Desktop/MAC_SONUCLARI/Turkiye/tff_tff_birinci_lig_13_14.xlsx',index=False)
        else:
            print("Fixture API'den veri alınamadı.")
    else:
        print("Token alınamadı.")


main()
