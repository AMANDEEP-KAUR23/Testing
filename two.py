from fastapi import APIRouter, HTTPException
from .schemas import NoteCreate, NoteResponse
from .data import notes_db

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate):
    note_id = len(notes_db) + 1
    new_note = {
        "id": note_id,
        "title": note.title,
        "content": note.content
    }
    notes_db.append(new_note)
    return new_note


@router.get("/", response_model=list[NoteResponse])
def get_all_notes():
    return notes_db


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    for note in notes_db:
        if note["id"] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")


@router.delete("/{note_id}")
def delete_note(note_id: int):
    for note in notes_db:
        if note["id"] == note_id:
            notes_db.remove(note)
            return {"message": "Note deleted"}
    raise HTTPException(status_code=404, detail="Note not found")

