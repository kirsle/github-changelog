# Revision history for github-changelog

* `1.05`  Jun 10, 2015
    * Add `--gitflow` option which prevents enumerating links from pull requests
      destined for the `master` or `staging` branches (also `stage`).

* `1.04`  Jun  9, 2015
    * Skip pull requests that were closed without being merged.

* `1.03`  May  4, 2015
    * Scan for HTML `<a>` style links in addition to Markdown style.

* `1.02`  Dec 17, 2014
    * Fix the date comparison including the given --after issue in the results.
    * Try to reduce redundant changelogs from other merge commits.

* `1.01`  Dec 15, 2014
    * Add the `--after` option as the new preferred way to generate change logs.

* `1.00`  Dec 10, 2014
    * Initial release of github-changelog.
