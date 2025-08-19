from dotenv import load_dotenv
import os

load_dotenv()

# t.me/sh_login_testing_bot
TOKEN_TG = os.getenv("TOKEN_TG")
HOST_DNS = os.getenv("HOST_DNS")
BOT_NAME = os.getenv("BOT_NAME")
#HARDCODE

# BASH_BEGINING = "#!/bin/bash\n"
BASH_SPLITER = "\necho \"----------------------------------------------------------------\""

# BASH_BEGINING = (
#     '#!/usr/bin/env bash\n'
#     'set -Eeuo pipefail\n'
#     'trap \'exit_code=$?; line_no=$LINENO; '
#     'printf "\\e[31mError at line %d (exit %d)\\e[0m\\n" "$line_no" "$exit_code"; '
#     'rm -f "$0"; exit "$exit_code"\' ERR\n'
# )

BASH_BEGIN = r"""#!/usr/bin/env bash
# strict mode + красивые ошибки
set -Eeu
# проверяем поддержку pipefail (bash-специфичная опция)
if [ -n "${BASH_VERSION:-}" ]; then
    set -o pipefail
fi

# цвета
RED="\033[31m"
GREEN="\033[32m"
RESET="\033[0m"

# флаг «скрипт завершился успешно»
__OK=true

# универсальная функция для проверки ошибок
check_error() {
    rc=$?
    if [ $rc -ne 0 ]; then
        __OK=false
        printf "\n${RED}[ERROR] Command failed with exit code %s${RESET}\n" "$rc" >&2
        exit "$rc"
    fi
}

# ловим ошибки (только в bash)
if [ -n "${BASH_VERSION:-}" ]; then
    trap '
        rc=$?
        cmd=${BASH_COMMAND}
        src=${BASH_SOURCE[1]:-$0}
        line=${BASH_LINENO[0]:-$LINENO}
        __OK=false
        printf "\n${RED}[ERROR] %s:%s: \"%s\" exited with code %s${RESET}\n" \
            "$src" "$line" "$cmd" "$rc" >&2
        exit "$rc"
    ' ERR
fi

# финальная обработка при выходе
trap '
    rc=$?
    if [ "${__OK}" = true ] && [ $rc -eq 0 ]; then
        printf "\n${GREEN}[OK] Script finished successfully.${RESET}\n"
    elif [ $rc -ne 0 ] && [ -z "${BASH_VERSION:-}" ]; then
        # для sh показываем ошибку только если не было обработана ранее
        printf "\n${RED}[ERROR] Script failed with exit code %s${RESET}\n" "$rc" >&2
    fi
    
    # самоудаление скрипта
    if [ -f "$0" ] && [ "$0" != "/dev/stdin" ] && [ "$0" != "-" ]; then
        printf "\n${GREEN}[CLEANUP] Removing script file: $0${RESET}\n"
        rm -f "$0" 2>/dev/null || true
    fi
' EXIT
"""





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
