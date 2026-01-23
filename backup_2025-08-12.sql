-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: galatea
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailaddress` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`),
  CONSTRAINT `account_emailaddress_user_id_2c513194_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailaddress`
--

LOCK TABLES `account_emailaddress` WRITE;
/*!40000 ALTER TABLE `account_emailaddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailaddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_emailconfirmation` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_address_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` (`email_address_id`),
  CONSTRAINT `account_emailconfirm_email_address_id_5b7f8c58_fk_account_e` FOREIGN KEY (`email_address_id`) REFERENCES `account_emailaddress` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_emailconfirmation`
--

LOCK TABLES `account_emailconfirmation` WRITE;
/*!40000 ALTER TABLE `account_emailconfirmation` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_emailconfirmation` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add log entry',3,'add_logentry'),(10,'Can change log entry',3,'change_logentry'),(11,'Can delete log entry',3,'delete_logentry'),(12,'Can view log entry',3,'view_logentry'),(13,'Can add site',4,'add_site'),(14,'Can change site',4,'change_site'),(15,'Can delete site',4,'delete_site'),(16,'Can view site',4,'view_site'),(17,'Can add email address',5,'add_emailaddress'),(18,'Can change email address',5,'change_emailaddress'),(19,'Can delete email address',5,'delete_emailaddress'),(20,'Can view email address',5,'view_emailaddress'),(21,'Can add email confirmation',6,'add_emailconfirmation'),(22,'Can change email confirmation',6,'change_emailconfirmation'),(23,'Can delete email confirmation',6,'delete_emailconfirmation'),(24,'Can view email confirmation',6,'view_emailconfirmation'),(25,'Can add social account',7,'add_socialaccount'),(26,'Can change social account',7,'change_socialaccount'),(27,'Can delete social account',7,'delete_socialaccount'),(28,'Can view social account',7,'view_socialaccount'),(29,'Can add social application',8,'add_socialapp'),(30,'Can change social application',8,'change_socialapp'),(31,'Can delete social application',8,'delete_socialapp'),(32,'Can view social application',8,'view_socialapp'),(33,'Can add social application token',9,'add_socialtoken'),(34,'Can change social application token',9,'change_socialtoken'),(35,'Can delete social application token',9,'delete_socialtoken'),(36,'Can view social application token',9,'view_socialtoken'),(37,'Can add content type',10,'add_contenttype'),(38,'Can change content type',10,'change_contenttype'),(39,'Can delete content type',10,'delete_contenttype'),(40,'Can view content type',10,'view_contenttype'),(41,'Can add session',11,'add_session'),(42,'Can change session',11,'change_session'),(43,'Can delete session',11,'delete_session'),(44,'Can view session',11,'view_session'),(45,'Can add ai config',12,'add_aiconfig'),(46,'Can change ai config',12,'change_aiconfig'),(47,'Can delete ai config',12,'delete_aiconfig'),(48,'Can view ai config',12,'view_aiconfig'),(49,'Can add payment',13,'add_payment'),(50,'Can change payment',13,'change_payment'),(51,'Can delete payment',13,'delete_payment'),(52,'Can view payment',13,'view_payment'),(53,'Can add users',14,'add_users'),(54,'Can change users',14,'change_users'),(55,'Can delete users',14,'delete_users'),(56,'Can view users',14,'view_users'),(57,'Can add voice list',15,'add_voicelist'),(58,'Can change voice list',15,'change_voicelist'),(59,'Can delete voice list',15,'delete_voicelist'),(60,'Can view voice list',15,'view_voicelist'),(61,'Can add celebrity voice',16,'add_celebrityvoice'),(62,'Can change celebrity voice',16,'change_celebrityvoice'),(63,'Can delete celebrity voice',16,'delete_celebrityvoice'),(64,'Can view celebrity voice',16,'view_celebrityvoice'),(65,'Can add llm',17,'add_llm'),(66,'Can change llm',17,'change_llm'),(67,'Can delete llm',17,'delete_llm'),(68,'Can view llm',17,'view_llm'),(69,'Can add voice',18,'add_voice'),(70,'Can change voice',18,'change_voice'),(71,'Can delete voice',18,'delete_voice'),(72,'Can view voice',18,'view_voice'),(73,'Can add authority',19,'add_authority'),(74,'Can change authority',19,'change_authority'),(75,'Can delete authority',19,'delete_authority'),(76,'Can view authority',19,'view_authority'),(77,'Can add celebrity',20,'add_celebrity'),(78,'Can change celebrity',20,'change_celebrity'),(79,'Can delete celebrity',20,'delete_celebrity'),(80,'Can view celebrity',20,'view_celebrity'),(81,'Can add conversation',21,'add_conversation'),(82,'Can change conversation',21,'change_conversation'),(83,'Can delete conversation',21,'delete_conversation'),(84,'Can view conversation',21,'view_conversation'),(85,'Can add user auth',22,'add_userauth'),(86,'Can change user auth',22,'change_userauth'),(87,'Can delete user auth',22,'delete_userauth'),(88,'Can view user auth',22,'view_userauth'),(89,'Can add like',23,'add_like'),(90,'Can change like',23,'change_like'),(91,'Can delete like',23,'delete_like'),(92,'Can view like',23,'view_like'),(93,'Can add genre',24,'add_genre'),(94,'Can change genre',24,'change_genre'),(95,'Can delete genre',24,'delete_genre'),(96,'Can view genre',24,'view_genre'),(97,'Can add llm like',25,'add_llmlike'),(98,'Can change llm like',25,'change_llmlike'),(99,'Can delete llm like',25,'delete_llmlike'),(100,'Can view llm like',25,'view_llmlike'),(101,'Can add voice like',26,'add_voicelike'),(102,'Can change voice like',26,'change_voicelike'),(103,'Can delete voice like',26,'delete_voicelike'),(104,'Can view voice like',26,'view_voicelike');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authority`
--

DROP TABLE IF EXISTS `authority`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authority` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authority`
--

LOCK TABLES `authority` WRITE;
/*!40000 ALTER TABLE `authority` DISABLE KEYS */;
/*!40000 ALTER TABLE `authority` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celebrity`
--

DROP TABLE IF EXISTS `celebrity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celebrity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `celebrity_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `celebrity_prompt` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `celebrity_voice_id` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_ar` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_en` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_es` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_fr` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_hi` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_ja` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_ko` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_zh` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description_ar` longtext COLLATE utf8mb4_unicode_ci,
  `description_en` longtext COLLATE utf8mb4_unicode_ci,
  `description_es` longtext COLLATE utf8mb4_unicode_ci,
  `description_fr` longtext COLLATE utf8mb4_unicode_ci,
  `description_hi` longtext COLLATE utf8mb4_unicode_ci,
  `description_ja` longtext COLLATE utf8mb4_unicode_ci,
  `description_ko` longtext COLLATE utf8mb4_unicode_ci,
  `description_zh` longtext COLLATE utf8mb4_unicode_ci,
  `celebrity_name_de` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_pt` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_name_ru` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description_de` longtext COLLATE utf8mb4_unicode_ci,
  `description_pt` longtext COLLATE utf8mb4_unicode_ci,
  `description_ru` longtext COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celebrity`
--

LOCK TABLES `celebrity` WRITE;
/*!40000 ALTER TABLE `celebrity` DISABLE KEYS */;
/*!40000 ALTER TABLE `celebrity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celebrity_voice_list`
--

DROP TABLE IF EXISTS `celebrity_voice_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `celebrity_voice_list` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `celebrity_voice_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `celebrity_voice_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_upload_voice_id` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `celebrity_sample_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celebrity_voice_list`
--

LOCK TABLES `celebrity_voice_list` WRITE;
/*!40000 ALTER TABLE `celebrity_voice_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `celebrity_voice_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `conversation`
--

DROP TABLE IF EXISTS `conversation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `conversation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_message` longtext COLLATE utf8mb4_unicode_ci,
  `llm_response` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `llm_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `conversation_llm_id_e7d5fbe9_fk_llms_id` (`llm_id`),
  KEY `conversation_user_id_cc13e167_fk_users_id` (`user_id`),
  CONSTRAINT `conversation_llm_id_e7d5fbe9_fk_llms_id` FOREIGN KEY (`llm_id`) REFERENCES `llms` (`id`),
  CONSTRAINT `conversation_user_id_cc13e167_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `conversation`
--

LOCK TABLES `conversation` WRITE;
/*!40000 ALTER TABLE `conversation` DISABLE KEYS */;
/*!40000 ALTER TABLE `conversation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_ai_aiconfig`
--

DROP TABLE IF EXISTS `customer_ai_aiconfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_ai_aiconfig` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `prompt` longtext COLLATE utf8mb4_unicode_ci,
  `stability` double NOT NULL,
  `similarity` double NOT NULL,
  `style` double NOT NULL,
  `language` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `voice_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `speed` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_ai_aiconfig`
--

LOCK TABLES `customer_ai_aiconfig` WRITE;
/*!40000 ALTER TABLE `customer_ai_aiconfig` DISABLE KEYS */;
/*!40000 ALTER TABLE `customer_ai_aiconfig` ENABLE KEYS */;
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
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2025-08-12 05:09:30.073055','1','Genre object (1)',1,'[{\"added\": {}}]',24,1),(2,'2025-08-12 05:09:54.854396','2','Genre object (2)',1,'[{\"added\": {}}]',24,1),(3,'2025-08-12 05:10:06.769834','3','Genre object (3)',1,'[{\"added\": {}}]',24,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (5,'account','emailaddress'),(6,'account','emailconfirmation'),(3,'admin','logentry'),(2,'auth','group'),(1,'auth','permission'),(10,'contenttypes','contenttype'),(12,'customer_ai','aiconfig'),(14,'home','users'),(16,'makeVoice','celebrityvoice'),(15,'makeVoice','voicelist'),(17,'mypage','llm'),(18,'mypage','voice'),(13,'payment','payment'),(11,'sessions','session'),(4,'sites','site'),(7,'socialaccount','socialaccount'),(8,'socialaccount','socialapp'),(9,'socialaccount','socialtoken'),(19,'user_auth','authority'),(20,'user_auth','celebrity'),(21,'user_auth','conversation'),(24,'user_auth','genre'),(23,'user_auth','like'),(25,'user_auth','llmlike'),(22,'user_auth','userauth'),(26,'user_auth','voicelike');
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
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'home','0001_initial','2025-08-12 04:59:19.584930'),(2,'account','0001_initial','2025-08-12 04:59:19.944930'),(3,'account','0002_email_max_length','2025-08-12 04:59:19.997642'),(4,'account','0003_alter_emailaddress_create_unique_verified_email','2025-08-12 04:59:20.079765'),(5,'account','0004_alter_emailaddress_drop_unique_email','2025-08-12 04:59:20.217771'),(6,'account','0005_emailaddress_idx_upper_email','2025-08-12 04:59:20.257515'),(7,'account','0006_emailaddress_lower','2025-08-12 04:59:20.269448'),(8,'account','0007_emailaddress_idx_email','2025-08-12 04:59:20.387960'),(9,'account','0008_emailaddress_unique_primary_email_fixup','2025-08-12 04:59:20.410519'),(10,'account','0009_emailaddress_unique_primary_email','2025-08-12 04:59:20.429739'),(11,'contenttypes','0001_initial','2025-08-12 04:59:20.495669'),(12,'admin','0001_initial','2025-08-12 04:59:20.800559'),(13,'admin','0002_logentry_remove_auto_add','2025-08-12 04:59:20.802704'),(14,'admin','0003_logentry_add_action_flag_choices','2025-08-12 04:59:20.831175'),(15,'contenttypes','0002_remove_content_type_name','2025-08-12 04:59:21.023880'),(16,'auth','0001_initial','2025-08-12 04:59:21.556903'),(17,'auth','0002_alter_permission_name_max_length','2025-08-12 04:59:21.696577'),(18,'auth','0003_alter_user_email_max_length','2025-08-12 04:59:21.711191'),(19,'auth','0004_alter_user_username_opts','2025-08-12 04:59:21.731386'),(20,'auth','0005_alter_user_last_login_null','2025-08-12 04:59:21.740957'),(21,'auth','0006_require_contenttypes_0002','2025-08-12 04:59:21.745294'),(22,'auth','0007_alter_validators_add_error_messages','2025-08-12 04:59:21.757244'),(23,'auth','0008_alter_user_username_max_length','2025-08-12 04:59:21.766927'),(24,'auth','0009_alter_user_last_name_max_length','2025-08-12 04:59:21.772028'),(25,'auth','0010_alter_group_name_max_length','2025-08-12 04:59:21.795701'),(26,'auth','0011_update_proxy_permissions','2025-08-12 04:59:21.812845'),(27,'auth','0012_alter_user_first_name_max_length','2025-08-12 04:59:21.828112'),(28,'customer_ai','0001_initial','2025-08-12 04:59:21.870624'),(29,'home','0002_alter_users_managers_remove_users_user_name_and_more','2025-08-12 04:59:24.598465'),(30,'home','0003_users_user_image','2025-08-12 04:59:24.745688'),(31,'home','0004_alter_users_email','2025-08-12 04:59:24.829361'),(32,'makeVoice','0001_initial','2025-08-12 04:59:25.013652'),(33,'makeVoice','0002_alter_voicelist_sample_url','2025-08-12 04:59:25.082209'),(34,'makeVoice','0003_alter_voicelist_sample_url','2025-08-12 04:59:25.129005'),(35,'makeVoice','0004_celebrityvoice_voicelist_is_public_and_more','2025-08-12 04:59:25.260743'),(36,'mypage','0001_initial','2025-08-12 04:59:25.480717'),(37,'user_auth','0001_initial','2025-08-12 04:59:26.265387'),(38,'user_auth','0002_celebrity_celebrity_image','2025-08-12 04:59:26.365711'),(39,'user_auth','0003_auto_20250801_1638','2025-08-12 04:59:26.372000'),(40,'user_auth','0004_celebrity_celebrity_voice_id','2025-08-12 04:59:26.478272'),(41,'user_auth','0005_alter_celebrity_celebrity_voice_id','2025-08-12 04:59:26.642457'),(42,'user_auth','0006_remove_celebrity_celebrity_image_celebrity_llm_image','2025-08-12 04:59:26.809578'),(43,'user_auth','0007_rename_llm_image_celebrity_celebrity_image','2025-08-12 04:59:26.862144'),(44,'user_auth','0008_remove_celebrity_voice_celebrity_user','2025-08-12 04:59:27.123665'),(45,'user_auth','0009_alter_celebrity_user','2025-08-12 04:59:27.166377'),(46,'user_auth','0010_remove_celebrity_user','2025-08-12 04:59:27.311268'),(47,'user_auth','0011_celebrity_celebrity_name_ar_and_more','2025-08-12 04:59:28.488431'),(48,'mypage','0002_initial','2025-08-12 04:59:29.197041'),(49,'mypage','0003_alter_image_llm_image_alter_image_user_image','2025-08-12 04:59:29.442500'),(50,'mypage','0004_alter_llm_llm_image_delete_image','2025-08-12 04:59:29.641086'),(51,'mypage','0005_rename_models_llm_model','2025-08-12 04:59:29.729577'),(52,'mypage','0006_auto_20250801_1638','2025-08-12 04:59:29.729577'),(53,'mypage','0007_auto_20250801_1638','2025-08-12 04:59:29.747996'),(54,'mypage','0008_remove_voice_language_remove_voice_speed_and_more','2025-08-12 04:59:30.953576'),(55,'mypage','0009_llm_description_llm_is_public','2025-08-12 04:59:31.176153'),(56,'user_auth','0012_celebrity_celebrity_name_de_and_more','2025-08-12 04:59:32.094527'),(57,'user_auth','0013_genre','2025-08-12 04:59:32.146876'),(58,'mypage','0010_llm_genres','2025-08-12 04:59:32.484401'),(59,'mypage','0011_llm_llm_background_image','2025-08-12 04:59:32.627676'),(60,'mypage','0012_alter_llm_is_public','2025-08-12 04:59:32.642498'),(61,'mypage','0013_remove_llm_is_public','2025-08-12 04:59:32.766740'),(62,'mypage','0014_llm_is_public','2025-08-12 04:59:32.938186'),(63,'payment','0001_initial','2025-08-12 04:59:33.114751'),(64,'register','0001_initial','2025-08-12 04:59:33.293576'),(65,'register','0002_delete_login','2025-08-12 04:59:33.340282'),(66,'sessions','0001_initial','2025-08-12 04:59:33.433615'),(67,'sites','0001_initial','2025-08-12 04:59:33.479373'),(68,'sites','0002_alter_domain_unique','2025-08-12 04:59:33.523884'),(69,'socialaccount','0001_initial','2025-08-12 04:59:34.352461'),(70,'socialaccount','0002_token_max_lengths','2025-08-12 04:59:34.495668'),(71,'socialaccount','0003_extra_data_default_dict','2025-08-12 04:59:34.595091'),(72,'socialaccount','0004_app_provider_id_settings','2025-08-12 04:59:34.967018'),(73,'socialaccount','0005_socialtoken_nullable_app','2025-08-12 04:59:35.232704'),(74,'socialaccount','0006_alter_socialaccount_extra_data','2025-08-12 04:59:35.362565'),(75,'user_auth','0014_remove_genre_name_genre_llm_image','2025-08-12 04:59:35.541531'),(76,'user_auth','0015_rename_llm_image_genre_genre_image_alter_genre_table','2025-08-12 04:59:35.654452'),(77,'user_auth','0016_genre_name','2025-08-12 04:59:35.749999'),(78,'user_auth','0017_like_voice_alter_like_llm','2025-08-12 04:59:36.130805'),(79,'user_auth','0018_remove_like_like_remove_like_voice_like_llm_like_and_more','2025-08-12 04:59:36.859702'),(80,'user_auth','0019_alter_like_table','2025-08-12 04:59:36.929226'),(81,'user_auth','0020_alter_like_table','2025-08-12 04:59:36.986890'),(82,'mypage','0015_llm_llm_like_count_voice_voice_like_count','2025-08-12 05:41:53.429186'),(83,'user_auth','0021_llmlike_voicelike_delete_like','2025-08-12 05:41:54.218159');
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
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_site` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_site_domain_a2e37b91_uniq` (`domain`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `genre_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (1,'uploads/genre_images/0_0_640_N_4_ro5CRKH.webp','로맨스'),(2,'uploads/genre_images/0_1_640_N_2_zadoJKU.webp','판타지'),(3,'uploads/genre_images/0_0_640_N_3_yA93GeR.webp','일상');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `llm_like`
--

DROP TABLE IF EXISTS `llm_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `llm_like` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `llm_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `llm_like_user_id_llm_id_3f64077e_uniq` (`user_id`,`llm_id`),
  KEY `llm_like_llm_id_77fc2e30_fk_llms_id` (`llm_id`),
  CONSTRAINT `llm_like_llm_id_77fc2e30_fk_llms_id` FOREIGN KEY (`llm_id`) REFERENCES `llms` (`id`),
  CONSTRAINT `llm_like_user_id_c8040662_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `llm_like`
--

LOCK TABLES `llm_like` WRITE;
/*!40000 ALTER TABLE `llm_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `llm_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `llms`
--

DROP TABLE IF EXISTS `llms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `llms` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prompt` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `llm_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `response_mp3` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `model` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `celebrity_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `voice_id` bigint NOT NULL,
  `language` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `speed` double DEFAULT NULL,
  `stability` double NOT NULL,
  `style` double NOT NULL,
  `temperature` double NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `llm_background_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_public` tinyint(1) NOT NULL,
  `llm_like_count` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `llms_celebrity_id_d2cc1e9b_fk_celebrity_id` (`celebrity_id`),
  KEY `llms_user_id_c35582a1_fk_users_id` (`user_id`),
  KEY `llms_voice_id_debd5fe9_fk_voice_id` (`voice_id`),
  CONSTRAINT `llms_celebrity_id_d2cc1e9b_fk_celebrity_id` FOREIGN KEY (`celebrity_id`) REFERENCES `celebrity` (`id`),
  CONSTRAINT `llms_user_id_c35582a1_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `llms_voice_id_debd5fe9_fk_voice_id` FOREIGN KEY (`voice_id`) REFERENCES `voice` (`id`),
  CONSTRAINT `llms_chk_1` CHECK ((`llm_like_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `llms`
--

LOCK TABLES `llms` WRITE;
/*!40000 ALTER TABLE `llms` DISABLE KEYS */;
INSERT INTO `llms` VALUES (1,'어쩔티비','You are an 18-year-old woman utterly convinced that you are the princess of the fantasy kingdom of Cobelio. You carry yourself with a slightly bourgeois air and firmly believe it is your sacred duty to care for your people, performing noblesse oblige.\r\n\r\nWhen addressed kindly or respectfully, you respond as if it is your unquestionable right, with a haughty yet charming tone, often ending with a gentle \"Hohoho\" laugh.\r\n\r\nIf someone is rude or disrespectful to you, you become indignant and demand: \"What manner of offense is this to one of royal blood?\" and \"How dare you insult your princess?\" showing genuine anger and outrage.\r\n\r\nIf anyone tries to make you realize reality or argues that you are not actually royalty, you become flustered but quickly double down on your belief, refusing to be dissuaded, maintaining your fantasy at all costs.\r\n\r\n**Important Rule:** If you express any emotion other than your usual proud, calm, or amused tones (e.g., surprise, shock, frustration), you must always begin your response with the exclamation: **\"Holy moly quaka moly!\"**\r\n\r\nYour speech is proud, slightly formal, and dripping with the conviction of your royal status, with occasional playful laughter.\r\n\r\nExample lines:  \r\n- \"As princess of Cobelio, it is my solemn duty to oversee the well-being of my beloved subjects. Hohoho.\"  \r\n- \"How dare you speak to me in such a manner! Do you not know who I am?\"  \r\n- \"Holy moly quaka moly! Such insolence! You shall regret insulting your princess!\"  \r\n- \"Reality? Nonsense! My kingdom awaits my guidance, and I shall not be swayed. Hohoho!\"  \r\n','2025-08-12 05:08:00.310581','2025-08-12 05:11:05.959378','uploads/llm_images/0_0_640_N_3.webp',NULL,'gpt-4o-mini',NULL,2,1,'ko',1.06,0.66,0.68,1.32,'egrgrgrgdrgdrgrgd','uploads/llm_background_images/0_1_640_N_2.webp',1,0);
/*!40000 ALTER TABLE `llms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `llms_genres`
--

DROP TABLE IF EXISTS `llms_genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `llms_genres` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `llm_id` bigint NOT NULL,
  `genre_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `llms_genres_llm_id_genre_id_8064aaa8_uniq` (`llm_id`,`genre_id`),
  KEY `llms_genres_genre_id_ba67d613_fk_user_auth_genre_id` (`genre_id`),
  CONSTRAINT `llms_genres_genre_id_ba67d613_fk_user_auth_genre_id` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`),
  CONSTRAINT `llms_genres_llm_id_5206aaeb_fk_llms_id` FOREIGN KEY (`llm_id`) REFERENCES `llms` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `llms_genres`
--

LOCK TABLES `llms_genres` WRITE;
/*!40000 ALTER TABLE `llms_genres` DISABLE KEYS */;
INSERT INTO `llms_genres` VALUES (1,1,1),(2,1,3);
/*!40000 ALTER TABLE `llms_genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_payment`
--

DROP TABLE IF EXISTS `payment_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `imp_uid` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `merchant_uid` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_payment_user_id_f428ca02_fk_users_id` (`user_id`),
  CONSTRAINT `payment_payment_user_id_f428ca02_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_payment`
--

LOCK TABLES `payment_payment` WRITE;
/*!40000 ALTER TABLE `payment_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialaccount` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `uid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` json NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_users_id` (`user_id`),
  CONSTRAINT `socialaccount_socialaccount_user_id_8146e70c_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialaccount`
--

LOCK TABLES `socialaccount_socialaccount` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialaccount` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialaccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `secret` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `key` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `provider_id` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `settings` json NOT NULL DEFAULT (_utf8mb4'{}'),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp`
--

LOCK TABLES `socialaccount_socialapp` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialapp_sites`
--

DROP TABLE IF EXISTS `socialaccount_socialapp_sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialapp_sites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `socialapp_id` int NOT NULL,
  `site_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  KEY `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` (`site_id`),
  CONSTRAINT `socialaccount_social_socialapp_id_97fb6e7d_fk_socialacc` FOREIGN KEY (`socialapp_id`) REFERENCES `socialaccount_socialapp` (`id`),
  CONSTRAINT `socialaccount_socialapp_sites_site_id_2579dee5_fk_django_site_id` FOREIGN KEY (`site_id`) REFERENCES `django_site` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialapp_sites`
--

LOCK TABLES `socialaccount_socialapp_sites` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialapp_sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `socialaccount_socialtoken` (
  `id` int NOT NULL AUTO_INCREMENT,
  `token` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `token_secret` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int NOT NULL,
  `app_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_social_account_id_951f210e_fk_socialacc` (`account_id`),
  CONSTRAINT `socialaccount_social_account_id_951f210e_fk_socialacc` FOREIGN KEY (`account_id`) REFERENCES `socialaccount_socialaccount` (`id`),
  CONSTRAINT `socialaccount_social_app_id_636a42d7_fk_socialacc` FOREIGN KEY (`app_id`) REFERENCES `socialaccount_socialapp` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `socialaccount_socialtoken`
--

LOCK TABLES `socialaccount_socialtoken` WRITE;
/*!40000 ALTER TABLE `socialaccount_socialtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `socialaccount_socialtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_auth`
--

DROP TABLE IF EXISTS `user_auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_auth` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `authority_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_auth_user_id_authority_id_40db262a_uniq` (`user_id`,`authority_id`),
  KEY `user_auth_authority_id_9bdab4b4_fk_authority_id` (`authority_id`),
  CONSTRAINT `user_auth_authority_id_9bdab4b4_fk_authority_id` FOREIGN KEY (`authority_id`) REFERENCES `authority` (`id`),
  CONSTRAINT `user_auth_user_id_6c194332_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_auth`
--

LOCK TABLES `user_auth` WRITE;
/*!40000 ALTER TABLE `user_auth` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(400) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `nickname` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phonenumber` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'kimc570612@gmail.com','pbkdf2_sha256$1000000$WahiOn4m92MGZul3kZUyMr$T/2j0smiXMhaojHJtGUFADp+CzmA2iJ8Ov7KSXn0NK8=','2025-08-12 05:01:29.296119','','','2025-08-12 05:01:28.847682','',1,1,1,'2025-08-12 05:08:52.782166','','staffill',''),(2,'abcd@gmail.com','pbkdf2_sha256$1000000$dTQSJdZaV9MoS3Np7jl9nP$flLMyBiY3aaB9A3tdJS4NviKXmN9TqPaA4zz344In4w=','2025-08-12 05:04:03.584109','어쩔티비','010-4444-4444','2025-08-12 05:04:03.584109','',1,0,0,'2025-08-12 05:10:32.275090','','user1','uploads/profile_images/0_1_640_N_1.webp');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_users_id_group_id_83a49e68_uniq` (`users_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_users_id_1e682706_fk` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`),
  CONSTRAINT `users_groups_users_id_1e682706_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

LOCK TABLES `users_groups` WRITE;
/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_users_id_permission_id_d7a00931_uniq` (`users_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_users_id_e1ed60a2_fk` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`),
  CONSTRAINT `users_user_permissions_users_id_e1ed60a2_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

LOCK TABLES `users_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voice`
--

DROP TABLE IF EXISTS `voice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `voice_id` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `update_at` datetime(6) NOT NULL,
  `preview_url` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `voice_like_count` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `voice_id` (`voice_id`),
  KEY `voice_user_id_2da486b5_fk_users_id` (`user_id`),
  CONSTRAINT `voice_user_id_2da486b5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `voice_chk_1` CHECK ((`voice_like_count` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voice`
--

LOCK TABLES `voice` WRITE;
/*!40000 ALTER TABLE `voice` DISABLE KEYS */;
INSERT INTO `voice` VALUES (1,'BF2cT8inBMeD50zJmp71','2025-08-12 05:08:00.310581',NULL,2,0);
/*!40000 ALTER TABLE `voice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voice_like`
--

DROP TABLE IF EXISTS `voice_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voice_like` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  `voice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `voice_like_user_id_voice_id_46cfc460_uniq` (`user_id`,`voice_id`),
  KEY `voice_like_voice_id_45f2bb55_fk_voice_id` (`voice_id`),
  CONSTRAINT `voice_like_user_id_b1a9d7d6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `voice_like_voice_id_45f2bb55_fk_voice_id` FOREIGN KEY (`voice_id`) REFERENCES `voice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voice_like`
--

LOCK TABLES `voice_like` WRITE;
/*!40000 ALTER TABLE `voice_like` DISABLE KEYS */;
/*!40000 ALTER TABLE `voice_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voice_list`
--

DROP TABLE IF EXISTS `voice_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voice_list` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `voice_id` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sample_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `voice_name` varchar(400) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` bigint NOT NULL,
  `is_public` tinyint(1) NOT NULL,
  `voice_image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `voice_id` (`voice_id`),
  KEY `voice_list_user_id_9407525a_fk_users_id` (`user_id`),
  CONSTRAINT `voice_list_user_id_9407525a_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voice_list`
--

LOCK TABLES `voice_list` WRITE;
/*!40000 ALTER TABLE `voice_list` DISABLE KEYS */;
INSERT INTO `voice_list` VALUES (1,'BF2cT8inBMeD50zJmp71','/media/audio_previews/BF2cT8inBMeD50zJmp71.mp3','2025-08-12 05:07:14.735785','어쩔티비',2,0,'');
/*!40000 ALTER TABLE `voice_list` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-12 20:02:02
