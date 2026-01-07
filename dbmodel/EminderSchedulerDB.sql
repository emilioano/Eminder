-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema EminderSchedulerDB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema EminderSchedulerDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `EminderSchedulerDB` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `EminderSchedulerDB` ;

-- -----------------------------------------------------
-- Table `EminderSchedulerDB`.`Tasks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `EminderSchedulerDB`.`Tasks` (
  `TaskId` INT NOT NULL AUTO_INCREMENT,
  `Subject` VARCHAR(250) NULL,
  `Message` TEXT(10000) NULL,
  `Dailyquote` TINYINT NOT NULL DEFAULT 0,
  `Dailyweather` TINYINT NOT NULL DEFAULT 0,
  `Schedule` JSON NULL,
  `Active` TINYINT NOT NULL DEFAULT 1,
  `Channel` INT NOT NULL DEFAULT 0,
  `Location` VARCHAR(45) NULL,
  `Lasttriggered` DATETIME NULL,
  `Createdtime` DATETIME NULL,
  PRIMARY KEY (`TaskId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `EminderSchedulerDB`.`Recipients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `EminderSchedulerDB`.`Recipients` (
  `RecipientId` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(100) NULL,
  `Email` VARCHAR(100) NULL,
  `Phone` VARCHAR(100) NULL,
  `Active` TINYINT NOT NULL DEFAULT 1,
  `DiscordHook` VARCHAR(500) NULL,
  PRIMARY KEY (`RecipientId`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `EminderSchedulerDB`.`TaskRecipients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `EminderSchedulerDB`.`TaskRecipients` (
  `TaskId` INT NOT NULL,
  `RecipientId` INT NOT NULL,
  INDEX `Id_idx1` (`RecipientId` ASC) VISIBLE,
  PRIMARY KEY (`TaskId`, `RecipientId`),
  CONSTRAINT `TaskId`
    FOREIGN KEY (`TaskId`)
    REFERENCES `EminderSchedulerDB`.`Tasks` (`TaskId`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `RecipientId`
    FOREIGN KEY (`RecipientId`)
    REFERENCES `EminderSchedulerDB`.`Recipients` (`RecipientId`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `EminderSchedulerDB`.`Performance`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `EminderSchedulerDB`.`Performance` (
  `Id` INT NOT NULL AUTO_INCREMENT,
  `Operation` VARCHAR(45) NOT NULL,
  `Starttime` DATETIME(2) NOT NULL,
  `Finishtime` DATETIME(2) NOT NULL,
  `TaskId` INT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE INDEX `Id_UNIQUE` (`Id` ASC) VISIBLE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
