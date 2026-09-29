from chooser import Chooser, Item, UserProfile


def test_recommendations_are_explainable_and_ranked():
    chooser = Chooser([
        Item("a", "Security", frozenset({"security"}), popularity=10),
        Item("b", "Cooking", frozenset({"food"}), popularity=10),
    ])
    result = chooser.recommend(UserProfile(interests=frozenset({"security"})))
    assert result[0].item.id == "a"
    assert result[0].reasons


def test_user_block_is_respected():
    chooser = Chooser([Item("a", "A"), Item("b", "B")])
    result = chooser.recommend(UserProfile(blocked_items=frozenset({"a"})))
    assert [choice.item.id for choice in result] == ["b"]


def test_explicit_policy_is_opt_in():
    def policy(item, profile):
        return item.id != "blocked", "application policy" if item.id == "blocked" else None

    chooser = Chooser([Item("blocked", "Blocked"), Item("open", "Open")], policy=policy)
    assert [choice.item.id for choice in chooser.recommend(UserProfile())] == ["open"]
