import unittest
import alpha_quant.common.env_config as ecfg


class TestEnvConfig(unittest.TestCase):
    def test_env(self):
        self.assertEqual(ecfg.get_env_config().env, 'RESEARCH')
    #

    def test_ib_tws(self):
        # host = ecfg.get_env_config().get(ecfg.Prop.IB_TWS_HOST)
        port = int(ecfg.get_env_config().get(ecfg.Prop.IB_TWS_PORT))
        self.assertEqual(port, 7497)

        client_id = int(ecfg.get_env_config().get(ecfg.Prop.IB_TWS_CLIENT_ID))
        self.assertEqual(client_id, 999)
    #
#


if __name__ == '__main__':
    unittest.main()
#
