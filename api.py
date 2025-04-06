import requests
import json
session = requests.Session()

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
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"فشل الحصول على التوكن: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"خطأ في get_access_token: {e}")
        return None

def thread1(quota, member1, access_token, number):
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
        if str(response.json()) == "{}":
            with open("a1.text", "w") as f:
                f.write(str(response.json()) + str(quota))
    except Exception as e:
        print(f"خطأ في thread1: {e}")

def thread2(quota, member2, access_token, number):
    url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
    headers = {
        "Host": "web.vodafone.com.eg",
        "Connection": "keep-alive",
        "msisdn": number,
        "Accept-Language": "AR",
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "clientId": "WebsiteConsumer",
        "Origin": "https://web.vodafone.com.eg",
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
        if str(response.json()) == "{}":
            with open("a2.text", "w") as f:
                f.write(str(response.json()) + str(quota))
    except Exception as e:
        print(f"خطأ في thread2: {e}")