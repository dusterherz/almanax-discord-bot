# almanax-discord-bot

![](https://derniercri.d.pr/JhOdpZ+)

Send everyday a picture of the current offering and bonus for the Dofus' Almanax in your discord server.
Uses `python`, `imgkit` and `discord.py`

# Installation
This project run with pipenv. To install it, use :
`pipenv install`

Then copy-paste .env.example into .env and complete the file with your variables.

You'll need also `wkhtmltopdf` to be installed on your distro for `imgkit` to work.

# Run
You can run the projet by doing :
`pipenv run python -m almanax`

If you don't have an xserver installed (required by imgkit) on your server, you can use xvfb to run the project:
`xvfb-run pipenv run python -m almanax`
