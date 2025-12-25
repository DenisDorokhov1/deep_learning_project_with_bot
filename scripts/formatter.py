def format_answer(result: dict) -> str:
    return (
        f"🏛 <b>{result['name']}</b>\n\n"
        f"📍 <b>Адрес:</b> {result['address']}\n"
        f"🏗 <b>Архитектор:</b> {result['architect']}\n"
        f"🎨 <b>Стиль:</b> {result['style']}\n"
        f"📅 <b>Год:</b> {result['year']}\n\n"
        f"🔍 <b>Уверенность:</b> {result['score']:.2f}"
    )
