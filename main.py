# -*- coding: utf-8 -*-
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler,
                          MessageHandler, ConversationHandler, filters, ContextTypes)

TOKEN = "8711482972:AAHj8hgs_Sv571J6BdfQP7QzpCqyJIN3VwM"
ADMIN_CHAT_ID = None  # Run /myid in the bot to get your ID, then set it here
logging.basicConfig(level=logging.INFO)

# Conversation states for application form
APPLY_NAME, APPLY_PLATFORM, APPLY_REVENUE, APPLY_DURATION, APPLY_WHY = range(5)

# Unicode escapes - immune to encoding issues
WAVE    = "\U0001F44B"
BLACK   = "\U0001F5A4"
FINGER  = "\U0001F447"
FAQ_ICO = "\U0001F4CB"
BRIEF   = "\U0001F4BC"
CHART   = "\U0001F4C8"
ROCKET  = "\U0001F680"
BACK    = "\U0001F519"
QUEST   = "\u2753"
MONEY   = "\U0001F4B0"
LOCK    = "\U0001F510"
RED     = "\U0001F534"
CAMERA  = "\U0001F4F8"
BUBBLE  = "\U0001F4AC"
FR_FLAG = "\U0001F1EB\U0001F1F7"
GB_FLAG = "\U0001F1EC\U0001F1E7"
GEAR    = "\u2699\uFE0F"
PHONE   = "\U0001F4F1"
STATS   = "\U0001F4CA"
CHECK   = "\u2705"
HANDS   = "\U0001F91D"
ONE     = "1\uFE0F\u20E3"
TWO     = "2\uFE0F\u20E3"
THREE   = "3\uFE0F\u20E3"
FOUR    = "4\uFE0F\u20E3"
FORM    = "\U0001F4DD"
STAR    = "\u2B50"
FIRE    = "\U0001F525"

def get_lang(update: Update) -> str:
    lang = update.effective_user.language_code or "en"
    return "fr" if lang.startswith("fr") else "en"

def t(fr_text: str, en_text: str, lang: str) -> str:
    return fr_text if lang == "fr" else en_text

def main_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{FAQ_ICO} FAQ", callback_data=f"faq|{lang}"),
         InlineKeyboardButton(t(f"{BRIEF} Nos Services", f"{BRIEF} Our Services", lang), callback_data=f"services|{lang}")],
        [InlineKeyboardButton(t(f"{CHART} Nos Resultats", f"{CHART} Our Results", lang), callback_data=f"results|{lang}"),
         InlineKeyboardButton(t(f"{ROCKET} Rejoindre l'agence", f"{ROCKET} Join the Agency", lang), callback_data=f"join|{lang}")],
        [InlineKeyboardButton(t(f"{FORM} Postuler maintenant", f"{FORM} Apply Now", lang), callback_data=f"apply|{lang}")],
        [InlineKeyboardButton(t(f"{GB_FLAG} Switch to English", f"{FR_FLAG} Passer en Francais", lang),
                              callback_data=f"switch|{'en' if lang == 'fr' else 'fr'}")],
    ])

def main_text(lang):
    return t(
        f"{WAVE} Bienvenue chez Seven Agency {BLACK}\n\nOn scale tes revenus OnlyFans.\nToi tu crees. On gere le reste.\n\nChoisis une option {FINGER}",
        f"{WAVE} Welcome to Seven Agency {BLACK}\n\nWe scale your OnlyFans income.\nYou create. We handle the rest.\n\nChoose an option {FINGER}",
        lang
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(main_text(lang), reply_markup=main_keyboard(lang), parse_mode=None)

async def myid_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_user.id
    await update.message.reply_text(f"Ton Telegram ID est: {chat_id}\n\nMets ce numero dans ADMIN_CHAT_ID du bot.")

async def switch_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    await query.edit_message_text(main_text(lang), reply_markup=main_keyboard(lang), parse_mode=None)

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    await query.edit_message_text(main_text(lang), reply_markup=main_keyboard(lang), parse_mode=None)

async def faq_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(t(f"{QUEST} Quelle est votre commission ?", f"{QUEST} What is your commission?", lang), callback_data=f"faq_commission|{lang}")],
        [InlineKeyboardButton(t(f"{QUEST} Je garde le controle ?", f"{QUEST} Do I keep control?", lang), callback_data=f"faq_control|{lang}")],
        [InlineKeyboardButton(t(f"{QUEST} Resultats en combien de temps ?", f"{QUEST} How fast will I see results?", lang), callback_data=f"faq_results|{lang}")],
        [InlineKeyboardButton(t(f"{QUEST} Comment ca fonctionne ?", f"{QUEST} How does it work?", lang), callback_data=f"faq_how|{lang}")],
        [InlineKeyboardButton(t(f"{QUEST} C'est gratuit pour commencer ?", f"{QUEST} Is it free to start?", lang), callback_data=f"faq_free|{lang}")],
        [InlineKeyboardButton(t(f"{BACK} Retour", f"{BACK} Back", lang), callback_data=f"menu|{lang}")],
    ])
    await query.edit_message_text(
        t(f"{FAQ_ICO} FAQ  -  Seven Agency\n\nChoisis ta question {FINGER}",
          f"{FAQ_ICO} FAQ  -  Seven Agency\n\nChoose your question {FINGER}", lang),
        reply_markup=keyboard, parse_mode=None
    )

