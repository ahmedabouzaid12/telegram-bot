import requests
import asyncio
import time

async def execute_break_percentage(user_data, context):
    family_owners_number = user_data['family_owners_number']
    family_owners_password = user_data['family_owners_password']
    member0 = user_data['member0']
    member1 = user_data['member1']
    member2 = user_data['member2']
    quota = 40  # النسبة الافتراضية
    attempts = user_data.get('attempts', 30)  # عدد المحاولات (إفتراضي 30 إذا لم يتم تحديده)

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
                response = requests.post(url, headers=headers, data=data, timeout=10)
                return response.json()["access_token"]
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    time.sleep(2)
                    continue
                return {"error": f"فشل الحصول على توكن صاحب العيلة: {str(e)}"}

    access_token = get_access_token()
    if isinstance(access_token, dict) and "error" in access_token:
        return access_token

    async def redistribute_quota_member1(quota_value):
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
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "createdBy": {"value": "MobileApp"},
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": quota_value}]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": family_owners_number}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": member1}], "type": "Member"}
                ]
            },
            "type": "QuotaRedistribution"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(2)
                    continue
                return {"error": f"فشل توزيع النسبة للفرد الأول: {str(e)}"}

    async def redistribute_quota_member2(quota_value):
        url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        headers = {
            "Host": "web.vodafone.com.eg",
            "Connection": "keep-alive",
            "msisdn": family_owners_number,
            "Accept-Language": "AR",
            "sec-ch-ua-mobile": "?1",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "clientId": "WebsiteConsumer",
            "Origin": "https://web.vodafone.com.eg",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://web.vodafone.com.eg/spa/familySharing/manageFamily",
            "Accept-Encoding": "gzip, deflate, br, zstd"
        }
        data = {
            "category": [{"listHierarchyId": "TemplateID", "value": "47"}],
            "createdBy": {"value": "MobileApp"},
            "parts": {
                "characteristicsValue": {
                    "characteristicsValue": [{"characteristicName": "quotaDist1", "type": "percentage", "value": quota_value}]
                },
                "member": [
                    {"id": [{"schemeName": "MSISDN", "value": family_owners_number}], "type": "Owner"},
                    {"id": [{"schemeName": "MSISDN", "value": member2}], "type": "Member"}
                ]
            },
            "type": "QuotaRedistribution"
        }
        for attempt in range(3):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=10)
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(2)
                    continue
                return {"error": f"فشل توزيع النسبة للفرد الثاني: {str(e)}"}

    try:
        # توزيع النسبة لـ member0 أولاً
        result0 = await redistribute_quota_member1(quota)
        if "error" in result0:
            return result0

        await asyncio.sleep(9)

        # كسر النسبة لـ member1 و member2
        for _ in range(attempts):  # استخدام عدد المحاولات المحدد من اليوزر
            result1 = await redistribute_quota_member1(10)
            if "error" in result1:
                return result1

            await asyncio.sleep(9)

            result2 = await redistribute_quota_member2(10)
            if "error" in result2:
                return result2

            await asyncio.sleep(8)

            result1_final = await redistribute_quota_member1(quota)
            if "error" in result1_final:
                return result1_final

            result2_final = await redistribute_quota_member2(quota)
            if "error" in result2_final:
                return result2_final

            if str(result1_final) == "{}" and str(result2_final) == "{}":
                break

        return {
            "break_result1": result1_final,
            "break_result2": result2_final,
            "attempts_used": attempts  # إرجاع عدد المحاولات المستخدمة
        }
    except Exception as e:
        return {"error": str(e)}