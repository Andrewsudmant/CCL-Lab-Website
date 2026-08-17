"""Fail-closed CAD budget controls for paid web discovery."""

from __future__ import annotations

import datetime as dt
import json
import os
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

from current_conversations.adapters.base import AdapterError


@dataclass(frozen=True)
class BudgetPolicy:
    per_run_cad: Decimal
    per_month_cad: Decimal
    usd_per_cad: Decimal
    rate_date: dt.date
    max_web_search_calls: int
    max_web_items: int
    safety_margin: Decimal = Decimal("0.10")

    @classmethod
    def from_env(cls, today: dt.date | None = None) -> "BudgetPolicy":
        today = today or dt.date.today()
        required = [
            "CURRENT_CONVERSATIONS_MAX_COST_CAD_PER_RUN",
            "CURRENT_CONVERSATIONS_MAX_COST_CAD_PER_MONTH",
            "CURRENT_CONVERSATIONS_USD_PER_CAD",
            "CURRENT_CONVERSATIONS_USD_PER_CAD_DATE",
            "CURRENT_CONVERSATIONS_MAX_WEB_SEARCH_CALLS",
            "CURRENT_CONVERSATIONS_MAX_WEB_ITEMS",
        ]
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise AdapterError("paid discovery disabled: missing cost controls " + ", ".join(missing))
        try:
            policy = cls(
                Decimal(os.environ[required[0]]),
                Decimal(os.environ[required[1]]),
                Decimal(os.environ[required[2]]),
                dt.date.fromisoformat(os.environ[required[3]]),
                int(os.environ[required[4]]),
                int(os.environ[required[5]]),
            )
        except (InvalidOperation, ValueError) as exc:
            raise AdapterError("paid discovery disabled: invalid cost controls") from exc
        if policy.per_run_cad <= 0 or policy.per_month_cad <= 0 or policy.usd_per_cad <= 0:
            raise AdapterError("paid discovery disabled: cost controls must be positive")
        if policy.per_run_cad > Decimal("2") or policy.per_month_cad > Decimal("20"):
            raise AdapterError("paid discovery disabled: configured CAD ceilings exceed owner approval")
        if (today - policy.rate_date).days > 31 or policy.rate_date > today:
            raise AdapterError("paid discovery disabled: currency conversion date is absent or stale")
        return policy

    def maximum_cad(self, maximum_usd: Decimal) -> Decimal:
        return (maximum_usd / self.usd_per_cad) * (Decimal("1") + self.safety_margin)


class BudgetLedger:
    def __init__(self, path: Path, policy: BudgetPolicy, now: dt.datetime | None = None):
        self.path = path
        self.policy = policy
        self.now = now or dt.datetime.now(dt.timezone.utc)
        self.month = self.now.strftime("%Y-%m")

    def load(self) -> dict:
        if not self.path.exists():
            return {"version": "1.0", "month": self.month, "spent_cad": "0.00", "runs": []}
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
            Decimal(value["spent_cad"])
            if value["month"] != self.month or not isinstance(value["runs"], list):
                raise ValueError
            return value
        except (json.JSONDecodeError, KeyError, InvalidOperation, ValueError) as exc:
            raise AdapterError("paid discovery disabled: budget ledger is corrupted or inconsistent") from exc

    def authorize(self, maximum_usd: Decimal) -> tuple[Decimal, Decimal]:
        ledger = self.load()
        maximum_cad = self.policy.maximum_cad(maximum_usd)
        spent = Decimal(ledger["spent_cad"])
        if maximum_cad > self.policy.per_run_cad:
            raise AdapterError("paid discovery disabled: maximum possible run cost exceeds CAD 2")
        if spent + maximum_cad > self.policy.per_month_cad:
            raise AdapterError("paid discovery disabled: maximum possible cost exceeds monthly CAD allowance")
        return maximum_cad, self.policy.per_month_cad - spent

    def record(self, run_id: str, actual_or_estimated_usd: Decimal, usage_basis: str, usage: dict | None = None) -> dict:
        ledger = self.load()
        cad = self.policy.maximum_cad(actual_or_estimated_usd)
        spent = Decimal(ledger["spent_cad"]) + cad
        if cad > self.policy.per_run_cad or spent > self.policy.per_month_cad:
            raise AdapterError("budget reconciliation would exceed an approved CAD ceiling")
        ledger["spent_cad"] = str(spent.quantize(Decimal("0.01")))
        ledger["conversion"] = {"usd_per_cad": str(self.policy.usd_per_cad), "rate_date": self.policy.rate_date.isoformat(), "safety_margin": str(self.policy.safety_margin)}
        ledger["runs"].append({
            "run_id": run_id, "recorded_at": self.now.isoformat(),
            "cost_cad": str(cad.quantize(Decimal("0.01"))), "usage_basis": usage_basis,
            "provider_usage": {
                "input_tokens": int((usage or {}).get("input_tokens", 0)),
                "output_tokens": int((usage or {}).get("output_tokens", 0)),
                "total_tokens": int((usage or {}).get("total_tokens", 0)),
            },
        })
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        return ledger
