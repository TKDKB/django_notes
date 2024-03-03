import uuid
import datetime
from django.core.handlers.wsgi import WSGIRequest
from .models import Note


class HistoryService:

    def __init__(self, request: WSGIRequest):
        self._session = request.session
        self._session.setdefault("history", [])

        if not isinstance(self._session["history"], list):
            self._session["history"] = []

    def add_to_history(self, note: Note):
        if note.uuid in self._session["history"] and len(self._session["history"]) < 20:
            self._session["history"].remove(str(note.uuid))
        self._session["history"].append(str(note.uuid))
        self._session.save()

    def del_from_history(self):
        # if len(self._session["history"]) > 20:
        self._session["history"].pop(0)
        self._session.save()

    def get_history(self):
        return self._session["history"]





