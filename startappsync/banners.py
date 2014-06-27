import sys
if sys.version_info < (2, 7):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

from pretty_line import CLDocument
from re import search

#to remove
from termcolor import colored

###
# This file is total mess!
# Fix it! God damn it!
###

document = CLDocument(width=72)
p = document.create_element()
br = document.br
hr = document.hr
heading = document.heading

def p_white(text):
    p.text(text)
    p.color('white')
    p.text_align.center
    p.render()

def p_yellow(text, **kwargs):
    align = kwargs.get('align', 'center')
    p.text(text)
    p.color('yellow')

    # Stupid implementation
    # Fix it! God damn it!
    if align == 'center':
        p.text_align.center
    elif align == 'left':
        p.text_align.left
    else:
        p.text_align.right

    p.render()

def p_green(text):
    p.text(text)
    p.color('green')
    p.text_align.center
    p.render()

def anchor(href):
    p.text(href)
    p.color('blue')
    p.text_decoration.underline
    p.text_align.center
    p.render()

def print_error(messages):
    # Stupid implementation
    # Fix it! God damn it!
    br()
    padding_left = " "*22
    uups = "{0}Uups ...".format(padding_left)
    heading(uups, 'big', 'red')
    br()
    if isinstance(messages, dict):
        for message in messages:
            _color = messages[message]
            color = 'white' if _color == '' else _color
            p.text(message)
            p.color(color)
            p.text_align.center
            p.render()
    else:
        p_white(messages)

    br()

def print_success(message):
    thumbs = """

                   .     __                 __
                        (  |               |  )
                     ____\  \             /  /_____
                    (____ _) \           /   (_____)
                    (_____ ) _)__(-,-)__(_  ( _____)
                    (__ ___)  )  |___|  (   (_  ___)
                     (_____)__/  /_/\_\  \__(____)
                                 "   "
    """
    print(colored(thumbs, 'green'))
    p_green(message)
    br()

def green(text):
    return colored(text, 'green')

def error():
    print_error("There is something shitty with this remote!")

def set_remote_success(remote_name):
    print_success("Remote with name '{0}' was successfuly added!".format(remote_name))

def git_repo_not_found():
    # Stupid implementation
    # Fix it! God damn it!
    messages = OrderedDict([
        ("Uuuups ... I can't find Git repo here!", ""),
        ("If tyou want to see the usage please type this:", ""),
        ("", ""),
        ("startappsync --help", "yellow"),
    ])
    print_error(messages)


def directory_not_exist():
    print_error("The directory you are looking for is not exist! :(")

def start_syncing(src, dest, version):
    br()
    p.text('v{}'.format(version)).color('white').text_align.right.render()
    heading('  StartAppSync', 'big', 'blue')
    br()

    start_syncing = "{}Start Syncing".format(" "*24)
    heading(start_syncing, 'italic', 'green')

    p_white("Now I'm watching for changes here:")
    p_green(str(src))
    br()

    p_white("I will sync them there:")
    p_green(str(dest))
    br()

    p_white("So that you can enjoy them here:")
    url = search('@(.+):~', dest).groups()[0]
    anchor("http://{0}/\n".format(url))


def no_rhc_in_gitconfig():
    # Stupid implementation
    # Fix it! God damn it!
    messages = OrderedDict([
        ("Sorry Dude :((", ""),
        ("... But I can't find StartApp App in the Git Config!", ""),
    ])
    print_error(messages)

def startapp_remotes(remotes):
    br()
    p_yellow('I fond these StartApp repos:', align = "left")
    br()
    for remote in remotes:
        print("    {0} - {1}".format(green(remote['name']), remote['url']))

    br()
    p_yellow('If you want to use some of them you have to type:', align = "left")
    br()
    print("    startappsync --set-remote {0}".format(green("<remote-name>")))
    print("    startappsync --repo <repo/path> --set-remote {0}\n".format(green("<remote-name>")))
