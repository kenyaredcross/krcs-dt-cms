"""
Seed script — inserts all default content into DT CMS doctypes.
Run: bench --site onerc.localhost execute krcs_dt_cms.dt_cms.seed.run
Idempotent: skips any record that already exists.
"""
import frappe


TEAM = [
    {
        "full_name": "Kelvin Njenga",
        "initials": "KN",
        "role_title": "Senior Digital Transformation Officer",
        "bio": "Digital transformation specialist leading the implementation of digital solutions and data governance at KRCS.",
        "skills": "Digital Transformation Strategy\nDigital Product Management",
        "display_order": 1,
        "avatar_index": 0,
    },
    {
        "full_name": "Mitchell Njeri",
        "initials": "MN",
        "role_title": "Product Manager",
        "bio": "Product Manager leading full product lifecycle and user-centered digital solutions at KRCS.",
        "skills": "Product Management & Product Lifecycle Development\nStakeholder Engagement & Requirements Engineering",
        "display_order": 2,
        "avatar_index": 1,
    },
    {
        "full_name": "Nigel Nasser",
        "initials": "NN",
        "role_title": "Software Developer",
        "bio": "Software developer focused on backend systems, Frappe/ERPNext, and cloud services for humanitarian platforms.",
        "skills": "Backend Development (Python, JavaScript, Java)\nFrappe & ERPNext Development",
        "display_order": 3,
        "avatar_index": 2,
    },
    {
        "full_name": "Lennox Mwita",
        "initials": "LM",
        "role_title": "Software Developer",
        "bio": "Full-stack developer experienced in fintech payments, data engineering, ERPNext, and cloud deployments.",
        "skills": "Full-Stack Development (Golang, Python, TypeScript, React, Django, Flutter)\nPayments & Fintech Integrations (M-Pesa Daraja, PesaLink)",
        "display_order": 4,
        "avatar_index": 3,
    },
]

def _bq(text, author, role):
    return f'<blockquote><p>{text}</p><footer><b>{author}</b> · {role}</footer></blockquote>'


