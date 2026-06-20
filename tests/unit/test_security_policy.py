from app.core.security import ensure_ingestion_allowed, is_blocked_path


def test_private_exports_are_blocked():
    assert is_blocked_path(r"D:\001 Agentic AI\05Chatgpt\conversations-000.json")
    assert is_blocked_path(r"D:\001 Agentic AI\Ollama\Models\model.gguf")
    assert is_blocked_path(r"D:\001 Agentic AI\Nodejs\node_modules\package")


def test_safe_demo_path_is_allowed():
    assert str(ensure_ingestion_allowed(r"D:\demo\synthetic_governance.md")).endswith("synthetic_governance.md")
