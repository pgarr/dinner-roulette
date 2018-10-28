CREATE DATABASE  IF NOT EXISTS `dinner-roulette`;
USE `dinner-roulette`;

DROP TABLE IF EXISTS `recipe_detail`;
CREATE TABLE `recipe_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `link` varchar(1000) DEFAULT NULL,
  `description` text DEFAULT NULL,
  
  PRIMARY KEY (`id`)
  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `recipe`;
CREATE TABLE `recipe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `recipe_detail_id` int(11) NOT NULL,
  
  PRIMARY KEY (`id`),
  
  UNIQUE KEY `NAME_UNIQUE` (`name`),
  
  CONSTRAINT `FK_DETAIL` 
  FOREIGN KEY (`recipe_detail_id`) 
  REFERENCES `recipe_detail` (`id`) 
  
  ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `ingredient`;
CREATE TABLE `ingredient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
    
  PRIMARY KEY (`id`),
  
  UNIQUE KEY `NAME_UNIQUE` (`name`)
  
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `recipe_ingredient` (
  `recipe_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  `amount` int(11) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  
  PRIMARY KEY (`recipe_id`,`ingredient_id`),
  
  KEY `FK_RECIPE_idx` (`recipe_id`),
  
  CONSTRAINT `FK_RECIPE` FOREIGN KEY (`recipe_id`) 
  REFERENCES `recipe` (`id`) 
  ON DELETE NO ACTION ON UPDATE NO ACTION,
  
  CONSTRAINT `FK_INGREDIENT` FOREIGN KEY (`ingredient_id`) 
  REFERENCES `ingredient` (`id`) 
  ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;





