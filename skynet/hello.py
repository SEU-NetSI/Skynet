import click

from motion import basic_flying


@click.group()
def skynet():
    pass


@click.command()
@click.option("--channel", help="crazyflie communication channel id", type=int)
def fly(channel):
    """
    Test basic motion
    """
    basic_flying(link_uri='radio://0/' + str(channel) + '/2M')


if __name__ == '__main__':
    fly()
