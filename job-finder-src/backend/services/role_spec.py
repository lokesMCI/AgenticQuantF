"""
role_spec.py - turn "what I want to apply for" into search queries + a title relevance filter.

Nothing here is specific to AI. Whatever you type becomes the topic:

    quantum computing internships        -> topic "quantum computing", level intern
    "agentic AI, applied AI" + intern    -> two topics, level intern
    robotics graduate roles              -> topic "robotics", level graduate

Pieces
- parse_request(text)      free text -> (topics, level)
- resolve_spec(...)        CLI flags / free text / profile defaults -> RoleSpec (or None = legacy behaviour)
- RoleSpec.queries         what to type into the job boards
- RoleSpec.matches(job)    does this posting's TITLE fit the topic and the level?

Topic terms are expanded once per topic with an LLM (abbreviations, adjacent role names) and cached in
data/topic_terms.json. If the LLM is unavailable the topic's own words are used, so it still works offline.
"""

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

# ─── levels ───────────────────────────────────────────────────────────────────
LEVELS: Dict[str, Dict[str, List[str]]] = {
    "intern": {
        "queries": ["Intern", "Internship"],
        "terms": ["intern", "interns", "internship", "internships", "placement", "industrial placement",
                  "summer analyst", "co-op", "coop", "working student", "year in industry"],
    },
    "graduate": {
        "queries": ["Graduate"],
        "terms": ["graduate", "graduates", "new grad", "grad scheme", "early careers", "early career",
                  "entry level", "entry-level", "trainee"],
    },
    "junior": {
        "queries": ["Junior"],
        "terms": ["junior", "jr", "entry level", "entry-level", "associate", "early career"],
    },
    "senior": {
        "queries": ["Senior"],
        "terms": ["senior", "sr", "staff", "lead", "principal"],
    },
    "any": {"queries": [], "terms": []},
}
# Words in the user's request that name a level -> canonical level.
_LEVEL_WORDS = {
    "intern": "intern", "interns": "intern", "internship": "intern", "internships": "intern",
    "placement": "intern", "placements": "intern",
    "graduate": "graduate", "graduates": "graduate", "grad": "graduate", "new grad": "graduate",
    "junior": "junior", "entry level": "junior", "entry-level": "junior",
    "senior": "senior", "staff": "senior", "lead": "senior", "principal": "senior",
}
_SENIOR_TITLE = re.compile(r"(?<![a-z0-9])(senior|sr|staff|principal|lead|head of|director|vp|vice president|manager)(?![a-z0-9])", re.I)
_FILLER = {"job", "jobs", "role", "roles", "position", "positions", "opportunity", "opportunities", "vacancy",
           "vacancies", "find", "search", "apply", "for", "me", "to", "in", "a", "an", "the", "some", "any",
           "scan", "look", "looking", "want", "please", "related", "type", "of", "new"}
# Single words too generic to count as "on topic" on their own.
_GENERIC = {"engineer", "engineering", "developer", "software", "research", "researcher", "data", "analyst",
            "scientist", "technology", "tech", "computing", "computer", "science", "manager", "specialist",
            "consultant", "applied", "advanced", "modern", "digital", "systems", "system", "product", "project",
            "and", "or", "the", "of", "for", "in", "with", "a", "an"}


def normalize_level(level: Optional[str]) -> Optional[str]:
    """'Internship' -> 'intern'. Raises ValueError for unknown levels. None stays None."""
    if level is None or not str(level).strip():
        return None
    key = str(level).strip().lower()
    if key in LEVELS:
        return key
    if key in _LEVEL_WORDS:
        return _LEVEL_WORDS[key]
    raise ValueError(f"Unknown level '{level}'. Use one of: {', '.join(LEVELS)} (or intern/internship, graduate, junior, senior).")


# ─── free-text parsing ────────────────────────────────────────────────────────
_LEVEL_RE = re.compile(
    r"(?<![A-Za-z0-9])(new grad|entry[- ]level|internships?|interns?|placements?|graduates?|grad|junior|senior|staff|lead|principal)(?![A-Za-z0-9])",
    re.I,
)


def parse_request(text: str) -> Tuple[List[str], Optional[str]]:
    """
    'quantum computing internships' -> (['quantum computing'], 'intern')
    'agentic AI, applied AI and AI engineering interns' -> (['agentic AI', 'applied AI', 'AI engineering'], 'intern')
    """
    text = (text or "").strip()
    if not text:
        return [], None
    m = _LEVEL_RE.search(text)
    level = _LEVEL_WORDS.get(re.sub(r"[- ]+", " ", m.group(1).lower())) if m else None
    rest = _LEVEL_RE.sub(" ", text)
    parts = re.split(r"\s*(?:,|;|\band\b|\bor\b|\+|&)\s*", rest, flags=re.I)
    topics: List[str] = []
    for part in parts:
        words = [w for w in part.split() if w.lower().strip(".:") not in _FILLER]
        phrase = " ".join(words).strip(" .:-")
        if phrase:
            topics.append(phrase)
    return list(dict.fromkeys(topics)), level


