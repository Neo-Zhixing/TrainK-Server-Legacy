## What will TrainK do

* Track the status of every single train running on Chinese railroad and provide users with real-time report and perditions about delays.

* Over time, TrainK will be able to give suggestions to help users choose between trains and avoid the ones with a higher delay possibility using the data accumulated.

* Provide users with a better ticket-booking interface and an easier procedure.

* Enable none-Chinese speakers to book tickets online. For now, the official booking website 12306.cn does not have a multi-language interface; the captcha is an impossible problem for a foreigner. What’s more, you’ll need a Chinese phone number and a Chinese bank account to purchase tickets – they don’t accept Visa, Master Card or American Express. Hopefully, TrainK will be able to deal with all these requirements for none-Chinese users.

## How I’m going to do it

Although 12306.cn doesn’t have a set of public APIs, we do have some APIs scraped from their website. That will make feature 1-3 available.

These APIs don't provide information in a convenient way, since they're for ajax. For example, the API for delays is only available -1 - +3 hours before the train departures. But over time, we can accumulate and intrepret these information, save them in the database, and show them in a straight-forward, user-friendly way.
