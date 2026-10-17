import re
import frappe

# curly/smart quote characters to strip from blockquote edges
_QUOTES = u'"“”‘’\''


def _fix_blockquote(m):
	inner = m.group(1).strip()
	# strip wrapping <span ...>...</span> injected by Quill
	inner = re.sub(r'^<span[^>]*>(.*)</span>$', r'\1', inner.strip(), flags=re.DOTALL).strip()
	# strip leading/trailing quote characters
	inner = inner.strip(_QUOTES)
	# if no block element inside, wrap in <p>
	if not re.search(r'^<(p|div|h[1-6])', inner):
		inner = '<p>' + inner + '</p>'
	return '<blockquote>' + inner + '</blockquote>'


def _clean_body(html):
	"""Strip Quill editor wrapper div, inline styles, and normalise blockquotes."""
	if not html:
		return ""
	# unwrap <div class="ql-editor ...">...</div>
	html = re.sub(r'^<div[^>]*class="[^"]*ql-editor[^"]*"[^>]*>(.*)</div>$', r'\1', html.strip(), flags=re.DOTALL)
	# remove inline font-size and color styles injected by Quill
	html = re.sub(r'\s*font-size:[^;";]+;?', '', html)
	html = re.sub(r'\s*color:[^;";]+;?', '', html)
	# clean up empty style attributes
	html = re.sub(r'\s*style=""', '', html)
	html = re.sub(r'\s*style="\s*"', '', html)
	# normalise blockquotes
	html = re.sub(r'<blockquote>(.*?)</blockquote>', _fix_blockquote, html, flags=re.DOTALL)
	return html.strip()


@frappe.whitelist(allow_guest=True)
def get_site_settings():
	doc = frappe.get_single("DT Site Settings")
	return {
		"hero_word_a": doc.hero_word_a or "PAPER",
		"hero_word_b": doc.hero_word_b or "PIXELS",
		"hero_body": doc.hero_body or "",
		"marquee_items": doc.marquee_items or "",
		"stat_counties": doc.stat_counties or 47,
		"stat_lives": doc.stat_lives or "100k+",
		"stat_projects": doc.stat_projects or "300+",
		"stat_awards": doc.stat_awards or "16+",
		"stat_team": doc.stat_team or "34+",
		"cta_headline": doc.cta_headline or "",
		"cta_body": doc.cta_body or "",
		"partner_email": doc.partner_email or "",
	}


@frappe.whitelist(allow_guest=True)
def get_team():
	"""Returns team members shaped to match the TeamMember TS interface {s,n,i,r,b,t}."""
	members = frappe.get_all(
		"DT Team Member",
		filters={"published": 1},
		fields=["full_name", "slug", "initials", "role_title", "bio", "photo", "skills", "email", "linkedin", "twitter", "github", "avatar_index"],
		order_by="display_order asc",
	)
	result = []
	for m in members:
		raw = m.get("skills") or ""
		result.append({
			"s": m["slug"] or "",
			"n": m["full_name"],
			"i": m["initials"],
			"r": m["role_title"],
			"b": m["bio"],
			"photo": m.get("photo") or "",
			"t": [s.strip() for s in raw.splitlines() if s.strip()],
			"email": m.get("email") or "",
			"linkedin": m.get("linkedin") or "",
			"twitter": m.get("twitter") or "",
			"github": m.get("github") or "",
			"avatar_index": m.get("avatar_index") or 0,
		})
	return result


@frappe.whitelist(allow_guest=True)
def get_posts(category=None):
	"""Returns posts shaped to match the Post TS interface {s,c,k,n,d,u,b}."""
	filters = {"published": 1}
	if category:
		filters["category"] = category

	posts = frappe.get_all(
		"DT Post",
		filters=filters,
		fields=["name", "title", "slug", "category", "label", "is_featured", "description", "external_url", "cover_image", "body"],
		order_by="display_order asc",
	)

	result = []
	for p in posts:
		result.append({
			"s": p.slug or "",
			"c": _cat_key(p.category),
			"k": p.label or "",
			"f": bool(p.is_featured),
			"n": p.title,
			"d": p.description or "",
			"u": p.external_url or "",
			"img": p.cover_image or "",
			"b": _clean_body(p.body),
			"people": _post_people(p.name),
			**_post_byline(p.name),
		})
	return result