async def faq_commission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t(f"{BACK} Retour FAQ", f"{BACK} Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t(f"{MONEY} Notre Commission\n\nNotre commission est de 40% des revenus generes.\n\nPas de frais caches. Pas de frais fixes.\nOn gagne quand toi tu gagnes. {HANDS}",
          f"{MONEY} Our Commission\n\nOur commission is 40% of the revenue generated.\n\nNo hidden fees. No fixed costs.\nWe earn when you earn. {HANDS}", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t(f"{BACK} Retour FAQ", f"{BACK} Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t(f"{LOCK} Tu gardes le controle total\n\n{CHECK} Tu valides tout le contenu\n{CHECK} Acces a ton compte a tout moment\n{CHECK} Tu decides des prix\n{CHECK} Contrat resiliable facilement\n\nTon compte reste le tien. {BLACK}",
          f"{LOCK} You Keep Full Control\n\n{CHECK} You approve all content\n{CHECK} Access to your account at all times\n{CHECK} You decide on prices\n{CHECK} Contract easily cancellable\n\nYour account stays yours. {BLACK}", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t(f"{BACK} Retour FAQ", f"{BACK} Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t(f"{CHART} Resultats en combien de temps ?\n\nEn moyenne 2 a 4 semaines.\n\nSemaine 1 {RED} Analyse du compte\nSemaine 2 {RED} Gestion des DMs\nSemaine 3 {RED} Marketing lance\nSemaine 4 {RED} Premiers resultats {ROCKET}",
          f"{CHART} How Fast Will I See Results?\n\nOn average 2 to 4 weeks.\n\nWeek 1 {RED} Account analysis\nWeek 2 {RED} DMs & fan management\nWeek 3 {RED} Marketing launched\nWeek 4 {RED} First results visible {ROCKET}", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_how(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t(f"{BACK} Retour FAQ", f"{BACK} Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t(f"{GEAR} Comment ca fonctionne ?\n\nOn s'occupe de tout pour que tu te concentres 100% sur la creation.\n\n{BUBBLE} Messages & DMs  -  on repond a tes fans 24h/24\n{MONEY} Strategie PPV  -  on envoie le bon contenu au bon moment\n{PHONE} Marketing  -  on fait grandir ton audience sur Instagram & TikTok\n{STATS} Analytics  -  on suit tes stats et optimise chaque semaine\n{LOCK} Protection du contenu  -  ton contenu reste en securite\n\nToi tu crees. On gere le reste. {BLACK}",
          f"{GEAR} How Does It Work?\n\nWe take care of everything so you can focus 100% on creating.\n\n{BUBBLE} Fan Messaging & DMs  -  we reply to your fans 24/7\n{MONEY} PPV Strategy  -  we send the right content at the right time\n{PHONE} Marketing  -  we grow your audience on Instagram & TikTok\n{STATS} Analytics  -  we track your stats and optimize every week\n{LOCK} Content Protection  -  your content stays safe\n\nYou create. We handle the rest. {BLACK}", lang),
        reply_markup=back, parse_mode=None
    )

async def faq_free(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t(f"{BACK} Retour FAQ", f"{BACK} Back to FAQ", lang), callback_data=f"faq|{lang}")]])
    await query.edit_message_text(
        t(f"{CHECK} C'est gratuit pour commencer ?\n\nOui  -  aucun frais fixe.\n\nOn prend uniquement une commission sur les revenus.\nSi on te rapporte rien, on prend rien. {HANDS}",
          f"{CHECK} Is It Free To Start?\n\nYes  -  no fixed fees.\n\nWe only take a commission on revenue.\nIf we don't make you money, we don't get paid. {HANDS}", lang),
        reply_markup=back, parse_mode=None
    )

