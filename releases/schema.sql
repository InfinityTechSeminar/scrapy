-- phpMyAdmin SQL Dump
-- version 4.5.0.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 30, 2018 at 01:52 PM
-- Server version: 5.6.35
-- PHP Version: 7.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `stackoverflow`
--
CREATE DATABASE IF NOT EXISTS `stackoverflow` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `stackoverflow`;

-- --------------------------------------------------------

--
-- Table structure for table `answers`
--

CREATE TABLE IF NOT EXISTS `answers` (
  `id` varchar(50) CHARACTER SET latin1 NOT NULL COMMENT 'commit gid',
  `data` longtext CHARACTER SET latin1 NOT NULL COMMENT 'commit json data',
  `created` int(10) UNSIGNED NOT NULL COMMENT 'commit created time',
  `updated` int(10) UNSIGNED NOT NULL COMMENT 'commit updated time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE IF NOT EXISTS `questions` (
  `id` varchar(50) CHARACTER SET latin1 NOT NULL COMMENT 'pullrequest gid',
  `data` longtext CHARACTER SET latin1 NOT NULL COMMENT 'pullrequest json data',
  `created` int(10) UNSIGNED NOT NULL COMMENT 'pullrequest created time',
  `updated` int(10) UNSIGNED NOT NULL COMMENT 'pullrequest updated time',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
