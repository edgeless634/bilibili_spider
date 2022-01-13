from email.policy import default
import click
import version

@click.group()
def cli():
    pass

@click.command(name="run")
def run_spider():
    click.echo("RUNNING")

@click.command(name="version")
def show_version():
    click.echo(version.VERSION)

if __name__ == '__main__':
    cli.add_command(run_spider)
    cli.add_command(show_version)
    cli()