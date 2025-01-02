from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation
INDUSTRY, OBJECTIVE, WEBSITE, SOCIAL_MEDIA, PPC_CAMPAIGN, AUDIENCE, LOCATION = range(7)

# Start the bot conversation
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Welcome to the Digital Marketing Assistant Bot!")
    await update.message.reply_text("Let's get started. What industry is your business in?")
    return INDUSTRY

# Collect the user's business industry
async def industry(update: Update, context: CallbackContext) -> int:
    context.user_data['industry'] = update.message.text
    await update.message.reply_text("Great! What is your business objective? (e.g., lead generation, sales, etc.)")
    return OBJECTIVE

# Collect the user's business objective
async def objective(update: Update, context: CallbackContext) -> int:
    context.user_data['objective'] = update.message.text
    await update.message.reply_text("Do you have a website? If yes, please provide the URL. (If no, type 'no')")
    return WEBSITE

# Collect the website URL
async def website(update: Update, context: CallbackContext) -> int:
    context.user_data['website'] = update.message.text if update.message.text.lower() != 'no' else None
    await update.message.reply_text("Do you have any social media platforms? If yes, provide the URL(s). (If no, type 'no')")
    return SOCIAL_MEDIA

# Collect social media URLs
async def social_media(update: Update, context: CallbackContext) -> int:
    context.user_data['social_media'] = update.message.text if update.message.text.lower() != 'no' else None
    await update.message.reply_text("Do you use PPC campaigns? (yes/no)")
    return PPC_CAMPAIGN

# Collect PPC campaign info
async def ppc_campaign(update: Update, context: CallbackContext) -> int:
    context.user_data['ppc_campaign'] = update.message.text.lower()
    await update.message.reply_text("Who are you trying to reach? (e.g., young adults, professionals, etc.)")
    return AUDIENCE

# Collect audience information
async def audience(update: Update, context: CallbackContext) -> int:
    context.user_data['audience'] = update.message.text
    await update.message.reply_text("What location would you like to target? (e.g., USA, UK, etc.)")
    return LOCATION

# Collect target location info
async def location(update: Update, context: CallbackContext) -> int:
    context.user_data['location'] = update.message.text
    await update.message.reply_text("Thanks for providing the details. Let me generate some relevant keywords for your business.")
    
    # Generate keywords (you can integrate your predefined dataset or use external APIs here)
    keywords = generate_keywords(context.user_data)
    await update.message.reply_text(f"Relevant keywords for your business: {', '.join(keywords)}")

    return ConversationHandler.END

# Function to generate relevant keywords (dummy function, extend this based on your use case)
def generate_keywords(user_data):
    # This can be replaced with actual keyword generation logic
    return ["business strategy", "lead generation", "PPC campaigns", "social media marketing"]

# Function to cancel the conversation
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Conversation has been cancelled.")
    return ConversationHandler.END

# Main function to set up the bot
def main() -> None:
    # Replace this with your bot token
    application = Application.builder().token("8079950255:AAG2WVbkEG4i54e5HZjtWH3EBTs0AWixwvI").build()

    # Conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INDUSTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, industry)],
            OBJECTIVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, objective)],
            WEBSITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, website)],
            SOCIAL_MEDIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, social_media)],
            PPC_CAMPAIGN: [MessageHandler(filters.TEXT & ~filters.COMMAND, ppc_campaign)],
            AUDIENCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, audience)],
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, location)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add the conversation handler to the application
    application.add_handler(conv_handler)

    # Start polling for updates
    logger.info("Starting the bot...")
    application.run_polling()

if __name__ == '__main__':
    main()
