import telebot
import requests
import random

# توكن البوت
token = '7114988330:AAEQsH4aGF5sEMbtWcQgUJB5XoDgM6tpOyY'

# رابط API لجلب كل الآيات
all_ayahs_url = 'https://api.alquran.cloud/v1/ayah/{}'

# إنشاء كائن البوت
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id

    try:
        # جلب اقتباس قرآني
        quote = get_quran_quote()
        # إرسال الاقتباس للمستخدم
        bot.send_message(chat_id, quote)
    except Exception as e:
        bot.send_message(chat_id, f"Error: {e}")

def get_quran_quote():
    try:
        random_ayah_number = random.randint(1, 6236)  # عدد الآيات في القرآن الكريم
        response = requests.get(all_ayahs_url.format(random_ayah_number))
        if response.status_code == 200:
            quote_data = response.json()
            if 'data' in quote_data:
                ayah_text = quote_data['data']['text']
                surah_name = quote_data['data']['surah']['englishName']
                ayah_number = quote_data['data']['numberInSurah']
                return f"{ayah_text} - [{surah_name}: {ayah_number}]"
            else:
                return "Error: Unexpected response structure."
        else:
            return f"Error fetching quote, status code: {response.status_code}"
    except json.JSONDecodeError:
        return "Error: Failed to decode JSON"
    except Exception as e:
        return f"Error: {e}"

# بدء البوت
bot.polling()