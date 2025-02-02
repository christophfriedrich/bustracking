-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:60032
-- Erstellungszeit: 30. Jan 2025 um 13:32
-- Server-Version: 10.6.19-MariaDB
-- PHP-Version: 8.2.20

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `chrfrd_bustracking`
--
CREATE DATABASE IF NOT EXISTS `chrfrd_bustracking` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `chrfrd_bustracking`;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `stopEvents`
--

CREATE TABLE `stopEvents` (
  `id` int(11) NOT NULL,
  `tripId` int(11) NOT NULL,
  `stopId` varchar(32) NOT NULL,
  `arrivalTimePlanned` datetime DEFAULT NULL,
  `departureTimePlanned` datetime DEFAULT NULL,
  `arrivalTimeEstimated` datetime DEFAULT NULL,
  `departureTimeEstimated` datetime DEFAULT NULL,
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `stops`
--

CREATE TABLE `stops` (
  `id` int(11) NOT NULL,
  `globalId` varchar(32) NOT NULL,
  `parentId` varchar(32) NOT NULL,
  `disassembledName` varchar(100) NOT NULL,
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `trips`
--

CREATE TABLE `trips` (
  `id` int(11) NOT NULL,
  `line` varchar(32) NOT NULL,
  `tripCode` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `departureTimePlanned` datetime NOT NULL,
  `arrivalTimePlanned` datetime NOT NULL,
  `completed` tinyint(1) NOT NULL DEFAULT 0,
  `created` datetime NOT NULL DEFAULT current_timestamp(),
  `updated` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `stopEvents`
--
ALTER TABLE `stopEvents`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tripId_stopId` (`tripId`,`stopId`);

--
-- Indizes für die Tabelle `stops`
--
ALTER TABLE `stops`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `globalId` (`globalId`);

--
-- Indizes für die Tabelle `trips`
--
ALTER TABLE `trips`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `line_tripCode_date` (`line`,`tripCode`,`date`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `stopEvents`
--
ALTER TABLE `stopEvents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `stops`
--
ALTER TABLE `stops`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `trips`
--
ALTER TABLE `trips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
