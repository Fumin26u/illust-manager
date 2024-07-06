-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- ホスト: 127.0.0.1
-- 生成日時: 2024-07-06 10:18:51
-- サーバのバージョン： 10.4.32-MariaDB
-- PHP のバージョン: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- データベース: `image_manager`
--

-- --------------------------------------------------------

--
-- テーブルの構造 `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `user_name` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(80) DEFAULT NULL,
  `uuid` binary(16) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `user_image`
--

CREATE TABLE `user_image` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `filename` varchar(80) NOT NULL,
  `delete_fg` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `user_image_tag`
--

CREATE TABLE `user_image_tag` (
  `id` bigint(20) NOT NULL,
  `user_image_id` bigint(20) NOT NULL,
  `tag_name` varchar(40) NOT NULL,
  `tag_name_jp` varchar(40) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `user_platform_account`
--

CREATE TABLE `user_platform_account` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `platform` enum('twitter','pixiv') NOT NULL,
  `platform_id` varchar(40) DEFAULT NULL COMMENT 'pfのIDを入れる。\r\n(例: twitterならtwitterのID)',
  `platform_password` varchar(255) DEFAULT NULL,
  `dl_count` int(11) NOT NULL DEFAULT 0 COMMENT '合計DL回数',
  `get_images_count` int(11) NOT NULL DEFAULT 0 COMMENT '合計取得画像枚数',
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- テーブルの構造 `user_platform_account_dl_log`
--

CREATE TABLE `user_platform_account_dl_log` (
  `id` int(11) NOT NULL,
  `user_platform_account_id` int(11) NOT NULL,
  `post_id` varchar(80) DEFAULT NULL,
  `filename` varchar(127) NOT NULL,
  `downloaded_at` datetime DEFAULT NULL,
  `delete_fg` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'comment: いるか分からない'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- ダンプしたテーブルのインデックス
--

--
-- テーブルのインデックス `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `user_image`
--
ALTER TABLE `user_image`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `user_image_tag`
--
ALTER TABLE `user_image_tag`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `user_platform_account`
--
ALTER TABLE `user_platform_account`
  ADD PRIMARY KEY (`id`);

--
-- テーブルのインデックス `user_platform_account_dl_log`
--
ALTER TABLE `user_platform_account_dl_log`
  ADD PRIMARY KEY (`id`);

--
-- ダンプしたテーブルの AUTO_INCREMENT
--

--
-- テーブルの AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `user_image`
--
ALTER TABLE `user_image`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `user_image_tag`
--
ALTER TABLE `user_image_tag`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `user_platform_account`
--
ALTER TABLE `user_platform_account`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- テーブルの AUTO_INCREMENT `user_platform_account_dl_log`
--
ALTER TABLE `user_platform_account_dl_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
