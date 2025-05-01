# Earn Tips 24 Telegram Bot

This is a Telegram bot built for "Earn Tips 24". The bot allows users to verify captcha, manage profiles, refer others for earning tips, withdraw cash, and much more.

## Features:
- Captcha verification
- Inline keyboard for various options
- User profile, referral system, and earning tips
- Cash withdrawal based on balance
- Multi-language support
- Admin panel to manage users and balances

## Setup Instructions:
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Create a `.env` file with your Telegram token and Firebase credentials.
4. Deploy the bot using Render or any other platform.

## Deployment:
- Render: Connect your GitHub repository to Render for deployment.
- Uptime Robot: Monitor the bot's uptime.

## Firebase Setup:
- Firebase Realtime Database is used to store user information and balances. Configure it in the Firebase Console and use the generated credentials in the `config/firebase_credentials.json` file.