# ─── term matching ────────────────────────────────────────────────────────────
# Word families that job titles use interchangeably ("Applied Science Intern" is an "applied scientist" role).
_FAMILIES = {
    **{w: r"scien(?:ce|ces|tist|tists|tific)" for w in ("science", "sciences", "scientist", "scientists", "scientific")},
    **{w: r"research(?:er|ers)?" for w in ("research", "researcher", "researchers")},
    **{w: r"engineer(?:s|ing)?" for w in ("engineer", "engineers", "engineering")},
    **{w: r"develop(?:er|ers|ment|ing)?" for w in ("developer", "developers", "development", "developing")},
    **{w: r"analy(?:st|sts|tics|tic|sis)" for w in ("analyst", "analysts", "analytics", "analytic", "analysis")},
}


def _word_pattern(word: str) -> str:
    """One word, tolerant of plural/singular and of the usual noun/profession forms (science~scientist, research~researcher)."""
    if word in _FAMILIES:
        return _FAMILIES[word]
    w = re.escape(word)
    if len(word) >= 5 and word.endswith("s") and not word.endswith("ss"):
        return re.escape(word[:-1]) + "s?"
    if len(word) >= 4 and word.endswith(("ic", "er", "or", "ist", "ent")):
        return w + "s?"
    return w


def _compile(terms: Iterable[str]) -> Optional[re.Pattern]:
    terms = sorted({t.strip().lower() for t in terms if t and t.strip()}, key=len, reverse=True)
    if not terms:
        return None
    parts = []
    for t in terms:
        words = re.split(r"[\s\-]+", t)
        parts.append(r"[\s\-]+".join(_word_pattern(w) for w in words if w))
    return re.compile(rf"(?<![a-z0-9])(?:{'|'.join(parts)})(?![a-z0-9])", re.I)


def _distinctive(topic: str) -> List[str]:
    words = [w for w in re.split(r"[^a-z0-9+#.]+", topic.strip().lower()) if w]
    return [w for w in words if w not in _GENERIC and len(w) >= 2]


def _own_terms(topic: str) -> List[str]:
    """
    Terms that identify `topic` by itself: the phrase, its joined spelling ('cyber security' -> 'cybersecurity'),
    and - only when exactly one word carries the meaning ('quantum computing' -> 'quantum') - that word.
    Topics with several meaningful words ('AI cyber security') are NOT split into separate alternatives, which
    would let any 'AI' job or any 'security' job through; they match via `_all_of` instead.
    """
    t = topic.strip().lower()
    terms = [t]
    if " " in t:
        terms.append(re.sub(r"[\s\-]+", "", t))
    dist = _distinctive(topic)
    if len(dist) == 1:
        terms.append(dist[0])
    return list(dict.fromkeys(terms))


def _all_of(topic: str) -> List[str]:
    """Distinctive words that must ALL appear in a title (any order) for a multi-word topic; [] if not applicable."""
    dist = _distinctive(topic)
    return dist if len(dist) >= 2 else []


def _cache_path() -> str:
    try:
        try:
            from config.constants import resolve_workspace_root
        except ImportError:
            from backend.config.constants import resolve_workspace_root
        root = resolve_workspace_root()
    except Exception:
        root = os.getcwd()
    return os.path.join(root, "data", "topic_terms.json")


@dataclass
class Family:
    """What a topic means as a FIELD: title terms to include, look-alikes to exclude, extra phrases to search."""
    include: List[str] = field(default_factory=list)
    exclude: List[str] = field(default_factory=list)
    search: List[str] = field(default_factory=list)


def _clean_terms(items, limit: int, allow_generic: bool = False) -> List[str]:
    out = []
    for t in items or []:
        t = re.sub(r"\s+", " ", str(t).strip().lower())
        if not t or len(t) > 40:
            continue
        if not allow_generic and t in _GENERIC:
            continue
        if any(w in _LEVEL_WORDS for w in t.split()):
            continue
        out.append(t)
    return list(dict.fromkeys(out))[:limit]


def _normalize_family(obj) -> Family:
    """Accept a plain term list (older format / simple callers) or a dict with include/exclude/search."""
    if isinstance(obj, Family):
        obj = {"include": obj.include, "exclude": obj.exclude, "search": obj.search}
    if isinstance(obj, (list, tuple)):
        obj = {"include": list(obj)}
    obj = obj or {}
    inc = _clean_terms(obj.get("include"), 70)
    exc = _clean_terms(obj.get("exclude"), 15, allow_generic=True)
    exc = [e for e in exc if e not in inc]
    return Family(include=inc, exclude=exc, search=_clean_terms(obj.get("search"), 8))


