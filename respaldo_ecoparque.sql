-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: ecoparque
-- ------------------------------------------------------
-- Server version	8.0.46

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

--
-- Current Database: `ecoparque`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `ecoparque` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `ecoparque`;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add perfil',7,'add_perfil'),(26,'Can change perfil',7,'change_perfil'),(27,'Can delete perfil',7,'delete_perfil'),(28,'Can view perfil',7,'view_perfil'),(29,'Can add inscripcion',8,'add_inscripcion'),(30,'Can change inscripcion',8,'change_inscripcion'),(31,'Can delete inscripcion',8,'delete_inscripcion'),(32,'Can view inscripcion',8,'view_inscripcion'),(33,'Can add categoria',9,'add_categoria'),(34,'Can change categoria',9,'change_categoria'),(35,'Can delete categoria',9,'delete_categoria'),(36,'Can view categoria',9,'view_categoria'),(37,'Can add experiencia',10,'add_experiencia'),(38,'Can change experiencia',10,'change_experiencia'),(39,'Can delete experiencia',10,'delete_experiencia'),(40,'Can view experiencia',10,'view_experiencia'),(41,'Can add valoracion',11,'add_valoracion'),(42,'Can change valoracion',11,'change_valoracion'),(43,'Can delete valoracion',11,'delete_valoracion'),(44,'Can view valoracion',11,'view_valoracion'),(45,'Can add Configuracion',12,'add_configuracion'),(46,'Can change Configuracion',12,'change_configuracion'),(47,'Can delete Configuracion',12,'delete_configuracion'),(48,'Can view Configuracion',12,'view_configuracion');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$Ii8FikvcIW1V5vSpA39V1q$b678sA3UgtrYfUzSWcucseKmYKhgjlqfcF89VyX3dBo=','2026-11-16 16:18:22.923984',1,'Julio','Julian','Amarillo','julio@mail.cl',1,1,'2026-11-15 00:12:31.200757'),(2,'pbkdf2_sha256$1000000$uUGUzXeodnxcWz0kgtgA8V$fUp5+nbPqmI0r6Qb97pp4aRBLdAVr5tpiFO8IAAKYSI=','2026-11-16 02:40:24.768432',0,'Juan','Juan','Perez','juan.perez@mail.cl',0,1,'2026-11-15 04:11:57.681091'),(3,'pbkdf2_sha256$1000000$cKl9BZHvsRyq9KI8BmWgWN$PtFW6UnRp2z3UrjRUJ6PMMYIZ3/MUuNilSAsNdVhig8=',NULL,1,'admin','Andrea','Fuentes','admin@aventurasdelsur.cl',1,1,'2026-11-15 04:36:46.837215'),(4,'pbkdf2_sha256$720000$IHnZLIVYttsBbx8tFoTU9O$0uP0Wfg1XNQS8gjEdy6g9PbQr6WyRoE3pTBMPAm81YQ=','2026-11-16 08:53:14.477170',0,'guia1','Camila','Rojas','guia1@aventurasdelsur.cl',0,1,'2026-11-15 04:36:47.381852'),(5,'pbkdf2_sha256$1000000$LwU5fnsX7K8fc4Sp5VbGHo$UGs9n6hRKWFDBaxDjip55F6w1BvVq4P4R0LhM8P1v8s=',NULL,0,'guia2','Matias','Soto','guia2@aventurasdelsur.cl',0,1,'2026-11-15 04:36:47.919010'),(6,'pbkdf2_sha256$720000$3ctCBWKAXwI41oxqkUTo8J$OM+BTE3YP4V3xMK1Q9uTgYAyQc6jVn7sSw+CfNwld4U=','2026-11-16 16:22:10.581576',0,'turista1','Valentina','Perez','turista1@aventurasdelsur.cl',0,1,'2026-11-15 04:36:48.455692'),(7,'pbkdf2_sha256$1000000$DQGzDm4zddbIjg0ptdL1MM$t+ZpUkNJTyIE3fc0KOb7/+v4s5JIj4UM+kjKhOcJ6ow=',NULL,0,'turista2','Diego','Munoz','turista2@aventurasdelsur.cl',0,1,'2026-11-15 04:36:48.995381'),(8,'pbkdf2_sha256$720000$3BF8ZjxnT9bS0nwg804dGu$p8qE3dc2tMr/gcM698cnpPCRcOQiW9wUuuZghlf27SM=','2026-11-16 07:15:08.475598',0,'Juanaz0','Juanazo','Gonazales','juanazo@mail.cl',0,1,'2026-11-16 02:00:14.777301');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_configuracion`
--

DROP TABLE IF EXISTS `core_configuracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_configuracion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `lema` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `horario` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mensaje_landing` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `reservas_abiertas` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_configuracion`
--

