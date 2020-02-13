#!/bin/bash

project_path="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

pip install -r "$project_path/requirements.txt"

if command -v apt-get 2>/dev/null; then
    sudo apt update -y
    sudo apt-get install -y libmagic-dev
elif command -v brew 2>/dev/null; then
    brew install libmagic
else 
    printf "This project requires libmagic. "
    printf "Figure out how to install it, then hit [Enter] to continue. "
    read
fi

printf "\n"

do_overwrite()
{
    rm "$project_path/.env" 2>/dev/null
    
    printf "ENVIRONMENT = (probably: production) "
    read -r environment

    printf "EMAIL_RECIPIENT = (something like: Your Name <your@email.address>) "
    read -r email_recipient
    printf "EMAIL_SENDER = (something like: Your NewsBot <your-newsbot@your.newsbot.domain>) "
    read -r email_sender
    printf "EMAIL_SENDER_DOMAIN = (something like: your.newsbot.domain) "
    read -r email_sender_domain
    
    printf "MAILGUN_API_KEY = (check https://app.mailgun.com/app/account/security/api_keys) "
    read -r mailgun_api_key

    printf "# This document was generated by config.sh\n\n" >> "$project_path/.env"
    printf "ENVIRONMENT='$environment'\n\n" >> "$project_path/.env"
    printf "EMAIL_RECIPIENT='$email_recipient'\n" >> "$project_path/.env"
    printf "EMAIL_SENDER='$email_sender'\n" >> "$project_path/.env"
    printf "EMAIL_SENDER_DOMAIN='$email_sender_domain'\n\n" >> "$project_path/.env"
    printf "MAILGUN_API_KEY='$mailgun_api_key'\n" >> "$project_path/.env"
    sudo chown "$project_path/.env"
    sudo chmod u=r,g=,o= "$project_path/.env"
    
    printf "$project_path/.env written\n"
}


printf "Do you want to write (or rewrite) .env?\n"
select answer in "Yes" "No"; do
    case $answer in
        Yes ) do_overwrite; break;;
        No ) break;;
    esac
done

printf "\n"

sudo mkdir -p /usr/local/lib/systemd/system && \
    printf "/usr/local/lib/systemd/system created. \n"
sudo cp -r $project_path /usr/local/src/NewsBot && \
    printf "Project copied; it is safe to delete this version.\n"
sudo ln -s /usr/local/src/NewsBot/newsbot.service /usr/local/lib/systemd/system/ && \
    printf "Service file linked.\n"

printf "Cool. Now do \`sudo systemctl enable newsbot.service\` to make it happen.\n"
