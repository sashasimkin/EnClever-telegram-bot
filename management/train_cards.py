import click
from .cli import cli
from leitnersystem.leitnersystem import train_cards


@click.command()
def start_train_cards():
    train_cards()


cli.add_command(start_train_cards)
