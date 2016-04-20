"""
This package contains the logic for scanning sub-Reddits and reporting stats
for each. The modules within roughly correspond to different categories of
stats. The only exception is the `common` sub-module, which has some utility
functions that the other sub-modules use.

.. tip:: When developing new stats that use Reddit API calls, be mindful of rate
    limiting!
"""
# The sub-modules in here are purely organizational. You'll want to import
# and use the stuff exposed below through this sr_scanner module.
from techsubs.sr_scanner.post_stats import calc_and_send_subreddit_post_stats  # noqa
from techsubs.sr_scanner.basic_stats import calc_and_send_basic_subreddit_stats  # noqa
