"""A small dependency-free recommender inspired by Microsoft Recommenders.

The module is intentionally deterministic and auditable. It is a starter layer,
not a security boundary: callers must enforce OS permissions separately.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import log1p
from typing import Callable, Iterable, Mapping


@dataclass(frozen=True)
class Item:
    id: str
    title: str
    tags: frozenset[str] = frozenset()
    description: str = ""
    popularity: float = 0.0


@dataclass(frozen=True)
class UserProfile:
    interests: frozenset[str] = frozenset()
    liked_items: frozenset[str] = frozenset()
    blocked_items: frozenset[str] = frozenset()


@dataclass(frozen=True)
class Choice:
    item: Item
    score: float
    reasons: tuple[str, ...]


Policy = Callable[[Item, UserProfile], tuple[bool, str | None]]


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


class Chooser:
    """Rank items with explicit scoring, diversity, and explanation records.

    `policy` is an opt-in hook. It should return `(allowed, reason)`. No hidden
    policy is applied by this class; an application can provide a benevolence,
    consent, legal, or host-security policy appropriate to its deployment.
    """

    def __init__(self, items: Iterable[Item], policy: Policy | None = None):
        self.items = tuple(items)
        self.policy = policy

    def recommend(
        self,
        profile: UserProfile,
        limit: int = 10,
        diversity: float = 0.25,
    ) -> list[Choice]:
        if limit < 1:
            return []

        candidates: list[Choice] = []
        for item in self.items:
            if item.id in profile.blocked_items:
                continue
            if self.policy is not None:
                allowed, reason = self.policy(item, profile)
                if not allowed:
                    # The reason is retained for an audit hook by the caller;
                    # this engine does not silently mutate the item or profile.
                    continue
            overlap = _jaccard(set(item.tags), set(profile.interests))
            popularity = min(log1p(max(item.popularity, 0.0)) / 10.0, 1.0)
            history_bonus = 0.10 if item.id in profile.liked_items else 0.0
            score = 0.70 * overlap + 0.20 * popularity + history_bonus
            reasons: list[str] = []
            if overlap:
                reasons.append(f"{len(set(item.tags) & set(profile.interests))} interest tag match")
            if popularity:
                reasons.append("popularity signal")
            if history_bonus:
                reasons.append("previously liked")
            candidates.append(Choice(item, score, tuple(reasons or ["neutral baseline"])))

        selected: list[Choice] = []
        remaining = candidates[:]
        while remaining and len(selected) < limit:
            def reranked(choice: Choice) -> float:
                novelty = 1.0
                if selected:
                    novelty -= max(
                        _jaccard(set(choice.item.tags), set(old.item.tags))
                        for old in selected
                    )
                return (1.0 - diversity) * choice.score + diversity * novelty

            best = max(remaining, key=reranked)
            selected.append(best)
            remaining.remove(best)
        return selected
