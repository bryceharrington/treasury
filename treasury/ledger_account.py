#!/usr/bin/python

import os
import sys
import ledger # Not python3-enabled yet

class LedgerAccount:
    """Interface to Ledger CLI to extract financial account data"""
    def __init__(self, project, ledger_filename):
        self.project = project
        self.founding_date = "2006/01/01"
        self.session = ledger.read_journal(ledger_filename)

    def assets(self, date, category=None):
        total = ledger.Balance()
        for post in self.session.query("assets --end %s" %(date)):
            total += post.amount

        return abs(float(str(total.number())))

    def entries(self, entry_type, begin_date=None, end_date=None, category=None):
        total = ledger.Balance()
        if category:
            field = "%s:%s:%s" %(entry_type, self.project, category)
        else:
            field = "%s:%s" %(entry_type, self.project)

        date_range = ""
        if begin_date:
            date_range += " --begin %s" %(begin_date)
        if end_date:
            date_range += " --end %s" %(end_date)

        for post in self.session.query("balance %s %s" %(field, date_range)):
            total += post.amount

        return abs(float(str(total.number())))

    def income(self, begin_date, end_date, category=None):
        return self.entries("Income", begin_date=begin_date, end_date=end_date)

    def expenses(self, begin_date, end_date, category=None):
        return self.entries("Expenses", begin_date=begin_date, end_date=end_date)

    def balance(self, date, category=None):
        """Flatten accounts receivable, accounts payable, and assets."""
        return ( self.income(begin_date=self.founding_date, end_date=date, category=category) -
                 self.expenses(begin_date=self.founding_date, end_date=date, category=category)
               )
