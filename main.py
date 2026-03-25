import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8711482972:AAHj8hgs_Sv571J6BdfQP7QzpCqyJIN3VwM"
logging.basicConfig(level=logging.INFO)

# ‚îÄ‚îÄ Detect language ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
def get_lang(update: Update) -> str:
    """Returns 'fr' if user's Telegram language is French, else 'en'"""
    lang = update.effective_user.language_code or "en"
    return "fr" if lang.startswith("fr") else "en"

def t(fr_text: str, en_text: str, lang: str) -> str:
    return fr_text if lang == "fr" else en_text

# ‚îÄ‚îÄ Main Menu ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
def main_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("üìã FAQ", "üìã FAQ", lang),
                              callback_data=f"faq|{lang}"),
         InlineKeyboardButton(t("üíº Nos Services", "üíº Our Services", lang),
                              callback_data=f"services|{lang}")],
        [InlineKeyboardButton(t("üìà Nos R√©sultats", "üìà Our Results", lang),
                              callback_data=f"results|{lang}"),
         InlineKeyboardButton(t("üöÄ Rejoindre l'agence", "üöÄ Join the Agency", lang),
                              callback_data=f"join|{lang}")],
        [InlineKeyboardButton(t("üá¨üáß Switch to English", "üá´üá∑ Passer en Fran√ßais", lang),
                              callback_data=f"switch|{'en' if lang == 'fr' else 'fr'}")],
    ])

def main_text(lang):
    return t(
        "üëã Bienvenue chez Seven Agency üñ§\n\nOn scale tes revenus OnlyFans.\nToi tu cr√©es. On g√®re le reste.\n\nChoisis une option üëá",
        "üëã Welcome to Seven Agency üñ§\n\nWe scale your OnlyFans income.\nYou create. We handle the rest.\n\nChoose an option üëá",
        lang
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(
        main_text(lang),
        reply_markup=main_keyboard(lang),
        parse_mode=None
    )

# ‚îÄ‚îÄ Switch Language ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def switch_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    await query.edit_message_text(
        main_text(lang),
        reply_markup=main_keyboard(lang),
        parse_mode=None
    )

# ‚îÄ‚îÄ Back to Menu ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    await query.edit_message_text(
        main_text(lang),
        reply_markup=main_keyboard(lang),
        parse_mode=None
    )

# ‚îÄ‚îÄ FAQ Menu ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def faq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t("‚ùì Quelle est votre commission ?", "‚ùì What is your commission?", lang), callback_data=f"faq_commission|{lang}")],
        [InlineKeyboardButton(t("‚ùì Je garde le contr√¥le ?", "‚ùì Do I keep control?", lang), callback_data=f"faq_control|{lang}")],
        [InlineKeyboardButton(t("‚ùì R√©sultats en combien de temps ?", "‚ùì How fast will I see results?", lang), callback_data=f"faq_results|{lang}")],
        [InlineKeyboardButton(t("‚ùì Comment √ßa fonctionne ?", "‚ùì How does it work?", lang), callback_data=f"faq_how|{lang}")],
        [InlineKeyboardButton(t("‚ùì C'est gratuit pour commencer ?", "‚ùì Is it free to start?", lang), callback_data=f"faq_free|{lang}")],
        [InlineKeyboardButton(t("üîô Retour", "üîô Back", lang), callback_data=f"menu|{lang}")],
    ])
    await query.edit_message_text(
        t("üìã FAQ ‚Äî Seven Agency\n\nChoisis ta question üëá",
          "üìã FAQ ‚Äî Seven Agency\n\nChoose your question üëá", lang),
        reply_markup=keyboard, parse_mode=None
    )

