-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 12, 2026 at 10:54 AM
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
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Admin_ID` int(11) NOT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`Admin_ID`, `First_Name`, `Last_Name`, `Username`, `Password`) VALUES
(1, 'System', 'Administrator', 'admin', 'scrypt:32768:8:1$2DwG0f6mzua1GvD3$4f96a7158d8ff625bb725b4df3ebc7492a3bb7b4670214aa688f5bc7b6fdbb274c98b6fa8abd0457b66733c048ba8b5e114f1fe2a10bd0e764977fbfa655b8ef');

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

--
-- Dumping data for table `class_schedule`
--

INSERT INTO `class_schedule` (`Schedule_ID`, `Course_Code`, `Room_Name`, `Schedule_Day`, `Start_Time`, `End_Time`) VALUES
(1, 'CPE111', 'Q304', 'Monday', '07:30:00', '09:00:00'),
(2, 'CPE011', 'Q502', 'Tuesday', '09:00:00', '12:00:00'),
(3, 'CS201', 'Q910', 'Wednesday', '13:00:00', '15:00:00'),
(4, 'MATH101', 'Q301', 'Thursday', '15:30:00', '17:00:00'),
(5, 'CPE111', 'Q511', 'Friday', '18:00:00', '20:30:00'),
(6, 'CPE011', 'Q905', 'Monday', '10:30:00', '13:30:00'),
(7, 'CS201', 'Q308', 'Tuesday', '14:00:00', '16:00:00'),
(8, 'MATH101', 'Q507', 'Wednesday', '08:00:00', '09:30:00'),
(9, 'CPE111', 'Q915', 'Thursday', '19:00:00', '21:30:00'),
(10, 'CPE011', 'Q312', 'Tuesday', '11:00:00', '14:00:00'),
(11, 'CPE011', 'Q5555', 'Friday', '10:30:00', '12:30:00'),
(12, 'MATH101', 'Q3241', 'Wednesday', '07:30:00', '08:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `class_session`
--

CREATE TABLE `class_session` (
  `Session_ID` int(11) NOT NULL,
  `Course_Code` varchar(20) DEFAULT NULL,
  `Session_Date` date DEFAULT NULL,
  `Topic` varchar(255) DEFAULT NULL,
  `Professor_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `class_session`
--

INSERT INTO `class_session` (`Session_ID`, `Course_Code`, `Session_Date`, `Topic`, `Professor_ID`) VALUES
(1, 'CPE111', '2026-04-10', 'Introduction to Microcontrollers', 101),
(2, 'CPE111', '2026-04-17', 'Logic Gates and Boolean Algebra', 101),
(3, 'CPE111', '2026-04-24', 'ESP32 and Relay Modules', 101),
(4, 'CPE112', '2026-04-12', 'Boolean Algebra and Logic Gates', 102),
(5, 'CPE112', '2026-04-19', 'K-map Simplification', 102),
(6, 'CPE112', '2026-04-26', 'Combinational Circuits: Encoders & 7-Segment Decoders', 102),
(7, 'CPE113', '2026-04-13', 'OSI Model and Network Topologies', 101),
(8, 'CPE113', '2026-04-20', 'IPv4 Addressing and FLSM', 101),
(9, 'CPE113', '2026-04-27', 'Advanced Subnetting and VLSM', 101),
(10, 'CPE114', '2026-04-14', 'Introduction to Microprocessors & DOSBox', 102),
(11, 'CPE114', '2026-04-21', 'Registers and Memory Addressing', 102),
(12, 'CPE114', '2026-04-28', 'String Operations and User Input', 102),
(13, 'CS201', '2026-04-15', 'Relational Algebra & SQL Basics', 105),
(14, 'CS201', '2026-04-22', 'Advanced JOINs and Subqueries', 105),
(15, 'CS201', '2026-04-29', 'Database Normalization (1NF to 3NF)', 105),
(16, 'MATH201', '2026-04-16', 'Introduction to Optimization Models', 103),
(17, 'MATH201', '2026-04-23', 'Graphical Method Solutions', 103),
(18, 'MATH201', '2026-04-30', 'Solving Models via the Simplex Method', 103);

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `Course_Code` varchar(20) NOT NULL,
  `Course_Title` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`Course_Code`, `Course_Title`) VALUES
