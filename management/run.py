import click
from .cli import cli

from bot.main import EnCleverBot


@click.command()
@click.argument('token')
def run(token):
    EnCleverBot(token).run()


cli.add_command(run)
