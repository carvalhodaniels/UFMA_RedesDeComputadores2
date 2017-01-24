
-- -----------------------------------------------------
-- Schema skynetdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `skynetdb` DEFAULT CHARACTER SET utf8 ;
USE `skynetdb` ;

-- -----------------------------------------------------
-- Table `skynetdb`.`conta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `skynetdb`.`conta` (
  `idconta` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(23) NOT NULL default '',
  `password` VARCHAR(23) NOT NULL default '',
  `nome` VARCHAR(23) NOT NULL default '',
  `last_ip` varchar(19) NOT NULL default '',
  PRIMARY KEY (`idconta`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `skynetdb`.`compromisso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `skynetdb`.`compromisso` (
  `idcompromisso` INT NOT NULL AUTO_INCREMENT,
  `data` DATE NOT NULL DEFAULT '00-00-0000',
  `descricao` TEXT NOT NULL default '',
  PRIMARY KEY (`idcompromisso`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `skynetdb`.`compromisso_conta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `skynetdb`.`compromisso_conta` (
  `idconta` INT NOT NULL,
  `idcompromisso` INT NOT NULL,
  PRIMARY KEY (`idconta`, `idcompromisso`),
  INDEX `fk_account_has_compromisso_compromisso1_idx` (`idcompromisso` ASC),
  INDEX `fk_account_has_compromisso_account_idx` (`idconta` ASC),
  CONSTRAINT `fk_account_has_compromisso_account`
    FOREIGN KEY (`idconta`)
    REFERENCES `skynetdb`.`conta` (`idconta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_account_has_compromisso_compromisso1`
    FOREIGN KEY (`idcompromisso`)
    REFERENCES `skynetdb`.`compromisso` (`idcompromisso`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

