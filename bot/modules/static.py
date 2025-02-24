WelcomeText = [
    """\
👋 **Hey %(first_name)s**, welcome!  

📤 **Send me a file** to instantly generate a file link.  

━━━━━━━━━━━━━━━━━━━  
🔹 **Commands:**  
🔹 /privacy - __View bot's privacy policy.__
🔹 /log - __Get bot's log file.__ **__(Owner only)__**
🔹 /help - __Show this message.__
━━━━━━━━━━━━━━━━━━━  
""",
    """\
╭━──◆ **Welcome, %(first_name)s!** ◆──━╮  
🚀 **Send me a file** to instantly generate a file link!  
╰━───────────────━╯  

✨ **Available Commands:**  
📜 /privacy - __View the bot's privacy policy.__
📂 /log - __Get the bot's log file.__ **__(Owner only)__**
ℹ️ /help - __Show this message.__

💠 **__Enjoy the seamless experience!__** 💠
""",
    """\
🚀 **Welcome, %(first_name)s!** 🚀  

📂 **__Send me a file to instantly generate a file link!__**

━━━━━━━━━━━━━━━━━━  
✨ **Available Commands:**  
📜 /privacy - __View bot's privacy policy.__
📂 /log - __Get the bot's log file.__ **__(Owner only)__**
ℹ️ /help - __Show this message.__
━━━━━━━━━━━━━━━━━━  

💠 **__Enjoy the seamless experience!__** 💠  
"""
]


PrivacyText = \
"""
**Privacy Policy**

**1.Data Storage:** Files you upload/send are securely saved in the bot's private Telegram channel.

**2.Download Links:** Links include a secret code to prevent unauthorized access.

**3.User Control:** You can revoke links anytime using the "Revoke" button.

**4.Moderation:** The bot owner can view and delete your files if necessary.

**5.Open Source:** The bot is [open source](https://github.com/TheCaduceus/FileStreamBot). Deploy your own instance for maximum privacy.

**6.Retention:** Files are stored until you revoke their links.

__By using this bot, you agree to this policy.__
"""

FileLinksText = \
"""
**Download Link:**
`%(dl_link)s`
"""

FileLinkText = """
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i> 🎉

📂 **Fɪʟᴇ ɴᴀᴍᴇ:** `{file_name}`

📦 **Fɪʟᴇ ꜱɪᴢᴇ:** `{file_size}`

📥 **Dᴏᴡɴʟᴏᴀᴅ:** __{dl_link}__

🚸 **Nᴏᴛᴇ:** **LINK WON'T EXPIRE TILL YOU REVOKE**
"""

MediaLinksText = \
"""
**Download Link:**
`%(dl_link)s`
**Stream Link:**
`%(stream_link)s`
"""

MediaLinkText = """
<i><u>𝗬𝗼𝘂𝗿 𝗟𝗶𝗻𝗸 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱 !</u></i> 🎉

📂 **Fɪʟᴇ ɴᴀᴍᴇ:** __{file_name}__

📦 **Fɪʟᴇ ꜱɪᴢᴇ:** `{file_size}`

📥 **Dᴏᴡɴʟᴏᴀᴅ:** __{dl_link}__

🖥 **WATCH:** __{stream_link}__

🚸 **Nᴏᴛᴇ:** **LINK WON'T EXPIRE TILL YOU REVOKE**
"""

InvalidQueryText = \
"""
Query data mismatched.
"""

MessageNotExist = \
"""
File revoked or not exist.
"""

LinkRevokedText = \
"""
The link has been revoked. It may take some time for the changes to take effect.
"""

InvalidPayloadText = \
"""
Invalid payload.
"""

UserNotInAllowedList = \
"""
You are not allowed to use this bot.
"""
