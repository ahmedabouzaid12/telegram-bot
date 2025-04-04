import requests
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

async def execute_break_percentage(user_data, context):
    family_owners_number = user_data['family_owners_number']
    family_owners_password = user_data['family_owners_password']
    member1 = user_data['member1']
    member1_password = user_data['member1_password']
    member2 = user_data['member2']
    member2_password = user_data['member2_password']
    quota = 40
    attempts = user_data.get('attempts', 30)

    await context.bot.send_message(
        chat_id=context._chat_id,
        text="🚀 بدء عملية كسر النسبة...\n⏳ جاري التحضير..."
    )

    # استخدام Session للحفاظ على الاتصال
    session = requests.Session()

    def get_access_token(username, password):
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
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_secret": "a2ec6fff-0b7f-4aa4-a733-96ceae5c84c3",
            "client_id": "my-vodafone-app"
        }
        for attempt in range(3):
            try:
                response = session.post(url, headers=headers, data=data, timeout=60)
                response.raise_for_status()
                json_response = response.json()
                if "access_token" in json_response:
                    return json_response["access_token"]
                else:
                    return {"error": "السيرفر رجع استجابة بدون توكن!"}
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    time.sleep(5)
                    continue
                return {"error": f"انتهى وقت الطلب للسيرفر بعد 3 محاولات: {str(e)}"}
            except requests.RequestException as e:
                return {"error": f"خطأ في الطلب: {str(e)}"}

    # الحصول على التوكنز
    access_token = get_access_token(family_owners_number, family_owners_password)
    if isinstance(access_token, dict) and "error" in access_token:
        await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل الحصول على توكن صاحب العيلة: {access_token['error']}")
        return access_token

    access_token_member1 = get_access_token(member1, member1_password)
    if isinstance(access_token_member1, dict) and "error" in access_token_member1:
        await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل الحصول على توكن الفرد الأول: {access_token_member1['error']}")
        return access_token_member1

    access_token_member2 = get_access_token(member2, member2_password)
    if isinstance(access_token_member2, dict) and "error" in access_token_member2:
        await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل الحصول على توكن الفرد الثاني: {access_token_member2['error']}")
        return access_token_member2

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
            "Accept": "application/json",  # السطر المصحح
            "Accept-Language": "ar",
            "Content-Type": "application/json; charset=UTF-8",
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
                response = session.post(url, headers=headers, json=data, timeout=60)
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(5)
                    continue
                return {"error": f"انتهى وقت الطلب للفرد الأول: {str(e)}"}

    async def redistribute_quota_member2(quota_value):
        url = "https://web.vodafone.com.eg/services/dxl/cg/customerGroupAPI/customerGroup"
        headers = {
            "Host": "web.vodafone.com.eg",
            "Connection": "keep-alive",
            "msisdn": family_owners_number,
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
                response = session.post(url, headers=headers, json=data, timeout=60)
                return response.json()
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < 2:
                    await asyncio.sleep(5)
                    continue
                return {"error": f"انتهى وقت الطلب للفرد الثاني: {str(e)}"}

    await context.bot.send_message(chat_id=context._chat_id, text=f"🔁 بدء {attempts} محاولة لكسر النسبة...")
    success = False
    attempts_used = 0
    last_result1 = None
    last_result2 = None

    for attempt in range(1, attempts + 1):
        await context.bot.send_message(chat_id=context._chat_id, text=f"🔄 جاري المحاولة رقم {attempt} من {attempts}...")

        # توزيع 10% للفرد الأول
        result1 = await redistribute_quota_member1(10)
        if "error" in result1:
            await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل توزيع 10% للفرد الأول: {result1['error']}")
            continue
        await asyncio.sleep(9)  # تأخير زي الكود اليدوي

        # توزيع 10% للفرد الثاني
        result2 = await redistribute_quota_member2(10)
        if "error" in result2:
            await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل توزيع 10% للفرد الثاني: {result2['error']}")
            continue
        await asyncio.sleep(9)

        # إعادة توزيع 40% للفرد الأول
        result1_final = await redistribute_quota_member1(quota)
        if "error" in result1_final:
            await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل إعادة 40% للفرد الأول: {result1_final['error']}")
            continue
        await asyncio.sleep(8)

        # إعادة توزيع 40% للفرد الثاني
        result2_final = await redistribute_quota_member2(quota)
        if "error" in result2_final:
            await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل إعادة 40% للفرد الثاني: {result2_final['error']}")
            continue

        # التحقق من النجاح بنفس طريقة الكود اليدوي
        combined_result = str(result1_final_AR) + str(quota) + str(result2_final) + str(quota)
        if combined_result == "{}40{}40":
            await context.bot.send_message(chat_id=context._chat_id, text=f"✅ المحاولة رقم {attempt} نجحت!")
            success = True
            attempts_used = attempt
            break
        else:
            await context.bot.send_message(chat_id=context._chat_id, text=f"❌ المحاولة رقم {attempt} فشلت! النتيجة: {combined_result}")
        last_result1 = result1_final
        last_result2 = result2_final

    if success:
        await context.bot.send_message(chat_id=context._chat_id, text="🎉 تم كسر النسبة بنجاح!")
        return {"break_result1": last_result1, "break_result2": last_result2, "attempts_used": attempts_used}
    else:
        await context.bot.send_message(chat_id=context._chat_id, text=f"❌ فشل كسر النسبة بعد {attempts} محاولة!")
        return {"break_result1": last_result1, "break_result2": last_result2, "attempts_used": attempts}