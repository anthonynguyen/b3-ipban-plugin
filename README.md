B3 IP Ban Plugin for BigBrotherBot
=================================
**By clearskies**

## Description

Allows b3 to handle IP banning as opposed to the game. Also supports limiting the number of client connections from one IP address (might be buggy due to b3/parser issues).

This plugin works with the iourt41 parser, I'm not sure about any intricacies the other parsers may have.

### Installing the plugin

* Copy **ipban.py** into **b3/extplugins**
* Import **mapcycle.sql** into your b3 database
* Load the plugin in your **b3.xml** configuration file

### Banning People
This plugin will automatically add IPs of players who are permbanned to its database. To manually add an IP address or a range, use the !ipban (!ipb) command. For ranges, make sure all blocks are filled out, with the banned blocks replaced with asterisks (e.g. 127.0.*.*).