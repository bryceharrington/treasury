#!/usr/bin/python

import unittest
from tempfile import mkstemp

import sys, os.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from treasury.ledger_account import LedgerAccount

sample_data = """
2019-01-01 * Opening Balance
    Assets:Savings                               $0.00
    Equity:Opening Balances                      $0.00

2019-02-01 Donation A
    Assets:Savings                              $10.00
    Income:TestProject:Donations                -$9.00
    Income:Parent:Donations                     -$1.00

2019-03-02 Donation B
    Assets:Savings                             $100.00
    Income:TestProject:Donations               -$90.00
    Income:Parent:Donations                    -$10.00

2019-03-03 Sponsorship
    Accrued:Accounts Receivable:TestProject   $1000.00
    Income:TestProject:Sponsorships           -$900.00
    Income:Parent:Donations                   -$100.00

2019-04-04 Grant Award
    Accrued:Accounts Receivable:TestProject  $10000.00
    Income:TestProject:Grants                -$9000.00
    Income:Parent:Donations                  -$1000.00

2019-03-02 Expense 1
    Accrued:Accounts Payable:TestProject        -$0.90
    Expenses:TestProject:Banking Fees            $0.90

2019-03-03 Expense 2
    Accrued:Accounts Payable:TestProject        -$8.00
    Expenses:TestProject:Reimbursement           $8.00

2019-03-03 Expense 3
    Accrued:Accounts Payable:TestProject       -$70.00
    Expenses:TestProject:Reimbursement          $70.00

2019-03-03 Expense 4
    Accrued:Accounts Payable:TestProject      -$600.00
    Expenses:TestProject:Travel Sponsorship    $600.00

2019-03-03 Expense 5
    Accrued:Accounts Payable:TestProject     -$5000.00
    Expenses:TestProject:Contract Work        $5000.00
"""

ledger_filename = None
ledger_account = None


class LedgerAccountTestCase(unittest.TestCase):
    def setUp(self):
        assert(ledger_filename is not None)
        self.assertIsNotNone(ledger_account)
        self.assertIsNotNone(ledger_account.session)
        self.assertEqual(ledger_account.project, "TestProject")

    def test_assets_begin(self):
        """Check that we begin with no assets."""
        self.assertEqual(ledger_account.assets("2018/12/31"),
                         0.00)

    def test_assets_end(self):
        """Check that we are getting the correct total assets."""
        self.assertEqual(ledger_account.assets("2019/12/31"),
                         110.00)

    def test_balance_beginning(self):
        """Check that we start with $0"""
        self.assertEqual(ledger_account.balance("2018/12/31"),
                         0.00)

    def test_balance_ending(self):
        """Check that the final total matches our expectations."""
        self.assertEqual(ledger_account.balance("2019/12/31"),
                         4320.10)

    def test_income(self):
        """Check that we are getting the correct total for income items."""
        self.assertEqual(ledger_account.income(begin_date="2018/12/31",
                                               end_date="2019/12/31"),
                         9999.00)

    def test_expenses(self):
        """Check that we are getting the correct total for expense items."""
        self.assertEqual(ledger_account.expenses(begin_date="2018/12/31",
                                                 end_date="2019/12/31"),
                         5678.90)


if __name__ == '__main__':
    # Create the ledger file
    fd, ledger_filename = mkstemp(suffix=".ledger", text=True)
    with os.fdopen (fd, 'w') as f:
        f.write(sample_data.strip())

    # Create the ledger object
    # We have to create this just once, not on a per-test baseis, due to
    # https://github.com/ledger/ledger/issues/514
    ledger_account = LedgerAccount("TestProject", ledger_filename)
    os.remove(ledger_filename)

    unittest.main()

