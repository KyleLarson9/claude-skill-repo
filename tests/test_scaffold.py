import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def _load_marketplace():
    assert MARKETPLACE.is_file(), f"marketplace manifest not found: {MARKETPLACE}"
    return json.loads(MARKETPLACE.read_text(encoding="utf-8"))


def test_marketplace_is_valid_json_with_required_keys():
    data = _load_marketplace()
    assert data["name"] == "larson-claude-plugins"
    assert isinstance(data["owner"], dict) and data["owner"].get("name")
    assert isinstance(data["plugins"], list) and data["plugins"]


def test_read_data_listed_in_marketplace():
    names = {p["name"] for p in _load_marketplace()["plugins"]}
    assert "read_data" in names


def test_each_plugin_source_exists_with_plugin_json():
    for plugin in _load_marketplace()["plugins"]:
        source = (REPO_ROOT / plugin["source"]).resolve()
        assert source.is_dir(), f"missing source dir for {plugin['name']}: {source}"
        plugin_json = source / ".claude-plugin" / "plugin.json"
        assert plugin_json.is_file(), f"missing plugin.json for {plugin['name']}"


def test_plugin_name_matches_marketplace_entry():
    for plugin in _load_marketplace()["plugins"]:
        plugin_json = (
            REPO_ROOT / plugin["source"] / ".claude-plugin" / "plugin.json"
        ).resolve()
        assert plugin_json.is_file(), f"missing plugin.json for {plugin['name']}"
        manifest = json.loads(plugin_json.read_text(encoding="utf-8"))
        assert manifest["name"] == plugin["name"]


def test_each_declared_skills_dir_has_a_skill_md():
    for plugin in _load_marketplace()["plugins"]:
        source = (REPO_ROOT / plugin["source"]).resolve()
        plugin_json = source / ".claude-plugin" / "plugin.json"
        assert plugin_json.is_file(), f"missing plugin.json for {plugin['name']}"
        manifest = json.loads(plugin_json.read_text(encoding="utf-8"))
        skills_rel = manifest.get("skills")
        if not skills_rel:
            continue
        skills_dir = (source / skills_rel).resolve()
        assert skills_dir.is_dir(), f"missing skills dir for {plugin['name']}"
        skill_files = list(skills_dir.rglob("SKILL.md"))
        assert skill_files, f"no SKILL.md under {skills_dir}"
