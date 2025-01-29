import os

class Settings:
    # Get the Microsoft App ID from environment variables or use a placeholder
    APP_ID = os.environ.get("MicrosoftAppId", "<<MICROSOFT-APP-ID>>")
    # Get the Microsoft App Password from environment variables or use a placeholder
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "<<MICROSOFT-APP-PASSWORD>>")
    # Get the Storage Account Connection String from environment variables or use a placeholder
    STORAGE_ACCOUNT_CONNECTION_STRING = os.environ.get("STORAGE_ACCOUNT_CONNECTION_STRING", "<<STORAGE_ACCOUNT_CONNECTION_STRING>>")
    # Get the Bot Endpoint from environment variables or use a placeholder
    BOT_ENDPOINT = os.environ.get("BOT_ENDPOINT","<<BOT_ENDPOINT>>")
    # Get the Teams App ID from environment variables or use a placeholder
    TEAMS_APP_ID = os.environ.get("TEAMS_APP_ID","<<TEAMS_APP_ID>>")

    # Define table names for different entities
    TABLE_NAME = {
        'PRODUCT': 'Products',
        'CATEGORY': 'Categories',
        'SUPPLIER': 'Suppliers',
        'ORDER_DETAIL': 'OrderDetails'
    }