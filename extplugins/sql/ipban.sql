CREATE TABLE IF NOT EXISTS `ipbans` (
  `client_id` int(11) NOT NULL,
  `ip` varchar(16) NOT NULL,
  UNIQUE KEY `ip` (`ip`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `iprangebans` (
  `range` varchar(16) NOT NULL,
  UNIQUE KEY `range` (`range`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;