@frappe.whitelist(allow_guest=True)
def get_post(slug):
	"""Returns a single post by slug, shaped to match the Post TS interface."""
	name = frappe.db.get_value("DT Post", {"slug": slug, "published": 1}, "name")
	if not name:
		frappe.throw("Post not found", frappe.DoesNotExistError)

	doc = frappe.get_doc("DT Post", name)
	out = {
		"s": doc.slug or "",
		"c": _cat_key(doc.category),
		"k": doc.label or "",
		"f": bool(doc.is_featured),
		"n": doc.title,
		"d": doc.description or "",
		"u": doc.external_url or "",
		"img": doc.cover_image or "",
		"b": _clean_body(doc.body),
	}
	out.update(_post_credits(doc))
	out["people"] = _post_people(name)
	return out


def _member_ref(member_name):
	"""Return {s, n, photo, i} for a DT Team Member document name, or None."""
	if not member_name:
		return None
	row = frappe.db.get_value(
		"DT Team Member", member_name,
		["slug", "full_name", "photo", "initials"], as_dict=True,
	)
	if not row:
		return None
	return {
		"s": row.slug or "",
		"n": row.full_name or "",
		"photo": row.photo or "",
		"i": row.initials or "",
	}


def _post_byline(post_name):
	"""Author + contributors (slug/name/role) for a post's byline."""
	author_name = frappe.db.get_value("DT Post", post_name, "primary_author")
	author = _member_ref(author_name)
	if author:
		author = {"s": author["s"], "n": author["n"]}

	contributors = []
	rows = frappe.get_all(
		"DT Blog Contributor",
		filters={"parent": post_name, "parenttype": "DT Post"},
		fields=["team_member", "person_name", "contribution_type"],
		order_by="idx asc",
	)
	for r in rows:
		ref = _member_ref(r.team_member) if r.team_member else None
		if ref:
			contributors.append({"s": ref["s"], "n": ref["n"], "role": r.contribution_type or ""})
		elif r.person_name:
			# person without a profile — no slug, name only
			contributors.append({"s": "", "n": r.person_name, "role": r.contribution_type or ""})

	return {"author": author, "contributors": contributors}


def _post_people(post_name):
	"""Deduped author + contributors (with photos) for a post, for avatar display."""
	author = frappe.db.get_value("DT Post", post_name, "primary_author")
	rows = frappe.get_all(
		"DT Blog Contributor",
		filters={"parent": post_name, "parenttype": "DT Post"},
		fields=["team_member", "person_name"],
		order_by="idx asc",
	)

	people, seen = [], set()

	# primary author first
	if author and author not in seen:
		seen.add(author)
		ref = _member_ref(author)
		if ref:
			people.append(ref)

	for r in rows:
		if r.team_member:
			if r.team_member in seen:
				continue
			seen.add(r.team_member)
			ref = _member_ref(r.team_member)
			if ref:
				people.append(ref)
		elif r.person_name:
			key = "name:" + r.person_name
			if key in seen:
				continue
			seen.add(key)
			# non-profile person: no slug, no photo, derived initials
			people.append({"s": "", "n": r.person_name, "photo": "", "i": _initials(r.person_name)})

	return people


def _initials(name):
	parts = [w for w in (name or "").split() if w]
	return "".join(w[0] for w in parts[:2]).upper()


def _post_credits(doc):
	"""Extract author / contributors / linked projects from a DT Post document."""
	# author + contributors (incl. free-text people with no profile)
	byline = _post_byline(doc.name)

	projects = []
	for lp in (doc.linked_projects or []):
		if not lp.project:
			continue
		row = frappe.db.get_value("DT Project", lp.project, ["slug", "title"], as_dict=True)
		if row:
			projects.append({"s": row.slug or "", "n": row.title or ""})

	return {"author": byline["author"], "contributors": byline["contributors"], "projects": projects}


@frappe.whitelist(allow_guest=True)
def get_voices():
	"""Returns voices shaped to match the Voice TS interface {n,i,r,q}."""
	voices = frappe.get_all(
		"DT Voice",
		filters={"published": 1},
		fields=["full_name", "initials", "role", "quote"],
		order_by="display_order asc",
	)
	return [{"n": v["full_name"], "i": v["initials"], "r": v["role"] or "", "q": v["quote"]} for v in voices]


@frappe.whitelist(allow_guest=True)
def get_services():
	return frappe.get_all(
		"DT Service Tag",
		filters={"published": 1},
		fields=["label", "dark", "x_pos", "y_pos", "rotate", "delay", "display_order"],
		order_by="display_order asc",
	)


def _project_members(doc):
	members = []
	for m in (doc.members or []):
		ref = _member_ref(m.team_member)
		if ref:
			members.append({**ref, "role": m.member_role or ""})
	return members


