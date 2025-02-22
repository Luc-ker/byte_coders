-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 22, 2025 at 03:51 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `autorecieptapp`
--

-- --------------------------------------------------------

--
-- Table structure for table `groups`
--

CREATE TABLE `groups` (
  `GroupID` int(11) NOT NULL,
  `Name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `groups`
--

INSERT INTO `groups` (`GroupID`, `Name`) VALUES
(1, 'Home'),
(2, 'Prison');

-- --------------------------------------------------------

--
-- Table structure for table `groupsusers`
--

CREATE TABLE `groupsusers` (
  `UserID` int(11) DEFAULT NULL,
  `GroupID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `groupsusers`
--

INSERT INTO `groupsusers` (`UserID`, `GroupID`) VALUES
(1, 1),
(2, 1),
(3, 2),
(1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `item`
--

CREATE TABLE `item` (
  `ItemID` int(11) NOT NULL,
  `Name` varchar(40) DEFAULT NULL,
  `Price` decimal(4,2) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`ItemID`, `Name`, `Price`, `Quantity`) VALUES
(1, 'Milk', 1.30, 500),
(2, 'Bread', 1.25, 250),
(3, 'Rice', 0.95, 500);

-- --------------------------------------------------------

--
-- Table structure for table `shoppinglist`
--

CREATE TABLE `shoppinglist` (
  `ListID` int(11) NOT NULL,
  `GroupID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shoppinglist`
--

INSERT INTO `shoppinglist` (`ListID`, `GroupID`) VALUES
(1, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `shoppinglistitem`
--

CREATE TABLE `shoppinglistitem` (
  `ItemID` int(11) DEFAULT NULL,
  `ListID` int(11) DEFAULT NULL,
  `DaysRemaining` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shoppinglistitem`
--

INSERT INTO `shoppinglistitem` (`ItemID`, `ListID`, `DaysRemaining`) VALUES
(1, 1, 5),
(1, 2, 4),
(2, 1, 6),
(3, 2, 7);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `Firstname` varchar(30) DEFAULT NULL,
  `Lastname` varchar(30) DEFAULT NULL,
  `UserID` int(11) NOT NULL,
  `Username` varchar(30) DEFAULT NULL,
  `Password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`Firstname`, `Lastname`, `UserID`, `Username`, `Password`) VALUES
('Jon', 'Doe', 1, 'JDoe', '1234'),
('Amanda', 'Person', 2, 'APerson', 'qwerty'),
('Guy', 'Fawkes', 3, 'GFawkes', 'Gunpowder');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`GroupID`);

--
-- Indexes for table `groupsusers`
--
ALTER TABLE `groupsusers`
  ADD KEY `UserID` (`UserID`),
  ADD KEY `GroupID` (`GroupID`);

--
-- Indexes for table `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`ItemID`);

--
-- Indexes for table `shoppinglist`
--
ALTER TABLE `shoppinglist`
  ADD PRIMARY KEY (`ListID`),
  ADD KEY `FK_GroupID` (`GroupID`);

--
-- Indexes for table `shoppinglistitem`
--
ALTER TABLE `shoppinglistitem`
  ADD KEY `ItemID` (`ItemID`),
  ADD KEY `ListID` (`ListID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`UserID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `groupsusers`
--
ALTER TABLE `groupsusers`
  ADD CONSTRAINT `groupsusers_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`),
  ADD CONSTRAINT `groupsusers_ibfk_2` FOREIGN KEY (`GroupID`) REFERENCES `groups` (`GroupID`);

--
-- Constraints for table `shoppinglist`
--
ALTER TABLE `shoppinglist`
  ADD CONSTRAINT `FK_GroupID` FOREIGN KEY (`GroupID`) REFERENCES `groups` (`GroupID`);

--
-- Constraints for table `shoppinglistitem`
--
ALTER TABLE `shoppinglistitem`
  ADD CONSTRAINT `shoppinglistitem_ibfk_1` FOREIGN KEY (`ItemID`) REFERENCES `item` (`ItemID`),
  ADD CONSTRAINT `shoppinglistitem_ibfk_2` FOREIGN KEY (`ListID`) REFERENCES `shoppinglist` (`ListID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