POSTS = [
    {
        "title": "Volunteer and Membership Management System (VMMS)",
        "category": "Tech",
        "label": "FEATURED WORK",
        "description": "A digital system for managing Kenya Red Cross volunteers and members, so branches can mobilise verified responders quickly.",
        "display_order": 1,
        "body": "\n".join([
            "<p>VMMS is one of the featured digital products from the Kenya Red Cross Digital Transformation Department.</p>",
            "<p>It gives volunteers access to accredited training modules and their deployment history from their phones, and helps branches mobilise verified volunteers during emergencies.</p>",
            _bq("With VMMS, our field volunteers access accredited training modules and track deployment history right from their phones, giving us unprecedented volunteer readiness during national emergencies.", "David Kiprop", "Senior Youth & Volunteer Officer, Rift Valley Region"),
            _bq("The Volunteer and Membership Management System (VMMS) completely transformed how our branch deploys responders during flash floods. What used to take days of phone calls and manual rosters now takes minutes to mobilize verified volunteers.", "Hassan Mohamed", "County Operations Coordinator, Tana River Branch"),
        ]),
    },
    {
        "title": "Prequalification Platform",
        "category": "Tech",
        "label": "FEATURED WORK",
        "description": "An online platform where local suppliers submit their compliance documentation for vendor evaluation.",
        "display_order": 2,
        "body": "\n".join([
            "<p>The Prequalification Platform is one of the featured digital products from the Digital Transformation Department.</p>",
            "<p>It digitises the vendor evaluation pipeline, with local suppliers submitting their compliance documentation online.</p>",
            _bq("Using the Prequalification Platform digitised our entire vendor evaluation pipeline. Local suppliers submit their compliance documentation online, cutting processing turnaround times by more than 70%.", "Faith Naisula", "Supply Chain & Procurement Lead, Logistics Unit"),
        ]),
    },
    {
        "title": "Community-Based Surveillance (CBS)",
        "category": "Field Notes",
        "label": "FEATURED WORK",
        "description": "Connects frontline health alerts from local health volunteers directly to rapid response teams.",
        "display_order": 3,
        "body": "\n".join([
            "<p>Community-Based Surveillance (CBS) is one of the featured digital platforms from the Digital Transformation Department.</p>",
            "<p>It links local health volunteers with rapid response teams, so early disease indicators reach them in real time.</p>",
            _bq("Integrating CBS with local health volunteers has fundamentally reduced our response latency during disease outbreaks, protecting thousands of families with timely health interventions.", "Grace Wambui", "Community Health Coordinator, Ministry of Health Partner Unit"),
            _bq("The Community-Based Surveillance (CBS) platform connects frontline health alerts directly to our rapid response teams. We receive early disease indicators in real-time before outbreaks escalate in remote pastoralist communities.", "Dr. Maria Santos", "Surveillance & Health Lead, IFRC Health & Care Team"),
        ]),
    },
    {
        "title": "Hazina Early Warning Platform",
        "category": "Field Notes",
        "label": "KEY INITIATIVE",
        "description": "One of the key initiatives deployed in Kenya, supporting early warning and anticipatory action.",
        "display_order": 4,
        "body": "\n".join([
            "<p>The Hazina Early Warning Platform is listed among the key initiatives deployed in Kenya.</p>",
            "<p>Early warnings and pre-agreed action protocols let county teams act before climate shocks strike.</p>",
            _bq("The Anticipatory Action platform gives us early forecast triggers before climate shocks strike. Receiving early warnings and pre-agreed action protocols allows county teams to protect lives and livestock ahead of extreme weather.", "Dr. James Omondi", "Climate & Preparedness Officer, Disaster Risk Management Unit"),
        ]),
    },
    {
        "title": "BomaCare Cash & Voucher Assistance",
        "category": "Story",
        "label": "KEY INITIATIVE",
        "description": "A key initiative for cash and voucher assistance, deployed across Kenya.",
        "display_order": 5,
        "body": "\n".join([
            "<p>BomaCare Cash &amp; Voucher Assistance is listed among the key initiatives deployed in Kenya.</p>",
            "<p>Cash assistance lets emergency units support families early, before disasters displace them.</p>",
            _bq("Deploying the Anticipatory Action framework helped our emergency units disburse emergency cash support before severe flooding displaced families in the Tana Delta.", "Zainab Hussein", "Field Cash Assistance Officer, Humanitarian Cash Assistance Unit"),
        ]),
    },
]

VOICES = [
    {
        "full_name": "Zainab Hussein",
        "initials": "ZH",
        "role": "Field Cash Assistance Officer · Humanitarian Cash Assistance Unit",
        "quote": "Deploying the Anticipatory Action framework helped our emergency units disburse emergency cash support before severe flooding displaced families in the Tana Delta.",
        "display_order": 1,
    },
    {
        "full_name": "Peter Ochieng",
        "initials": "PO",
        "role": "Corporate Relations Manager · Digital Philanthropy Group",
        "quote": "The Donations Platform's instant digital receipting and campaign analytics have built high trust with corporate partners and individual donors across Kenya.",
        "display_order": 2,
    },
    {
        "full_name": "Grace Wambui",
        "initials": "GW",
        "role": "Community Health Coordinator · Ministry of Health Partner Unit",
        "quote": "Integrating CBS with local health volunteers has fundamentally reduced our response latency during disease outbreaks, protecting thousands of families with timely health interventions.",
        "display_order": 3,
    },
    {
        "full_name": "David Kiprop",
        "initials": "DK",
        "role": "Senior Youth & Volunteer Officer · Rift Valley Region",
        "quote": "With VMMS, our field volunteers access accredited training modules and track deployment history right from their phones, giving us unprecedented volunteer readiness during national emergencies.",
        "display_order": 4,
    },
]

