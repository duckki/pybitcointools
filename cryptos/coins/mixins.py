import asyncio
from concurrent.futures import Future
import threading
import inspect
import janus
from ..coins_async.base import BaseCoin
from cryptos.utils import alist
from ..electrumx_client.types import (ElectrumXBalanceResponse, ElectrumXMultiBalanceResponse, ElectrumXTx,
                                      ElectrumXMerkleResponse, ElectrumXUnspentResponse, ElectrumXMultiTxResponse,
                                      ElectrumXHistoryResponse)
from ..types import (Tx, BlockHeader, BlockHeaderCallbackSync, AddressCallbackSync, AddressTXCallbackSync, MerkleProof,
                     AddressBalance, TxOut, TxInput)
from typing import Optional, Tuple, Any, List, Union, Dict, AnyStr


class SyncCoinMixin(BaseCoin):
    is_closing: bool = False
    _thread: threading.Thread = None

    def __init__(self, testnet: bool = False, use_ssl: bool = None, **kwargs):
        super().__init__(testnet=testnet, use_ssl=use_ssl, **kwargs)
        self._request_queue: Optional[janus.Queue[Tuple[Future, str, tuple, dict[str, Any]]]] = None
        self._loop_is_started = threading.Event()

    def start(self, *args, **kwargs):
        if not self._thread or not self._thread.is_alive():
            self._thread = threading.Thread(target=self.start_event_loop, daemon=True)
            self._thread.start()
        self._loop_is_started.wait(timeout=10)

    def start_event_loop(self):
        asyncio.run(self.run())

    async def run(self):
        self._request_queue = janus.Queue()
        fut: Future
        method: str
        args: tuple
        kwargs: dict
        if not self.is_closing:
            try:
                asyncio.get_running_loop().call_soon(self._loop_is_started.set)
                while True:
                    val = await self._request_queue.async_q.get()
                    fut, method, args, kwargs = val
                    if method == "close":
                        break
                    elif method == "_property":
                        return await getattr(super(), args[0])
                    try:
                        result = await getattr(super(), method)(*args, **kwargs)
                        if inspect.isasyncgen(result):
                            result = await alist(result)
                        fut.set_result(result)
                    except Exception as e:
                        fut.set_exception(e)
            finally:
                await super().close()
            self._loop_is_started.clear()

    def _run_async(self, method: str, *args, **kwargs):
        self.start()
        fut = Future()
        self._request_queue.sync_q.put((fut, method, args, kwargs))
        return fut.result()

    def __del__(self):
        self.close()

    def close(self):
        self.is_closing = True
        if self._loop_is_started.is_set():
            fut = Future()
            self._request_queue.sync_q.put((fut, "close", (), {}))
            fut.result(timeout=10)

    def estimate_fee_per_kb(self, numblocks: int = 6) -> float:
        return self._run_async("estimate_fee_per_kb", numblocks=numblocks)

    def estimate_fee(self, txobj: Tx, numblocks: int = 6) -> int:
        return self._run_async("estimate_fee", numblocks=numblocks)

    def raw_block_header(self, height: int) -> str:
        return self._run_async("raw_block_header", height)

    def block_header(self, height: int) -> BlockHeader:
        return self._run_async("block_header", height)

    def subscribe_to_block_headers(self, callback: BlockHeaderCallbackSync) -> None:
        return self._run_async("subscribe_to_block_headers", callback)

    def unsubscribe_from_block_headers(self) -> None:
        return self._run_async("unsubscribe_from_block_headers")

    @property
    def block(self) -> Tuple[int, str, BlockHeader]:
        return self._run_async("_property", "block")

    def confirmations(self, height: int) -> int:
        return self._run_async("confirmations", height)

    def subscribe_to_address(self,  callback: AddressCallbackSync, addr: str) -> None:
        return self._run_async("subscribe_to_address", callback, addr)

    def unsubscribe_from_address(self, addr: str) -> None:
        return self._run_async("unsubscribe_from_address", addr)

    def subscribe_to_address_transactions(self, callback: AddressTXCallbackSync, addr: str) -> None:
        return self._run_async("subscribe_to_address_transactions", callback, addr)

    def get_balance(self, addr: str) -> ElectrumXBalanceResponse:
        return self._run_async("get_balance", addr)

    def get_balances(self, *args: str) -> List[ElectrumXMultiBalanceResponse]:
        return self._run_async("get_balances", *args)

    def get_merkle(self, tx: ElectrumXTx) -> Optional[ElectrumXMerkleResponse]:
        return self._run_async("get_merkle", tx)

    def merkle_prove(self, tx: ElectrumXTx) -> MerkleProof:
        return self._run_async("merkle_prove", tx)

    def merkle_prove_by_txid(self, tx_hash: str) -> MerkleProof:
        return self._run_async("merkle_prove_by_txid", tx_hash)

    def unspent(self, addr: str, merkle_proof: bool = False) -> ElectrumXUnspentResponse:
        return self._run_async("unspent", addr, merkle_proof=merkle_proof)

    def get_unspents(self, *args: str, merkle_proof: bool = False) -> List[ElectrumXMultiTxResponse]:
        return self._run_async("unspent", *args, merkle_proof=merkle_proof)

    def balance_merkle_proven(self, addr: str) -> int:
        return self._run_async("balance_merkle_proven", addr)

    def balances_merkle_proven(self, *args: str) -> List[AddressBalance]:
        return self._run_async("balances_merkle_proven", *args)

    def history(self, addr: str, merkle_proof: bool = False) -> ElectrumXHistoryResponse:
        return self._run_async("history", addr, merkle_proof=merkle_proof)

    def get_histories(self, *args: str, merkle_proof: bool = False) -> List[ElectrumXMultiTxResponse]:
        return self._run_async("get_histories", *args, merkle_proof=merkle_proof)

    def get_raw_tx(self, tx_hash: str) -> str:
        return self._run_async("get_raw_tx", tx_hash)

    def get_tx(self, tx_hash: str) -> Tx:
        return self._run_async("get_tx", tx_hash)

    def get_verbose_tx(self, tx_hash: str) -> Dict[str, Any]:       # Make TypedDict
        return self._run_async("get_verbose_tx", tx_hash)

    def get_txs(self, *args: str) -> List[Tx]:
        return self._run_async("get_txs", *args)

    def pushtx(self, tx: Union[str, Tx]):
        return self._run_async("pushtx", tx)

    def mktx_with_change(self, ins: List[Union[TxInput, AnyStr]], outs: List[Union[TxOut, AnyStr]],
                         change_addr: str = None, fee: int = None, estimate_fee_blocks: int = 6, locktime: int = 0,
                         sequence: int = 0xFFFFFFFF) -> Tx:
        return self._run_async("mktx_with_change", ins, outs, change_addr=change_addr, fee=fee,
                               estimate_fee_blocks=estimate_fee_blocks, locktime=locktime, sequence=sequence)

    def preparemultitx(self, frm: str, outs: List[TxOut], change_addr: str = None,
                       fee: int = None, estimate_fee_blocks: int = 6) -> Tx:
        return self._run_async("preparemultitx", frm, outs, change_addr=change, fee=fee,
                               estimate_fee_blocks=estimate_fee_blocks, locktime=locktime, sequence=sequence)

    def preparetx(self, frm: str, to: str, value: int, fee: int = None, estimate_fee_blocks: int = 6,
                  change_addr: str = None) -> Tx:
        return self._run_async("preparetx", frm, to, value, fee=fee, estimate_fee_blocks=estimate_fee_blocks,
                               change_addr=change_addr)

    def preparesignedmultirecipienttx(self, privkey, frm: str, outs: List[TxOut], change_addr: str = None,      # Privkey Type?
                                      fee: int = None, estimate_fee_blocks: int = 6) -> Tx:
        return self._run_async("preparesignedmultirecipienttx", privkey, frm, outs,
                               change_addr=change_addr, fee=fee, estimate_fee_blocks=estimate_fee_blocks)

    def preparesignedtx(self, privkey, frm: str, to: str, value: int, change_addr: str = None,                    # Privkey Type?
                        fee: int = None, estimate_fee_blocks: int = 6) -> Tx:
        return self._run_async("preparesignedtx", privkey, to, value,
                               change_addr=change_addr, fee=fee, estimate_fee_blocks=estimate_fee_blocks)

    def send_to_multiple_receivers_tx(self, privkey, addr: str, outs: List[TxOut], change_addr: str = None,         # Privkey Type?
                                      fee: int = None, estimate_fee_blocks: int = 6):
        return self._run_async("send_to_multiple_receivers_tx", privkey, addr, outs,
                               change_addr=change_addr, fee=fee, estimate_fee_blocks=estimate_fee_blocks)

    def send(self, privkey, frm: str, to: str, value: int, change_addr: str = None,                                 # Privkey Type?
             fee: int = None, estimate_fee_blocks: int = 6):
        return self._run_async("send", privkey, frm, to, value,
                               change_addr=change_addr, fee=fee, estimate_fee_blocks=estimate_fee_blocks)

    def inspect(self, tx: Union[str, Tx]) -> Dict[str, Any]:                # Better typing
        return self._run_async("inspect", tx)
