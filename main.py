import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

TOKEN = "9119631795:AAF05DD13aLhtmN5wE-1Q9tuIMskQ5Q5dV0"
bot = telebot.TeleBot(TOKEN)

CHANNEL_USERNAME = "@weq_zxber"
GROUP_USERNAME = "@weq_sohbet"
ADMIN_ID = 0  

def check_membership(user_id):
    try:
        channel_status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if channel_status not in ['member', 'administrator', 'creator']:
            return False
        return True
    except Exception as e:
        print(f"Hata: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 WEQ Kanal", url=f"https://t.me/weq_zxber"))
    markup.add(InlineKeyboardButton("💬 WEQ Sohbet Grubu", url=f"https://t.me/weq_sohbet"))
    markup.add(InlineKeyboardButton("✅ Katıldım, kontrol et", callback_data="check_join"))

    welcome_text = (
        "Selam, hoş geldin!\n\n"
        "Bu botu başlattığın için teşekkür ederim.\n"
        "Burası, **WEQ - S** dünyasına açılan kapın.\n\n"
        "Kanalıma ve sohbet grubuma katılarak topluluğun bir parçası olabilir, sohbete dahil olabilirsin.\n\n"
        "Bu botun iki temel amacı vardır:\n"
        "⚙️ **① Topluluğu bir araya getirmek** ve iletişim kurabileceğimiz bir ortam oluşturmak.\n\n"
        "🛠️ **② Dijital Sistemler ve Geliştirme:** Sıfırdan geliştirilen Telegram botları, otomasyon sistemleri ve Termux üzerinde çalışan özel siber güvenlik / pratik araç (tool) projelerini tek bir çatı altında toplamak, geliştirmek ve topluluğun kullanımına sunmak."
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    
    if call.data == "check_join":
        is_member = check_membership(user_id)
        
        if is_member:
            bot.answer_callback_query(call.id, "Tebrikler, katılım onaylandı!")
            
            menu_markup = InlineKeyboardMarkup()
            menu_markup.add(InlineKeyboardButton("🛠️ Tool 1: Bilgi Toplama Aracı", callback_data="tool_1"))
            menu_markup.add(InlineKeyboardButton("⚡ Tool 2: Otomatik Bot Taslağı", callback_data="tool_2"))
            menu_markup.add(InlineKeyboardButton("🚀 Tool 3: Termux Performans Aracı", callback_data="tool_3"))
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🎉 Kanallara katılımın doğrulandı! Aşağıdaki menüden dilediğin tool'u seçebilirsin:",
                reply_markup=menu_markup
            )
        else:
            bot.answer_callback_query(call.id, "❌ Henüz kanallara katılmamış görünüyorsun!", show_alert=True)

    elif call.data.startswith("tool_"):
        tool_names = {
            "tool_1": "Tool 1: Bilgi Toplama Aracı",
            "tool_2": "Tool 2: Otomatik Bot Taslağı",
            "tool_3": "Tool 3: Termux Performans Aracı"
        }
        selected_tool = tool_names.get(call.data, "Bilinmeyen Tool")
        
        bot.answer_callback_query(call.id, "Talebin alındı!")
        bot.send_message(
            call.message.chat.id,
            f"✅ Talebin Alındı! Seçtiğin araç ({selected_tool}) yöneticiye bildirildi. En kısa sürede dönüş sağlanacaktır."
        )

# Bağlantı kopmalarına karşı korumalı yeniden bağlanma döngüsü
print("WEQ Bot aktif ve çalışıyor (Auto-Reconnect aktif)...")
while True:
    try:
        bot.infinity_polling(none_stop=True, interval=0, timeout=20, long_polling_timeout=20)
    except Exception as e:
        print(f"Bağlantı koptu, yeniden bağlanılıyor... Hata: {e}")
        time.sleep(3)
  