def _project_partners(doc):
	return [
		{
			"n": p.name_ or "",
			"url": p.url or "",
			"logo": p.logo or "",
			"type": p.partner_type or "",
		}
		for p in (doc.partners or [])
	]


def _project_card(doc):
	"""Shape a DT Project document into the Project card dict."""
	return {
		"s": doc.slug or "",
		"n": doc.title,
		"sum": doc.summary or "",
		"img": doc.cover_image or "",
		"status": doc.status or "",
		"live": doc.live_url or "",
		"repo": doc.repo_url or "",
		"members": _project_members(doc),
		"tech": [t.strip() for t in (doc.tech_stack or "").splitlines() if t.strip()],
		"partners": _project_partners(doc),
	}


@frappe.whitelist(allow_guest=True)
def get_projects():
	"""Returns published projects as card dicts (with members)."""
	names = frappe.get_all(
		"DT Project",
		filters={"published": 1},
		pluck="name",
		order_by="display_order asc",
	)
	return [_project_card(frappe.get_doc("DT Project", n)) for n in names]


@frappe.whitelist(allow_guest=True)
def get_project(slug):
	"""Returns a single project by slug, with description HTML + members + related posts."""
	name = frappe.db.get_value("DT Project", {"slug": slug, "published": 1}, "name")
	if not name:
		frappe.throw("Project not found", frappe.DoesNotExistError)

	doc = frappe.get_doc("DT Project", name)
	out = _project_card(doc)
	out["description"] = _clean_body(doc.description)
	out["posts"] = _posts_linking_project(name)
	out["sections"] = [
		{"eyebrow": s.eyebrow or "", "heading": s.heading or "", "body": s.body or ""}
		for s in (doc.case_sections or [])
	]
	return out


def _posts_linking_project(project_name):
	"""Published posts that reference the given project in their linked_projects table."""
	post_names = frappe.get_all(
		"DT Blog Project",
		filters={"project": project_name, "parenttype": "DT Post"},
		pluck="parent",
	)
	return _post_cards(post_names)


def _post_cards(post_names):
	"""Shape a list of DT Post names into lightweight card dicts, published only."""
	if not post_names:
		return []
	rows = frappe.get_all(
		"DT Post",
		filters={"name": ["in", list(set(post_names))], "published": 1},
		fields=["title", "slug", "category", "label", "is_featured", "description", "cover_image"],
		order_by="display_order asc",
	)
	return [{
		"s": r.slug or "",
		"n": r.title,
		"d": r.description or "",
		"c": _cat_key(r.category),
		"k": r.label or "",
		"f": bool(r.is_featured),
		"img": r.cover_image or "",
	} for r in rows]


@frappe.whitelist(allow_guest=True)
def get_team_member(slug):
	"""Returns a single team member profile enriched with their posts and projects."""
	name = frappe.db.get_value("DT Team Member", {"slug": slug, "published": 1}, "name")
	if not name:
		frappe.throw("Team member not found", frappe.DoesNotExistError)

	m = frappe.get_doc("DT Team Member", name)
	raw = m.skills or ""
	out = {
		"s": m.slug or "",
		"n": m.full_name,
		"i": m.initials,
		"r": m.role_title,
		"b": m.bio,
		"photo": m.photo or "",
		"t": [s.strip() for s in raw.splitlines() if s.strip()],
		"email": m.email or "",
		"linkedin": m.linkedin or "",
		"twitter": m.twitter or "",
		"github": m.github or "",
		"avatar_index": m.avatar_index or 0,
		"posts": _member_posts(name),
		"projects": _member_projects(name),
	}
	return out


def _member_posts(member_name):
	"""Published posts where the member is primary author or a contributor."""
	as_author = frappe.get_all(
		"DT Post",
		filters={"primary_author": member_name, "published": 1},
		pluck="name",
	)
	as_contrib = frappe.get_all(
		"DT Blog Contributor",
		filters={"team_member": member_name, "parenttype": "DT Post"},
		pluck="parent",
	)
	return _post_cards(as_author + as_contrib)


def _member_projects(member_name):
	"""Published projects where the member appears in the members table."""
	project_names = frappe.get_all(
		"DT Project Member",
		filters={"team_member": member_name, "parenttype": "DT Project"},
		pluck="parent",
	)
	if not project_names:
		return []
	names = frappe.get_all(
		"DT Project",
		filters={"name": ["in", list(set(project_names))], "published": 1},
		pluck="name",
		order_by="display_order asc",
	)
	return [_project_card(frappe.get_doc("DT Project", n)) for n in names]


def _cat_key(category):
	return {
		"Story": "story",
		"Field Notes": "field",
		"Tech": "tech",
	}.get(category, "story")
