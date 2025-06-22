SELECT p.model, pc.price
FROM product p
JOIN pc ON p.model = pc.model
WHERE p.maker = 'B'
UNION
SELECT p.model, l.price
FROM product p
JOIN laptop l ON p.model = l.model
WHERE p.maker = 'B'
UNION
SELECT p.model, pr.price
FROM product p
JOIN printer pr ON p.model = pr.model
WHERE p.maker = 'B';