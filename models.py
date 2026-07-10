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
        "subtitle": "Pick a quest",
        "activity": "About 20 to 30 minutes. Do it on your own, bring it to your 1:1. You're doing two things: chasing a career you're curious about, and helping us make Hope Street better.",
        "prompts": [
            "A career, job, or major you're low-key curious about",
            "Why it caught your eye",
            "Take one quest, your pick: [Career Safari](https://discover.hopestreetgroup.org/student-quest/career-safari?launchId=506) • [Find Your Fit](https://discover.hopestreetgroup.org/student-quest/interest-inventory?launchId=507) • [Building Next Steps](https://discover.hopestreetgroup.org/student-quest/academic-planning?launchId=505)",
            "The coolest or most surprising thing you learned",
            "One 'huh, I didn't know that' moment",
            "Did it change how you see this path?",
            "What felt helpful or fun?",
            "What was confusing, slow, or off?",
            "One thing you'd change or add",
            "One small thing you want to explore next"
        ]
    },
    2: {
        "title": "Down the Rabbit Hole",
        "subtitle": "Watch, listen, read",
        "activity": "The best way to learn what a job is really like is to go see it. No quest this week, just you and the internet. Watch, listen, read, follow your curiosity.",
        "prompts": [
            "Watch two or three 'day in the life' videos for your field",
            "Listen to a podcast episode with someone who does this work",
            "Read an article, a thread, or a blog post from inside the field",
            "The most surprising thing I found",
            "One person, channel, or account worth following",
            "Something that made this field more exciting to me",
            "Something that gave me pause",
            "Am I more or less into this than last week, and why?",
            "One question this raised that you want to answer"
        ]
    },
    3: {
        "title": "Talk to a Real Human",
        "subtitle": "Reach out to one person",
        "activity": "Nothing beats hearing it straight from someone living it. Reach out to one real person and ask about their path. Your mentor can help you find someone.",
        "prompts": [
            "Find one person in or near your field",
            "Reach out, short and kind: who you are, why you're curious, two or three questions",
            "Who I talked to (name or role)",
            "The questions I asked",
            "The best thing they said",
            "One myth this busted, or something that surprised me",
            "One piece of advice I want to remember",
            "Thank-you note sent (always)",
            "One thing you'll do because of this chat"
        ]
    },
    4: {
        "title": "Map the Route",
        "subtitle": "What's the road there?",
        "activity": "Now you know the destination. What's the road there? Part detective, part planner: figure out what it takes, and sketch your route.",
        "prompts": [
            "The education or training it usually takes",
            "The skills that matter most, and which ones you already have",
            "What a first job or entry point looks like",
            "A rough sense of the pay range",
            "One or two real programs, schools, or paths you found",
            "Now (sketch your route)",
            "Next (this year)",
            "Later",
            "One senior-year move you can make toward this"
        ]
    },
    5: {
        "title": "Make Something Real",
        "subtitle": "Turn your exploration into one real artifact",
        "activity": "Explorers make things. Turn your exploration into one real artifact you could actually show someone. Great to build during an AI Maker session.",
        "prompts": [
            "Pick one (resume bullet, portfolio piece, outreach message, mock project, mood board, or your own idea)",
            "What I made",
            "Why I chose this",
            "What I'm proud of",
            "What I'd improve with more time",
            "Show it off (in the cohort channel, to your mentor, or in your Weekly Share)"
        ]
    },
    6: {
        "title": "Your Version 1.0 Plan",
        "subtitle": "Pull it all together",
        "activity": "Time to pull it all together. Not a final answer, a Version 1.0, a plan you can keep updating as you grow. Look back at Entry 1 and see how far you've come.",
        "prompts": [
            "The path I'm most curious about right now",
            "Why it fits me (interests, strengths, values)",
            "My next three steps (this summer, this school year, beyond)",
            "What I still want to explore",
            "How did my thinking shift from that first quest (Entry 1) to now?",
            "The most useful thing I did during these Field Notes",
            "Comparing your first Hope Street quest (Entry 1) to everything since, where did Hope Street help most, and where should it grow?"
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
