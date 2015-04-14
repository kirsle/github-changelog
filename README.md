# GitHub Changelog Generator

This is a changelog generator for GitHub pull requests. It works well with the
[git-flow](http://nvie.com/posts/a-successful-git-branching-model/) workflow
where you have a `master` branch for production and a `develop` branch for
development (it also works if you have a `staging` branch in there too).

This script can generate a pretty changelog for your "develop to production"
pull request which sums up *all* of the other pull requests that were merged
since your *last* production merge. Additionally, it scans all of the comments
in each pull request to extract links, so if you use an external issue tracking
system and you link to your ticket numbers (either in the pull request's message
or in a comment), it will be included in the generated changelog under that
pull request. Example:

```text
Changes:

* #19 - Some other bug fixes - @alice
* #20 - Add a new feature - @bob
  * [Bugzilla #1234](https://bugzilla.example.com/bug/1234)
* #21 - Fix an internal server error - @alice
  * [Bugzilla #1238](https://bugzilla.example.com/bug/1238)
```

GitHub will automatically link the issue numbers and author usernames, making it
easy to review what changes went into each pull request.

# Quick Start

It's recommended to make a virtualenv. See `requirements.txt` for a list of
PyPI dependencies if you want to install them globally using your package
manager.

```bash
$ git clone https://github.com/kirsle/github-changelog
$ cd github-changelog
$ pip install -r requirements.txt
$ ./gitchangelog.py --init
```

The init command will guide you through setting up GitHub access credentials.
You can use your GitHub username, or an organization name if you want it to
default to that instead (you can always override the username at run-time with
the `--user` option). The credentials are stored at `~/.config/gitchangelog`
and you can reconfigure them by running with the `--init` option again.

Now, to scan a repository's pull requests and generate a change log:

```bash
$ ./gitchangelog.py [--user ORG_NAME] --repo <repo name> --after <issue ID>
```

The repo name and issue ID are required. The script will scan all of the repo's
**closed** pull requests, starting with the one that was closed *after* the
date that the `--after` issue was closed on.

So, if you regularly merge from `develop` into `master`, and the *last* time you
did that, the pull request issue number was #12, you would provide the option
`--after 12` and all pull requests that were *closed* on a later date than #12
will be included.

You can provide the `--user` option to override the username used for the repo;
for example, if you have access to an organization and want to get a change log
of one of *their* repos, instead of one of your own. Your access token will
work for accessing organization repos that you have permissions for.

Shortcut options `-u`, `-r`, and `-a` may be used too:

```bash
$ ./gitchangelog.py [-u ORG_NAME] -r <repo name> -a <issue ID>
```

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
                        provided, you will be prompted for it and the setting
                        will be saved in ~/.config/gitchangelog or equivalent
                        for your system.
  --repo REPO, -r REPO  Repository to run the changelog for.
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