async def services_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t(f"{BACK} Retour", f"{BACK} Back", lang), callback_data=f"menu|{lang}")]])
    await query.edit_message_text(
        t(f"{BRIEF} Nos Services\n\n{RED} Gestion DMs & fans  -  24h/24\n{RED} Strategie PPV  -  maximisation des revenus\n{RED} Marketing Instagram & TikTok\n{RED} Analyse des stats\n{RED} Protection du contenu\n{RED} Onboarding complet\n\nToi tu crees. On gere le reste. {BLACK}",
          f"{BRIEF} Our Services\n\n{RED} DMs & Fan Management  -  24/7\n{RED} PPV Strategy  -  revenue maximization\n{RED} Instagram & TikTok Marketing\n{RED} Stats Analysis\n{RED} Content Protection\n{RED} Full Onboarding\n\nYou create. We handle the rest. {BLACK}", lang),
        reply_markup=back, parse_mode=None
    )

async def results_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    back = InlineKeyboardMarkup([[InlineKeyboardButton(t(f"{BACK} Retour", f"{BACK} Back", lang), callback_data=f"menu|{lang}")]])
    await query.edit_message_text(
        t(f"{CHART} Nos Resultats\n\nSeven Agency vient de lancer {ROCKET}\n\nOn embarque nos premieres creatrices a conditions exceptionnelles.\n\n{RED} Commission reduite le 1er mois\n{RED} Gestion complete prise en charge\n{RED} Contrat 1 mois sans engagement\n\nSois parmi les premieres.\nObtiens les meilleures conditions.\n\nLe premier pas c'est juste un DM {RED}\n{CAMERA} Instagram: @seven._agency",
          f"{CHART} Our Results\n\nSeven Agency just launched {ROCKET}\n\nWe are onboarding our first creators under exceptional conditions.\n\n{RED} Reduced commission for the 1st month\n{RED} Full management taken care of\n{RED} 1 month contract, no commitment\n\nBe one of the first.\nGet the best conditions.\n\nThe first step is just a DM {RED}\n{CAMERA} Instagram: @seven._agency", lang),
        reply_markup=back, parse_mode=None
    )

async def join_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"{CAMERA} Instagram", url="https://ig.me/u/seven._agency")],
        [InlineKeyboardButton(t(f"{BUBBLE} Contacter le Manager", f"{BUBBLE} Contact the Manager", lang), url="https://t.me/seven_manager_of")],
        [InlineKeyboardButton(t(f"{BACK} Retour", f"{BACK} Back", lang), callback_data=f"menu|{lang}")],
    ])
    await query.edit_message_text(
        t(f"{ROCKET} Rejoindre Seven Agency\n\n{ONE} Clique ci-dessous\n{TWO} Envoie 'SEVEN' en DM\n{THREE} On te repond sous 24h\n{FOUR} Appel {RED} Contrat {RED} C'est parti {RED}\n\nPlaces limitees ce mois-ci. {BLACK}",
          f"{ROCKET} Join Seven Agency\n\n{ONE} Click below\n{TWO} Send 'SEVEN' in DM\n{THREE} We reply within 24h\n{FOUR} Call {RED} Contract {RED} Let's go {RED}\n\nSpots are limited this month. {BLACK}", lang),
        reply_markup=keyboard, parse_mode=None
    )

# ‚îÄ‚îÄ‚îÄ APPLICATION FORM ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

async def apply_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("|")[1]
    context.user_data['lang'] = lang
    context.user_data['apply'] = {}
    await query.message.reply_text(
        t(
            f"{FORM} Candidature Seven Agency\n\nSuper ! Quelques questions rapides.\n\nQuestion 1/5\nQuel est ton prenom ?",
            f"{FORM} Seven Agency Application\n\nGreat! Just a few quick questions.\n\nQuestion 1/5\nWhat is your first name?",
            lang
        ),
        parse_mode=None
    )
    return APPLY_NAME

