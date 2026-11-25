# Copyright (c) 2026, Lennox Mwita and contributors

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

# Multi-select option lists. Stored on the document as one value per line.
# Single-select options (organisation type, duration) live on the DocType
# itself so they can be edited from Customize Form.
PARTNERSHIP_TYPES = [
	"Funding / Financial Support",
	"Technical Assistance",
	"Programme Implementation",
	"Research and Knowledge Sharing",
	"Training and Capacity Building",
	"Technology and Innovation",
	"Resource Mobilisation",
	"Advocacy and Awareness",
	"Equipment and In-kind Support",
	"Strategic Collaboration",
	"Other",
]

AREAS_OF_INTEREST = [
	"Disaster Risk Reduction",
	"Emergency Response",
	"Health and Nutrition",
	"Climate Change and Resilience",
	"Youth Empowerment",
	"Volunteerism",
	"Community Development",
	"Education and Training",
	"Digital Transformation and Innovation",
	"Research and Knowledge Management",
	"Livelihoods and Economic Empowerment",
	"Other",
]

AREAS_OF_OPERATION = [
	"Local / Community",
	"County",
	"National",
	"Regional (East Africa)",
	"Continental (Africa)",
	"Global",
]

GEOGRAPHIC_SCOPES = [
	"Specific counties",
	"Nationwide (Kenya)",
	"Regional (East Africa)",
	"International",
]

MULTI_SELECT_FIELDS = {
	"partnership_types": PARTNERSHIP_TYPES,
	"areas_of_interest": AREAS_OF_INTEREST,
	"areas_of_operation": AREAS_OF_OPERATION,
	"geographic_scope": GEOGRAPHIC_SCOPES,
}


def split_lines(value):
	return [v.strip() for v in (value or "").splitlines() if v.strip()]


class DTPartnershipRequest(Document):
	def before_insert(self):
		self.submitted_at = frappe.utils.now()

	def validate(self):
		self.validate_multi_selects()
		self.validate_year_established()
		self.validate_start_date()

	def validate_multi_selects(self):
		for fieldname, allowed in MULTI_SELECT_FIELDS.items():
			values = split_lines(self.get(fieldname))
			invalid = [v for v in values if v not in allowed]
			if invalid:
				label = self.meta.get_label(fieldname)
				frappe.throw(_("Invalid value for {0}: {1}").format(label, ", ".join(invalid)))
			# normalise: dedupe, keep the canonical order
			self.set(fieldname, "\n".join(v for v in allowed if v in values))

	def validate_year_established(self):
		if not self.year_established:
			return
		current = getdate(nowdate()).year
		if not 1800 <= self.year_established <= current:
			frappe.throw(_("Year Established must be between 1800 and {0}").format(current))

	def validate_start_date(self):
		# Only enforce on new submissions so staff can still edit older records.
		if self.is_new() and self.proposed_start_date and getdate(self.proposed_start_date) < getdate(nowdate()):
			frappe.throw(_("Proposed Start Date cannot be in the past"))
