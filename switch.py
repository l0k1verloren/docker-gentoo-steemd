#!/usr/bin/python3
#
# l0k1's monitor client and witness toggle
#
# Usage:
# 
# WIF="<posting active or master key for witness account>" \
# WITNESS="<public key corresponding to private key on backup witness>" \
# switch 
#

import asyncio
import websockets
import time
import sys
import random
import os
from pistonbase import operations
from collections import OrderedDict
from piston.transactionbuilder import TransactionBuilder
from graphenebase import base58
from piston import Steem

import config

st = Steem ( keys = config.wif )

tx = TransactionBuilder ()
tx.appendOps (
  operations.Witness_update (
    **{ "owner": config.owner,
        "url": config.url,
        "block_signing_key": config.block_signing_public_key,
        "props": { "account_creation_fee": config.account_creation_fee,
                   "maximum_block_size": config.maximum_block_size,
                   "sbd_interest_rate": config.sbd_interest_rate},
         "fee": config.fee,
      }
    )
  )
tx.appendSigner ( config.owner, "active" )
tx.sign()
try:
  tx.broadcast ()
  print ( "Successfully switched to secondary witness" )
except:
  print ( "Transaction broadcast failed - DANGER WILL ROBINSON!" )
