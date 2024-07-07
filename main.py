from loader import bot
from handlers import special, default
from handlers.default import empty
from telebot.custom_filters import StateFilter


bot.add_custom_filter(StateFilter(bot))
bot.infinity_polling()
