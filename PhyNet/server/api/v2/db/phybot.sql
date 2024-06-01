SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

DROP TABLE IF EXISTS `gkeys`;
CREATE TABLE IF NOT EXISTS `gkeys` (
  `gkey` text COLLATE utf8_unicode_ci NOT NULL,
  `ogkey` text COLLATE utf8_unicode_ci NOT NULL,
  `relay` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `relays`;
CREATE TABLE IF NOT EXISTS `relays` (
  `relay_ip` text COLLATE utf8_unicode_ci NOT NULL,
  `relay_bots` int NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` text COLLATE utf8_unicode_ci NOT NULL,
  `password` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_unicode_ci;

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'root', 'a528e21133187fecdd0c8f5c583733cfe86e7b6e3857dcd5682f6f54fb17fcce8f9da13c8c90854741df8d096f3d415291a4f6b7f08028a47c6abc82a2ea760c');
COMMIT;