# ‚îÄ‚îÄ FAQ Answers ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def faq_commission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t("üîô Retour FAQ", "üîô Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t("üí∞ Notre Commission\n\nNotre commission est de 40% des revenus g√©n√©r√©s.\n\nPas de frais cach√©s. Pas de frais fixes.\nOn gagne quand toi tu gagnes. ü§ù",
          "üí∞ Our Commission\n\nOur commission is 40% of the revenue generated.\n\nNo hidden fees. No fixed costs.\nWe earn when you earn. ü§ù", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t("üîô Retour FAQ", "üîô Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t("üîê Tu gardes le contr√¥le total\n\n‚úÖ Tu valides tout le contenu\n‚úÖ Acc√®s √† ton compte √† tout moment\n‚úÖ Tu d√©cides des prix\n‚úÖ Contrat r√©siliable facilement\n\nTon compte reste le tien. üñ§",
          "üîê You Keep Full Control\n\n‚úÖ You approve all content\n‚úÖ Access to your account at all times\n‚úÖ You decide on prices\n‚úÖ Contract easily cancellable\n\nYour account stays yours. üñ§", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t("üîô Retour FAQ", "üîô Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t("üìà R√©sultats en combien de temps ?\n\nEn moyenne 2 √† 4 semaines.\n\nSemaine 1 ‚Üí Analyse du compte\nSemaine 2 ‚Üí Gestion des DMs\nSemaine 3 ‚Üí Marketing lanc√©\nSemaine 4 ‚Üí Premiers r√©sultats üöÄ",
          "üìà How Fast Will I See Results?\n\nOn average 2 to 4 weeks.\n\nWeek 1 ‚Üí Account analysis\nWeek 2 ‚Üí DMs & fan management\nWeek 3 ‚Üí Marketing launched\nWeek 4 ‚Üí First results visible üöÄ", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_how(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t("üîô Retour FAQ", "üîô Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t("‚öôÔ∏è Comment √ßa fonctionne ?\n\nOn s'occupe de tout pour que tu te concentres 100% sur la cr√©ation.\n\nüí¨ Messages & DMs ‚Äî on r√©pond √† tes fans 24h/24 pour maximiser l'engagement\n\nüí∞ Strat√©gie PPV ‚Äî on envoie le bon contenu aux bons fans au bon moment\n\nüì± Marketing ‚Äî on fait grandir ton audience sur Instagram & TikTok\n\nüìä Analytics ‚Äî on suit tes stats et optimise chaque semaine\n\nüîê Protection du contenu ‚Äî ton contenu reste en s√©curit√©\n\nToi tu cr√©es. On g√®re le reste. üñ§",
          "‚öôÔ∏è How Does It Work?\n\nWe take care of everything so you can focus 100% on creating content.\n\nüí¨ Fan Messaging & DMs ‚Äî we reply to your fans 24/7 to maximize engagement\n\nüí∞ PPV Strategy ‚Äî we send the right content to the right fans at the right time\n\nüì± Marketing ‚Äî we grow your audience on Instagram & TikTok\n\nüìä Analytics ‚Äî we track your stats and optimize every week\n\nüîê Content Protection ‚Äî we make sure your content stays safe\n\nYou create. We handle the rest. üñ§", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t("üîô Retour FAQ", "üîô Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t("‚úÖ C'est gratuit pour commencer ?\n\nOui ‚Äî aucun frais fixe.\n\nOn prend uniquement une commission sur les revenus.\nSi on te rapporte rien, on prend rien. ü§ù",
          "‚úÖ Is It Free To Start?\n\nYes ‚Äî no fixed fees.\n\nWe only take a commission on revenue.\nIf we don't make you money, we don't get paid. ü§ù", lang),
        reply_markup=back, parse_mode=None
    )

# ‚îÄ‚îÄ Services ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def services_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t("üîô Retour", "üîô Back", lang), callback_data=f"menu|{lang}")]])
    await query.edit_message_text(
        t("üíº Nos Services\n\nüî¥ Gestion DMs & fans ‚Äî 24h/24\nüî¥ Strat√©gie PPV ‚Äî maximisation des revenus\nüî¥ Marketing Instagram & TikTok\nüî¥ Analyse des stats\nüî¥ Protection du contenu\nüî¥ Onboarding complet\n\nToi tu cr√©es. On g√®re le reste. üñ§",
          "üíº Our Services\n\nüî¥ DMs & Fan Management ‚Äî 24/7\nüî¥ PPV Strategy ‚Äî revenue maximization\nüî¥ Instagram & TikTok Marketing\nüî¥ Stats Analysis\nüî¥ Content Protection\nüî¥ Full Onboarding\n\nYou create. We handle the rest. üñ§", lang),
        reply_markup=back, parse_mode=None
    )

# ‚îÄ‚îÄ Results ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def results_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t("üîô Retour", "üîô Back", lang), callback_data=f"menu|{lang}")]])
    await query.edit_message_text(
        t("üìà Nos R√©sultats\n\nSeven Agency vient de lancer üöÄ\n\nOn embarque nos premi√®res cr√©atrices √† conditions exceptionnelles.\n\nüî¥ Commission r√©duite le 1er mois\nüî¥ Gestion compl√®te prise en charge\nüî¥ Contrat 1 mois sans engagement\n\nSois parmi les premi√®res.\nObtiens les meilleures conditions.\n\nLe premier pas c'est juste un DM üî¥\nüì© Instagram: @seven._agency",
          "üìà Our Results\n\nSeven Agency just launched üöÄ\n\nWe are onboarding our first creators under exceptional conditions.\n\nüî¥ Reduced commission for the 1st month\nüî¥ Full management taken care of\nüî¥ 1 month contract, no commitment\n\nBe one of the first.\nGet the best conditions.\n\nThe first step is just a DM üî¥\nüì© Instagram: @seven._agency", lang),
        reply_markup=back, parse_mode=None
    )

# ‚îÄ‚îÄ Join ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def join_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("üì∏ Instagram", url="https://ig.me/u/seven._agency")],
        [InlineKeyboardButton(t("üí¨ Contacter le Manager", "üí¨ Contact the Manager", lang), url="https://t.me/seven_manager_of")],
        [InlineKeyboardButton(t("üîô Retour", "üîô Back", lang), callback_data=f"menu|{lang}")],
    ])
    await query.edit_message_text(
        t("üöÄ Rejoindre Seven Agency\n\n1Ô∏è‚É£ Clique ci-dessous\n2Ô∏è‚É£ Envoie 'SEVEN' en DM\n3Ô∏è‚É£ On te r√©pond sous 24h\n4Ô∏è‚É£ Appel ‚Üí Contrat ‚Üí C'est parti üî¥\n\nPlaces limit√©es ce mois-ci. üñ§",
          "üöÄ Join Seven Agency\n\n1Ô∏è‚É£ Click below\n2Ô∏è‚É£ Send 'SEVEN' in DM\n3Ô∏è‚É£ We reply within 24h\n4Ô∏è‚É£ Call ‚Üí Contract ‚Üí Let's go üî¥\n\nSpots are limited this month. üñ§", lang),
        reply_markup=keyboard, parse_mode=None
    )

# ‚îÄ‚îÄ Contact ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("üì∏ Instagram @seven._agency", url="https://ig.me/u/seven._agency")],
        [InlineKeyboardButton(t("üîô Retour", "üîô Back", lang), callback_data=f"menu|{lang}")],
    ])
    await query.edit_message_text(
        t("üí¨ Nous contacter\n\nüì∏ Instagram ‚Üí @seven._agency\n\nOn r√©pond √† tous les messages sous 24h. üñ§\n\nTu peux aussi rejoindre l'agence directement via le bouton üöÄ Rejoindre l'agence dans le menu.",
          "üí¨ Contact Us\n\nüì∏ Instagram ‚Üí @seven._agency\n\nWe reply to all messages within 24h. üñ§\n\nYou can also join the agency directly via the üöÄ Join the Agency button in the menu.", lang),
        reply_markup=keyboard, parse_mode=None
    )

# ‚îÄ‚îÄ Main ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(switch_handler, pattern=r"^switch\|"))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern=r"^menu\|"))
    app.add_handler(CallbackQueryHandler(faq_handler, pattern=r"^faq\|"))
    app.add_handler(CallbackQueryHandler(faq_commission, pattern=r"^faq_commission\|"))
    app.add_handler(CallbackQueryHandler(faq_control, pattern=r"^faq_control\|"))
    app.add_handler(CallbackQueryHandler(faq_results, pattern=r"^faq_results\|"))
    app.add_handler(CallbackQueryHandler(faq_how, pattern=r"^faq_how\|"))
    app.add_handler(CallbackQueryHandler(faq_free, pattern=r"^faq_free\|"))
    app.add_handler(CallbackQueryHandler(services_handler, pattern=r"^services\|"))
    app.add_handler(CallbackQueryHandler(results_handler, pattern=r"^results\|"))
    app.add_handler(CallbackQueryHandler(join_handler, pattern=r"^join\|"))
    app.add_handler(CallbackQueryHandler(contact_handler, pattern=r"^contact\|"))
    print("‚úÖ Seven Agency Bot FR/EN is running... üñ§")
    app.run_polling()

if __name__ == "__main__":
    main()
