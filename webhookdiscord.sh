#!/bin/sh

# Change url to your discord webhook
url="https://discord.com/api/webhooks/1183288853650477116/F_efA77TF_Mjbg_FdmegWmAXkV_TloVB7r7zUjkmJkLfxMuei0X5LO2ZjDCtjfOz-BEv"

domain="$1"

curl -H "Content-Type: application/json" -X POST -d '{"content":"'"${domain} $1"'"}' "$url"