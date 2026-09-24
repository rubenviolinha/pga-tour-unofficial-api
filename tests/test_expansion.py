"""Offline regression tests for the September expansion."""
import pytest
import pga_tour_api as p
from tests.conftest import compress_payload

@pytest.mark.parametrize("fn,args", [
    (p.pga_scorecard_stats, ("R2026030", "001")),
    (p.pga_course_stats_details, ()),
    (p.pga_record_catalog, ()),
    (p.pga_all_time_records, ("2-1-11",)),
])
def test_empty(mock_graphql, fn, args):
    mock_graphql({})
    assert fn(*args).empty

def test_scorecard_sections(mock_graphql):
    mock_graphql({"scorecardStatsV3Compressed": {"payload": compress_payload({
        "id": "event-player", "rounds": [
            {"round": "-1", "performance": [{"statId": "02675", "total": "2.0"}],
             "scoring": [{"statId": "106", "total": "1"}],
             "strokesGained": [{"statId": "02675", "totalNum": 2.0}]},
            {"round": "1", "performance": [{"statId": "02675", "total": "1.0"}]}]})}})
    df = p.pga_scorecard_stats("event", "001", round="-1")
    assert len(df) == 3
    assert df.iloc[0].stat_id == "02675"
    assert df.iloc[0].player_id == "001"
    assert df.iloc[2].total_num == 2.0
    assert df.attrs["id"] == "event-player"

def test_course_headers(mock_graphql):
    mock_graphql({"courseStatsDetails": {"headers": ["PAR", "+/-", "PAR"],
        "round": "ONE", "rows": [{"rank": 1, "values": [
            {"value": "72"}, {"value": "+1", "tendency": "ABOVE"}, {"value": "100"}]}]}})
    df = p.pga_course_stats_details(round="ONE")
    assert df.iloc[0].par == "72"
    assert df.iloc[0].par_1 == "100"
    assert df.iloc[0].to_par_tendency == "ABOVE"
    assert df.attrs["round"] == "ONE"

def test_catalog(mock_graphql):
    mock_graphql({"allTimeRecordCategories": {"categories": [
        {"categoryId": "SCORING", "displayText": "Scoring", "subCategories": [
            {"displayText": "Rounds", "statistics": [
                {"recordId": "2-1-11", "displayText": "Lowest"}]}]}]}})
    df = p.pga_record_catalog()
    assert df.iloc[0].record_id == "2-1-11"
    assert df.iloc[0].subcategory == "Rounds"

def test_records(mock_graphql):
    mock_graphql({"allTimeRecordStat": {"statHeaders": ["Score", "Player"],
        "primaryColumnIndex": 0, "rows": [{"playerId": "001", "values": ["58", "Example"]}]}})
    df = p.pga_all_time_records("2-1-11")
    assert df.iloc[0].player_id == "001"
    assert df.iloc[0].score == "58"
    assert df.attrs["primaryColumnIndex"] == 0

@pytest.mark.parametrize("fn,args,response", [
    (p.pga_course_stats_details, (), {"courseStatsDetails": {"headers": ["PAR"], "rows": [{"values": []}]}}),
    (p.pga_all_time_records, ("x",), {"allTimeRecordStat": {"statHeaders": ["Score"], "rows": [{"values": []}]}}),
])
def test_mismatched_headers(mock_graphql, fn, args, response):
    mock_graphql(response)
    with pytest.raises(p.PgaTourError):
        fn(*args)

@pytest.mark.parametrize("fn,args", [(p.pga_course_stats_details, ()), (p.pga_record_catalog, ()), (p.pga_all_time_records, ("x",))])
def test_invalid_tour(fn, args):
    with pytest.raises(ValueError):
        fn(*args, tour="INVALID")

def test_invalid_ranking():
    with pytest.raises(ValueError):
        p.pga_course_stats_details("INVALID")

@pytest.mark.parametrize("method,args,operation,root", [
    ("scorecard_stats", ("event", "001"), "ScorecardStatsV3Compressed", "scorecardStatsV3Compressed"),
    ("course_stats_details", (), "CourseStatsDetails", "courseStatsDetails"),
    ("record_catalog", (), "AllTimeRecordCategories", "allTimeRecordCategories"),
    ("all_time_records", ("2-1-11",), "AllTimeRecordStat", "allTimeRecordStat"),
])
def test_raw(monkeypatch, method, args, operation, root):
    api = p.PgaApi()
    def request(op, variables):
        assert op == operation
        if method == "scorecard_stats":
            assert variables == {"scorecardStatsV3CompressedId": "event", "playerId": "001"}
            return {root: {"payload": compress_payload({"example": True})}}
        return {root: {"example": True}}
    monkeypatch.setattr(api, "graphql", request)
    assert getattr(api, method)(*args) == {"example": True}


def test_player_comparison(mock_graphql):
    mock_graphql({"playerComparison": {"category": "SCORING", "year": 2026,
        "table": {"header": "Scoring", "headerRow": [
            {"playerId": "001", "displayText": "A", "country": "USA", "yearData": True},
            {"playerId": "002", "displayText": "B", "country": "GBR", "yearData": False}],
            "rows": [{"statName": "Scoring Average", "statId": "120", "values": [
                {"displayValue": "69.1", "bold": True, "rankDeviation": .9, "rank": "1st"},
                {"displayValue": "70.2", "bold": False, "rankDeviation": .2, "rank": "2nd"}]}]}}})
    df = p.pga_player_comparison(["001", "002"], year=2026)
    assert len(df) == 2
    assert list(df.player_id) == ["001", "002"]
    assert df.attrs["header"] == "Scoring"

def test_player_comparison_empty(mock_graphql):
    mock_graphql({})
    assert p.pga_player_comparison(["001"]).empty

def test_university_rankings(mock_graphql):
    mock_graphql({"universityRankings": {"year": 2027, "players": [
        {"playerId": "001", "displayName": "A", "rank": 1, "schoolName": "U",
         "tournaments": [{"name": "Event", "points": "10"}]}]}})
    df = p.pga_university_rankings(year=2027)
    assert df.iloc[0].player_id == "001"
    assert df.iloc[0].tournaments[0]["name"] == "Event"
    assert df.attrs["year"] == 2027

def test_university_points(mock_graphql):
    mock_graphql({"universityTotalPoints": {"headers": ["FedExCup Points", "Combined Points"],
        "season": 2026, "players": [{"playerId": "001", "playerName": "A",
        "rank": "1", "rankSort": 1, "data": ["-", "123.4"], "tournaments": []}]}})
    df = p.pga_university_total_points(season=2026)
    assert df.iloc[0].combined_points == "123.4"
    assert df.attrs["headers"] == ["FedExCup Points", "Combined Points"]

def test_university_empty(mock_graphql):
    mock_graphql({})
    assert p.pga_university_rankings().empty
    assert p.pga_university_total_points().empty

def test_dp_world_eligibility(mock_graphql):
    mock_graphql({"tourCupSplit": {"title": "Race to Dubai", "officialPlayers": [
        {"id": "001", "displayName": "A", "thisWeekRank": "1",
         "pointData": {"official": "123.4"}}]}})
    df = p.pga_dp_world_tour_eligibility(year=2026)
    assert df.iloc[0].player_id == "001"
    assert df.iloc[0].points == "123.4"
