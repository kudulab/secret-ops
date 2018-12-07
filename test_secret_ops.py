from secret_ops import *
import unittest
from secret_ops import _replace_vault_token_line

class TestSecretMethods(unittest.TestCase):

    def test_replace_vault_token_line(self):
        line = '  VAULT_TOKEN: some thing'
        replaced = _replace_vault_token_line(line, 'new token')
        self.assertEqual('  VAULT_TOKEN: "new token"', replaced)

    def test_replace_vault_token_line_not_matching(self):
        line = 'VAULT_TOKEN'
        replaced = _replace_vault_token_line(line, 'new token')
        self.assertEqual(line, replaced)

if __name__ == '__main__':
    unittest.main()


