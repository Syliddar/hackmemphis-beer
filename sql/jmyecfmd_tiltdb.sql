SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `Beer` (
  `entry_id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `sg` decimal(8,4) NOT NULL,
  `temp` decimal(5,2) NOT NULL,
  `beer_name` tinytext CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `batch_id` tinytext CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL,
  PRIMARY KEY (`entry_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;