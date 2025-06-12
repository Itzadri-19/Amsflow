-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-06-2025 a las 14:37:17
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `amsflow`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias_productos`
--

CREATE TABLE `categorias_productos` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Volcado de datos para la tabla `categorias_productos`
--

INSERT INTO `categorias_productos` (`id_categoria`, `nombre`) VALUES
(1, 'Tecnología'),
(2, 'Ropa'),
(3, 'Alimentos'),
(4, 'Hogar'),
(5, 'Deportes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `correo`, `telefono`, `direccion`) VALUES
(1, 'Laura Pérez', 'laura.perez@email.com', '611223344', 'Calle Mayor 12, Madrid'),
(2, 'Carlos Ruiz', 'carlos.ruiz@email.com', '622334455', 'Av. del Sol 45, Sevilla'),
(3, 'Marta López', 'marta.lopez@email.com', '633445566', 'Calle Luna 3, Valencia'),
(4, 'Luis Fernández', 'luis.fernandez@email.com', '644556677', 'Paseo de la Castellana 101, Madrid');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalles_venta`
--

CREATE TABLE `detalles_venta` (
  `id_detalle` int(11) NOT NULL,
  `id_venta` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Volcado de datos para la tabla `detalles_venta`
--

INSERT INTO `detalles_venta` (`id_detalle`, `id_venta`, `id_producto`, `cantidad`, `precio_unitario`) VALUES
(1, 1, 1, 1, 699.99),
(2, 1, 2, 1, 14.99),
(3, 1, 6, 1, 89.00),
(4, 2, 5, 1, 25.00),
(5, 2, 2, 1, 14.99),
(6, 2, 7, 1, 69.95),
(7, 3, 4, 1, 499.00),
(8, 3, 8, 1, 4.25),
(9, 3, 9, 1, 22.15),
(10, 4, 3, 1, 6.50),
(11, 4, 10, 1, 59.95),
(12, 4, 2, 1, 42.79),
(13, 5, 1, 1, 699.99),
(14, 5, 4, 1, 29.99),
(15, 5, 6, 1, 105.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `nombre`, `correo`, `telefono`, `direccion`) VALUES
(1, 'Ana Gómez', 'ana.gomez@empresa.com', '611111111', 'Calle Empresa 1, Madrid'),
(2, 'Javier Torres', 'javier.torres@empresa.com', '622222222', 'Calle Trabajo 2, Barcelona'),
(3, 'Elena Martín', 'elena.martin@empresa.com', '633333333', 'Av. Comercial 3, Bilbao');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `precio_coste` decimal(10,2) DEFAULT NULL,
  `id_categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `precio`, `stock`, `precio_coste`, `id_categoria`) VALUES
(1, 'Portátil Lenovo', 'Portátil i5, 8GB RAM, SSD 512GB', 699.99, 50, 500.00, 1),
(2, 'Camiseta Blanca', '100% algodón, talla M', 14.99, 200, 5.00, 2),
(3, 'Aceite de Oliva 1L', 'Virgen extra', 6.50, 150, 3.00, 3),
(4, 'Sofá 3 plazas', 'Sofá gris moderno', 499.00, 10, 300.00, 4),
(5, 'Balón de fútbol', 'Tamaño oficial FIFA', 25.00, 100, 10.00, 5),
(6, 'Auriculares Bluetooth', 'Con cancelación de ruido', 89.99, 80, 50.00, 1),
(7, 'Pantalón vaquero', 'Talla 42, azul', 39.99, 120, 15.00, 2),
(8, 'Café molido 500g', '100% arábica', 4.25, 180, 2.00, 3),
(9, 'Lámpara de escritorio', 'LED, regulable', 29.90, 40, 15.00, 4),
(10, 'Zapatillas running', 'Talla 43, transpirables', 59.95, 60, 30.00, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `DNI` varchar(9) NOT NULL,
  `NombreApellidos` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contrasegna` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`DNI`, `NombreApellidos`, `correo`, `contrasegna`) VALUES
('73022056T', 'Adrian Mariñosa Garcia', 'a@a.com', '1234'),
('73022056T', 'Adrian Mariñosa Garcia', 'a@a.com', '1234');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_empleado` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `fecha`, `total`, `id_cliente`, `id_empleado`) VALUES
(1, '2025-06-01', 809.98, 1, 1),
(2, '2025-06-02', 109.94, 2, 2),
(3, '2025-06-03', 525.40, 3, 1),
(4, '2025-06-04', 109.24, 4, 3),
(5, '2025-06-05', 834.98, 1, 2);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `vista_totales_venta`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `vista_totales_venta` (
`id_venta` int(11)
,`total_venta` decimal(42,2)
);

-- --------------------------------------------------------

--
-- Estructura para la vista `vista_totales_venta`
--
DROP TABLE IF EXISTS `vista_totales_venta`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vista_totales_venta`  AS SELECT `detalles_venta`.`id_venta` AS `id_venta`, sum(`detalles_venta`.`cantidad` * `detalles_venta`.`precio_unitario`) AS `total_venta` FROM `detalles_venta` GROUP BY `detalles_venta`.`id_venta` ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias_productos`
--
ALTER TABLE `categorias_productos`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_empleado` (`id_empleado`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias_productos`
--
ALTER TABLE `categorias_productos`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalles_venta`
--
ALTER TABLE `detalles_venta`
  ADD CONSTRAINT `detalles_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  ADD CONSTRAINT `detalles_venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_productos` (`id_categoria`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
