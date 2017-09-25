import click
from .cli import cli


@click.command()
def parse_cards():
    click.echo('Will parse all the cards!')


cli.add_command(parse_cards)
