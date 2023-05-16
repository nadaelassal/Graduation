CREATE DATABASE  IF NOT EXISTS `ai_trainer` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ai_trainer`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ai_trainer
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_info`
--

DROP TABLE IF EXISTS `user_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_info` (
  `email` varchar(45) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `height` int DEFAULT NULL,
  `weight` int DEFAULT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_info`
--

LOCK TABLES `user_info` WRITE;
/*!40000 ALTER TABLE `user_info` DISABLE KEYS */;
INSERT INTO `user_info` VALUES ('ali@gmail.com','ali','$2b$12$L7Vw7ineY3Xm5bchDdPmb.plju4ArXwPfxSCFk20v7x4V/9s0tbXG',NULL,180,80,30),('alii@gmail.com','ali','$2b$12$OXJ/eOZBOgiN0KqqC9dY5.Tqtivbgnp4USgwznjJ2stDT/yuF6jl2',NULL,NULL,NULL,NULL),('asd@gmail.com','asdas','$2b$12$KXIZI3gzK4WRWiTANPIJ5uMslOVRj7172teadu1My5.e9e.T7VDSS',NULL,NULL,NULL,NULL),('essamonly111@gmail.com','essamsasa','$2b$12$3W6yH9I7Gr86TrhVftc4wuhCNSK8Il454j7mPDU7XJUsZf4TiFiaa',NULL,NULL,NULL,NULL),('essamonly111@gmail.comas','essamsasa','$2b$12$LiVcj65IjLiI/r9MH89A6.x4S8z5Zcp3rC/W0DAcQ.pj2k2ngaFRC',NULL,NULL,NULL,NULL),('essamonly1121@gmail.com','asdasd','$2b$12$pGdnjLuKKms.q3V30JZG/e.fjQn5E3/pD3HFXAukjPqilb3NRUga2',NULL,NULL,NULL,NULL),('essamonly1asdas11@gmail.com','asdasd','$2b$12$dxdL0EZT1rYqx8beVXO27.29SHxMAju04XjKPu/OQUMSy1phR4Rb6',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-07 20:59:25
