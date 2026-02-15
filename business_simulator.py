from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Dict, List, Tuple


@dataclass
class BusinessState:
    cash: int = 10_000
    reputation: int = 50
    staff: int = 5
    product_quality: int = 50
    marketing_level: int = 1
    month: int = 1
    game_over: bool = False

    def score(self) -> int:
        """Simple score that rewards healthy finances and brand strength."""
        return self.cash // 100 + self.reputation * 10 + self.product_quality * 8 + self.staff * 20


@dataclass
class BusinessSimulator:
    rng: Random = field(default_factory=Random)
    state: BusinessState = field(default_factory=BusinessState)

    ACTIONS: Dict[str, Tuple[int, int, int, int]] = field(
        default_factory=lambda: {
            "improve_product": (2000, 0, 8, 2),
            "hire_staff": (1500, 0, 2, 1),
            "marketing_campaign": (1200, 3, 0, 0),
            "cut_costs": (-1000, -4, -3, -1),
            "do_nothing": (0, 0, 0, 0),
        }
    )

    def apply_action(self, action: str) -> str:
        if self.state.game_over:
            return "The game is over. Restart to play again."

        if action not in self.ACTIONS:
            return f"Unknown action '{action}'."

        cash_delta, rep_delta, quality_delta, staff_delta = self.ACTIONS[action]
        self.state.cash -= cash_delta
        self.state.reputation = clamp(self.state.reputation + rep_delta, 0, 100)
        self.state.product_quality = clamp(self.state.product_quality + quality_delta, 0, 100)
        self.state.staff = max(0, self.state.staff + staff_delta)

        self._monthly_update()
        return self._format_monthly_report(action)

    def available_actions(self) -> List[str]:
        return list(self.ACTIONS.keys())

    def _monthly_update(self) -> None:
        demand = self.state.marketing_level * 10 + self.state.reputation // 2
        productivity = self.state.staff * (self.state.product_quality // 5)
        revenue = demand * productivity // 10

        random_shock = self.rng.randint(-2000, 2500)
        operating_cost = self.state.staff * 800 + self.state.marketing_level * 600

        self.state.cash += revenue + random_shock - operating_cost

        if random_shock < -1200:
            self.state.reputation = clamp(self.state.reputation - 3, 0, 100)

        if self.state.cash < 0:
            self.state.reputation = clamp(self.state.reputation - 5, 0, 100)

        self.state.month += 1
        self.state.game_over = self.state.month > 12 or self.state.cash <= -5000

    def _format_monthly_report(self, action: str) -> str:
        status = (
            f"\nMonth {self.state.month - 1} action: {action}\n"
            f"Cash: ${self.state.cash}\n"
            f"Reputation: {self.state.reputation}\n"
            f"Staff: {self.state.staff}\n"
            f"Product Quality: {self.state.product_quality}\n"
        )

        if self.state.game_over:
            ending = "Company survived the year!" if self.state.cash > 0 else "Company went bankrupt."
            status += f"\nGame Over: {ending}\nFinal Score: {self.state.score()}\n"

        return status


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(value, high))


def run_cli() -> None:
    print("=== Business Simulator Game ===")
    print("Goal: Keep your company alive for 12 months and maximize score.\n")

    simulator = BusinessSimulator()

    while not simulator.state.game_over:
        print(f"Month {simulator.state.month}")
        print("Choose an action:")
        for action in simulator.available_actions():
            print(f" - {action}")

        selected = input("Your action: ").strip().lower()
        print(simulator.apply_action(selected))

    print("Thanks for playing!")


if __name__ == "__main__":
    run_cli()
