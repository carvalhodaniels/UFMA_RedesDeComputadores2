-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: 29-Jan-2017 às 23:22
-- Versão do servidor: 10.1.19-MariaDB
-- PHP Version: 7.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `skynetdb`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `compromisso`
--

CREATE TABLE `compromisso` (
  `idcompromisso` int(11) NOT NULL,
  `data` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `descricao` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `compromisso`
--

INSERT INTO `compromisso` (`idcompromisso`, `data`, `descricao`) VALUES
(1, '2222-12-12 12:12:00', 'shshshs'),
(3, '9999-11-12 12:12:00', 'ddhdhhd'),
(4, '2017-01-25 16:00:00', 'o fim dessa merda'),
(5, '2017-01-25 17:00:00', 'o fim dessa merda ainda nao chegou'),
(6, '2019-10-01 10:10:00', 'porque'),
(7, '2019-10-10 10:12:00', 'coisasa'),
(8, '2018-10-10 12:12:00', 'teste do convite'),
(9, '2021-12-19 10:30:00', 'coisas'),
(10, '2018-07-22 00:00:00', ''),
(11, '2111-11-11 12:12:00', 'deded'),
(12, '2333-11-11 12:12:00', 'deded'),
(13, '2111-10-10 12:12:00', 'edede'),
(14, '2121-12-10 12:12:00', 'deded'),
(15, '8888-12-22 12:12:00', 'deded'),
(16, '2016-02-19 10:10:00', 'coisas');

-- --------------------------------------------------------

--
-- Estrutura da tabela `compromisso_conta`
--

CREATE TABLE `compromisso_conta` (
  `idconta` int(11) NOT NULL,
  `idcompromisso` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `compromisso_conta`
--

INSERT INTO `compromisso_conta` (`idconta`, `idcompromisso`, `status`) VALUES
(1, 1, 1),
(1, 3, 1),
(1, 4, 1),
(1, 5, 1),
(1, 6, 1),
(1, 7, 1),
(1, 8, 1),
(1, 9, 1),
(1, 10, 1),
(1, 11, 1),
(1, 12, 1),
(1, 13, 1),
(1, 14, 1),
(1, 15, 1),
(1, 16, 1),
(2, 15, 0),
(2, 16, 0);

-- --------------------------------------------------------

--
-- Estrutura da tabela `conta`
--

CREATE TABLE `conta` (
  `idconta` int(11) NOT NULL,
  `login` varchar(23) NOT NULL DEFAULT '',
  `password` varchar(23) NOT NULL DEFAULT '',
  `nome` varchar(23) NOT NULL DEFAULT '',
  `last_ip` varchar(19) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `conta`
--

INSERT INTO `conta` (`idconta`, `login`, `password`, `nome`, `last_ip`) VALUES
(1, 'teste', 'teste', 'teste', ''),
(2, 'coisa', 'coisa', 'coisa', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `compromisso`
--
ALTER TABLE `compromisso`
  ADD PRIMARY KEY (`idcompromisso`);

--
-- Indexes for table `compromisso_conta`
--
ALTER TABLE `compromisso_conta`
  ADD PRIMARY KEY (`idconta`,`idcompromisso`),
  ADD KEY `fk_account_has_compromisso_compromisso1_idx` (`idcompromisso`),
  ADD KEY `fk_account_has_compromisso_account_idx` (`idconta`);

--
-- Indexes for table `conta`
--
ALTER TABLE `conta`
  ADD PRIMARY KEY (`idconta`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `compromisso`
--
ALTER TABLE `compromisso`
  MODIFY `idcompromisso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
--
-- AUTO_INCREMENT for table `conta`
--
ALTER TABLE `conta`
  MODIFY `idconta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `compromisso_conta`
--
ALTER TABLE `compromisso_conta`
  ADD CONSTRAINT `fk_account_has_compromisso_account` FOREIGN KEY (`idconta`) REFERENCES `conta` (`idconta`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_account_has_compromisso_compromisso1` FOREIGN KEY (`idcompromisso`) REFERENCES `compromisso` (`idcompromisso`) ON DELETE NO ACTION ON UPDATE NO ACTION;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
