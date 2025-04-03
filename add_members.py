import requests
import asyncio
import time

async def execute_vodafone_operations(user_data, context):
    quota = 10
    family_owners_number = user_data['family_owners_number']
    family_owners_password = user_data['family_owners_password']
    member0 = user_data['member0']
    member1 = user_data['member1']
    member2 = user_data['member2']
    
    def get_access_token():
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
            "username": family_owners_number,
            "password": family_owners_password,
            "grant_type": "password",
            "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
            "client_id": "my-vodafone-app"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, data=data, timeout=30)  
                return response.json()["access_token"]
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    time.sleep(2)
                    continue
                return {"error": f"فشل الاتصال بسيرفر فودافون: {str(e)}"}
    
    access_token = get_access_token()
    if isinstance(access_token, dict) and "error" in access_token:
        return access_token
    
    async def add_member1():
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
            "msisdn": family_owners_number,
            "Accept": "application/json",
            "Accept-Language": "ar",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "mobile.vodafone.com.eg",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.11.0"
        }
        data = {
            "category": [
                {"listHierarchyId": "PackageID", "value": "523"},
                {"listHierarchyId": "TemplateID", "value": quota},
                {"listHierarchyId": "TierID", "value": "523"}
            ],
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [
                        {"characteristicName": "quotaDist1", "type": "percentage", "value": quota}
                    ]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": family_owners_number}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": member1}], "type": "Member"}
                ]
            },
            "type": "SendInvitation"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)  
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(2)
                    continue
                return {"error": f"فشل إضافة الفرد الأول: {str(e)}"}
    
    async def add_member2():
        url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        headers = {
            "Host": "web.vodafone.com.eg",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            "msisdn": family_owners_number,
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
        data = {
            "category": [
                {"listHierarchyId": "PackageID", "value": "523"},
                {"listHierarchyId": "TemplateID", "value": quota},
                {"listHierarchyId": "TierID", "value": "523"}
            ],
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [
                        {"characteristicName": "quotaDist1", "type": "percentage", "value": quota}
                    ]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": family_owners_number}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": member2}], "type": "Member"}
                ]
            },
            "type": "SendInvitation"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)  
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(2)
                    continue
                return {"error": f"فشل إضافة الفرد الثاني: {str(e)}"}
    
    try:
        result1 = await add_member1()
        if "error" in result1:
            return {"add_result1": result1}
        
        await asyncio.sleep(10)  
        result2 = await add_member2()
        
        return {
            "add_result1": result1,
            "add_result2": result2
        }
    except Exception as e:
        return {"error": str(e)}