CREATE TABLE `chat_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(255) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `first_name` text NOT NULL,
  `user_name` text,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `chats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(255) NOT NULL,
  `first_name` text,
  `join_time` datetime NOT NULL DEFAULT (now()),
  `locales` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_id` (`chat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `pidor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `chat_id` (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `pidor_stats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(255) NOT NULL,
  `first_name` text,
  `user_id` varchar(255) NOT NULL,
  `stat` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `unibook` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) NOT NULL,
  `login` text NOT NULL,
  `password` text NOT NULL,
  `uni` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;