def _llm_terms(topic: str) -> dict:
    """Ask the LLM what `topic` means as a whole field. Returns {} on any failure."""
    from pydantic import BaseModel

    class TopicFamily(BaseModel):
        include: List[str]
        exclude: List[str]
        search: List[str]

    try:
        try:
            from services.gemini_client import generate_content_with_fallback
        except ImportError:
            from backend.services.gemini_client import generate_content_with_fallback
        prompt = (
            f"A job seeker wants roles in the FIELD: '{topic}'. Treat it as a whole field, not a literal phrase: "
            "they want every kind of job in it.\n\n"
            "Return JSON with:\n"
            "- include: 40-60 lowercase words or short phrases that appear in JOB TITLES anywhere in this field. Be "
            "EXHAUSTIVE: think of every team and specialisation in a large organisation in this field, including the "
            "less obvious ones (e.g. for security: digital forensics, privacy, risk and compliance, fraud), plus adjacent "
            "role names (researcher, scientist, analyst, engineer variants) and standard abbreviations. "
            "Example for 'cyber security': software/application security, cloud security, "
            "network security, system security, AI/ML/LLM security, penetration testing, red team, threat intelligence, "
            "incident response, malware, cryptography, devsecops, infosec, appsec, GRC... Example for 'applied AI': "
            "machine learning, ml engineer, ml researcher, ai researcher, research scientist, applied scientist, deep "
            "learning, nlp, computer vision, llm, generative ai, mlops, data scientist... A single distinctive word is "
            "fine when it identifies the field on its own (e.g. 'security', 'ml'). Do NOT include seniority words "
            "(intern, junior, senior) and do not include generic words alone such as 'engineer', 'developer', "
            "'software', 'research', 'data', 'analyst'.\n"
            "- exclude: up to 12 lowercase phrases that look similar in a job title but belong to a DIFFERENT field "
            "(e.g. for security: 'security guard', 'security officer', 'social security', 'door supervisor'). "
            "Empty list if there are none.\n"
            "- search: 4-6 short job-board search phrases, each a different sub-area of the field, that together "
            "would surface the whole field (e.g. 'application security', 'penetration testing', 'AI security')."
        )
        raw = generate_content_with_fallback(prompt, TopicFamily)
        return json.loads(raw)
    except Exception:
        return {}


def _read_cache(path: str) -> Dict[str, Any]:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}
    return {}


def get_family(topic: str, llm: Optional[Callable[[str], Any]] = None, use_cache: bool = True,
               refresh: bool = False) -> Family:
    """
    The cached/LLM family for `topic`. You can edit data/topic_terms.json by hand: add or remove terms under
    include / exclude / search and the next scan uses them (the file is only rewritten when a topic is refreshed).
    """
    key = topic.strip().lower()
    path = _cache_path()
    cache = _read_cache(path) if use_cache else {}
    entry = cache.get(key)
    if isinstance(entry, dict) and not refresh and entry.get("include"):
        return _normalize_family(entry)                        # current format
    fam = _normalize_family((llm or _llm_terms)(topic))        # miss, refresh, or an older narrow list-format entry
    if fam.include and use_cache:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            cache[key] = {"include": fam.include, "exclude": fam.exclude, "search": fam.search}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cache, f, indent=2, sort_keys=True)
        except Exception:
            pass
    return fam


def expand_topic(topic: str, llm: Optional[Callable[[str], Any]] = None, use_cache: bool = True) -> List[str]:
    """Terms that identify `topic` in a job title: its own words plus the field's include terms."""
    return list(dict.fromkeys(_own_terms(topic) + get_family(topic, llm=llm, use_cache=use_cache).include))


