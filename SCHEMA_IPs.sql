-- MariaDB dump 10.19  Distrib 10.11.6-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: IPs
-- ------------------------------------------------------
-- Server version	10.11.6-MariaDB-0+deb12u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `IPs`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `IPs` /*!40100 DEFAULT CHARACTER SET utf16 COLLATE utf16_general_ci */;

USE `IPs`;

--
-- Table structure for table `Equipos`
--

DROP TABLE IF EXISTS `Equipos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Equipos` (
  `id` smallint(6) unsigned NOT NULL AUTO_INCREMENT,
  `IP` varchar(15) NOT NULL DEFAULT '',
  `DireccionMAC` varchar(17) DEFAULT NULL,
  `NombrePc` varchar(20) DEFAULT NULL,
  `IdUsuario` tinyint(3) unsigned DEFAULT NULL,
  `fini` date NOT NULL DEFAULT '0000-00-00',
  `fexp` date NOT NULL DEFAULT '0000-00-00',
  `valido` char(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `FK_Equipos` (`IdUsuario`),
  CONSTRAINT `FK_Equipos` FOREIGN KEY (`IdUsuario`) REFERENCES `datos_personales` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Equipos`
--

LOCK TABLES `Equipos` WRITE;
/*!40000 ALTER TABLE `Equipos` DISABLE KEYS */;
INSERT INTO `Equipos` VALUES
(1,'192.168.10.11','11:22:33:44:55:66','javier-pc',1,'2025-03-21','2026-12-31','1'),
(2,'192.168.10.12','68:45:F1:B8:23:34','jfl-portatil',1,'2025-03-21','2026-12-31','1'),
(3,'192.168.20.11','11:11:11:22:22:22','agarcia-pc1',2,'2025-03-21','2026-12-31','1');
/*!40000 ALTER TABLE `Equipos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_personales`
--

DROP TABLE IF EXISTS `datos_personales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datos_personales` (
  `id` tinyint(3) unsigned NOT NULL AUTO_INCREMENT,
  `dni_nie` char(20) DEFAULT '',
  `Nombre` char(30) NOT NULL DEFAULT '',
  `Apellido1` char(50) NOT NULL DEFAULT '',
  `Apellido2` char(50) DEFAULT '',
  `email` char(50) DEFAULT '',
  `Valido` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_personales`
--

LOCK TABLES `datos_personales` WRITE;
/*!40000 ALTER TABLE `datos_personales` DISABLE KEYS */;
INSERT INTO `datos_personales` VALUES
(1,'12345678A','Javier','de la Fuente','López','javi.delafuentelopez@gmail.com',1),
(2,'11111111Z','Ana','García','García','ana.garciagarcia.11Z@foo.com',1);
/*!40000 ALTER TABLE `datos_personales` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-21 11:21:08
