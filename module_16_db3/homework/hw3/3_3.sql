SELECT DISTINCT p.maker
FROM product p
JOIN pc ON p.model = pc.model
WHERE pc.speed >= 450;