# ─── the spec ─────────────────────────────────────────────────────────────────
@dataclass
class RoleSpec:
    topics: List[str] = field(default_factory=list)
    level: str = "any"
    queries: List[str] = field(default_factory=list)
    topic_terms: List[str] = field(default_factory=list)
    topic_all_of: List[List[str]] = field(default_factory=list)  # each group: every word must be in the title
    topic_exclude: List[str] = field(default_factory=list)       # look-alike titles from other fields ("security guard")
    loose: bool = False  # also accept a match in the job description when the title doesn't match

    def __post_init__(self):
        self._topic_re = _compile(self.topic_terms)
        self._level_re = _compile(LEVELS[self.level]["terms"])
        self._group_res = [[_compile([w]) for w in grp] for grp in self.topic_all_of]
        self._exclude_re = _compile(self.topic_exclude)

    def _topic_in_title(self, title: str) -> bool:
        if self._topic_re and self._topic_re.search(title):
            return True
        return any(all(r.search(title) for r in grp) for grp in self._group_res)

    def describe(self) -> str:
        bits = []
        if self.topics:
            bits.append(f"topic: {', '.join(self.topics)}")
        bits.append(f"level: {self.level}")
        if self.topic_exclude:
            bits.append(f"avoiding: {', '.join(self.topic_exclude[:5])}")
        return " | ".join(bits)

    def matches(self, title: str, description: str = "") -> Tuple[bool, str]:
        """(ok, reason). Strict mode looks at the title only; loose also reads the description."""
        title = title or ""
        if self.level in ("intern", "graduate", "junior") and _SENIOR_TITLE.search(title):
            return False, "senior title"
        if self._level_re:
            title_level = bool(self._level_re.search(title))
            desc_level = bool(self.loose and description and self._level_re.search(description[:600]))
            if not (title_level or desc_level):
                return False, f"title has no {self.level} keyword"
        if self._exclude_re:
            bad = self._exclude_re.search(title)
            if bad:
                return False, f"look-alike from another field ({bad.group(0).lower()})"
        if self._topic_re or self._group_res:
            if self._topic_in_title(title):
                return True, "title match"
            if self.loose and description and self._topic_re:
                hits = len(self._topic_re.findall(description[:4000]))
                if hits >= 3:
                    return True, f"description mentions topic {hits}x"
            return False, "off topic"
        return True, "level match"


def build_queries(topics: List[str], level: str, sub_searches: Optional[List[List[str]]] = None, cap: int = 12) -> List[str]:
    """
    What to type into the job boards. Order matters (the cap trims the tail): every topic first, then each
    topic's sub-field searches (round-robin so no topic starves), then the alternate level wording.
    """
    suffixes = LEVELS[level]["queries"] or [""]
    first = suffixes[0]
    out = [f"{t} {first}".strip() for t in topics]
    lists = [l for l in (sub_searches or []) if l]
    for i in range(max((len(l) for l in lists), default=0)):
        for l in lists:
            if i < len(l):
                out.append(f"{l[i]} {first}".strip())
    for suf in suffixes[1:]:
        out += [f"{t} {suf}".strip() for t in topics]
    return list(dict.fromkeys(out))[:cap]


def resolve_spec(
    topic: Optional[str] = None,
    level: Optional[str] = None,
    request: Optional[str] = None,
    role: Optional[str] = None,
    prefs: Optional[dict] = None,
    loose: bool = False,
    exact: bool = False,
    llm: Optional[Callable[[str], Any]] = None,
    refresh: bool = False,
) -> Optional[RoleSpec]:
    """
    Decide what to search for. `--role` gives explicit queries (no topic filtering). Otherwise free text /
    --topic / --level, with anything not typed filled from the profile's `topics` / `level`. With nothing
    typed and no profile defaults: None (legacy behaviour: profile `target_roles`, no filtering).
    An explicit --level always wins over a level found in free text.
    """
    prefs = prefs or {}
    topics: List[str] = []
    lvl: Optional[str] = None
    if request:
        t, l = parse_request(request)
        topics += t
        lvl = l
    if topic:
        topics += [p.strip() for p in re.split(r"[,;]", topic) if p.strip()]
    if level:
        lvl = normalize_level(level)

    if role:  # explicit queries: don't second-guess them, but honour an explicit level filter
        queries = [r.strip() for r in role.split(",") if r.strip()]
        if not lvl:
            return None
        return RoleSpec(topics=[], level=lvl, queries=queries, topic_terms=[], loose=loose)

    # Whatever wasn't typed falls back to the profile's defaults (`topics`, `level`).
    if not topics:
        topics = [t for t in prefs.get("topics", []) if t]
    if not lvl and prefs.get("level"):
        lvl = normalize_level(prefs.get("level"))
    if not topics and not lvl:
        return None

    topics = list(dict.fromkeys(topics))
    lvl = lvl or "any"
    terms: List[str] = []
    groups: List[List[str]] = []
    excludes: List[str] = []
    searches: List[List[str]] = []
    for t in topics:
        if exact:
            terms += _own_terms(t)
        else:
            fam = get_family(t, llm=llm, refresh=refresh)
            terms += _own_terms(t) + fam.include
            excludes += fam.exclude
            searches.append([q for q in fam.search if q.lower() != t.lower()])
        if _all_of(t):
            groups.append(_all_of(t))
    terms = list(dict.fromkeys(terms))
    return RoleSpec(topics=topics, level=lvl, queries=build_queries(topics, lvl, searches) if topics else [],
                    topic_terms=terms, topic_all_of=groups,
                    topic_exclude=[e for e in dict.fromkeys(excludes) if e not in terms], loose=loose)
