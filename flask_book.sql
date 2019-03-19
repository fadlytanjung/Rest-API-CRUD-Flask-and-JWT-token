-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 19, 2019 at 03:55 PM
-- Server version: 5.7.25-0ubuntu0.18.04.2
-- PHP Version: 7.2.15-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask_book`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_books`
--

CREATE TABLE `tbl_books` (
  `id_book` int(10) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `author` varchar(255) NOT NULL,
  `date_book` date NOT NULL,
  `price` varchar(255) NOT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `book_status` enum('available','borrowed') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_books`
--

INSERT INTO `tbl_books` (`id_book`, `title`, `description`, `author`, `date_book`, `price`, `cover`, `book_status`) VALUES
(1, 'Api Sejarah', 'Sejarah Besar bangsa Indonesia dari sudut pandang ulama dan santri', 'Ahmad Mansyur Suryanegara', '2019-03-12', '101000', '', 'available'),
(2, 'Api Sejarah 2', 'Sejarah Indonesia Lanjutan', 'Ahmad Mansyur S', '2019-03-02', '150000', '', 'available'),
(5, 'Api Sejarah 3', 'Api Sejarah 3 ni', 'Ahmad Mansyur S', '2019-03-01', '140000', 'fadlytanjung2.jpg', 'available'),
(6, 'Api Sejarah 4', 'Api Sejarah 4 ni', 'Ahmad Mansyur S', '2019-03-01', '140000', 'fadlytanjung2.jpg', 'available'),
(7, 'Api Sejarah 5', 'Api Sejarah 4 ni', 'Ahmad Mansyur S', '2019-03-01', '140000', '', 'available');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_books`
--
ALTER TABLE `tbl_books`
  ADD PRIMARY KEY (`id_book`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_books`
--
ALTER TABLE `tbl_books`
  MODIFY `id_book` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;