import click
from .cli import cli

from bot.main import EnCleverBot


@click.command()
def run():
    EnCleverBot().run()


cli.add_command(run)
