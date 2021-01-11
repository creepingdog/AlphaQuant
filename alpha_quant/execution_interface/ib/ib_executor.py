import os
import time
import atexit
import traceback
from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
import alpha_quant.common.env_config as ecfg

from alpha_quant.common.logger import LOG
logger = LOG.get_logger(__name__)


def execute(ib_connection, order_id, ticker, action, quantity, price=None):
    contract = Contract()
    contract.m_symbol = ticker
    contract.m_secType = 'STK'
    contract.m_exchange = 'SMART'
    # contract.m_primaryExch = 'ISLAND'
    contract.m_currency = 'USD'

    order = Order()
    if price is not None:
        order.m_orderType = 'LMT'
        order.m_lmtPrice = price
    else:
        order.m_orderType = 'MKT'
    #
    order.m_totalQuantity = quantity
    order.m_action = action

    ib_connection.placeOrder(int(order_id), contract, order)
#


class IBExecutor:
    def __init__(self, env='RESEARCH', init_order_id=None, order_id_file=None):
        self.ib_connections = dict()
        self.curr_ib_connection = None
        self.curr_ib_connection_key = None

        if order_id_file is None:
            order_id_file = os.path.join(os.path.dirname(__file__), 'order_id.txt')
        #
        self.order_id_file = order_id_file

        if init_order_id is not None:
            self.curr_order_id = init_order_id
        else:
            with open(order_id_file, 'r') as fh:
                self.curr_order_id = int(fh.read())
            #
        #

        if env is not None:
            host = ecfg.get_env_config().get(ecfg.Prop.IB_TWS_HOST)
            port = int(ecfg.get_env_config().get(ecfg.Prop.IB_TWS_PORT))
            client_id = int(ecfg.get_env_config().get(ecfg.Prop.IB_TWS_CLIENT_ID))

            self._get_connection(port=port, client_id=client_id, host=host)
        #

        atexit.register(self.cleanup)
    #

    def cleanup(self):
        with open(self.order_id_file, 'w') as fh:
            fh.write(str(self.curr_order_id))
        #
        logger.info(f'curr_order_id={self.curr_order_id} => {self.order_id_file}')

        for ib_connection_key, ib_connection in self.ib_connections.items():
            ib_connection.disconnect()
            logger.info(f'ib_connection({ib_connection_key}) disconnected')
        #
    #

    def _get_connection(self, host='127.0.0.1', port=None, client_id=None,
                        ib_connection_key=None):
        if ib_connection_key is None:
            ib_connection_key = f'{host}:{port}:{client_id}'
        #
        if ib_connection_key not in self.ib_connections:
            # print(f'port={port}, client_id={client_id}')
            ib_connection = Connection.create(port=port, clientId=client_id)
            self.ib_connections[ib_connection_key] = ib_connection
        #

        ib_connection = self.ib_connections[ib_connection_key]
        try:
            ib_connection.connect()
            ib_connection.registerAll(lambda x : print(x))
            self.curr_ib_connection = ib_connection
            self.curr_ib_connection_key = ib_connection_key
            logger.info(f'ib_connection({self.curr_ib_connection_key}) established')
        except Exception:
            logger.error(f'Failed to connect to IB TWS with ib_connection_key={ib_connection_key}')
        #

        return self.curr_ib_connection
    #

    def place_order(self, ticker, action, quantity, price=None,
                    order_id=None,
                    ib_connection_key=None):
        if ib_connection_key is not None:
            self._get_connection(ib_connection_key=ib_connection_key)
        #

        try:
            self.curr_order_id = self.curr_order_id+1 if order_id is None else int(order_id)
            execute(ib_connection=self.curr_ib_connection,
                    order_id=self.curr_order_id, ticker=ticker, action=action, quantity=quantity, price=price)
            logger.info(f'Placed order(order_id={self.curr_order_id}, ticker={ticker}, action={action}, quantity={quantity}, price={price}) => {self.curr_ib_connection_key}')
        except Exception:
            logger.error(f'Failed to place order(order_id={self.curr_order_id}, ticker={ticker}, action={action}, quantity={quantity}, price={price}) => {self.curr_ib_connection_key}')
            traceback.print_exc()
        #
    #
#


if __name__ == '__main__':
    ib_executor = IBExecutor()
    # ib_executor.place_order(ticker='TSLA', action='BUY', quantity=100)
    # ib_executor.place_order(ticker='SPY', action='BUY', quantity=100)
    ib_executor.place_order(ticker='SPY', action='SELL', quantity=10)
    time.sleep(2)
#
