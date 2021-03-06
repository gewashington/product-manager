DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
  value INTEGER NOT NULL
);

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  productName TEXT NOT NULL,
  price FLOAT NOT NULL,
  quantity INTEGER NOT NULL,
  added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);