from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class Student:
    id: str
    display_name: str
    internship_date: str  # "Summer 2024", "2025", etc
    created_date: datetime
    avatar: str = "🚀"  # emoji or avatar name
    custom_title: str = ""  # "My Journey to Becoming a [Career]"

@dataclass
class EntryResponse:
    student_id: str
    entry_number: int
    fields: Dict[str, Any]
    status: str  # "not_started", "in_progress", "done"
    updated_timestamp: datetime

# Entry templates (1-6)
ENTRIES = {
    1: {
        "title": "First Contact",
        "subtitle": "Career Safari",
        "activity": "Name a career, run Career Safari quest (external link)",
        "prompts": [
            "A career you are curious about",
            "Why it caught your eye",
            "Most surprising thing learned",
            "One 'huh, I didn't know that' moment",
            "Did it change how you see this path?",
            "Real talk: What felt helpful/fun? What was confusing? One thing to change?",
            "One small thing you want to explore next"
        ]
    },
    2: {
        "title": "Down the Rabbit Hole",
        "subtitle": "Off Platform",
        "activity": "Watch 2-3 'day in the life' videos, listen to podcast, or read article/blog post",
        "prompts": [
            "Most surprising thing I found",
            "One person/channel/account worth following (with link)",
            "Something that made this field more exciting",
            "Something that gave me pause",
            "Am I more or less into this than last week, and why?",
            "One question this raised"
        ]
    },
    3: {
        "title": "Talk to a Real Human",
        "subtitle": "Mentorship",
        "activity": "Message one professional/college student/mentor with questions",
        "prompts": [
            "Who I talked to (name or role)",
            "Questions I asked",
            "Best thing they said",
            "One myth busted or surprise",
            "One piece of advice to remember",
            "Thank-you note sent (yes/no)",
            "One thing I will do because of this chat"
        ]
    },
    4: {
        "title": "Map the Route",
        "subtitle": "Research",
        "activity": "Research the path and sketch out what it takes",
        "prompts": [
            "Education/training it usually takes",
            "Skills that matter most, which I already have",
            "What a first job/entry point looks like",
            "Rough pay range",
            "One or two real programs/schools/paths I found",
            "My route: Now / Next (this year) / Later",
            "One senior-year move I can make toward this"
        ]
    },
    5: {
        "title": "Make Something Real",
        "subtitle": "Creation",
        "activity": "Create one artifact (choose: resume bullet, portfolio piece, outreach message, mock project, mood board, or your own idea)",
        "prompts": [
            "What I am making",
            "Upload or link to what I made",
            "Why I chose this",
            "What I'm proud of",
            "What I'd improve with more time"
        ]
    },
    6: {
        "title": "Your Version 1.0 Plan",
        "subtitle": "Reflection",
        "activity": "Write your plan and look back on the journey",
        "prompts": [
            "The path I'm most curious about right now",
            "Why it fits me (interests, strengths, values)",
            "My next three steps (this summer, school year, beyond)",
            "What I still want to explore",
            "How did my thinking shift from Entry 1 to now?",
            "Most useful thing I did during Field Notes",
            "Closing feedback for us: Where did Career Safari help most? Where should it grow?"
        ]
    }
}

@dataclass
class Resource:
    student_id: str
    id: str
    title: str
    url: str
    resource_type: str  # "link", "article", "video", "image", "note"
    notes: str = ""
    added_date: datetime = field(default_factory=datetime.now)
