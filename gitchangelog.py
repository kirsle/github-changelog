#!/usr/bin/env python

"""gitchangelog: Generate a change log based on closed pull requests."""

import six
from six.moves import input
import sys
import os
import os.path
import json
import codecs
import argparse
import re
from pygithub3 import Github

class GithubChangelog(object):
    MARKDOWN_LINK = re.compile(r'\[(.+?)\]\((.+?)\)')

    def __init__(self, debug=False):
        self.debug = debug
        self.api   = None  # Github API object
        self.repo  = None  # Active repo name

    def main(self, args):
        """Entry point for running this module as an app."""
        self.debug = args.debug

        # The user's profile directory.
        self.profile = os.path.expanduser("~/.config")
        self.config  = os.path.join(self.profile, "gitchangelog")

        # Authenticate.
        self.authenticate(user=args.user, token=args.token, repo=args.repo,
            reset=args.init)

        # If not using --init, the repo name and start number are required.
        if not args.init:
            if not args.repo:
                die("The repository name (--repo) is required to continue.")
            if not args.start:
                die("The issue start number (--start) is required to continue.")
        else:
            sys.exit(0)

        self.repo = args.repo

        # Scan the pull requests.
        changes = self.scan_pulls(start=args.start, stop=args.stop)

        # Pretty print the result!
        six.print_("\nChanges:\n")
        six.print_("\n".join(changes))

    def authenticate(self, user=None, token=None, repo=None, reset=False):
        """Handle authentication with the GitHub API."""
        self.say("Authentication begin")
        save = False # Save settings to their config file.

        # Read settings from disk.
        if not user or not token:
            config = self.read_settings()
            if not user:
                user = config[0]
            if not token:
                token = config[1]

        # Resetting credentials?
        if reset:
            user = token = None

        # Username provided?
        if not user:
            save = True
            user = input("GitHub username> ")
            user = user.strip()
            if not user:
                die("Username is required for GitHub authentication.")

        # Token provided?
        if not token:
            save = True
            six.print_("This app will require a personal access token for\n" \
                    + "your GitHub account. Visit the URL below and create\n" \
                    + "a personal access token, and then paste that token\n" \
                    + "at the prompt below:\n" \
                    + "https://github.com/settings/applications\n")
            token = input("Personal access token> ")
            token = token.strip()
            if not token:
                die("Token is required for GitHub authentication.")

        # Saving the configuration?
        if save:
            # Create the profile directory, if necessary.
            if not os.path.isdir(self.profile):
                self.say("Creating config directory: {}".format(self.profile))
                os.mkdir(self.profile)
            self.save_settings(user, token)
            six.print_("Settings saved to {}".format(self.config))

        # Initialize the GitHub API object.
        self.api = Github(user=user, token=token, repo=repo)

    def scan_pulls(self, start, stop=None):
        """Scan closed pull requests starting from #start and optionally
        stopping at #stop."""
        six.print_("-- Scanning pull requests... --")

        changes = list()

        pulls = self.api.pull_requests.list(state="closed").all()
        for pull in pulls:
            # Skip pull requests outside our requested range.
            if stop and pull.number > stop:
                continue
            if pull.number <= start:
                continue

            # Add the pull request title to our change log.
            changes.append("* #{} - {} - @{}".format(
                pull.number, pull.title, pull.user.get("login")
            ))
            self.say("Found closed pull request: {}".format(changes[-1]))

            # Get the issue for it to look up the comments (cuz comments on
            # the pull object don't work???)
            comments = self.api.issues.comments.list(pull.number).all()
            for comment in comments:
                # Scan it for links.
                for match in re.findall(self.MARKDOWN_LINK, comment.body):
                    label, url = match
                    changes.append("  * [{}]({})".format(label, url))
                    self.say("Found link in comment: {}".format(changes[-1]))

        return changes

    def save_settings(self, user, token):
        """Save settings to disk."""
        fh = codecs.open(self.config, "w", "utf-8")
        fh.write(json.dumps(dict(
            user=user,
            token=token,
        )))
        fh.close()

    def read_settings(self):
        """Read settings from disk.

        Returns (user, token) or (None, None) if no setting file found."""
        if not os.path.isfile(self.config):
            return (None, None)
        fh = codecs.open(self.config, "r", "utf-8")
        data = json.loads(fh.read())
        fh.close()
        return (data.get("user"), data.get("token"))

    def say(self, message):
        """Print a debug message if debugging is on."""
        if self.debug:
            six.print_("DEBUG:", message)


def die(error):
    six.print_(error)
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("gitchangelog")
    parser.add_argument("--debug", "-d",
        help="Debug mode.",
        action="store_true",
    )
    parser.add_argument("--init", "-i",
        help="Initialize the authentication settings ONLY. You can use this " \
            + "to configure your default username and access token without " \
            + "actually continuing with scanning a repository's pull requests.",
        action="store_true",
    )
    parser.add_argument("--user", "-u",
        help="Username to authenticate with in Github. If not provided, you " \
            + "will be prompted for it and the setting will be saved in " \
            + "~/.config/gitchangelog or equivalent for your system. " \
            + "If working with an organization, use the org username.",
    )
    parser.add_argument("--token", "-t",
        help="OAuth personal access token for authentication. If not " \
            + "provided, you will be promtped for it and the setting will be " \
            + "saved in ~/.config/gitchangelog or equivalent for your system.",
    )
    parser.add_argument("--repo", "-r",
        help="Repository to run the changelog for. Can either be a single " \
            + "name, or in user/name format.",
    )
    parser.add_argument("--start", "-s",
        help="Issue number for the pull request you want to start from. " \
            + "For example, if you occasionally do a merge from 'develop' to " \
            + "'master', and you want a change log of the pull requests " \
            + "merged from your last deploy, you'd enter the issue number of " \
            + "the *last* merge from develop to master.",
        type=int,
    )
    parser.add_argument("--stop", "-x",
        help="Issue number to stop at (optional). The default is to check " \
            + "all pull requests *after* the `--start` option. Provide " \
            + "`--stop` to stop at a different number instead.",
        type=int,
    )
    args = parser.parse_args()

    github = GithubChangelog()
    github.main(args)