LOCK TABLES `core_configuracion` WRITE;
/*!40000 ALTER TABLE `core_configuracion` DISABLE KEYS */;
INSERT INTO `core_configuracion` VALUES (1,'Aventuras del Sur','Ecoparque y Reserva Natural','Reserva tu proxima experiencia al aire libre.','','12345678','','Lunes a domingo, 09:00 a 18:00','',0);
/*!40000 ALTER TABLE `core_configuracion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuentas_perfil`
--

DROP TABLE IF EXISTS `cuentas_perfil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas_perfil` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rol` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `cuentas_perfil_usuario_id_06f8a1e5_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuentas_perfil`
--

LOCK TABLES `cuentas_perfil` WRITE;
/*!40000 ALTER TABLE `cuentas_perfil` DISABLE KEYS */;
INSERT INTO `cuentas_perfil` VALUES (1,'administrador','8767655543',1),(2,'guia','12345678',2),(3,'administrador','',3),(4,'guia','',4),(5,'guia','',5),(6,'turista','',6),(7,'turista','',7),(8,'turista','+56912345678',8);
/*!40000 ALTER TABLE `cuentas_perfil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(12,'core','configuracion'),(7,'cuentas','perfil'),(9,'experiencias','categoria'),(10,'experiencias','experiencia'),(8,'experiencias','inscripcion'),(11,'experiencias','valoracion'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-11-12 00:18:37.886404'),(2,'auth','0001_initial','2026-11-12 00:18:39.085302'),(3,'admin','0001_initial','2026-11-12 00:18:39.327337'),(4,'admin','0002_logentry_remove_auto_add','2026-11-12 00:18:39.350974'),(5,'admin','0003_logentry_add_action_flag_choices','2026-11-12 00:18:39.361512'),(6,'contenttypes','0002_remove_content_type_name','2026-11-12 00:18:39.527381'),(7,'auth','0002_alter_permission_name_max_length','2026-11-12 00:18:39.629939'),(8,'auth','0003_alter_user_email_max_length','2026-11-12 00:18:39.662026'),(9,'auth','0004_alter_user_username_opts','2026-11-12 00:18:39.670595'),(10,'auth','0005_alter_user_last_login_null','2026-11-12 00:18:39.753302'),(11,'auth','0006_require_contenttypes_0002','2026-11-12 00:18:39.758316'),(12,'auth','0007_alter_validators_add_error_messages','2026-11-12 00:18:39.770313'),(13,'auth','0008_alter_user_username_max_length','2026-11-12 00:18:39.875971'),(14,'auth','0009_alter_user_last_name_max_length','2026-11-12 00:18:39.984073'),(15,'auth','0010_alter_group_name_max_length','2026-11-12 00:18:40.010644'),(16,'auth','0011_update_proxy_permissions','2026-11-12 00:18:40.020140'),(17,'auth','0012_alter_user_first_name_max_length','2026-11-12 00:18:40.125394'),(18,'sessions','0001_initial','2026-11-12 00:18:40.194796'),(19,'cuentas','0001_initial','2026-11-14 17:16:33.169804'),(20,'experiencias','0001_initial','2026-11-14 17:16:33.483702'),(21,'experiencias','0002_experiencia_estado_ruta_inscripcion_asistio','2026-11-16 07:21:07.432847'),(22,'experiencias','0003_valoracion','2026-11-16 08:05:30.215463'),(23,'core','0001_initial','2026-11-16 15:54:06.466723');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4e7vcmiz4v4k9nfzvhmodxwc92kbnaac','.eJxVjEEOwiAURO_C2hCgnw-4dN8zECgfqRpISrsy3t026UJXk8x7M2_mw7YWv3Va_JzYlSG7_HYxTE-qB0iPUO-NT62uyxz5ofCTdj62RK_b6f4dlNDLvgZNFBGEQzIos3Euo7LJDgI1OsoaYiaYdNIopRrAaFQk0h5Z2WiBfb7Jrjbl:1xSzT8:I-CDVdtC4CDs9fyx-4K6MCAk5NtQdWuVA1IeF27QRdg','2026-11-30 16:22:10.584577');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiencias_categoria`
--

DROP TABLE IF EXISTS `experiencias_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencias_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiencias_categoria`
--

LOCK TABLES `experiencias_categoria` WRITE;
/*!40000 ALTER TABLE `experiencias_categoria` DISABLE KEYS */;
INSERT INTO `experiencias_categoria` VALUES (1,'Trekking','Caminatas guiadas por los senderos de la reserva.',1),(2,'Canopy','Circuitos de tirolesas entre los arboles.',1),(3,'Kayak','Paseos en kayak por aguas tranquilas.',1),(4,'Arriendo de equipos','Equipamiento para actividades al aire libre.',1),(5,'Acampar','Acampadas en los distintos lugares que ofrece Aventuras del Sur',1);
/*!40000 ALTER TABLE `experiencias_categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiencias_experiencia`
--

DROP TABLE IF EXISTS `experiencias_experiencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencias_experiencia` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio` decimal(10,0) NOT NULL,
  `cupo_maximo` int unsigned NOT NULL,
  `fecha_hora` datetime(6) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `categoria_id` bigint NOT NULL,
  `creador_id` int NOT NULL,
  `estado_ruta` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `experiencias_experie_categoria_id_b03f452f_fk_experienc` (`categoria_id`),
  KEY `experiencias_experiencia_creador_id_70b19025_fk_auth_user_id` (`creador_id`),
  CONSTRAINT `experiencias_experie_categoria_id_b03f452f_fk_experienc` FOREIGN KEY (`categoria_id`) REFERENCES `experiencias_categoria` (`id`),
  CONSTRAINT `experiencias_experiencia_creador_id_70b19025_fk_auth_user_id` FOREIGN KEY (`creador_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `experiencias_experiencia_chk_1` CHECK ((`cupo_maximo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiencias_experiencia`
--

LOCK TABLES `experiencias_experiencia` WRITE;
/*!40000 ALTER TABLE `experiencias_experiencia` DISABLE KEYS */;
INSERT INTO `experiencias_experiencia` VALUES (1,'Kayak al amanecer','Paseo en kayak mientras sale el sol sobre el lago.',25000,2,'2026-11-20 10:00:00.000000',0,3,4,'cancelada'),(2,'Trekking Sendero del Bosque','Caminata de 4 horas por el bosque nativo.',15000,12,'2026-11-23 10:00:00.000000',1,1,4,'en_curso'),(3,'Canopy Alto','Circuito de 8 tirolesas sobre el valle.',30000,10,'2026-11-27 10:00:00.000000',1,2,4,'programada'),(4,'Arriendo de equipo de camping','Carpa, saco de dormir y cocinilla por un fin de semana.',12000,20,'2026-11-30 10:00:00.000000',1,4,4,'programada'),(5,'Trekking a la Cascada','Ruta guiada hasta la cascada de la reserva.',18000,15,'2026-11-21 10:00:00.000000',1,1,5,'finalizada'),(6,'Kayak en el Lago','Recorrido tranquilo para toda la familia.',22000,8,'2026-11-25 10:00:00.000000',1,3,5,'programada'),(7,'Canopy Nocturno','Tirolesas con iluminacion especial al atardecer.',35000,6,'2026-11-29 10:00:00.000000',1,2,5,'programada'),(8,'Arriendo de bicicletas','Bicicletas de montana por el dia, con casco.',10000,15,'2026-12-05 10:00:00.000000',1,4,5,'programada'),(9,'Acampada en el Lago Matuta','Acampada en el lago matuta de noche viendo las estrellas alrededor de una fogata tocando guitarra',15000,10,'2026-11-25 09:42:00.000000',1,5,1,'programada'),(11,'Clase de Kayak (Juan)','Juan dando clases de Kayak mientras farmea aura a los pobres gusanos que de verdad creen que le enseñara algo',20000,15,'2026-11-29 02:40:00.000000',1,3,2,'finalizada'),(12,'Kayak al anochecer','Kayak pero al anochecer',12000,12,'2026-11-17 15:48:00.000000',1,3,1,'programada'),(13,'Trekking 2','Otro Trekking',12000,12,'2026-11-17 18:52:00.000000',1,1,1,'programada');
/*!40000 ALTER TABLE `experiencias_experiencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiencias_inscripcion`
--

DROP TABLE IF EXISTS `experiencias_inscripcion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencias_inscripcion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_inscripcion` datetime(6) NOT NULL,
  `estado_pago` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `experiencia_id` bigint NOT NULL,
  `usuario_id` int NOT NULL,
  `asistio` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `experiencias_inscripcion_usuario_id_experiencia_id_996e38c7_uniq` (`usuario_id`,`experiencia_id`),
  KEY `experiencias_inscrip_experiencia_id_2fbecc6b_fk_experienc` (`experiencia_id`),
  CONSTRAINT `experiencias_inscrip_experiencia_id_2fbecc6b_fk_experienc` FOREIGN KEY (`experiencia_id`) REFERENCES `experiencias_experiencia` (`id`),
  CONSTRAINT `experiencias_inscripcion_usuario_id_9d6f5da2_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiencias_inscripcion`
--

LOCK TABLES `experiencias_inscripcion` WRITE;
/*!40000 ALTER TABLE `experiencias_inscripcion` DISABLE KEYS */;
INSERT INTO `experiencias_inscripcion` VALUES (1,'2026-11-15 04:36:49.555075','confirmado',1,6,0),(3,'2026-11-15 04:36:49.561131','confirmado',5,6,1),(4,'2026-11-15 04:36:49.562156','confirmado',7,6,0),(5,'2026-11-15 04:36:49.563155','confirmado',1,7,0),(6,'2026-11-15 04:36:49.564666','pendiente',3,7,0),(7,'2026-11-15 04:36:49.565684','confirmado',5,7,1),(8,'2026-11-15 04:36:49.566685','pendiente',6,7,0),(9,'2026-11-16 02:31:20.200723','pendiente',6,8,0),(10,'2026-11-16 02:41:29.369521','pendiente',11,8,1),(11,'2026-11-16 04:03:49.585160','confirmado',11,6,1);
/*!40000 ALTER TABLE `experiencias_inscripcion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiencias_valoracion`
--

DROP TABLE IF EXISTS `experiencias_valoracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiencias_valoracion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `puntaje` smallint unsigned NOT NULL,
  `comentario` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `inscripcion_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inscripcion_id` (`inscripcion_id`),
  CONSTRAINT `experiencias_valorac_inscripcion_id_9cef1e39_fk_experienc` FOREIGN KEY (`inscripcion_id`) REFERENCES `experiencias_inscripcion` (`id`),
  CONSTRAINT `experiencias_valoracion_chk_1` CHECK ((`puntaje` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiencias_valoracion`
--

LOCK TABLES `experiencias_valoracion` WRITE;
/*!40000 ALTER TABLE `experiencias_valoracion` DISABLE KEYS */;
INSERT INTO `experiencias_valoracion` VALUES (1,1,'Juan solo queria farmear aura y no me enseño nada','2026-11-16 08:26:15.497405',11);
/*!40000 ALTER TABLE `experiencias_valoracion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'ecoparque'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-11-16 13:30:26
