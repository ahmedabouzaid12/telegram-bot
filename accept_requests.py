import requests
import asyncio
import time

async def execute_accept_requests(user_data, context):
    family_owners_number = user_data['family_owners_number']
    family_owners_password = user_data['family_owners_password']
    member0 = user_data['member0']  # جديد
    member0_password = user_data['member0_password']  # جديد
    member1 = user_data['member1']
    member1_password = user_data['member1_password']
    member2 = user_data['member2']
    member2_password = user_data['member2_password']

    def get_access_token_member1():
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
            "username": member1,
            "password": member1_password,
            "grant_type": "password",
            "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
            "client_id": "my-vodafone-app"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, data=data, timeout=10)
                return response.json()["access_token"]
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    time.sleep(2)
                    continue
                return {"error": f"فشل الحصول على توكن الفرد الأول: {str(e)}"}

    def get_access_token_member2():
        url = "https://mobile.vodafone.com.eg/auth/realms/vf-realm/protocol/openid-connect/token"
        headers = {
            "x-dynatrace": "MT_3_8_2164993384_64-0_a556db1b-4506-43f3-854a-1d2527767923_0_1080_235",
            "x-agent-operatingsystem": "1601266300",
            "clientId": "AnaVodafoneAndroid",
            "x-agent-device": "RMX1851",
            "x-agent-version": "2021.12.2",
            "x-agent-build": "493",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.1"
        }
        data = {
            "username": member2,
            "password": member2_password,
            "grant_type": "password",
            "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
            "client_id": "my-vodafone-app"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, data=data, timeout=10)
                return response.json()["access_token"]
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    time.sleep(2)
                    continue
                return {"error": f"فشل الحصول على توكن الفرد الثاني: {str(e)}"}

    access_token1 = get_access_token_member1()
    if isinstance(access_token1, dict) and "error" in access_token1:
        return access_token1

    access_token2 = get_access_token_member2()
    if isinstance(access_token2, dict) and "error" in access_token2:
        return access_token2

    async def accept_member1():
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        headers = {
            "api-host": "ProductOrderingManagement",
            "useCase": "MIProfile",
            "Authorization": f"Bearer {access_token1}",
            "api-version": "v2",
            "x-agent-operatingsystem": "9",
            "clientId": "AnaVodafoneAndroid",
            "x-agent-device": "Xiaomi Redmi 6A",
            "x-agent-version": "2024.3.2",
            "x-agent-build": "592",
            "msisdn": member1,
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
            "name": "FlexFamily",
            "parts": {
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": family_owners_number}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": member1}], "type": "Member"}
                ]
            },
            "type": "AcceptInvitation"
        }
        for attempt in range(3):
            try:
                response = requests.patch(url, headers=headers, json=data, timeout=10)
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(2)
                    continue
                return {"error": f"فشل قبول دعوة الفرد الأول: {str(e)}"}

    async def accept_member2():
        url = "https://mobile.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        headers = {
            "Host": "web.vodafone.com.eg",
            "Connection": "keep-alive",
            "msisdn": member2,
            "Accept-Language": "AR",
            "sec-ch-ua-mobile": "?1",
            "Authorization": f"Bearer {access_token2}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "clientId": "WebsiteConsumer",
            "Origin": "https://web.vodafone.com.eg",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web.vodafone.com.eg/spa/familySharing/invitation",
            "Accept-Encoding": "gzip, deflate, br, zstd"
        }
        data = {
            "name": "FlexFamily",
            "type": "AcceptInvitation",
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "parts": {
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": family_owners_number}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": member2}], "type": "Member"}
                ]
            }
        }
        for attempt in range(3):
            try:
                response = requests.patch(url, headers=headers, json=data, timeout=10)
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(2)
                    continue
                return {"error": f"فشل قبول دعوة الفرد الثاني: {str(e)}"}

    try:
        result1 = await accept_member1()
        if "error" in result1:
            return result1

        await asyncio.sleep(2)
        result2 = await accept_member2()

        if "error" in result2:
            return result2

        return {
            "accept_result1": result1,
            "accept_result2": result2
        }
    except Exception as e:
        return {"error": str(e)}