async def apply_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    context.user_data['apply']['name'] = update.message.text
    await update.message.reply_text(
        t(
            f"Question 2/5\nQuel est le lien de ton profil OnlyFans ?",
            f"Question 2/5\nWhat is your OnlyFans profile link?",
            lang
        ),
        parse_mode=None
    )
    return APPLY_PLATFORM

async def apply_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    context.user_data['apply']['platform'] = update.message.text
    await update.message.reply_text(
        t(
            f"Question 3/5\nQuels sont tes revenus mensuels actuels sur OnlyFans ?\n(ex: 500$, 1000$, 2000$...)",
            f"Question 3/5\nWhat is your current monthly revenue on OnlyFans?\n(e.g. $500, $1000, $2000...)",
            lang
        ),
        parse_mode=None
    )
    return APPLY_REVENUE

async def apply_revenue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    context.user_data['apply']['revenue'] = update.message.text
    await update.message.reply_text(
        t(
            f"Question 4/5\nDepuis combien de temps tu es sur OnlyFans ?",
            f"Question 4/5\nHow long have you been on OnlyFans?",
            lang
        ),
        parse_mode=None
    )
    return APPLY_DURATION

async def apply_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    context.user_data['apply']['duration'] = update.message.text
    await update.message.reply_text(
        t(
            f"Question 5/5\nPourquoi tu veux travailler avec Seven Agency ?",
            f"Question 5/5\nWhy do you want to work with Seven Agency?",
            lang
        ),
        parse_mode=None
    )
    return APPLY_WHY

async def apply_why(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    context.user_data['apply']['why'] = update.message.text
    data = context.user_data['apply']
    user = update.effective_user

    # Confirm to applicant
    await update.message.reply_text(
        t(
            f"{CHECK} Candidature envoyee {FIRE}\n\nOn te recontacte sous 24h.\n\nEn attendant, rejoins notre canal :\nt.me/seven_agency_ofm",
            f"{CHECK} Application sent {FIRE}\n\nWe will get back to you within 24h.\n\nMeanwhile, join our channel:\nt.me/seven_agency_ofm",
            lang
        ),
        reply_markup=main_keyboard(lang),
        parse_mode=None
    )

    # Send dossier to admin
    if ADMIN_CHAT_ID:
        username = f"@{user.username}" if user.username else f"ID: {user.id}"
        summary = (
            f"{STAR}{STAR} NOUVELLE CANDIDATURE {STAR}{STAR}\n\n"
            f"{FORM} Prenom: {data.get('name', 'N/A')}\n"
            f"{CAMERA} Profil OF: {data.get('platform', 'N/A')}\n"
            f"{MONEY} Revenus actuels: {data.get('revenue', 'N/A')}\n"
            f"{CHART} Anciennete: {data.get('duration', 'N/A')}\n"
            f"{BUBBLE} Motivation: {data.get('why', 'N/A')}\n\n"
            f"Telegram: {username}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=summary, parse_mode=None)

    context.user_data.pop('apply', None)
    return ConversationHandler.END

async def apply_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('lang', 'en')
    context.user_data.pop('apply', None)
    await update.message.reply_text(
        t("Candidature annulee.", "Application cancelled.", lang),
        reply_markup=main_keyboard(lang),
        parse_mode=None
    )
    return ConversationHandler.END

# ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ‚îÄ

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = get_lang(update)
    await update.message.reply_text(
        t(f"{WAVE} Salut ! Utilise /start pour voir le menu.",
          f"{WAVE} Hey! Use /start to see the menu.", lang),
        parse_mode=None
    )

def main():
    app = Application.builder().token(TOKEN).build()

    # Application form conversation
    apply_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(apply_start, pattern=r"^apply\|")],
        states={
            APPLY_NAME:     [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_name)],
            APPLY_PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_platform)],
            APPLY_REVENUE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_revenue)],
            APPLY_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_duration)],
            APPLY_WHY:      [MessageHandler(filters.TEXT & ~filters.COMMAND, apply_why)],
        },
        fallbacks=[CommandHandler("cancel", apply_cancel)],
    )

    app.add_handler(apply_conv)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myid", myid_handler))
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Seven Agency Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
