""" help comand """

import click

@click.command()
@click.argument('command')
@click.pass_context
def help(ctx, command):
    """
    help to a command
    """

    #print(ctx.parent.command.commands)
    
    if command is None:
        print(ctx.parent.get_help())
    else:
        print(ctx.parent.command.commands[command].get_help(ctx))