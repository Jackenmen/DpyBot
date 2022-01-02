# DpyBot

[![Subscribe on Patreon](https://img.shields.io/badge/Support%20me%20on-Patreon-orange.svg?logo=patreon)](https://www.patreon.com/Jackenmen)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This is a very simple d.py bot that's intended for my own testing of functionalities of d.py. This is not meant for anything more than testing.

# How to use

1. Make a venv.
1. Activate the venv.
1. Run `pip install -r requirements.txt`.
1. Make a copy of `.env.example` file with a name `.env` and configure it
   according to the comments inside it.
1. Start the bot with `python -m dpybot`.

# External cogs

Aside from the cogs in this repository, you can add external cogs in `dpybot/ext_cogs` directory.

``dpybot_ext_mgr`` is a tool that helps with managing repositories and installed cogs.

For example, to install a cog from https://github.com/jack1142/DpyBot-DevCog, you can:
1. Activate the venv.
1. Run `python -m dpybot_ext_mgr`.
1. Choose "Add a repository." option.
1. Paste this URL: `https://github.com/jack1142/DpyBot-DevCog`
1. Choose "Install a cog." option.
1. Choose the repository (`DpyBot-DevCog`) and cog (`dev`).
1. Exit the tool with `Exit.` option.

# License

Please see [LICENSE file](LICENSE) for details. In short, this project is open source and you are free to modify and use my work as long as you credit me.

---

> Jakub Kuczys &nbsp;&middot;&nbsp;
> GitHub [@jack1142](https://github.com/jack1142)