('CPE011', 'Logic Circuits and Design'),
('CPE021', 'Computer Architecture and Organization'),
('CPE021A', 'Computer Organization with Assembly'),
('CPE111', 'Internet of Things'),
('CPE112', 'Digital Logic Design'),
('CPE113', 'Computer Networks'),
('CPE114', 'Assembly Language Programming'),
('CS201', 'Database Management Systems'),
('CS202', 'Data Structures'),
('MATH101', 'Calculus 1'),
('MATH201', 'Linear Programming');

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

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` (`Enrollment_ID`, `Student_ID`, `Course_Code`, `Academic_Year`, `Semester`, `Current_Grade`) VALUES
(1, 2024003, 'CPE111', '2025-2026', 2, 92.50),
(2, 2024004, 'CPE011', '2025-2026', 2, 88.00),
(3, 2024005, 'CS201', '2025-2026', 2, 95.00),
(4, 2024006, 'CPE111', '2025-2026', 2, 89.50),
(5, 2024007, 'MATH101', '2025-2026', 2, 78.00),
(6, 2024008, 'CPE011', '2025-2026', 2, 91.00),
(7, 2024009, 'CS201', '2025-2026', 2, 85.50),
(8, 2024010, 'CPE111', '2025-2026', 2, 94.00),
(9, 2024011, 'MATH101', '2025-2026', 2, 82.00),
(10, 2024012, 'CPE011', '2025-2026', 2, 90.00),
(11, 2024005, 'MATH101', '2025-2026', 2, 76.00);

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
  `Additional_Comments` text DEFAULT NULL,
  `Study_Hours` int(11) DEFAULT NULL,
  `Submission_Date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `evaluation`
--

INSERT INTO `evaluation` (`Evaluation_ID`, `Session_ID`, `Student_ID`, `Clarity_Score`, `Pacing_Score`, `Comprehension_Score`, `Engagement_Score`, `Additional_Comments`, `Study_Hours`, `Submission_Date`) VALUES
(1, 1, 2024001, 5, 3, 3, 3, '', NULL, '2026-04-11 21:43:47'),
(2, 1, 2024001, 5, 3, 3, 3, '', NULL, '2026-04-11 21:43:47'),
(3, 1, 2024001, 5, 3, 3, 3, '', NULL, '2026-04-11 21:43:47'),
(4, 1, 2024001, 5, 3, 3, 3, '', NULL, '2026-04-11 21:43:47'),
(5, 1, 2024001, 5, 3, 3, 3, '', NULL, '2026-04-11 21:43:47'),
(6, 2, 2024001, 3, 3, 3, 3, '', NULL, '2026-04-11 21:43:47'),
(7, 1, 2024001, 3, 3, 3, 3, '', NULL, '2026-04-11 21:43:47'),
(8, 1, 2024001, 3, 3, 3, 3, '', 8, '2026-04-11 21:43:47'),
(9, 2, 2024001, 1, 1, 1, 1, 'testing', 67, '2026-04-11 21:43:47'),
(10, 11, 2024002, 5, 4, 3, 2, 'hahahaha', 143, '2026-04-11 21:43:47'),
(11, 18, 2024002, 5, 2, 4, 1, '4:46pm', 4, '2026-04-11 21:43:47'),
(12, 14, 2024003, 1, 1, 1, 1, '9:28', 12, '2026-04-11 21:43:47'),
(13, 7, 2024003, 5, 4, 2, 1, 'try', 11, '2026-04-11 21:43:47'),
(14, 5, 2024003, 5, 5, 5, 5, 'pls', 67, '2026-04-11 22:04:32'),
(15, 1, 2024003, 3, 3, 3, 3, 'week 13', 0, '2026-03-26 00:00:00'),
(16, 15, 2024003, 4, 2, 3, 1, 'Now Working!', 5, '2026-04-12 00:32:51'),
(17, 15, 2024003, 1, 1, 1, 1, '', 2, '2026-04-12 11:52:39'),
(19, 15, 2024003, 4, 4, 4, 4, 'does this still works', 3, '2026-04-12 16:41:22');

