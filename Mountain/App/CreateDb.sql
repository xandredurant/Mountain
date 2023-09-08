IF DB_ID('MountainDb') IS NULL
	CREATE DATABASE MountainDb;

GO
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
           WHERE TABLE_NAME = 'Files')
	CREATE TABLE MountainDb.dbo.Files(
		File_id int NOT NULL IDENTITY(0,1) PRIMARY KEY,
		File_name nvarchar(20) NOT NULL UNIQUE,
		File_n_columns int NOT NULL,
		File_n_rows int NOT NULL
	);

IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = 'Files')
	CREATE TABLE MountainDb.dbo.DataPoints(
		DataPoint_id int NOT NULL IDENTITY(0,1) PRIMARY KEY,
		DataPoint_elevation float NOT NULL,
		DataPoint_base_color nvarchar(20) NOT NULL,
		File_id int NOT NULL FOREIGN KEY REFERENCES MountainDb.dbo.Files(File_id)
	);