CREATE TABLE IF NOT EXISTS `dhs` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `time` float(11) NOT NULL,
  `count` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS `shs` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `time` float(11) NOT NULL,
  `count` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS `dleaderboard` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `type` int(1) NOT NULL,
  `time` float(11) NOT NULL,
  `count` int(11) NOT NULL,
  `rank` int(11) NOT NULL DEFAULT -1,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS `sleaderboard` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `type` int(1) NOT NULL,
  `time` float(11) NOT NULL,
  `count` int(11) NOT NULL,
  `rank` int(11) NOT NULL DEFAULT -1,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS `gtracker` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `type` int(1) NOT NULL,
  `seed` varchar(20),
  `completed` float(11) NOT NULL,
  `count` int(11) NOT NULL,
  `date` varchar(20) NOT NULL,
  `time` float(11) NOT NULL
);
CREATE TABLE IF NOT EXISTS `daily` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `type` int(1) NOT NULL,
  `time` float(11) NOT NULL,
  `count` int(11) NOT NULL,
  `rank` int(11) NOT NULL DEFAULT -1,
  `points` int(11) NOT NULL DEFAULT -1
);
CREATE TABLE IF NOT EXISTS `monthly` (
  `user_id` varchar(20) NOT NULL,
  `server_id` varchar(20) NOT NULL,
  `time` float(11) NOT NULL,
  `count` int(11) NOT NULL,
  `rank` int(11) NOT NULL DEFAULT -1,
  `points` int(11) NOT NULL DEFAULT -1
);