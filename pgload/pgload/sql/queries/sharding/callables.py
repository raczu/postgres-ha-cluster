from typing import Any

from faker import Faker

from pgload.sql.models import Product, PurchaseWithStore, Store
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
        product_id UUID DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        description VARCHAR(2048) NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        quantity INTEGER NOT NULL,
        store_id UUID NOT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        PRIMARY KEY (store_id, product_id),
        FOREIGN KEY (store_id) REFERENCES ecommerce.stores (store_id)
    );

    CREATE TABLE IF NOT EXISTS ecommerce.purchases (
        purchase_id UUID DEFAULT gen_random_uuid(),
        product_id UUID NOT NULL,
        store_id UUID NOT NULL,
        price NUMERIC(10, 2) NOT NULL,
        purchased_at TIMESTAMPTZ DEFAULT NOW(),
        PRIMARY KEY (store_id, purchase_id),
        FOREIGN KEY (store_id, product_id)
            REFERENCES ecommerce.products (store_id, product_id)
    );

    SELECT create_reference_table('ecommerce.stores');
    SELECT create_distributed_table('ecommerce.products', 'store_id');
    SELECT create_distributed_table('ecommerce.purchases', 'store_id');
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
        PurchaseWithStore(
            purchase_id=fake.uuid4(),
            product_id=product.product_id,
            store_id=product.store_id,
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


def get_random_store_purchases(conn: Any) -> list[tuple]:
    sql = """
    SELECT p.name, pu.purchase_id, pu.price, pu.purchased_at
    FROM ecommerce.products p
    JOIN ecommerce.purchases pu ON p.store_id = pu.store_id AND p.product_id = pu.product_id
    WHERE p.store_id = (SELECT store_id FROM ecommerce.stores ORDER BY random() LIMIT 1);
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result


def get_random_store_total_sales(conn: Any) -> list[tuple]:
    sql = """
    SELECT s.name, SUM(pu.price) as total_sales
    FROM ecommerce.stores s
    JOIN ecommerce.purchases pu ON s.store_id = pu.store_id
    WHERE s.store_id = (SELECT store_id FROM ecommerce.stores ORDER BY random() LIMIT 1)
    GROUP BY s.name;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result