SERVICES = [
    {"label": "Digital Health", "dark": 0, "x_pos": "22%", "y_pos": "2%", "rotate": "-6deg", "delay": "0s", "display_order": 1},
    {"label": "Field Tech", "dark": 0, "x_pos": "10%", "y_pos": "38%", "rotate": "4deg", "delay": "0.15s", "display_order": 2},
    {"label": "UX Design", "dark": 0, "x_pos": "70%", "y_pos": "35%", "rotate": "-3deg", "delay": "0.2s", "display_order": 3},
    {"label": "Systems Integration", "dark": 1, "x_pos": "30%", "y_pos": "68%", "rotate": "5deg", "delay": "0.05s", "display_order": 4},
    {"label": "Capacity Building", "dark": 0, "x_pos": "62%", "y_pos": "72%", "rotate": "-4deg", "delay": "0.25s", "display_order": 5},
]

SITE_SETTINGS = {
    "hero_word_a": "PAPER",
    "hero_word_b": "PIXELS",
    "hero_body": "Kenya Red Cross Society's Digital Transformation Department replaces paper-based processes with connected, data-driven systems — so aid reaches people faster, smarter, and more accountably.",
    "marquee_items": "DIGITAL HEALTH, DATA SYSTEMS, FIELD TECHNOLOGY, UX & DESIGN, CAPACITY BUILDING, SYSTEMS INTEGRATION",
    "stat_counties": 47,
    "stat_lives": "100k+",
    "stat_projects": "300+",
    "stat_awards": "16+",
    "stat_team": "34+",
    "cta_headline": "Humanity,",
    "cta_body": "Partner with the Digital Transformation Department to bring faster, smarter help to every community we serve.",
    "partner_email": "developer@redcross.or.ke",
}


def run():
    frappe.set_user("Administrator")

    _seed_site_settings()
    _seed_team()
    _seed_posts()
    _seed_voices()
    _seed_services()

    frappe.db.commit()
    print("Seed complete.")


def _seed_site_settings():
    doc = frappe.new_doc("DT Site Settings")
    for k, v in SITE_SETTINGS.items():
        doc.set(k, v)
    doc.flags.ignore_permissions = True
    doc.flags.ignore_mandatory = True
    try:
        doc.save()
    except Exception:
        frappe.db.sql(
            "DELETE FROM `tabSingles` WHERE doctype='DT Site Settings'"
        )
        doc.save()
    print("  site settings saved")


def _seed_team():
    for m in TEAM:
        if frappe.db.exists("DT Team Member", m["full_name"]):
            print(f"  team: {m['full_name']} already exists, skipping")
            continue
        doc = frappe.get_doc({"doctype": "DT Team Member", **m})
        doc.insert(ignore_permissions=True)
        print(f"  team: {m['full_name']} inserted")


def _seed_posts():
    for p in POSTS:
        title = p["title"]
        if frappe.db.exists("DT Post", {"title": title}):
            print(f"  post: {title[:50]} already exists, skipping")
            continue
        doc = frappe.get_doc({"doctype": "DT Post", **p})
        doc.insert(ignore_permissions=True)
        print(f"  post: {title[:50]} inserted")


def _seed_voices():
    for v in VOICES:
        if frappe.db.exists("DT Voice", v["full_name"]):
            print(f"  voice: {v['full_name']} already exists, skipping")
            continue
        doc = frappe.get_doc({"doctype": "DT Voice", **v})
        doc.insert(ignore_permissions=True)
        print(f"  voice: {v['full_name']} inserted")


def _seed_services():
    for s in SERVICES:
        if frappe.db.exists("DT Service Tag", s["label"]):
            print(f"  service: {s['label']} already exists, skipping")
            continue
        doc = frappe.get_doc({"doctype": "DT Service Tag", **s})
        doc.insert(ignore_permissions=True)
        print(f"  service: {s['label']} inserted")
