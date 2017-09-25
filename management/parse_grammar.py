import click
from .cli import cli


@click.command()
def parse_grammar():
    click.echo('Will parse all the grammar!')


cli.add_command(parse_grammar)
