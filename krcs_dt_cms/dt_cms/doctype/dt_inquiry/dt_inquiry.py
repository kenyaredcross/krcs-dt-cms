import frappe
from frappe.model.document import Document

class DTInquiry(Document):
	def before_insert(self):
		self.submitted_at = frappe.utils.now()
