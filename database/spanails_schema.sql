-- Esquema MySQL 8+ basado en los modelos reales de SpaNails_Web_Service/development.
-- Crear en una base nueva: no mezcla el esquema genérico anterior.
CREATE DATABASE IF NOT EXISTS spanails_backend
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
USE spanails_backend;

CREATE TABLE clientes (
  id_cliente INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(120) NOT NULL,
  documento VARCHAR(30) NOT NULL,
  email VARCHAR(254) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  fecha_registro DATE NOT NULL,
  PRIMARY KEY (id_cliente),
  UNIQUE KEY uq_clientes_email (email),
  KEY ix_clientes_email (email)
) ENGINE=InnoDB;

CREATE TABLE servicios (
  id_servicio INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(150) NOT NULL,
  precio FLOAT NOT NULL,
  duracion_minutos INT NOT NULL,
  estado VARCHAR(30) NOT NULL,
  aplica_domicilio BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (id_servicio),
  CONSTRAINT chk_servicios_precio CHECK (precio >= 0),
  CONSTRAINT chk_servicios_duracion CHECK (duracion_minutos > 0)
) ENGINE=InnoDB;

CREATE TABLE zonas (
  id_zona INT NOT NULL AUTO_INCREMENT,
  nombre_zona VARCHAR(120) NOT NULL,
  estado VARCHAR(30) NOT NULL,
  tarifa_domicilio INT NULL,
  PRIMARY KEY (id_zona),
  CONSTRAINT chk_zonas_tarifa CHECK (tarifa_domicilio IS NULL OR tarifa_domicilio >= 0)
) ENGINE=InnoDB;

CREATE TABLE paises (
  id_pais INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (id_pais)
) ENGINE=InnoDB;

CREATE TABLE departamentos (
  id_departamento INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  id_pais INT NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (id_departamento),
  KEY ix_departamentos_pais (id_pais),
  CONSTRAINT fk_departamentos_pais FOREIGN KEY (id_pais)
    REFERENCES paises (id_pais) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE municipios (
  id_municipio INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  id_departamento INT NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (id_municipio),
  KEY ix_municipios_departamento (id_departamento),
  CONSTRAINT fk_municipios_departamento FOREIGN KEY (id_departamento)
    REFERENCES departamentos (id_departamento) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE direcciones (
  id INT NOT NULL AUTO_INCREMENT,
  usuario_id INT NOT NULL,
  municipio_id INT NOT NULL,
  direccion VARCHAR(255) NOT NULL,
  barrio VARCHAR(100) NOT NULL,
  observaciones VARCHAR(255) NULL,
  PRIMARY KEY (id),
  KEY ix_direcciones_usuario (usuario_id),
  KEY ix_direcciones_municipio (municipio_id),
  CONSTRAINT fk_direcciones_municipio FOREIGN KEY (municipio_id)
    REFERENCES municipios (id_municipio) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE reservas (
  id_reserva INT NOT NULL AUTO_INCREMENT,
  cliente_id INT NOT NULL,
  fecha DATE NOT NULL,
  hora_inicio VARCHAR(5) NOT NULL,
  hora_fin_servicio VARCHAR(5) NOT NULL,
  hora_fin_bloqueo VARCHAR(5) NOT NULL,
  modalidad VARCHAR(30) NOT NULL,
  id_direccion INT NULL,
  servicios_detalle JSON NOT NULL,
  subtotal FLOAT NOT NULL,
  costo_domicilio INT NOT NULL DEFAULT 0,
  total FLOAT NOT NULL,
  moneda VARCHAR(3) NOT NULL DEFAULT 'COP',
  estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
  PRIMARY KEY (id_reserva),
  KEY ix_reservas_cliente (cliente_id),
  KEY ix_reservas_fecha (fecha),
  KEY ix_reservas_modalidad (modalidad),
  KEY ix_reservas_estado (estado),
  CONSTRAINT chk_reservas_montos CHECK (subtotal >= 0 AND costo_domicilio >= 0 AND total >= 0),
  CONSTRAINT fk_reservas_cliente FOREIGN KEY (cliente_id)
    REFERENCES clientes (id_cliente) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_reservas_direccion FOREIGN KEY (id_direccion)
    REFERENCES direcciones (id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE resenas (
  id INT NOT NULL AUTO_INCREMENT,
  id_reserva INT NOT NULL,
  calificacion INT NOT NULL,
  comentario VARCHAR(500) NULL,
  estado VARCHAR(50) NOT NULL DEFAULT 'Activa',
  fecha_creacion DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY ix_resenas_reserva (id_reserva),
  CONSTRAINT chk_resenas_calificacion CHECK (calificacion BETWEEN 1 AND 5),
  CONSTRAINT fk_resenas_reserva FOREIGN KEY (id_reserva)
    REFERENCES reservas (id_reserva) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE viajes (
  id INT NOT NULL AUTO_INCREMENT,
  id_reserva INT NOT NULL,
  domiciliario_id INT NOT NULL,
  estado VARCHAR(50) NOT NULL DEFAULT 'Activo',
  resultado VARCHAR(50) NULL,
  observaciones VARCHAR(255) NULL,
  fecha_hora_fin DATETIME NULL,
  PRIMARY KEY (id),
  KEY ix_viajes_reserva (id_reserva),
  KEY ix_viajes_domiciliario (domiciliario_id),
  CONSTRAINT fk_viajes_reserva FOREIGN KEY (id_reserva)
    REFERENCES reservas (id_reserva) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;
