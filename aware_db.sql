-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: mysql-c9ec3ac-aware-system.b.aivencloud.com    Database: aware_db
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '88e46cca-364f-11f1-a9f6-92d4f443bfc5:1-109,
f48ccc7e-376c-11f1-9130-3208d8f094f1:1-143';

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `Admin_ID` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Username` varchar(100) NOT NULL,
  `Password` varchar(255) NOT NULL,
  PRIMARY KEY (`Admin_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'System','Administrator','admin','scrypt:32768:8:1$2DwG0f6mzua1GvD3$4f96a7158d8ff625bb725b4df3ebc7492a3bb7b4670214aa688f5bc7b6fdbb274c98b6fa8abd0457b66733c048ba8b5e114f1fe2a10bd0e764977fbfa655b8ef');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_schedule`
--

DROP TABLE IF EXISTS `class_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_schedule` (
  `Schedule_ID` int NOT NULL AUTO_INCREMENT,
  `Course_Code` varchar(50) NOT NULL,
  `Room_Name` varchar(100) DEFAULT NULL,
  `Schedule_Day` varchar(20) DEFAULT NULL,
  `Start_Time` time DEFAULT NULL,
  `End_Time` time DEFAULT NULL,
  PRIMARY KEY (`Schedule_ID`),
  KEY `class_schedule_course_FK` (`Course_Code`),
  CONSTRAINT `class_schedule_course_FK` FOREIGN KEY (`Course_Code`) REFERENCES `course` (`Course_Code`)
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_schedule`
--

