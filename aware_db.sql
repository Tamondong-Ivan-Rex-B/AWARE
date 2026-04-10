-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 10, 2026 at 08:22 AM
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
-- Database: `aware_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `class_schedule`
--

CREATE TABLE `class_schedule` (
  `Schedule_ID` int(11) NOT NULL,
  `Course_Code` varchar(20) DEFAULT NULL,
  `Room_Name` varchar(50) DEFAULT NULL,
  `Schedule_Day` varchar(20) DEFAULT NULL,
  `Start_Time` time DEFAULT NULL,
  `End_Time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `class_session`
--

CREATE TABLE `class_session` (
  `Session_ID` int(11) NOT NULL,
  `Course_Code` varchar(20) DEFAULT NULL,
  `Session_Date` date DEFAULT NULL,
  `Topic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `class_session`
--

INSERT INTO `class_session` (`Session_ID`, `Course_Code`, `Session_Date`, `Topic`) VALUES
(1, 'CPE111', '2026-04-10', 'Introduction to Microcontrollers'),
(2, 'CPE111', '2026-04-17', 'Logic Gates and Boolean Algebra'),
(3, 'CPE111', '2026-04-24', 'ESP32 and Relay Modules');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `Course_Code` varchar(20) NOT NULL,
  `Professor_ID` int(11) DEFAULT NULL,
  `Course_Title` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`Course_Code`, `Professor_ID`, `Course_Title`) VALUES
('CPE111', 101, 'Internet of Things');

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

CREATE TABLE `enrollment` (
  `Enrollment_ID` int(11) NOT NULL,
  `Student_ID` int(11) DEFAULT NULL,
  `Course_Code` varchar(20) DEFAULT NULL,
  `Academic_Year` varchar(10) DEFAULT NULL,
  `Semester` int(11) DEFAULT NULL,
  `Current_Grade` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `evaluation`
--

CREATE TABLE `evaluation` (
  `Evaluation_ID` int(11) NOT NULL,
  `Session_ID` int(11) DEFAULT NULL,
  `Student_ID` int(11) DEFAULT NULL,
  `Clarity_Score` int(11) DEFAULT NULL,
  `Pacing_Score` int(11) DEFAULT NULL,
  `Comprehension_Score` int(11) DEFAULT NULL,
  `Engagement_Score` int(11) DEFAULT NULL,
  `Confusing_Point` text DEFAULT NULL,
  `Study_Hours` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `evaluation`
--

INSERT INTO `evaluation` (`Evaluation_ID`, `Session_ID`, `Student_ID`, `Clarity_Score`, `Pacing_Score`, `Comprehension_Score`, `Engagement_Score`, `Confusing_Point`, `Study_Hours`) VALUES
(1, 1, 2024001, 5, 3, 3, 3, '', NULL),
(2, 1, 2024001, 5, 3, 3, 3, '', NULL),
(3, 1, 2024001, 5, 3, 3, 3, '', NULL),
(4, 1, 2024001, 5, 3, 3, 3, '', NULL),
(5, 1, 2024001, 5, 3, 3, 3, '', NULL),
(6, 2, 2024001, 3, 3, 3, 3, '', NULL),
(7, 1, 2024001, 3, 3, 3, 3, '', NULL),
(8, 1, 2024001, 3, 3, 3, 3, '', 8);

-- --------------------------------------------------------

--
-- Table structure for table `guardian`
--

CREATE TABLE `guardian` (
  `Guardian_ID` int(11) NOT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guardian`
--

INSERT INTO `guardian` (`Guardian_ID`, `First_Name`, `Last_Name`) VALUES
(1001, 'Roberto', 'Dela Cruz'),
(1002, 'Maria', 'Santos');

-- --------------------------------------------------------

--
-- Table structure for table `professor`
--

CREATE TABLE `professor` (
  `Professor_ID` int(11) NOT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL,
  `Department` varchar(100) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `professor`
--

INSERT INTO `professor` (`Professor_ID`, `First_Name`, `Last_Name`, `Department`, `Username`, `Password`) VALUES
(101, 'Rudo', 'Surebrec', 'Computer Engineering', 'alovelace', 'password123'),
(102, 'Ada', 'Lovelace', 'Computer Engineering', 'aturing', 'password123'),
(103, 'Alan', 'Turing', 'Mathematics', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `Student_ID` int(11) NOT NULL,
  `Guardian_ID` int(11) DEFAULT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL,
  `Program` varchar(50) DEFAULT NULL,
  `Year_Level` int(11) DEFAULT NULL,
  `Username` varchar(50) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`Student_ID`, `Guardian_ID`, `First_Name`, `Last_Name`, `Program`, `Year_Level`, `Username`, `Password`) VALUES
(2024001, 1001, 'Miguel', 'Dela Cruz', 'BSCpE', 2, 'mdelacruz', 'password123'),
(2024002, 1002, 'Sofia', 'Santos', 'BSCS', 2, 'ssantos', 'password123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `class_schedule`
--
ALTER TABLE `class_schedule`
  ADD PRIMARY KEY (`Schedule_ID`),
  ADD KEY `Course_Code` (`Course_Code`);

--
-- Indexes for table `class_session`
--
ALTER TABLE `class_session`
  ADD PRIMARY KEY (`Session_ID`),
  ADD KEY `Course_Code` (`Course_Code`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`Course_Code`),
  ADD KEY `Professor_ID` (`Professor_ID`);

--
-- Indexes for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD PRIMARY KEY (`Enrollment_ID`),
  ADD KEY `Student_ID` (`Student_ID`),
  ADD KEY `Course_Code` (`Course_Code`);

--
-- Indexes for table `evaluation`
--
ALTER TABLE `evaluation`
  ADD PRIMARY KEY (`Evaluation_ID`),
  ADD KEY `Session_ID` (`Session_ID`),
  ADD KEY `Student_ID` (`Student_ID`);

--
-- Indexes for table `guardian`
--
ALTER TABLE `guardian`
  ADD PRIMARY KEY (`Guardian_ID`);

--
-- Indexes for table `professor`
--
ALTER TABLE `professor`
  ADD PRIMARY KEY (`Professor_ID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`Student_ID`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD KEY `Guardian_ID` (`Guardian_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `class_schedule`
--
ALTER TABLE `class_schedule`
  MODIFY `Schedule_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `class_session`
--
ALTER TABLE `class_session`
  MODIFY `Session_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `enrollment`
--
ALTER TABLE `enrollment`
  MODIFY `Enrollment_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `evaluation`
--
ALTER TABLE `evaluation`
  MODIFY `Evaluation_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `class_schedule`
--
ALTER TABLE `class_schedule`
  ADD CONSTRAINT `class_schedule_ibfk_1` FOREIGN KEY (`Course_Code`) REFERENCES `course` (`Course_Code`);

--
-- Constraints for table `class_session`
--
ALTER TABLE `class_session`
  ADD CONSTRAINT `class_session_ibfk_1` FOREIGN KEY (`Course_Code`) REFERENCES `course` (`Course_Code`);

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`Professor_ID`) REFERENCES `professor` (`Professor_ID`);

--
-- Constraints for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`Student_ID`) REFERENCES `student` (`Student_ID`),
  ADD CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`Course_Code`) REFERENCES `course` (`Course_Code`);

--
-- Constraints for table `evaluation`
--
ALTER TABLE `evaluation`
  ADD CONSTRAINT `evaluation_ibfk_1` FOREIGN KEY (`Session_ID`) REFERENCES `class_session` (`Session_ID`),
  ADD CONSTRAINT `evaluation_ibfk_2` FOREIGN KEY (`Student_ID`) REFERENCES `student` (`Student_ID`);

--
-- Constraints for table `student`
--
ALTER TABLE `student`
  ADD CONSTRAINT `student_ibfk_1` FOREIGN KEY (`Guardian_ID`) REFERENCES `guardian` (`Guardian_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
