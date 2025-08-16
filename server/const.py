from dotenv import load_dotenv
import os

load_dotenv()

# t.me/sh_login_testing_bot
TOKEN_TG = os.getenv("TOKEN_TG")
HOST_DNS = os.getenv("HOST_DNS")
BOT_NAME = os.getenv("BOT_NAME")
#HARDCODE

BASH_BEGINING = "#!/bin/bash\n"
BASH_SPLITER = "\necho \"----------------------------------------------------------------\""
# BASH_END = "\necho \"----------------------------------------------------------------\"\necho \"Cleaning up...\"\nrm -f \"$0\"\necho \"Script completed and removed.\""

BASH_END = (
    '\necho "----------------------------------------------------------------"'
    '\necho "Cleaning up..."'
    '\nrm -f "$0"'
    '\nprintf "\e[32mScript completed and removed.\e[0m\n"'
)



#BUTTONS

BACK_BUTTON= {
    "inline_keyboard" :  [
        [
            {'text': 'Вернуться на сайт', 'url': f"https://{HOST_DNS}/"}      
        ]
    ]
}

CLEAN_BUTTON= {
    "inline_keyboard" :  [
        [
            {'text': 'Вернуться на сайт', 'url': f"https://{HOST_DNS}/logout/"}      
        ]
    ]
}
