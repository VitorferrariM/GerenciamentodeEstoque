CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    quantidade INTEGER,
    preco DECIMAL(10, 2),
    imagem VARCHAR(255)  -- Para armazenar o nome da imagem
);
