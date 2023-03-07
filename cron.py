base_url = 'https://api.telegram.org/bot{token}'


async def send_message(chat_id, text, reply_markup=None, parse_mode=None, disable_web_page_preview=None):
    ...


async def send_photo(chat_id, photo, reply_markup=None, caption=None, parse_mode=None, disable_web_page_preview=None):
    ...


async def edit_message_text(chat_id, message_id, text, reply_markup=None, parse_mode=None,
                            disable_web_page_preview=None):
    ...
