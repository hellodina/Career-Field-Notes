import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
from models import Student, EntryResponse, Resource

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

STUDENTS_FILE = DATA_DIR / "students.json"
RESPONSES_FILE = DATA_DIR / "responses.json"
RESOURCES_FILE = DATA_DIR / "resources.json"

def _serialize(obj):
    """JSON serializer for datetime objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def _load_json(filepath: Path) -> Dict[str, Any]:
    """Load JSON file, return empty dict if missing."""
    if filepath.exists():
        return json.loads(filepath.read_text())
    return {}

def _save_json(filepath: Path, data: Dict[str, Any]):
    """Save dict to JSON."""
    filepath.write_text(json.dumps(data, indent=2, default=_serialize))

# Students
def create_student(display_name: str, internship_date: str) -> Student:
    """Create and save new student."""
    import uuid
    student = Student(
        id=str(uuid.uuid4()),
        display_name=display_name,
        internship_date=internship_date,
        created_date=datetime.now(),
        avatar="🚀",
        custom_title=""
    )
    students = _load_json(STUDENTS_FILE)
    students[student.id] = {
        "id": student.id,
        "display_name": student.display_name,
        "internship_date": student.internship_date,
        "created_date": student.created_date.isoformat(),
        "avatar": student.avatar,
        "custom_title": student.custom_title
    }
    _save_json(STUDENTS_FILE, students)
    return student

def get_student(student_id: str) -> Optional[Student]:
    """Get student by ID."""
    students = _load_json(STUDENTS_FILE)
    if student_id in students:
        data = students[student_id]
        return Student(
            id=data["id"],
            display_name=data["display_name"],
            internship_date=data["internship_date"],
            created_date=datetime.fromisoformat(data["created_date"]),
            avatar=data.get("avatar", "🚀"),
            custom_title=data.get("custom_title", "")
        )
    return None

def update_student(student_id: str, avatar: str = None, custom_title: str = None):
    """Update student avatar and/or custom_title."""
    students = _load_json(STUDENTS_FILE)
    if student_id in students:
        if avatar:
            students[student_id]["avatar"] = avatar
        if custom_title is not None:
            students[student_id]["custom_title"] = custom_title
        _save_json(STUDENTS_FILE, students)

# Entry responses
def save_entry_response(student_id: str, entry_number: int, fields: Dict[str, str], status: str):
    """Save or update entry response."""
    response = EntryResponse(
        student_id=student_id,
        entry_number=entry_number,
        fields=fields,
        status=status,
        updated_timestamp=datetime.now()
    )
    responses = _load_json(RESPONSES_FILE)
    key = f"{student_id}_{entry_number}"
    responses[key] = {
        "student_id": response.student_id,
        "entry_number": response.entry_number,
        "fields": response.fields,
        "status": response.status,
        "updated_timestamp": response.updated_timestamp.isoformat()
    }
    _save_json(RESPONSES_FILE, responses)
    return response

def get_entry_response(student_id: str, entry_number: int) -> Optional[EntryResponse]:
    """Get entry response for student."""
    responses = _load_json(RESPONSES_FILE)
    key = f"{student_id}_{entry_number}"
    if key in responses:
        data = responses[key]
        return EntryResponse(
            student_id=data["student_id"],
            entry_number=data["entry_number"],
            fields=data["fields"],
            status=data["status"],
            updated_timestamp=datetime.fromisoformat(data["updated_timestamp"])
        )
    return None

def get_student_entries(student_id: str) -> Dict[int, Optional[EntryResponse]]:
    """Get all entries for a student (1-6, None if not started)."""
    result = {}
    for entry_num in range(1, 7):
        result[entry_num] = get_entry_response(student_id, entry_num)
    return result

def get_entry_status(student_id: str, entry_number: int) -> str:
    """Get status of entry (not_started, in_progress, done)."""
    response = get_entry_response(student_id, entry_number)
    return response.status if response else "not_started"

# Resources (My Finds)
def add_resource(student_id: str, title: str, url: str, resource_type: str, notes: str = "") -> Resource:
    """Add a resource to student's My Finds."""
    import uuid
    resource = Resource(
        student_id=student_id,
        id=str(uuid.uuid4()),
        title=title,
        url=url,
        resource_type=resource_type,
        notes=notes,
        added_date=datetime.now()
    )
    resources = _load_json(RESOURCES_FILE)
    key = f"{student_id}_{resource.id}"
    resources[key] = {
        "student_id": resource.student_id,
        "id": resource.id,
        "title": resource.title,
        "url": resource.url,
        "resource_type": resource.resource_type,
        "notes": resource.notes,
        "added_date": resource.added_date.isoformat()
    }
    _save_json(RESOURCES_FILE, resources)
    return resource

def get_student_resources(student_id: str) -> List[Resource]:
    """Get all resources for a student."""
    resources = _load_json(RESOURCES_FILE)
    result = []
    for data in resources.values():
        if data["student_id"] == student_id:
            result.append(Resource(
                student_id=data["student_id"],
                id=data["id"],
                title=data["title"],
                url=data["url"],
                resource_type=data["resource_type"],
                notes=data.get("notes", ""),
                added_date=datetime.fromisoformat(data["added_date"])
            ))
    return sorted(result, key=lambda r: r.added_date, reverse=True)

def delete_resource(student_id: str, resource_id: str):
    """Delete a resource."""
    resources = _load_json(RESOURCES_FILE)
    key = f"{student_id}_{resource_id}"
    if key in resources:
        del resources[key]
        _save_json(RESOURCES_FILE, resources)
