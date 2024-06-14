-- creates a trigger that decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.
DELIMITER $$
CREATE TRIGGER decreases_quantity_after_order AFTER INSERT
ON orders FOR EACH ROW
BEGIN
    DECLARE current_quantity INT;

    SELECT quantity INTO current_quantity FROM items WHERE name = NEW.item_name;
    UPDATE items SET quantity = (current_quantity - NEW.number)
    WHERE name = NEW.item_name;
END$$
DELIMITER ;