LOCK TABLES `class_schedule` WRITE;
/*!40000 ALTER TABLE `class_schedule` DISABLE KEYS */;
INSERT INTO `class_schedule` VALUES (1,'CPE111','Q3046','Monday','07:30:00','09:00:00'),(2,'CPE011','Q5022','Tuesday','09:00:00','12:00:00'),(3,'CS201','Q9210','Wednesday','13:00:00','15:00:00'),(4,'MATH101','Q301','Thursday','15:30:00','17:00:00'),(5,'CPE111','Q5112','Friday','18:00:00','20:30:00'),(6,'CPE011','Q9305','Monday','10:30:00','13:30:00'),(7,'CS201','Q308','Tuesday','14:00:00','16:00:00'),(8,'MATH101','Q5507','Wednesday','08:00:00','09:30:00'),(9,'CPE111','Q9154','Thursday','19:00:00','21:30:00'),(10,'CPE011','Q3123','Tuesday','11:00:00','14:00:00'),(11,'CPE011','Q5555','Friday','10:30:00','12:30:00'),(12,'MATH101','Q3241','Wednesday','07:30:00','08:30:00'),(101,'CPE100','Q3301','Monday','08:00:00','10:00:00'),(102,'CPE100','Q3302','Wednesday','08:00:00','10:00:00'),(105,'CPE102','Q9405','Friday','09:00:00','12:00:00'),(106,'CPE102','Q9405','Saturday','09:00:00','12:00:00'),(107,'CPE111','Q3301','Monday','08:00:00','10:00:00'),(108,'CPE111','Q3302','Wednesday','08:00:00','10:00:00'),(109,'CPE112','Q5210','Tuesday','13:00:00','16:00:00'),(110,'CPE112','Lab 1','Thursday','13:00:00','16:00:00'),(111,'CPE113','Q9405','Friday','09:00:00','12:00:00'),(112,'CPE114','Q9405','Saturday','09:00:00','12:00:00'),(113,'CPE111','Q3301','Monday','08:00:00','10:00:00'),(114,'CPE111','Q3302','Wednesday','08:00:00','10:00:00'),(115,'CPE112','Q5210','Tuesday','13:00:00','16:00:00'),(116,'CPE112','Lab 1','Thursday','13:00:00','16:00:00'),(117,'CPE113','Q9405','Friday','09:00:00','12:00:00'),(118,'CPE114','Q9405','Saturday','09:00:00','12:00:00');
/*!40000 ALTER TABLE `class_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_session`
--

DROP TABLE IF EXISTS `class_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_session` (
  `Session_ID` int NOT NULL AUTO_INCREMENT,
  `Course_Code` varchar(50) NOT NULL,
  `Topic` varchar(255) DEFAULT NULL,
  `Session_Date` date DEFAULT NULL,
  `Professor_ID` int NOT NULL,
  PRIMARY KEY (`Session_ID`),
  KEY `class_session_course_FK` (`Course_Code`),
  KEY `class_session_professor_FK` (`Professor_ID`),
  CONSTRAINT `class_session_course_FK` FOREIGN KEY (`Course_Code`) REFERENCES `course` (`Course_Code`),
  CONSTRAINT `class_session_professor_FK` FOREIGN KEY (`Professor_ID`) REFERENCES `professor` (`Professor_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=216 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_session`
--

LOCK TABLES `class_session` WRITE;
/*!40000 ALTER TABLE `class_session` DISABLE KEYS */;
INSERT INTO `class_session` VALUES (4,'CPE112','Boolean Algebra and Logic Gates','2026-04-12',102),(5,'CPE112','K-map Simplification','2026-04-19',102),(6,'CPE112','Combinational Circuits: Encoders & 7-Segment Decoders','2026-04-26',102),(7,'CPE113','OSI Model and Network Topologies','2026-04-13',101),(8,'CPE113','IPv4 Addressing and FLSM','2026-04-20',101),(9,'CPE113','Advanced Subnetting and VLSM','2026-04-27',101),(10,'CPE114','Introduction to Microprocessors & DOSBox','2026-04-14',102),(11,'CPE114','Registers and Memory Addressing','2026-04-21',102),(12,'CPE114','String Operations and User Input','2026-04-28',102),(13,'CS201','Relational Algebra & SQL Basics','2026-04-15',105),(14,'CS201','Advanced JOINs and Subqueries','2026-04-22',105),(15,'CS201','Database Normalization (1NF to 3NF)','2026-04-29',105),(16,'MATH201','Introduction to Optimization Models','2026-04-16',103),(17,'MATH201','Graphical Method Solutions','2026-04-23',103),(18,'MATH201','Solving Models via the Simplex Method','2026-04-30',103),(101,'CPE100','Week 1: Introduction to CPE','2025-12-10',101),(102,'CPE100','Week 2: Binary Mathematics','2025-12-17',101),(103,'CPE100','Week 3: Logic Gates Overview','2026-01-08',101),(104,'CPE100','Week 4: Boolean Algebra','2026-01-15',101),(105,'CPE100','Week 5: Combinational Logic','2026-01-22',101),(111,'CPE102','Week 1: CPU Architecture','2025-12-12',104),(112,'CPE102','Week 2: Memory Hierarchy','2025-12-19',104),(113,'CPE102','Week 3: Assembly Basics','2026-01-10',104),(114,'CPE102','Week 4: Registers & ALU','2026-01-17',104),(115,'CPE102','Week 5: Interrupts and IO','2026-01-24',104),(201,'CPE111','Week 1: Introduction to IoT','2025-12-10',201),(202,'CPE111','Week 2: Sensors and Actuators','2025-12-17',201),(203,'CPE111','Week 3: Microcontroller Basics','2026-01-08',201),(204,'CPE111','Week 4: ESP32 Wi-Fi Setup','2026-01-15',201),(205,'CPE111','Week 5: Cloud Data Integration','2026-01-22',201),(206,'CPE112','Week 1: Karnaugh Maps','2025-12-11',202),(207,'CPE112','Week 2: Multiplexers','2025-12-18',202),(208,'CPE112','Week 3: Encoders and Decoders','2026-01-09',202),(209,'CPE112','Week 4: Arithmetic Circuits','2026-01-16',202),(210,'CPE112','Week 5: Flip-Flops & Sequential Logic','2026-01-23',202),(211,'CPE113','Week 1: OSI Model','2025-12-12',204),(212,'CPE113','Week 2: Network Topologies','2025-12-19',204),(213,'CPE113','Week 3: IP Addressing','2026-01-10',204),(214,'CPE113','Week 4: Subnetting Basics','2026-01-17',204),(215,'CPE113','Week 5: Routing Protocols','2026-01-24',204);
/*!40000 ALTER TABLE `class_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `Course_Code` varchar(50) NOT NULL,
  `Course_Title` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`Course_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES ('CPE011','Logic Circuits and Design'),('CPE021','Computer Architecture and Organization With Assembly'),('CPE100','Intro to Computer Engineering'),('CPE102','Microprocessor Systems'),('CPE111','Internet of Things'),('CPE112','Digital Logic Design'),('CPE113','Computer Networks'),('CPE114','Assembly Language Programming'),('CS201','Database Management Systems'),('CS202','Data Structures'),('MATH101','Calculus 1'),('MATH201','Linear Programming');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrollment`
--

DROP TABLE IF EXISTS `enrollment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enrollment` (
  `Enrollment_ID` int NOT NULL AUTO_INCREMENT,
  `Student_ID` int NOT NULL,
  `Course_Code` varchar(50) NOT NULL,
  `Academic_Year` varchar(10) DEFAULT NULL,
  `Semester` int DEFAULT NULL,
  `Current_Grade` decimal(5,2) DEFAULT NULL,
  PRIMARY KEY (`Enrollment_ID`),
  KEY `enrollment_student_FK` (`Student_ID`),
  KEY `enrollment_course_FK` (`Course_Code`),
  CONSTRAINT `enrollment_course_FK` FOREIGN KEY (`Course_Code`) REFERENCES `course` (`Course_Code`),
  CONSTRAINT `enrollment_student_FK` FOREIGN KEY (`Student_ID`) REFERENCES `student` (`Student_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrollment`
--

LOCK TABLES `enrollment` WRITE;
/*!40000 ALTER TABLE `enrollment` DISABLE KEYS */;
INSERT INTO `enrollment` VALUES (1,2024003,'CPE111','2025-2026',2,92.50),(2,2024004,'CPE011','2025-2026',2,88.00),(3,2024005,'CS201','2025-2026',2,95.00),(4,2024006,'CPE111','2025-2026',2,89.50),(5,2024007,'MATH101','2025-2026',2,78.00),(6,2024008,'CPE011','2025-2026',2,91.00),(7,2024009,'CS201','2025-2026',2,85.50),(9,2024011,'MATH101','2025-2026',2,82.00),(10,2024012,'CPE011','2025-2026',2,90.00),(11,2024005,'MATH101','2025-2026',2,76.00),(28,2025001,'CPE111','2025-2026',1,95.00),(29,2025002,'CPE111','2025-2026',1,98.00),(32,2025005,'CPE112','2025-2026',1,74.00),(34,2025007,'CPE113','2025-2026',1,76.50),(35,2025008,'CPE113','2025-2026',1,65.00),(36,2025009,'CPE111','2025-2026',1,92.00),(37,2025010,'CPE112','2025-2026',1,94.50),(38,2025011,'CPE113','2025-2026',1,74.00),(39,2025012,'CPE111','2025-2026',1,70.00),(40,2025013,'CPE111','2025-2026',1,85.00),(41,2025014,'CPE112','2025-2026',1,82.50),(42,2025015,'CPE113','2025-2026',1,86.00),(43,2025016,'CPE111','2025-2026',1,84.00),(46,2025003,'CPE112','2025-2026',1,92.50),(49,2025006,'CPE111','2025-2026',1,68.00);
/*!40000 ALTER TABLE `enrollment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `evaluation`
--

DROP TABLE IF EXISTS `evaluation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `evaluation` (
  `Evaluation_ID` int NOT NULL AUTO_INCREMENT,
  `Session_ID` int NOT NULL,
  `Student_ID` int NOT NULL,
  `Clarity_Score` int DEFAULT NULL,
  `Pacing_Score` int DEFAULT NULL,
  `Comprehension_Score` int DEFAULT NULL,
  `Engagement_Score` int DEFAULT NULL,
  `Additional_Comments` text,
  `Study_Hours` decimal(5,2) DEFAULT NULL,
  `Submission_Date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Evaluation_ID`),
  KEY `evaluation_class_session_FK` (`Session_ID`),
  KEY `evaluation_student_FK` (`Student_ID`),
  CONSTRAINT `evaluation_class_session_FK` FOREIGN KEY (`Session_ID`) REFERENCES `class_session` (`Session_ID`),
  CONSTRAINT `evaluation_student_FK` FOREIGN KEY (`Student_ID`) REFERENCES `student` (`Student_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `evaluation`
--

LOCK TABLES `evaluation` WRITE;
/*!40000 ALTER TABLE `evaluation` DISABLE KEYS */;
INSERT INTO `evaluation` VALUES (10,11,2024002,5,4,3,2,'hahahaha',143.00,'2026-04-11 21:43:47'),(11,18,2024002,5,2,4,1,'4:46pm',4.00,'2026-04-11 21:43:47'),(12,14,2024003,1,1,1,1,'9:28',12.00,'2026-04-11 21:43:47'),(13,7,2024003,5,4,2,1,'try',11.00,'2026-04-11 21:43:47'),(14,5,2024003,5,5,5,5,'pls',67.00,'2026-04-11 22:04:32'),(16,15,2024003,4,2,3,1,'Now Working!',5.00,'2026-04-12 00:32:51'),(17,15,2024003,1,1,1,1,'',2.00,'2026-04-12 11:52:39'),(19,15,2024003,4,4,4,4,'does this still works',3.00,'2026-04-12 16:41:22'),(20,5,2024003,1,1,1,1,'online testing',23.00,'2026-04-12 12:18:59'),(22,15,2024003,1,1,1,1,'ayoko na',3.00,'2026-04-12 12:30:04'),(23,9,2024003,4,4,1,3,'',1.00,'2026-04-12 13:03:46'),(24,14,2024003,2,4,2,2,'',2.00,'2026-04-13 07:53:34'),(27,9,2024003,4,4,5,4,'Progress Report',3.00,'2026-04-14 14:54:34'),(48,201,2025001,5,3,5,5,'Very clear intro!',3.00,'2025-12-10 14:00:00'),(49,201,2025002,4,3,4,4,'Good pace.',2.00,'2025-12-10 15:00:00'),(50,202,2025001,4,3,5,5,'Math is fun.',4.00,'2025-12-17 14:00:00'),(51,206,2025003,5,3,4,5,'Understood K-Maps.',3.00,'2025-12-11 16:00:00'),(52,202,2025006,2,5,1,2,'I studied all weekend but failed the quiz.',14.00,'2025-12-17 18:00:00'),(53,208,2025008,1,4,2,1,'I am so lost and tired.',12.00,'2026-01-09 20:00:00'),(54,212,2025005,2,5,1,2,'Reading the book is not helping.',15.00,'2025-12-19 22:00:00'),(55,203,2025009,3,4,2,4,'I feel like I am falling behind everyone else.',6.00,'2026-01-08 19:00:00'),(56,209,2025010,4,3,2,3,'I guessed on the homework and got lucky.',5.00,'2026-01-16 18:00:00'),(57,204,2025012,5,3,5,2,'Too easy, skipped the reading.',1.00,'2026-01-15 12:00:00'),(58,211,2025011,4,3,5,3,'I already know this from Youtube.',0.00,'2025-12-12 14:00:00'),(59,204,2025013,2,5,2,1,'Professor was talking way too fast.',4.00,'2026-01-15 16:00:00'),(60,204,2025014,3,5,3,2,'Could not keep up with the slides.',5.00,'2026-01-15 16:30:00'),(61,213,2025015,4,1,5,1,'I fell asleep, way too slow.',2.00,'2026-01-10 10:00:00'),(62,213,2025016,5,1,5,2,'Boring lecture.',1.00,'2026-01-10 10:15:00'),(63,210,2025003,1,4,1,2,'I do not understand flip-flops at all.',8.00,'2026-01-23 18:00:00'),(65,210,2025005,1,5,1,1,'Please do a review session next week.',12.00,'2026-01-23 20:00:00'),(66,210,2025010,2,4,2,2,'The diagrams are too confusing.',9.00,'2026-01-23 21:00:00'),(67,210,2025014,1,5,1,2,'I am totally lost on state machines.',11.00,'2026-01-23 22:00:00'),(68,201,2025001,5,3,5,5,'Very clear intro!',3.00,'2025-12-10 14:00:00'),(69,201,2025002,4,3,4,4,'Good pace.',2.00,'2025-12-10 15:00:00'),(70,202,2025001,4,3,5,5,'Math is fun.',4.00,'2025-12-17 14:00:00'),(71,206,2025003,5,3,4,5,'Understood K-Maps.',3.00,'2025-12-11 16:00:00'),(73,208,2025008,1,4,2,1,'I am so lost and tired.',12.00,'2026-01-09 20:00:00'),(74,212,2025005,2,5,1,2,'Reading the book is not helping.',15.00,'2025-12-19 22:00:00'),(75,203,2025009,3,4,2,4,'I feel like I am falling behind everyone else.',6.00,'2026-01-08 19:00:00'),(76,209,2025010,4,3,2,3,'I guessed on the homework and got lucky.',5.00,'2026-01-16 18:00:00'),(77,204,2025012,5,3,5,2,'Too easy, skipped the reading.',1.00,'2026-01-15 12:00:00'),(78,211,2025011,4,3,5,3,'I already know this from Youtube.',0.00,'2025-12-12 14:00:00'),(79,204,2025013,2,5,2,1,'Professor was talking way too fast.',4.00,'2026-01-15 16:00:00'),(80,204,2025014,3,5,3,2,'Could not keep up with the slides.',5.00,'2026-01-15 16:30:00'),(81,213,2025015,4,1,5,1,'I fell asleep, way too slow.',2.00,'2026-01-10 10:00:00'),(82,213,2025016,5,1,5,2,'Boring lecture.',1.00,'2026-01-10 10:15:00'),(83,210,2025003,1,4,1,2,'I do not understand flip-flops at all.',8.00,'2026-01-23 18:00:00'),(85,210,2025005,1,5,1,1,'Please do a review session next week.',12.00,'2026-01-23 20:00:00'),(86,210,2025010,2,4,2,2,'The diagrams are too confusing.',9.00,'2026-01-23 21:00:00'),(87,210,2025014,1,5,1,2,'I am totally lost on state machines.',11.00,'2026-01-23 22:00:00'),(88,213,2024003,5,5,5,5,'online again',0.00,'2026-04-14 19:08:17'),(89,112,2025001,4,2,3,2,'oh my god wow',4.00,'2026-04-14 19:28:20'),(90,214,2025001,4,2,4,5,'Demo Progress Test',2.00,'2026-04-15 03:49:44'),(91,105,2025001,4,2,4,5,'Progress Report',2.00,'2026-04-15 04:17:15'),(92,101,2025001,2,2,2,2,'test 1',2.00,'2026-04-15 00:00:00'),(93,104,2025001,3,3,3,3,'wat',5.00,'2026-04-15 00:00:00'),(94,103,2025001,3,3,3,3,'2',2.00,'2026-04-15 00:00:00'),(99,9,2025001,4,2,4,2,'',2.00,'2026-04-15 00:00:00'),(100,113,2025001,3,3,3,3,'yiz galing taina!!!&@₱₱₱',0.00,'2026-04-15 00:00:00'),(101,7,2024006,5,5,5,5,'Very nice.',25.00,'2026-04-15 00:00:00'),(102,18,2025027,4,3,4,3,'uwu',15.00,'2026-04-15 00:00:00');
/*!40000 ALTER TABLE `evaluation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guardian`
--

DROP TABLE IF EXISTS `guardian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guardian` (
  `Guardian_ID` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Contact_Number` varchar(50) DEFAULT NULL,
  `Email` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`Guardian_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2031 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guardian`
--

LOCK TABLES `guardian` WRITE;
/*!40000 ALTER TABLE `guardian` DISABLE KEYS */;
INSERT INTO `guardian` VALUES (101,'Arthur','Abad','09170000001','arthur@test.com'),(102,'Brenda','Agoncillo','09170000002','brenda@test.com'),(103,'Carlos','Alcantara','09170000003','carlos@test.com'),(104,'Diana','Alonzo','09170000004','diana@test.com'),(105,'Edward','Amador','09170000005','edward@test.com'),(106,'Felicia','Asuncion','09170000006','felicia@test.com'),(107,'George','Balagtas','09170000007','george@test.com'),(108,'Helen','Baltazar','09170000008','helen@test.com'),(109,'Ivan','Barrameda','09170000009','ivan@test.com'),(110,'Julia','Beltran','09170000010','julia@test.com'),(111,'Kevin','Bernardo','09170000011','kevin@test.com'),(112,'Laura','Bonifacio','09170000012','laura@test.com'),(113,'Marco','Cabal','09170000013','marco@test.com'),(114,'Nancy','Calderon','09170000014','nancy@test.com'),(115,'Oscar','Calma','09170000015','oscar@test.com'),(116,'Paula','Camacho','09170000016','paula@test.com'),(117,'Quincy','Capulong','09170000017','quincy@test.com'),(118,'Rita','Carillo','09170000018','rita@test.com'),(119,'Simon','Carlos','09170000019','simon@test.com'),(120,'Teresa','Clemente','09170000020','teresa@test.com'),(121,'Ulysses','Dalisay','09170000021','ulysses@test.com'),(122,'Victor','Datu','09170000022','victor@test.com'),(123,'Walter','David','09170000023','walter@test.com'),(124,'Xavier','Del Rosario','09170000024','xavier@test.com'),(125,'Yvonne','Delgado','09170000025','yvonne@test.com'),(126,'Zack','Dimaculangan','09170000026','zack@test.com'),(127,'Albert','Dizon','09170000027','albert@test.com'),(128,'Barbara','Enriquez','09170000028','barbara@test.com'),(129,'Colin','Esguerra','09170000029','colin@test.com'),(130,'Dana','Estrada','09170000030','dana@test.com'),(1001,'Roberto','Dela Cruz',NULL,NULL),(1002,'Maria','Santos',NULL,NULL),(1003,'Jose','Rizal',NULL,NULL),(1005,'Emilio','Aguinaldo','09111111121','apolinario.com'),(1006,'Apolinario','Mabini',NULL,NULL),(1007,'Marcelo','Del Pilar',NULL,NULL),(1008,'Juan','Luna',NULL,NULL),(1009,'Melchora','Aquino',NULL,NULL),(1010,'Gabriela','Silang',NULL,NULL),(1011,'Antonio','Luna',NULL,NULL),(1012,'Emilio','Jacinto',NULL,NULL),(2001,'Arthur','Abad','09170000001','arthur@test.com'),(2002,'Brenda','Agoncillo','09170000002','brenda@test.com'),(2003,'Carlos','Alcantara','09170000003','carlos@test.com'),(2004,'Diana','Alonzo','09170000004','diana@test.com'),(2005,'Edward','Amador','09170000005','edward@test.com'),(2006,'Felicia','Asuncion','09170000006','felicia@test.com'),(2007,'George','Balagtas','09170000007','george@test.com'),(2008,'Helen','Baltazar','09170000008','helen@test.com'),(2009,'Ivan','Barrameda','09170000009','ivan@test.com'),(2010,'Julia','Beltran','09170000010','julia@test.com'),(2011,'Kevin','Bernardo','09170000011','kevin@test.com'),(2012,'Laura','Bonifacio','09170000012','laura@test.com'),(2013,'Marco','Cabal','09170000013','marco@test.com'),(2014,'Nancy','Calderon','09170000014','nancy@test.com'),(2015,'Oscar','Calma','09170000015','oscar@test.com'),(2016,'Paula','Camacho','09170000016','paula@test.com'),(2017,'Quincy','Capulong','09170000017','quincy@test.com'),(2018,'Rita','Carillo','09170000018','rita@test.com'),(2019,'Simon','Carlos','09170000019','simon@test.com'),(2020,'Teresa','Clemente','09170000020','teresa@test.com'),(2021,'Ulysses','Dalisay','09170000021','ulysses@test.com'),(2022,'Victor','Datu','09170000022','victor@test.com'),(2023,'Walter','David','09170000023','walter@test.com'),(2024,'Xavier','Del Rosario','09170000024','xavier@test.com'),(2025,'Yvonne','Delgado','09170000025','yvonne@test.com'),(2026,'Zack','Dimaculangan','09170000026','zack@test.com'),(2027,'Albert','Dizon','09170000027','albert@test.com'),(2028,'Barbara','Enriquez','09170000028','barbara@test.com'),(2029,'Colin','Esguerra','09170000029','colin@test.com'),(2030,'Dana','Estrada','09170000030','dana@test.com');
/*!40000 ALTER TABLE `guardian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `professor`
--

DROP TABLE IF EXISTS `professor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `professor` (
  `Professor_ID` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Username` varchar(100) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Department` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`Professor_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `professor`
--

LOCK TABLES `professor` WRITE;
/*!40000 ALTER TABLE `professor` DISABLE KEYS */;
INSERT INTO `professor` VALUES (101,'Rudo','Surebrec','rsuberec','scrypt:32768:8:1$tyS2oO1wNPIlq4m4$4abca336f51210b42da5f4b2442ae2868effb04c5fbfbc6ae60dda53e96eff147149967efce4e1cb11be68641e08ac9f97c9ae1ec6541a24fdbce0f6dfc7ba4a','Computer Engineering'),(102,'Ada','Lovelace','aalovelace','scrypt:32768:8:1$MrOP2Qo9G31N9ttJ$2155bbb6c42b74cac7c7eda66f93f6883700a2ff0a437398b83d0bd636aa6db503a8930fd8e4df7784f0b76861443939ac8db63b71df24dbb41a8b45035f6a2f','Computer Engineering'),(103,'Alan','Turing','aturing','scrypt:32768:8:1$Vx216X7xDsEtcMPZ$1443606bddb00b33a577ca9c6fe47a76809a4e5bf41b3f0cfb0774d9b5a7e274cd8e248516153e45b2a312e4f6878befeb6c381f21a75a29bef9633b44074ebd','Mathematics'),(104,'Grace','Hopper','ghopper','scrypt:32768:8:1$DDiOeySV3Xm2jzVP$0aef26ede2c3ec31b660f92c3e83ef60c0cf5d084ddfc9094d676e94e04de8fb5285e64591aaba0bfd8c5bd41df339e80816ecb2d229225649e609f792419cdc','Computer Engineering'),(105,'Tim','Berners-Lee','tlee','scrypt:32768:8:1$lN7eGDIbTnDj7Y2a$8c9332f4763010cdfb2b1c034ab68c4a3dcfecd780490f8ab66bbcdd11cc5a868ee42ff50a8a087abe2ac08acdbbab15d530a142a6b94fa167bab7440d8fc8d5','Computer Science'),(106,'Linus','Tech Tips','ltt','scrypt:32768:8:1$QkU5Zh1FN6LqGNYz$3d3671a051e4674e5b2aa6e648c164903e0ca84cffa6ccab863c519c676a8fff35ce49a59f5c0408d09646e1ad51d9caac9a830c70143d26687b3b9a7a05ba4a','Computer Engineering'),(107,'Dennis','Ritchie','dritchie','scrypt:32768:8:1$eCZSYi13lZxpWxDR$8e52a6259f97c2990e0b21817595a88745e40076335993bd46a0e13ca1444b2e22dfef2215b652a6a5f8a9ea03f456b4807670c4589831351e323c93a2ea6b18','Computer Science'),(108,'Ken','Thompson','kthompson','scrypt:32768:8:1$bXjbQEvFsxcoZ0qs$5b56f7dc60624bdcbed26bebc6a910491249b6b4f559e608649f04250ff159323a557281e57321ed2a9e854b68227c65081dfc44bcdf9a5ad09421ae95e65691','Computer Science'),(109,'Bjarne','Stroustrup','bstroustrup','scrypt:32768:8:1$wXSUtGjbk6QYkGho$fe5876fae0b273bdf71544a1b23006412b1fdaeb73a5c01c18eb09c36d28cb092374ad35917a3ded90bcc571ed36e32a82bbfcaa8d6defc3a9935c103bd66474','Computer Engineering'),(110,'James','Gosling','jgosling','scrypt:32768:8:1$w1DqEnRWTGz0Ovfz$a5a252b977309b6673ac2b1a0c560640fdce53a0fd846dfce64da6b76809e2ccbeaf95bb5f22a7d290fd0df368bf57d56924db348dead6de16597b33dff26708','Computer Science'),(111,'Guido','van Rossum','grossum','scrypt:32768:8:1$bvmXY9xJdfjqduf6$ccc2ebb0eea4553530aa57ec68d616305bbea5a4458bd9204891825ffeed2cd57f0a5969fa46e0a46aa4ec5e72bcffba0764566224e89a4a00e31edd13078abf','Computer Science'),(112,'Margaret','Hamilton','mhamilton','scrypt:32768:8:1$eiJCGIn93XKH1shd$3bd9b26bd86db8f8a57e83b7431e3652afc3ca38278ff113bd78e36656b9a2e5951802cb860606fe37324f0d057b1f8e2f0a4cae43ae57e8918bb810203e5a4a','Computer Engineering'),(113,'Katherine','Johnson','kjohnson','scrypt:32768:8:1$Lw14VAYmPbfHqJgI$8a7348d2b2844ad0d59438a4fb60baeeb2c71fae5c4dab76f7fb92ac9fff623368224a78320d9c06c492fcb615b9867cd58334b0b7fc9aaac2271d6ee06cef35','Mathematics'),(201,'Richard','Feynman','rfeynman','pbkdf2:sha256:1000000$dwfyIcpd70le0iB4$16e6db49f83c836e71214ae747983a7e490e3f370e82faf057cf1ef803125fce','Computer Engineering'),(202,'Marie','Curie','mcurie','pbkdf2:sha256:1000000$dwfyIcpd70le0iB4$16e6db49f83c836e71214ae747983a7e490e3f370e82faf057cf1ef803125fce','Computer Engineering'),(203,'Isaac','Newton','inewton','pbkdf2:sha256:1000000$dwfyIcpd70le0iB4$16e6db49f83c836e71214ae747983a7e490e3f370e82faf057cf1ef803125fce','Mathematics'),(204,'Rosalind','Franklin','rfranklin','pbkdf2:sha256:1000000$dwfyIcpd70le0iB4$16e6db49f83c836e71214ae747983a7e490e3f370e82faf057cf1ef803125fce','Computer Science'),(205,'Albert','Einstein','aeinstein','pbkdf2:sha256:1000000$dwfyIcpd70le0iB4$16e6db49f83c836e71214ae747983a7e490e3f370e82faf057cf1ef803125fce','Computer Science');
/*!40000 ALTER TABLE `professor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `Student_ID` int NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Program` varchar(50) DEFAULT NULL,
  `Year_Level` int DEFAULT NULL,
  `Username` varchar(100) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Guardian_ID` int DEFAULT NULL,
  `streak_count` int DEFAULT '0',
  `best_streak` int DEFAULT '0',
  `last_study_date` date DEFAULT NULL,
  `freeze_count` int DEFAULT '0',
  `streak_frozen` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Student_ID`),
  KEY `student_guardian_FK` (`Guardian_ID`),
  CONSTRAINT `student_guardian_FK` FOREIGN KEY (`Guardian_ID`) REFERENCES `guardian` (`Guardian_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2025032 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (2024001,'Miguel','Dela Cruz','BSCpE',2,'mdelacruz','scrypt:32768:8:1$wALyS086CCHLULE7$23a7c354d50c2326467421ffb0043f81138ee0f29dcd91c078b1b617c6a68f2255820b30e669b8abe9b64a7af8d9f1b8fa2b56398a95edf320be2b03cadff854',1001,0,0,NULL,0,0),(2024002,'Sofia','Santos','BSCS',2,'ssantos','scrypt:32768:8:1$MSliJO8eLcD6jHhY$e92474ac335a2ce0e8773a9d5bd95a351ddc1eb0c1e158544227a17582135e03a98db76280dbaf84b68f569717872ec5bc3f4745bfc2178d2d6709891c07a630',1002,0,0,NULL,0,0),(2024003,'Juan','Dela Cruz','BSCpE',2,'jcruz','scrypt:32768:8:1$lxMUkU2KTADCQ11w$9866b939f73b5b7ac30835ab0104728c10b652c9e4f52e88bf86ca9969bfe4cebbcffa3555c1e55125c78345fd0cb8f871c3dbd71836dce623e81bd465124a2b',1003,1,1,'2026-04-13',0,0),(2024004,'Maria','Clara','BSCpE',2,'mclara','scrypt:32768:8:1$ycpSftw2bN3FxKT8$028a2c4a0c42cd73e2c1a27c96a64043d2455c1c6012fb093b72b4244a9670d0d03859fd6ab047c7da3c9914e271dae6f5c4e0bdf4b144441245fc304be1d030',NULL,0,0,NULL,0,0),(2024005,'Pedro','Penduko','BSCS',1,'ppenduko','scrypt:32768:8:1$Mx5jP0oMtUoCfo7u$f64c24b9828dd282c79d724581c1a898ca546722e4199c8b3e25ee39f871f82282e030899cf4b395089562c25dadd9ebafbc81c1e479850b16c39df1571a6139',1005,0,0,NULL,0,0),(2024006,'Ana','Roces','BSCpE',3,'aroces','scrypt:32768:8:1$KAg0V84hkdQ66XLU$1f8e0b6f7b401f5ddb2e93a376159783489969d05514675f12ef9db4b21c95b55b577c28dd1edd0834ac2e5dd89424e719198ac2eaa7880e5a9b5d79d4e704c3',1006,1,1,'2026-04-15',0,0),(2024007,'Luis','Manzano','BSCS',2,'lmanzano','scrypt:32768:8:1$rFQf5kxFaAnMr5Ku$4ab8832738e46bc99be555ba6e09ecf96c4c3fc74c6146933a13136d124d4cd60995118d3c2f7cda573f57c8fca8c4aeea1537944c5cef7a91191cfbaf2bc6f2',1007,0,0,NULL,0,0),(2024008,'Carmen','Rosales','BSCpE',4,'crosales','scrypt:32768:8:1$kQjFyZculCRiF7uJ$0a7531a90729428f2253cef0c9cc01f92908e2938989f4ed9401cbb5931cdd56394417488b1ea61ee38a66d96c0acb459b16789b2140cce378fb8dd2a25a6feb',1008,0,0,NULL,0,0),(2024009,'Fernando','Poe','BSCS',1,'fpoe','scrypt:32768:8:1$JAzmGANwhS334DVm$d7350ca00e902980ab4dd1a6d1c8b8dafe42ae422b0ad74fbbbb32769889fcd9607c92ea0658031ff14b589be23d835e99c92cf016c87e9013d92d1d0f8fe362',1009,0,0,NULL,0,0),(2024010,'Gloria','Romero','BSCpE',3,'gromero','scrypt:32768:8:1$hFssoSZ7bcrpGNy1$83c59e416b06bebba143db0ecc9f31da057725d8afa88e8c1ec9388a81f1f93b9935c0e07800ff7a94da8fbafc679d8cbac2f034ac2f0f470e07256c2038edfe',1010,0,0,NULL,0,0),(2024011,'Ramon','Revilla','BSCS',4,'rrevilla','scrypt:32768:8:1$R7Uydk0guP1MvG1B$91fb57ac8ec97be6a66e3f929f7fd76e38f0c3261fd28adde6b9f5c4baa2978318708a8e8a67d6c0154ef493b45691db62038d745c32a8a9ee86a5046abda1a6',1011,0,0,NULL,0,0),(2024012,'Susan','Roces','BSCpE',2,'sroces','scrypt:32768:8:1$Ij2MCWGxdDNnue3l$7d22a160d21236095d6f85719452ce2a27228607fc01b0873301e81d540e84ab998eb50bab84dc8cb243de19595bfb9a82110e506e85ff257d81ea4b46c72d96',1012,0,0,NULL,0,0),(2025001,'Aaron','Abad','BSCpE',2,'aabad','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2001,1,1,'2026-04-15',0,0),(2025002,'Assyria','Interno','BSCS',2,'Yhelle','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',NULL,0,0,NULL,0,0),(2025003,'Caleb','Alcantara','BSCpE',3,'calcantara','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2003,0,0,NULL,0,0),(2025005,'Elias','Amador','BSCS',1,'eamador','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2005,0,0,NULL,0,0),(2025006,'Fiona','Asuncion','BSCpE',4,'fasuncion','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2006,0,0,NULL,0,0),(2025007,'Gabriel','Balagtas','BSCS',2,'gbalagtas','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2007,0,0,NULL,0,0),(2025008,'Hannah','Baltazar','BSCpE',3,'hbaltazar','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2008,0,0,NULL,0,0),(2025009,'Ian','Barrameda','BSCS',1,'ibarrameda','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2009,0,0,NULL,0,0),(2025010,'Jasmine','Beltran','BSCpE',2,'jbeltran','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2010,0,0,NULL,0,0),(2025011,'Kevin','Bernardo','BSCS',4,'kbernardo','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2011,0,0,NULL,0,0),(2025012,'Luna','Bonifacio','BSCpE',3,'lbonifacio','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2012,0,0,NULL,0,0),(2025013,'Mateo','Cabal','BSCS',2,'mcabal','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2013,0,0,NULL,0,0),(2025014,'Nina','Calderon','BSCpE',1,'ncalderon','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2014,0,0,NULL,0,0),(2025015,'Oscar','Calma','BSCS',3,'ocalma','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2015,0,0,NULL,0,0),(2025016,'Penelope','Camacho','BSCpE',2,'pcamacho','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2016,0,0,NULL,0,0),(2025017,'Quinn','Capulong','BSCS',4,'qcapulong','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2017,0,0,NULL,0,0),(2025018,'Ruby','Carillo','BSCpE',1,'rcarillo','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2018,0,0,NULL,0,0),(2025019,'Samuel','Carlos','BSCS',2,'scarlos','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2019,0,0,NULL,0,0),(2025020,'Tara','Clemente','BSCpE',3,'tclemente','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2020,0,0,NULL,0,0),(2025021,'Ulysses','Dalisay','BSCS',4,'udalisay','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2021,0,0,NULL,0,0),(2025022,'Violet','Datu','BSCpE',2,'vdatu','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2022,0,0,NULL,0,0),(2025023,'Wyatt','David','BSCS',1,'wdavid','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2023,0,0,NULL,0,0),(2025024,'Xena','Del Rosario','BSCpE',3,'xdelrosario','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2024,0,0,NULL,0,0),(2025025,'Yusuf','Delgado','BSCS',2,'ydelgado','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2025,0,0,NULL,0,0),(2025026,'Zara','Dimaculangan','BSCpE',4,'zdimaculangan','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2026,0,0,NULL,0,0),(2025027,'Andrew','Dizon','BSCS',1,'adizon','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2027,1,1,'2026-04-15',0,0),(2025028,'Bella','Enriquez','BSCpE',2,'benriquez','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2028,0,0,NULL,0,0),(2025029,'Christian','Esguerra','BSCS',3,'cesguerra','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2029,0,0,NULL,0,0),(2025030,'Delilah','Estrada','BSCpE',1,'destrada','pbkdf2:sha256:1000000$wdinpvgbqYXNOruM$e75240197dc588cd501f3e4f3e1f61ff602783d9089349296144b3ffb7a8c794',2030,0,0,NULL,0,0);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'aware_db'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-16  2:34:57
