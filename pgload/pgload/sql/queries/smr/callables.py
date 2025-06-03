from typing import Any

from faker import Faker

from pgload.sql.models import Product, Purchase, Store
from pgload.sql.utils import batchify, pgtransaction, write2buffer


def init_database(conn: Any) -> None:
    sql = """
    CREATE SCHEMA IF NOT EXISTS ecommerce;

    CREATE TABLE IF NOT EXISTS ecommerce.stores (
        store_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        owner_email VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS ecommerce.products (
        product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        description VARCHAR(2048) NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        quantity INTEGER NOT NULL,
        store_id UUID NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        FOREIGN KEY (store_id) REFERENCES ecommerce.stores (store_id)
    );

    CREATE TABLE IF NOT EXISTS ecommerce.purchases (
        purchase_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        product_id UUID NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        purchased_at TIMESTAMPTZ DEFAULT NOW(),
        FOREIGN KEY (product_id) REFERENCES ecommerce.products (product_id)
    );
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)


def insert_test_data(conn: Any, scale: int, seed: int) -> None:
    Faker.seed(seed)
    fake = Faker()

    stores = [
        Store(
            store_id=fake.uuid4(),
            owner_email=fake.email(),
            name=fake.company(),
            created_at=fake.date_time_this_year(before_now=True),
        )
        for _ in range(scale)
    ]

    products = [
        Product(
            product_id=fake.uuid4(),
            name=fake.unique.bothify("P##??"),
            description=fake.sentence(),
            price=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            quantity=fake.random_int(min=1, max=100),
            store_id=store.store_id,
            created_at=fake.date_time_this_year(before_now=True),
            updated_at=fake.date_time_this_year(after_now=True),
        )
        for store in stores
        for _ in range(10 * scale)
    ]

    purchases = [
        Purchase(
            purchase_id=fake.uuid4(),
            product_id=product.product_id,
            price=round(fake.pyfloat(left_digits=3, right_digits=2, positive=True), 2),
            purchased_at=fake.date_time_between(start_date="-30d", end_date="now"),
        )
        for product in products
        for _ in range(100 * scale)
    ]

    with pgtransaction(conn) as tx:
        tx.copy_expert("COPY ecommerce.stores FROM STDIN", write2buffer(stores))

    for batch in batchify(products, 250_000):
        with pgtransaction(conn) as tx:
            tx.copy_expert("COPY ecommerce.products FROM STDIN", write2buffer(batch))

    for batch in batchify(purchases, 250_000):
        with pgtransaction(conn) as tx:
            tx.copy_expert("COPY ecommerce.purchases FROM STDIN", write2buffer(batch))


def get_top_5_stores_by_total_purchase_value(conn: Any) -> list[tuple]:
    sql = """
    SELECT
        s.store_id,
        s.name AS store_name,
        COUNT(pu.purchase_id) AS total_purchases,
        SUM(pu.price) AS total_value
    FROM ecommerce.stores s
    JOIN ecommerce.products pr ON s.store_id = pr.store_id
    JOIN ecommerce.purchases pu ON pr.product_id = pu.product_id
    WHERE pu.purchased_at >= NOW() - INTERVAL '30 days'
    GROUP BY s.store_id, s.name
    ORDER BY total_value DESC
    LIMIT 5;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result


def get_products_with_high_purchase_and_low_stock(conn: Any) -> list[tuple]:
    sql = """
    SELECT
        pr.product_id,
        pr.name,
        pr.quantity,
        COUNT(pu.purchase_id) AS purchase_count,
        AVG(pu.price) AS avg_purchase_price
    FROM ecommerce.products pr
    JOIN ecommerce.purchases pu ON pr.product_id = pu.product_id
    WHERE pr.quantity < 10
    AND pu.purchased_at >= NOW() - INTERVAL '7 days'
    GROUP BY pr.product_id, pr.name, pr.quantity
    HAVING COUNT(pu.purchase_id) > 5
    ORDER BY purchase_count DESC
    LIMIT 10;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result


def get_products_with_high_purchases_and_low_stock_randomly(conn: Any) -> list[tuple]:
    sql = """
    SELECT
        pr.product_id,
        pr.name,
        pr.quantity,
        COUNT(pu.purchase_id) AS purchase_count,
        AVG(pu.price) AS avg_purchase_price
    FROM ecommerce.products pr
    JOIN ecommerce.purchases pu TABLESAMPLE BERNOULLI(10) ON pr.product_id = pu.product_id
    WHERE pr.quantity < 10
    AND pu.purchased_at >= NOW() - INTERVAL '7 days'
    GROUP BY pr.product_id, pr.name, pr.quantity
    HAVING COUNT(pu.purchase_id) > 5
    ORDER BY purchase_count DESC
    LIMIT 10;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result


def create_new_store(conn: Any) -> tuple:
    sql = """
    INSERT INTO ecommerce.stores (owner_email, name)
    VALUES (%s, %s)
    RETURNING store_id;
    """
    fake = Faker()
    with pgtransaction(conn) as tx:
        tx.execute(sql, (fake.email(), fake.company()))
        result = tx.fetchone()
    return result


def register_purchase_for_random_product(conn: Any) -> tuple:
    sql = """
    WITH random_product AS (
        SELECT product_id, store_id, price
        FROM ecommerce.products
        WHERE quantity >= 1
        ORDER BY RANDOM()
        LIMIT 1
    ),
    updated_product AS (
        UPDATE ecommerce.products
        SET quantity = quantity - 1,
            updated_at = NOW()
        WHERE product_id = (SELECT product_id FROM random_product)
          AND store_id = (SELECT store_id FROM random_product)
        RETURNING product_id, store_id, price
    )
    INSERT INTO ecommerce.purchases (product_id, price)
    SELECT product_id, price
    FROM updated_product
    RETURNING purchase_id, purchased_at;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchone()
    return result


def update_random_product_quantity(conn: Any) -> None:
    sql = """
    UPDATE ecommerce.products
    SET quantity = quantity + 1
    WHERE product_id = (
        SELECT product_id
        FROM ecommerce.products
        ORDER BY RANDOM()
        LIMIT 1
    );
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)


def get_random_store_purchases(conn: Any) -> list[tuple]:
    sql = """
    SELECT p.name, pu.purchase_id, pu.price, pu.purchased_at
    FROM ecommerce.products p
    JOIN ecommerce.purchases pu ON p.product_id = pu.product_id
    WHERE p.store_id = (SELECT store_id FROM ecommerce.stores ORDER BY random() LIMIT 1);
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result


def get_random_store_total_sales(conn: Any) -> list[tuple]:
    sql = """
    SELECT s.name, COALESCE(SUM(pu.price), 0) as total_sales
    FROM ecommerce.stores s
    LEFT JOIN ecommerce.products p ON s.store_id = p.store_id
    LEFT JOIN ecommerce.purchases pu ON p.product_id = pu.product_id
    WHERE s.store_id = (SELECT store_id FROM ecommerce.stores ORDER BY random() LIMIT 1)
    GROUP BY s.name;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result
