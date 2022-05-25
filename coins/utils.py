from .models import CoinType, Coins, ProductPurchase, PurchaseCoins
from products.models import Product

import logging

logger = logging.getLogger('coins-logger')


def get_total_purchase_coins_value(purchase_coins):
    # print('purchase_coins', purchase_coins)
    total_value = 0
    for p_coin in purchase_coins:
        coin_type = CoinType.objects.filter(id=p_coin['coin_type']).first()
        if not coin_type:
            raise Exception('Coin type is not valid')
        coins_value = int(p_coin['coin_count']) * coin_type.value
        total_value += coins_value

    return total_value


def get_products_value(price, quantity):
    return price * quantity


def calculate_balance(purchase_coins, total_price) -> float:
    return float(purchase_coins - total_price)


def get_available_coins() -> dict:
    res = {}
    coin_types = CoinType.objects.order_by('-value').all()
    for c_type in coin_types:
        coins = Coins.objects.filter(coin_type=c_type.id).all()
        sum_count = 0
        for coin in coins:
            sum_count += coin.coin_count
        res[c_type.slug] = sum_count
    return res


def is_balance_enough(coins: dict, balance: float) -> tuple:
    total_coins_value = 0
    for i in coins:
        if i:
            # print('i', coins[i])
            coin_type = CoinType.objects.filter(slug=i).first()
            total_coins_value += coins[i] * coin_type.value

    return float(total_coins_value), balance < total_coins_value


def get_balance(balance: float):
    """
    Check if sum of coins in machine is greater or equal to the balance being expected.

    """
    balance_coins = {}
    if balance == 0:
        return 0

    available_coins = get_available_coins()
    # print('a_coins', available_coins)
    available_balance, is_enough = is_balance_enough(available_coins, balance)
    logger.info(f'Available balance {available_balance}')
    if is_enough:
        new_balance = balance
        logger.info(f'init_balance: {new_balance}')
        for coin_slug in available_coins:
            if float(new_balance) == float(0):
                return balance_coins
            # TODO figure out why the coin count goes to negative after being updated.
            logger.info(f'Available coins: {coin_slug}={available_coins[coin_slug]}')
            coin_value = CoinType.objects.get(slug=coin_slug)
            val, mod = divmod(float(new_balance), float(coin_value.value))
            logger.info(f'{coin_slug} count for change= {val}')
            available_coins_after_change = int(available_coins[coin_slug]) - int(val)
            logger.info(f'Available coins after change: {available_coins_after_change}')
            if available_coins_after_change < 0:
                continue
            elif available_coins_after_change == 0:
                new_balance = float(new_balance) - float(float(available_coins[coin_slug]) * float(coin_value.value))
                balance_coins[coin_slug] = available_coins[coin_slug]
            else:
                new_balance = float(new_balance) - float(float(val) * float(coin_value.value))
                balance_coins[coin_slug] = val
            logger.info(f'Final balance{new_balance}')
            logger.info(f'v {float(new_balance) / float(coin_value.value) == float(0)}')
    else:
        raise Exception('Change is not enough for this purchase')


def make_purchase(product, quantity: int, purchase_coins: list):
    logger.info(f'Purchase coins{purchase_coins}')
    product_purchase = ProductPurchase.objects.create(
        product=Product.objects.get(id=product),
        quantity=quantity
    )
    product_purchase.refresh_from_db()
    for p_coins in purchase_coins:
        PurchaseCoins.objects.create(
            coin_count=p_coins['coin_count'],
            coin_type=CoinType.objects.get(id=p_coins['coin_type']),
            product_purchase=product_purchase
        )
    return
