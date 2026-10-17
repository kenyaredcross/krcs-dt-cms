import re
import frappe
from frappe.model.document import Document


class DTProject(Document):
    def before_save(self):
        self.slug = _slugify(self.title)


def _slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-")
