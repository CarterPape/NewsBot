# NewsBot

NewsBot runs scheduled tasks — chiefly web scraping — in support of journalistic pursuits.

## prerequisites

You will need either a [Mailgun account](https://signup.mailgun.com/new/signup) for sending emails or to modify the `newsbot.item_pipelines.item_emailer.ItemEmailer1 class. Mailgun charges $0.80 per 1000 emails sent, following a 3-month free trial.

If you want to send and or receive mail from a domain that isn't the Mailgun sandbox, obtain your own domain name. Domain registration costs as little as $8 per year if [registered through Cloudflare](https://www.cloudflare.com/products/registrar/).

Note that if you do want Cloudflare as your registrar, you will need to make the initial domain name purchase elsewhere first. Many registrars have low introductory rates; play them like a fiddle by making the initial purchase with them then immediately moving the registration to Cloudflare.

## installation

This project is not meant to be used as-is. It is only useful as-is in the narrow case of supporting the work of the project's author.

This project is open source to allow developers to either use it for parts or to build their own NewsBot on top of this (still-developing, unstable) framework.

The author, [Carter Pape](https://carterpape.com), is a developer by background and reporter by profession. As much as he would love to have this project become stable and usable for anyone who wants to run it out-of-the-box — non-developers, in particular — the scope is more limited than that so that he can do his full-time job effectively. while using this tool in a support capacity.

The author is sharing his work to show off but also to give others an opportunity to copy it.

With all of that said, here is how to install this project:

`cd` to a nice spot for the project to be, then do

```zsh
git clone https://github.com/CarterPape/NewsBot.git
cd NewsBot
./setup.sh
```

follow the prompts, then:

```zsh
./scripts/set_up_default_email_recipient.py
```

to make sure there's at least one email that receives all emailed items. Then:

```zsh
./scripts/add_email_subscription.py
```

to add other email subscriptions for items.