-- --------------------------------------------------------

--
-- Table structure for table `guardian`
--

CREATE TABLE `guardian` (
  `Guardian_ID` int(11) NOT NULL,
  `First_Name` varchar(50) DEFAULT NULL,
  `Last_Name` varchar(50) DEFAULT NULL,
  `Contact_Number` varchar(50) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guardian`
--

INSERT INTO `guardian` (`Guardian_ID`, `First_Name`, `Last_Name`, `Contact_Number`, `Email`) VALUES
(1001, 'Roberto', 'Dela Cruz', NULL, NULL),
(1002, 'Maria', 'Santos', NULL, NULL),
(1003, 'Jose', 'Rizal', NULL, NULL),
(1004, 'Andres', 'Bonifacio', NULL, NULL),
(1005, 'Emilio', 'Aguinaldo', '09111111121', 'apolinario.com'),
(1006, 'Apolinario', 'Mabini', NULL, NULL),
(1007, 'Marcelo', 'Del Pilar', NULL, NULL),
(1008, 'Juan', 'Luna', NULL, NULL),
(1009, 'Melchora', 'Aquino', NULL, NULL),
(1010, 'Gabriela', 'Silang', NULL, NULL),
(1011, 'Antonio', 'Luna', NULL, NULL),
(1012, 'Emilio', 'Jacinto', NULL, NULL);

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
(101, 'Rudo', 'Surebrec', 'Computer Engineering', 'rsuberec', 'scrypt:32768:8:1$tyS2oO1wNPIlq4m4$4abca336f51210b42da5f4b2442ae2868effb04c5fbfbc6ae60dda53e96eff147149967efce4e1cb11be68641e08ac9f97c9ae1ec6541a24fdbce0f6dfc7ba4a'),
(102, 'Ada', 'Lovelace', 'Computer Engineering', 'aalovelace', 'scrypt:32768:8:1$MrOP2Qo9G31N9ttJ$2155bbb6c42b74cac7c7eda66f93f6883700a2ff0a437398b83d0bd636aa6db503a8930fd8e4df7784f0b76861443939ac8db63b71df24dbb41a8b45035f6a2f'),
(103, 'Alan', 'Turing', 'Mathematics', 'aturing', 'scrypt:32768:8:1$Vx216X7xDsEtcMPZ$1443606bddb00b33a577ca9c6fe47a76809a4e5bf41b3f0cfb0774d9b5a7e274cd8e248516153e45b2a312e4f6878befeb6c381f21a75a29bef9633b44074ebd'),
(104, 'Grace', 'Hopper', 'Computer Engineering', 'ghopper', 'scrypt:32768:8:1$DDiOeySV3Xm2jzVP$0aef26ede2c3ec31b660f92c3e83ef60c0cf5d084ddfc9094d676e94e04de8fb5285e64591aaba0bfd8c5bd41df339e80816ecb2d229225649e609f792419cdc'),
(105, 'Tim', 'Berners-Lee', 'Computer Science', 'tlee', 'scrypt:32768:8:1$lN7eGDIbTnDj7Y2a$8c9332f4763010cdfb2b1c034ab68c4a3dcfecd780490f8ab66bbcdd11cc5a868ee42ff50a8a087abe2ac08acdbbab15d530a142a6b94fa167bab7440d8fc8d5'),
(106, 'Linus', 'Tech Tips', 'Computer Engineering', 'ltt', 'scrypt:32768:8:1$QkU5Zh1FN6LqGNYz$3d3671a051e4674e5b2aa6e648c164903e0ca84cffa6ccab863c519c676a8fff35ce49a59f5c0408d09646e1ad51d9caac9a830c70143d26687b3b9a7a05ba4a'),
(107, 'Dennis', 'Ritchie', 'Computer Science', 'dritchie', 'scrypt:32768:8:1$eCZSYi13lZxpWxDR$8e52a6259f97c2990e0b21817595a88745e40076335993bd46a0e13ca1444b2e22dfef2215b652a6a5f8a9ea03f456b4807670c4589831351e323c93a2ea6b18'),
(108, 'Ken', 'Thompson', 'Computer Science', 'kthompson', 'scrypt:32768:8:1$bXjbQEvFsxcoZ0qs$5b56f7dc60624bdcbed26bebc6a910491249b6b4f559e608649f04250ff159323a557281e57321ed2a9e854b68227c65081dfc44bcdf9a5ad09421ae95e65691'),
(109, 'Bjarne', 'Stroustrup', 'Computer Engineering', 'bstroustrup', 'scrypt:32768:8:1$wXSUtGjbk6QYkGho$fe5876fae0b273bdf71544a1b23006412b1fdaeb73a5c01c18eb09c36d28cb092374ad35917a3ded90bcc571ed36e32a82bbfcaa8d6defc3a9935c103bd66474'),
(110, 'James', 'Gosling', 'Computer Science', 'jgosling', 'scrypt:32768:8:1$w1DqEnRWTGz0Ovfz$a5a252b977309b6673ac2b1a0c560640fdce53a0fd846dfce64da6b76809e2ccbeaf95bb5f22a7d290fd0df368bf57d56924db348dead6de16597b33dff26708'),
(111, 'Guido', 'van Rossum', 'Computer Science', 'grossum', 'scrypt:32768:8:1$bvmXY9xJdfjqduf6$ccc2ebb0eea4553530aa57ec68d616305bbea5a4458bd9204891825ffeed2cd57f0a5969fa46e0a46aa4ec5e72bcffba0764566224e89a4a00e31edd13078abf'),
(112, 'Margaret', 'Hamilton', 'Computer Engineering', 'mhamilton', 'scrypt:32768:8:1$eiJCGIn93XKH1shd$3bd9b26bd86db8f8a57e83b7431e3652afc3ca38278ff113bd78e36656b9a2e5951802cb860606fe37324f0d057b1f8e2f0a4cae43ae57e8918bb810203e5a4a'),
(113, 'Katherine', 'Johnson', 'Mathematics', 'kjohnson', 'scrypt:32768:8:1$Lw14VAYmPbfHqJgI$8a7348d2b2844ad0d59438a4fb60baeeb2c71fae5c4dab76f7fb92ac9fff623368224a78320d9c06c492fcb615b9867cd58334b0b7fc9aaac2271d6ee06cef35');

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
(2024001, 1001, 'Miguel', 'Dela Cruz', 'BSCpE', 2, 'mdelacruz', 'scrypt:32768:8:1$wALyS086CCHLULE7$23a7c354d50c2326467421ffb0043f81138ee0f29dcd91c078b1b617c6a68f2255820b30e669b8abe9b64a7af8d9f1b8fa2b56398a95edf320be2b03cadff854'),
(2024002, 1002, 'Sofia', 'Santos', 'BSCS', 2, 'ssantos', 'scrypt:32768:8:1$MSliJO8eLcD6jHhY$e92474ac335a2ce0e8773a9d5bd95a351ddc1eb0c1e158544227a17582135e03a98db76280dbaf84b68f569717872ec5bc3f4745bfc2178d2d6709891c07a630'),
(2024003, 1003, 'Juan', 'Dela Cruz', 'BSCpE', 2, 'jcruz', 'scrypt:32768:8:1$lxMUkU2KTADCQ11w$9866b939f73b5b7ac30835ab0104728c10b652c9e4f52e88bf86ca9969bfe4cebbcffa3555c1e55125c78345fd0cb8f871c3dbd71836dce623e81bd465124a2b'),
(2024004, 1004, 'Maria', 'Clara', 'BSCpE', 2, 'mclara', 'scrypt:32768:8:1$ycpSftw2bN3FxKT8$028a2c4a0c42cd73e2c1a27c96a64043d2455c1c6012fb093b72b4244a9670d0d03859fd6ab047c7da3c9914e271dae6f5c4e0bdf4b144441245fc304be1d030'),
(2024005, 1005, 'Pedro', 'Penduko', 'BSCS', 1, 'ppenduko', 'scrypt:32768:8:1$Mx5jP0oMtUoCfo7u$f64c24b9828dd282c79d724581c1a898ca546722e4199c8b3e25ee39f871f82282e030899cf4b395089562c25dadd9ebafbc81c1e479850b16c39df1571a6139'),
(2024006, 1006, 'Ana', 'Roces', 'BSCpE', 3, 'aroces', 'scrypt:32768:8:1$KAg0V84hkdQ66XLU$1f8e0b6f7b401f5ddb2e93a376159783489969d05514675f12ef9db4b21c95b55b577c28dd1edd0834ac2e5dd89424e719198ac2eaa7880e5a9b5d79d4e704c3'),
(2024007, 1007, 'Luis', 'Manzano', 'BSCS', 2, 'lmanzano', 'scrypt:32768:8:1$rFQf5kxFaAnMr5Ku$4ab8832738e46bc99be555ba6e09ecf96c4c3fc74c6146933a13136d124d4cd60995118d3c2f7cda573f57c8fca8c4aeea1537944c5cef7a91191cfbaf2bc6f2'),
(2024008, 1008, 'Carmen', 'Rosales', 'BSCpE', 4, 'crosales', 'scrypt:32768:8:1$kQjFyZculCRiF7uJ$0a7531a90729428f2253cef0c9cc01f92908e2938989f4ed9401cbb5931cdd56394417488b1ea61ee38a66d96c0acb459b16789b2140cce378fb8dd2a25a6feb'),
(2024009, 1009, 'Fernando', 'Poe', 'BSCS', 1, 'fpoe', 'scrypt:32768:8:1$JAzmGANwhS334DVm$d7350ca00e902980ab4dd1a6d1c8b8dafe42ae422b0ad74fbbbb32769889fcd9607c92ea0658031ff14b589be23d835e99c92cf016c87e9013d92d1d0f8fe362'),
(2024010, 1010, 'Gloria', 'Romero', 'BSCpE', 3, 'gromero', 'scrypt:32768:8:1$hFssoSZ7bcrpGNy1$83c59e416b06bebba143db0ecc9f31da057725d8afa88e8c1ec9388a81f1f93b9935c0e07800ff7a94da8fbafc679d8cbac2f034ac2f0f470e07256c2038edfe'),
(2024011, 1011, 'Ramon', 'Revilla', 'BSCS', 4, 'rrevilla', 'scrypt:32768:8:1$R7Uydk0guP1MvG1B$91fb57ac8ec97be6a66e3f929f7fd76e38f0c3261fd28adde6b9f5c4baa2978318708a8e8a67d6c0154ef493b45691db62038d745c32a8a9ee86a5046abda1a6'),
(2024012, 1012, 'Susan', 'Roces', 'BSCpE', 2, 'sroces', 'scrypt:32768:8:1$Ij2MCWGxdDNnue3l$7d22a160d21236095d6f85719452ce2a27228607fc01b0873301e81d540e84ab998eb50bab84dc8cb243de19595bfb9a82110e506e85ff257d81ea4b46c72d96');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Admin_ID`),
  ADD UNIQUE KEY `Username` (`Username`);

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
  ADD KEY `Course_Code` (`Course_Code`),
  ADD KEY `class_session_prof_fk` (`Professor_ID`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`Course_Code`);

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
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `Admin_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `class_schedule`
--
ALTER TABLE `class_schedule`
  MODIFY `Schedule_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `class_session`
--
ALTER TABLE `class_session`
  MODIFY `Session_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `enrollment`
--
ALTER TABLE `enrollment`
  MODIFY `Enrollment_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `evaluation`
--
ALTER TABLE `evaluation`
  MODIFY `Evaluation_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
  ADD CONSTRAINT `class_session_ibfk_1` FOREIGN KEY (`Course_Code`) REFERENCES `course` (`Course_Code`),
  ADD CONSTRAINT `class_session_prof_fk` FOREIGN KEY (`Professor_ID`) REFERENCES `professor` (`Professor_ID`);

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
