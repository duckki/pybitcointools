from cryptos import coins_async
from cryptos.testing.testcases_async import BaseAsyncCoinTestCase
from typing import List
from unittest import mock


class TestDoge(BaseAsyncCoinTestCase):
    name = "Dogecoin"
    coin = coins_async.Doge
    addresses = ['DRqYjcRNeRMWw7c3gPBv3L8i3ZJSqbm6PV',
                 'DCML95nTwBZf7p4Zfzgkv3Nm5qHqY1g17S',
                 'DBDTTTFPfyMLXSooXUXHhgUiDEFcTRnvFf']
    multisig_addresses: List[str] = ["9uxMmYZ64cQjH8LqWBeSNNv99YmMznrBuN",
                                     "9seARs8HgPPJR2tCJoUZcdKoc87FNnHZhg"]
    privkeys: List[str] = ["098ddf01ebb71ead01fc52cb4ad1f5cafffb5f2d052dd233b3cad18e255e1db1",
                           "0861e1bb62504f5e9f03b59308005a6f2c12c34df108c6f7c52e5e712a08e91401",
                           "c396c62dfdc529645b822dc4eaa7b9ddc97dd8424de09ca19decce61e6732f71"]
    privkey_standard_wifs: List[str] = ['6JCpvU7HkF7F2TGbzAvn2QBxP2WapoQNKJcF16en8yCghYr1m7W',
                                       'QNtvQAmjvG9MD1qwZCA5342p4Bs9koez8pAspPnBeoxwFxbqYcre',
                                       '6KckvyPW6MWrkKMXvhMN8ihfVKKNFzeatNq5jEdsN9RKVnJrynQ']
    native_segwit_addresses: List[str] = ["doge1q95cgql39zvtc57g4vn8ytzmlvtt43sknp354v0",
                                          "tb1qfuvnn87p787z7nqv9seu4e8fqel83yacg7yf2r",
                                          "tb1qst3pkm860tjt9y70ugnaluqyqnfa7h54ekyj66"]
    privkey_native_segwit_wifs: List[str] = ["QXWq6A1f62BgsvxdyRDFXMSqgesE8Q5sFELgMtHqiepHW9vBUBfE",
                                             "cWSdHQKWGsGd7SvvuQXJKKnkTpLeD7tbV3FZheBwv3mJM6yc95xc",
                                             "cciXnTS5mEg4Ud6crDU7ZLpRHcKZHVgVuzRukfbVZZxhiqfSyfBH"]
    fee: int = 250
    max_fee: int = 1500
    testnet = False

    min_latest_height = 4464523
    unspent_addresses = ["DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8"]

    balance = {'confirmed': 730696900, 'unconfirmed': 0}
    balances = [{'address': unspent_addresses[0]} | dict(balance)]

    unspent = [{'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
                 'height': 3101154,
                 'tx_hash': '770e6cb667a07c74a73ed74950224cb536ceed34dc678182a0d86c7a7703ed9c',
                 'tx_pos': 0,
                 'value': 100000000},
               {'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
                 'height': 3133347,
                 'tx_hash': '976a9e6cd24d44cce4098401398a37663973a297ab60c2f42db7dc46640ca410',
                 'tx_pos': 0,
                 'value': 69696900},
                 {'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
                  'height': 3311542,
                  'tx_hash': 'd19cd7b01a6e7320f3b5efb90dc2cc4505ac8bf32b2e6b6fae87a87615752976',
                  'tx_pos': 0,
                  'value': 420000000},
                 {'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
                  'height': 4073469,
                  'tx_hash': 'aa5cb5cccf8dadd5a42d039134b732f76226b6c09aca629cbf0489a5974578e6',
                  'tx_pos': 0,
                  'value': 141000000}]
    unspents = unspent
    history = [
        {'height': 3101154,
          'tx_hash': '770e6cb667a07c74a73ed74950224cb536ceed34dc678182a0d86c7a7703ed9c'},
        {'height': 3133347,
          'tx_hash': '976a9e6cd24d44cce4098401398a37663973a297ab60c2f42db7dc46640ca410'},
        {'height': 3311542,
          'tx_hash': 'd19cd7b01a6e7320f3b5efb90dc2cc4505ac8bf32b2e6b6fae87a87615752976'},
        {'height': 4073469,
          'tx_hash': 'aa5cb5cccf8dadd5a42d039134b732f76226b6c09aca629cbf0489a5974578e6'}]
    histories = [{'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
  'height': 3101154,
  'tx_hash': '770e6cb667a07c74a73ed74950224cb536ceed34dc678182a0d86c7a7703ed9c'},
 {'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
  'height': 3133347,
  'tx_hash': '976a9e6cd24d44cce4098401398a37663973a297ab60c2f42db7dc46640ca410'},
 {'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
  'height': 4073469,
  'tx_hash': 'aa5cb5cccf8dadd5a42d039134b732f76226b6c09aca629cbf0489a5974578e6'},
 {'address': 'DLAznsPDLDRgsVcTFWRMYMG5uH6GddDtv8',
  'height': 3311542,
  'tx_hash': 'd19cd7b01a6e7320f3b5efb90dc2cc4505ac8bf32b2e6b6fae87a87615752976'}]
    txid: str = "345c28885d265edbf8565f553f9491c511b6549d3923a1d63fe158b8000bbee2"
    txheight: int = 2046470
    block_hash: str = "404646bb8958730e133c2a363b79ef1c9c300db4134988060c6c9215e9a6694a"
    raw_tx: str = "010000000185229c0ab8804cb1e4bf465d9e3e0bcbc0a40481a5892eb03d61d7411f1fee72000000006a47304402202da8ad356685fe8f3337cd14c7a20861fc332b79a49581c062fe2f648e4b8d0b0220106fed579b94c0bf1b6bdb199c8147deb65b40f6618bab89c00262090124b70d012102960791fd0876b1b00ae11ea858d4f3f44a3184d8d4bff0336417b969b9f11809feffffff02928eccfd280000001976a91466f79e401b78766cbea8791ec76c8d6b2cf6441788ac75969b6e2b0300001976a914f594b41cfd73d290bbbb298d71e63d1c613d35ee88acf8391f00"

    def test_standard_wif_ok(self):
        self.assertStandardWifOK()

    async def test_balance(self):
        await self.assertBalanceOK()

    async def test_balances(self):
        await self.assertBalancesOK()

    async def test_unspent(self):
        await self.assertUnspentOK()

    async def test_unspents(self):
        await self.assertUnspentsOK()

    async def test_merkle_proof(self):
        await self.assertMerkleProofOK()

    async def test_history(self):
        await self.assertHistoryOK()

    async def test_histories(self):
        await self.assertHistoriesOK()

    async def test_balance_merkle_proven(self):
        await self.assertBalanceMerkleProvenOK()

    async def test_balances_merkle_proven(self):
        await self.assertBalancesMerkleProvenOK()

    async def test_block_header(self):
        await self.assertBlockHeaderOK()

    async def test_block_headers(self):
        await self.assertBlockHeadersOK()

    async def test_gettx(self):
        await self.assertGetTXOK()

    async def test_getverbosetx(self):
        await self.assertGetVerboseTXOK()

    async def test_gettxs(self):
        await self.assertGetTxsOK()

    async def test_transaction(self):
        with mock.patch('cryptos.electrumx_client.client.NotificationSession.send_request',
                        side_effect=self.mock_electrumx_send_request):
            await self.assertTransactionOK("b264a42895f556491f2d51622478305e7c25d97ed799b9dfa2bdd592125f75ff")

    async def test_transaction_multisig(self):
        with mock.patch('cryptos.electrumx_client.client.NotificationSession.send_request',
                        side_effect=self.mock_electrumx_send_request):
            await self.assertMultiSigTransactionOK("02e026224aff90708cffa2938cd2e7cdec44e06f82ba4ea6966ac24ccbd4aca6")

    async def test_sendmulti_recipient_tx(self):
        with mock.patch('cryptos.electrumx_client.client.NotificationSession.send_request',
                        side_effect=self.mock_electrumx_send_request):
            await self.assertSendMultiRecipientsTXOK("73962dba75d3581f069bcfc63b0697008347d6b272c6bb421e1a58d5b84dcb16")

    async def test_send(self):
        with mock.patch('cryptos.electrumx_client.client.NotificationSession.send_request',
                        side_effect=self.mock_electrumx_send_request):
            await self.assertSendOK("e3a160d1ee8b521c48a36e3215e0912202685dc18ce985208320f76139b837cb")

    async def test_subscribe_block_headers(self):
        await self.assertSubscribeBlockHeadersOK()

    async def test_subscribe_block_headers_sync(self):
        await self.assertSubscribeBlockHeadersSyncCallbackOK()

    async def test_latest_block(self):
        await self.assertLatestBlockOK()

    async def test_confirmations(self):
        await self.assertConfirmationsOK()

