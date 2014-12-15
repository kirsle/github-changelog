# gitchangelog

This is a changelog generator for GitHub pull requests.

# Intended Use Case

You have a GitHub repository, maybe as part of an organization, and you have a
separate `master` (production-ready) and `develop` branch. Maybe a `staging`
branch too, but that's not important.

Your development cycle is that developers create feature branches for specific
bug tickets or new features, and merge them from their feature branch into the
`develop` branch.

At some point down the road, you merge `develop` into `master` to do your final
deployment. And you want that pull request to include a simple change log that
documents all of the pull requests that had gone into `develop` ever since the
*last* time you deployed into the `master` branch.

This script will enable you to do that. It will generate Markdown-formatted
text output listing the change log, in a format similar to this:

```text
Changes:

* #19 - Some other bug fixes - @alice
* #20 - Add a new feature - @bob
  * [Bugzilla #1234](https://bugzilla.example.com/bug/1234)
* #21 - Fix an internal server error - @alice
```

This script scans through all the closed pull requests in your repo and outputs
a list of changes *since* a given pull request issue number. So for example,
if your issue `#10` was your last `develop -> master` push, you'd start at
issue 10 and it would only scan through issues 11 and newer. You can also
specify an issue number to *stop* at.

It will also scan comments on a pull request and pull out any hyperlinks found
therein. So, if you use an external bug tracker like FogBugz or Bugzilla and
you link your GitHub issues to it in comments, this will pull those links out
and include them in the generated change log.

# Setup

It's recommended to make a virtualenv. This project depends on the following
modules available for installation via PyPI:

* pygithub3
* six

```bash
$ git clone https://github.com/kirsle/github-changelog
$ cd github-changelog
$ pip install -r requirements.txt
```

First you'll need to create a Personal Access Token on GitHub
(<https://github.com/settings/applications>), as this app will require it for
getting access to your repositories via the GitHub API. The default permissions
will do; it really only needs access to repositories.

Run the command `./gitchangelog.py --init` to initialize the settings with your
username and token (this step is optional if you don't want these saved to
disk, and will always use `--user` and `--token` command line options). The
`--init` option will simply save these settings to disk and exit. If you want
to change the settings in the future, run it with the `--init` option again.

It's recommended that you run it with `--init` first and enter *your* GitHub
username and access token. You can always override the `--user` option if you
need to query an organization's GitHub repo that you have access to.

# Quick Start

Now, to scan a repository's pull requests and generate a change log:

```bash
$ ./gitchangelog.py [--user ORG_NAME] --repo <repo name> --after <issue ID>
```

The repo name and start ID are required. The script will scan all of the repo's
**closed** pull requests, starting with the one that was closed *after* the
date that the `--after` option was closed on.

So, if you regularly merge from `develop` into `master`, and the *last* time you
did that, the pull request issue number was `#12`... you would provide the
option `--after 12` and all pull requests that were *closed* on a later date
than `#12` will be included.

You can provide the `--user` option to override the username used for the repo;
for example, if you have access to an organization and want to get a change log
of one of *their* repos, instead of one of your own. Your access token will
work for accessing organization repos that you have permissions for.

# Help

```
usage: gitchangelog [-h] [--debug] [--init] [--user USER] [--token TOKEN]
                    [--repo REPO] [--after AFTER] [--start START]
                    [--stop STOP]

optional arguments:
  -h, --help            show this help message and exit
  --debug, -d           Debug mode.
  --init, -i            Initialize the authentication settings ONLY. You can
                        use this to configure your default username and access
                        token without actually continuing with scanning a
                        repository's pull requests.
  --user USER, -u USER  Username to authenticate with in Github. If not
                        provided, you will be prompted for it and the setting
                        will be saved in ~/.config/gitchangelog or equivalent
                        for your system. If working with an organization, use
                        the org username.
  --token TOKEN, -t TOKEN
                        OAuth personal access token for authentication. If not
                        provided, you will be promtped for it and the setting
                        will be saved in ~/.config/gitchangelog or equivalent
                        for your system.
  --repo REPO, -r REPO  Repository to run the changelog for. Can either be a
                        single name, or in user/name format.
  --after AFTER, -a AFTER
                        Include all pull requests that were merged *after* the
                        date that this one was merged on. This is the simplest
                        option to use; just set `--after` to be the pull
                        request ID of your latest deployment pull request. All
                        PR's that were merged *after* that one was merged will
                        be included (you can use this instead of
                        --start/--stop)
  --start START, -s START
                        Issue number for the pull request you want to start
                        from. For example, if you occasionally do a merge from
                        'develop' to 'master', and you want a change log of
                        the pull requests merged from your last deploy, you'd
                        enter the issue number of the *last* merge from
                        develop to master.
  --stop STOP, -x STOP  Issue number to stop at (optional). The default is to
                        check all pull requests *after* the `--start` option.
                        Provide `--stop` to stop at a different number
                        instead.
```

# License

```
The MIT License (MIT)

Copyright (c) 2014 Noah Petherbridge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
