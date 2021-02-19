# NewsBot

NewsBot runs scheduled tasks — chiefly web scraping — in support of journalistic pursuits.

## authorship

I am [Carter Pape](https://carterpape.com). I developed this project from [Python](https://python.org), [Scrapy](https://scrapy.org), and a list of open source Python libraries listed in the `requirements.txt` document.

## prerequisites

You will need either a [Mailgun account](https://signup.mailgun.com/new/signup) for sending emails or to modify the `newsbot.item_pipelines.item_emailer.ItemEmailer1 class. Mailgun charges $0.80 per 1000 emails sent, following a 3-month free trial.

If you want to send and or receive mail from a domain that isn't the Mailgun sandbox, obtain your own domain name. Domain registration costs as little as $8 per year if [registered through Cloudflare](https://www.cloudflare.com/products/registrar/).

Note that if you do want Cloudflare as your registrar, you will need to make the initial domain name purchase elsewhere first. Many registrars have low introductory rates; play them like a fiddle by making the initial purchase with them then immediately moving the registration to Cloudflare.

I'm pretty sure this project works with most Python 3.x versions, but I have only tested the current version of NewsBot (0.3.0) against Python 3.8.

## installation

This project is not meant to be used as-is. It is only useful as-is in the narrow case of supporting the work of the project's author.

This project is open source to allow developers to either use it for parts or to build their own NewsBot on top of this (still-developing, unstable) framework.

I am a developer by background and reporter by profession. As much as I would love to have this project become stable and usable for anyone who wants to run it out-of-the-box — non-developers, in particular — the scope is more limited than that so that I can do my full-time job effectively while using this tool in a support capacity.

I am sharing his work to show off but also to give others an opportunity to copy it.

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

# The `private` subproject

Transparency is the ultimate name of the game for me when it comes to my reporting and just life in general. However, to maximize transparency — i.e., to do the best job that I can in gathering and disseminating information — some things are for me to know and nobody else to find out.

It is no different than maintaining the confidentiality of sources. That is, in fact, exactly what it is.

Whenever possible, I have made components of this project publicly available. Whenever making a component publicly accessible would violate the confidentiality of a source, the component is private.

As of [last count](https://github.com/AlDanial/cloc) (Feb. 19, 2021), this project contains 2,971 lines of code, and the private components collectively account for 594 lines.
