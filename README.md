# NewsBot
A bot that runs journalistic tasks, such as web scraping

## prerequisites

You will also need a [Mailgun account](https://signup.mailgun.com/new/signup) for sending emails. It's free.

If you want to send and or receive mail from a non-Mailgun-sandbox URL, obtain your own domain name. Domain registration costs as little as $8 per year if [registered through Cloudflare](https://www.cloudflare.com/products/registrar/).

Note that if you do want Cloudflare as your registrar, you will need to make the initial domain name purchase elsewhere first. Many registrars have low introductory rates; play them like a fiddle by making the initial purchase with them then moving the registration to Cloudflare.

## installation

`cd` to a nice spot for the project to be, then do

```zsh
git clone https://github.com/CarterPape/NewsBot.git
cd NewsBot
make config
```

and follow the prompts.
