from typing import Any

from pgload.sql.utils import pgtransaction


def drop_database(conn: Any) -> None:
    with pgtransaction(conn) as tx:
        tx.execute("DROP SCHEMA IF EXISTS ecommerce CASCADE;")


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


def get_random_store_products(conn: Any) -> list[tuple]:
    sql = """
    SELECT p.name, p.price, p.quantity
    FROM ecommerce.products p
    WHERE p.store_id = (SELECT store_id FROM ecommerce.stores ORDER BY random() LIMIT 1);
    """
    with pgtransaction(conn) as tx:
        tx.execute(sql)
        result = tx.fetchall()
    return result
