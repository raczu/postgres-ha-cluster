from dataclasses import astuple
from typing import Any

from faker import Faker

from pgload.sql.models import Product, PurchaseWithStore, Store
from pgload.sql.utils import pgtransaction


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

    SELECT create_distributed_table('ecommerce.stores', 'store_id');
    SELECT create_distributed_table('ecommerce.products', 'store_id');
    SELECT create_distributed_table('ecommerce.purchases', 'store_id');
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)


def drop_database(conn: Any) -> None:
    with pgtransaction(conn) as tx:
        tx.execute("DROP SCHEMA IF EXISTS ecommerce CASCADE;")


def insert_test_data(conn: Any, scale: int, seed: int) -> None:
    Faker.seed(seed)
    fake = Faker()
    with pgtransaction(conn) as tx:
        stores = [
            Store(
                store_id=fake.uuid4(),
                owner_email=fake.email(),
                name=fake.company(),
                created_at=fake.date_time_this_year(before_now=True),
            )
            for _ in range(scale)
        ]
        tx.executemany(
            """
            INSERT INTO ecommerce.stores (store_id, owner_email, name, created_at)
            VALUES (%s, %s, %s, %s);
            """,
            [astuple(store) for store in stores],  # type: ignore
        )

        for store in stores:
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
                for _ in range(10 * scale)
            ]
            tx.executemany(
                """
                INSERT INTO ecommerce.products
                    (
                        product_id,
                        name,
                        description,
                        price,
                        quantity,
                        store_id,
                        created_at,
                        updated_at
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """,
                [astuple(product) for product in products],  # type: ignore
            )

            for product in products:
                purchases = [
                    PurchaseWithStore(
                        purchase_id=fake.uuid4(),
                        product_id=product.product_id,
                        store_id=store.store_id,
                        price=round(
                            fake.pyfloat(left_digits=3, right_digits=2, positive=True),
                            2,
                        ),
                        purchased_at=fake.date_time_between(start_date="-30d", end_date="now"),
                    )
                    for _ in range(100 * scale)
                ]
                tx.executemany(
                    """
                    INSERT INTO ecommerce.purchases
                        (purchase_id, product_id, store_id, price, purchased_at)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    [astuple(purchase) for purchase in purchases],  # type: ignore
                )


def get_random_purchase(conn: Any) -> tuple:
    sql = """
    SELECT *
    FROM ecommerce.purchases
    ORDER BY RANDOM()
    LIMIT 1;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchone()
    return result


def get_random_store(conn: Any) -> tuple:
    sql = """
    SELECT *
    FROM ecommerce.stores
    ORDER BY RANDOM()
    LIMIT 1;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchone()
    return result


def get_random_product(conn: Any) -> tuple:
    sql = """
    SELECT *
    FROM ecommerce.products
    ORDER BY RANDOM()
    LIMIT 1;
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchone()
    return result
