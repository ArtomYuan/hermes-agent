"""i18n 翻译层（fork 自定义，非上游）——输出层按语言翻译用户可见消息。

机制：
- 源码保留上游英文原版，翻译发生在消息发送出口（gateway send 层）。
- 三级匹配：① 完整字符串精确匹配（strip 归一）② f-string 模板正则（{} → 捕获组回填）
  ③ 短前缀替换（片段 key）。
- 未命中的文本原样返回（英文保底），绝不破坏 markdown/代码块/占位符。
- 语言开关：config.yaml → display.language: en | zh（缺省 en）。
"""
from __future__ import annotations

import json
import logging
import os
import re
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

_TABLE_PATH = os.path.join(os.path.dirname(__file__), "zh-CN.json")


class Translator:
    """基于映射表的输出层翻译器。"""

    def __init__(self, table_path: str = _TABLE_PATH):
        with open(table_path, encoding="utf-8") as f:
            data = json.load(f)
        self.language = data.get("language", "zh-CN")
        self.strings: Dict[str, str] = {}
        for k, v in data.get("strings", {}).items():
            self.strings[k.strip()] = v.strip()
        # 前缀 key：短片段（6-30 字符）按长度降序
        self.prefixes: List[Tuple[str, str]] = sorted(
            ((k, v) for k, v in self.strings.items() if 6 <= len(k) <= 30),
            key=lambda kv: -len(kv[0]),
        )
        self.templates: List[Tuple[re.Pattern, str]] = []
        for pat, repl in data.get("templates", {}).items():
            pat_s = pat.strip()
            escaped = re.escape(pat_s).replace(r"\{\}", "(.+?)")
            self.templates.append((re.compile("^" + escaped + "$"), repl.strip()))
        # 长模板优先（精确/完整句先于通用模板匹配，避免短模板抢先导致半翻译）
        self.templates.sort(key=lambda t: -len(t[1]))

    def translate(self, text: str, _depth: int = 0) -> str:
        if not text:
            return text
        t = text.strip()
        # 1. 精确匹配
        if t in self.strings:
            return self.strings[t]
        # 2. 模板正则（整句，占位符回填 + 捕获组递归翻译）
        for rx, repl in self.templates:
            m = rx.match(t)
            if m:
                out = repl
                for i, g in enumerate(m.groups(), 1):
                    # 捕获组递归翻译（动态段如 status_detail），防深循环
                    g_raw = g.strip()
                    g_inner = g_raw[1:-1] if g_raw.startswith("(") and g_raw.endswith(")") else g_raw
                    if _depth < 3:
                        # 逗号分段递归（status_detail 常为多段），段首剥符号再尝试
                        g_t = "，".join(
                            self.translate(p.strip().lstrip("—–-:·| ").strip(), _depth + 1)
                            for p in re.split(r",| · ", g_inner) if p.strip()
                        )
                    else:
                        g_t = g_inner
                    if g_raw != g_inner:
                        g_t = f"（{g_t}）"
                    out = out.replace("{}", g_t, 1)
                return out
        # 3. 顶层分段（' · ' 或 ', ' 连接的多句组合——逐段翻译再拼接，防深循环）
        if _depth < 3 and (" · " in t or ", " in t):
            parts = [p.strip() for p in re.split(r" · |, ", t) if p.strip()]
            if len(parts) > 1:
                translated = "，".join(self.translate(p, _depth + 1) for p in parts)
                translated = translated.replace("。，", "。").replace("！，", "！").replace("？，", "？")
                if translated != t:
                    return translated
        # 4. 前缀替换（尾部递归翻译——前缀+组合消息第二段也能翻）
        for k, v in self.prefixes:
            if t.startswith(k):
                tail = t[len(k):]
                sep = ""
                m2 = re.match(r"^[，,·]+", tail)
                if m2:
                    sep = "，"
                    tail = tail[m2.end():]
                return v + sep + self.translate(tail, _depth + 1)
        return text


@lru_cache(maxsize=1)
def _get_translator() -> Optional[Translator]:
    try:
        return Translator()
    except Exception as e:
        logger.warning("i18n: 翻译表加载失败，保持英文输出: %s", e)
        return None


def _zh_enabled() -> bool:
    """读取 display.language 开关（缺省 zh——fork 默认中文，setup/Dashboard 可切换）。
    不缓存：Dashboard/setup 修改后立即生效。"""
    try:
        import yaml
        cfg_path = os.path.join(os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes")), "config.yaml")
        if os.path.exists(cfg_path):
            cfg = yaml.safe_load(open(cfg_path, encoding="utf-8")) or {}
            lang = (cfg.get("display") or {}).get("language", "zh")
            return str(lang).lower() == "zh"
    except Exception:
        pass
    return True


def translate(text: str) -> str:
    """对外入口：zh 模式翻译，en 模式原样。"""
    if not _zh_enabled():
        return text
    tr = _get_translator()
    if tr is None:
        return text
    try:
        return tr.translate(text)
    except Exception:
        return text
