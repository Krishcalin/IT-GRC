"""ISO 27001:2022 Annex A controls seed data and seeding functions."""

from __future__ import annotations

ANNEX_A_CONTROLS: list[dict] = [
    # ── A.5 Organizational controls (37) ──────────────────────
    {"clause": "A.5.1", "title": "Policies for information security", "theme": "Organizational",
     "description": "Define and approve information security policies, communicate them to relevant parties, and review them at planned intervals or when significant changes occur."},
    {"clause": "A.5.2", "title": "Information security roles and responsibilities", "theme": "Organizational",
     "description": "Clearly define, allocate, and communicate all information security roles and responsibilities across the organization."},
    {"clause": "A.5.3", "title": "Segregation of duties", "theme": "Organizational",
     "description": "Separate conflicting duties and areas of responsibility to reduce opportunities for unauthorized or unintentional modification or misuse of assets."},
    {"clause": "A.5.4", "title": "Management responsibilities", "theme": "Organizational",
     "description": "Ensure management requires all personnel to apply information security in accordance with established policies and procedures."},
    {"clause": "A.5.5", "title": "Contact with authorities", "theme": "Organizational",
     "description": "Establish and maintain contact with relevant authorities such as law enforcement, regulatory bodies, and supervisory authorities."},
    {"clause": "A.5.6", "title": "Contact with special interest groups", "theme": "Organizational",
     "description": "Establish and maintain contact with special interest groups, security forums, and professional associations to stay current on threats and best practices."},
    {"clause": "A.5.7", "title": "Threat intelligence", "theme": "Organizational",
     "description": "Collect and analyze information about threats to information security to produce actionable threat intelligence for risk-informed decisions."},
    {"clause": "A.5.8", "title": "Information security in project management", "theme": "Organizational",
     "description": "Integrate information security into project management processes regardless of the type of project to ensure risks are identified and addressed."},
    {"clause": "A.5.9", "title": "Inventory of information and other associated assets", "theme": "Organizational",
     "description": "Identify, document, and maintain an inventory of information and associated assets including their owners throughout their lifecycle."},
    {"clause": "A.5.10", "title": "Acceptable use of information and other associated assets", "theme": "Organizational",
     "description": "Define, document, and implement rules for the acceptable use and handling of information and associated assets."},
    {"clause": "A.5.11", "title": "Return of assets", "theme": "Organizational",
     "description": "Ensure personnel and external parties return all organizational assets in their possession upon termination of employment, contract, or agreement."},
    {"clause": "A.5.12", "title": "Classification of information", "theme": "Organizational",
     "description": "Classify information according to the organization's information security needs based on confidentiality, integrity, and availability requirements."},
    {"clause": "A.5.13", "title": "Labelling of information", "theme": "Organizational",
     "description": "Develop and implement procedures for labelling information in accordance with the adopted information classification scheme."},
    {"clause": "A.5.14", "title": "Information transfer", "theme": "Organizational",
     "description": "Establish rules, procedures, and agreements for the secure transfer of information within the organization and with external parties."},
    {"clause": "A.5.15", "title": "Access control", "theme": "Organizational",
     "description": "Define and implement rules to control physical and logical access to information and processing facilities based on business and security requirements."},
    {"clause": "A.5.16", "title": "Identity management", "theme": "Organizational",
     "description": "Manage the full lifecycle of identities including registration, provisioning, maintenance, and deactivation of user and service identities."},
    {"clause": "A.5.17", "title": "Authentication information", "theme": "Organizational",
     "description": "Control the allocation and management of authentication information through a formal process including password policies and multi-factor authentication."},
    {"clause": "A.5.18", "title": "Access rights", "theme": "Organizational",
     "description": "Provision, review, modify, and remove access rights in accordance with the access control policy and on a need-to-know basis."},
    {"clause": "A.5.19", "title": "Information security in supplier relationships", "theme": "Organizational",
     "description": "Define and implement processes to manage information security risks associated with the use of supplier products and services."},
    {"clause": "A.5.20", "title": "Addressing information security within supplier agreements", "theme": "Organizational",
     "description": "Establish and agree relevant information security requirements with each supplier based on the type and criticality of the supplier relationship."},
    {"clause": "A.5.21", "title": "Managing information security in the ICT supply chain", "theme": "Organizational",
     "description": "Define and implement processes to manage information security risks associated with the ICT products and services supply chain."},
    {"clause": "A.5.22", "title": "Monitoring, review and change management of supplier services", "theme": "Organizational",
     "description": "Regularly monitor, review, evaluate, and manage changes in supplier information security practices and service delivery."},
    {"clause": "A.5.23", "title": "Information security for use of cloud services", "theme": "Organizational",
     "description": "Establish processes for acquisition, use, management, and exit from cloud services in accordance with information security requirements."},
    {"clause": "A.5.24", "title": "Information security incident management planning and preparation", "theme": "Organizational",
     "description": "Plan and prepare for information security incident management by defining roles, responsibilities, procedures, and communication channels."},
    {"clause": "A.5.25", "title": "Assessment and decision on information security events", "theme": "Organizational",
     "description": "Assess information security events and decide whether they should be categorized as information security incidents requiring formal response."},
    {"clause": "A.5.26", "title": "Response to information security incidents", "theme": "Organizational",
     "description": "Respond to information security incidents in accordance with documented procedures including containment, eradication, and recovery."},
    {"clause": "A.5.27", "title": "Learning from information security incidents", "theme": "Organizational",
     "description": "Use knowledge gained from information security incidents to strengthen preventive and corrective controls and reduce future risk."},
    {"clause": "A.5.28", "title": "Collection of evidence", "theme": "Organizational",
     "description": "Establish and apply procedures for the identification, collection, acquisition, and preservation of evidence related to information security events."},
    {"clause": "A.5.29", "title": "Information security during disruption", "theme": "Organizational",
     "description": "Plan how to maintain information security at an appropriate level during disruption to normal operations."},
    {"clause": "A.5.30", "title": "ICT readiness for business continuity", "theme": "Organizational",
     "description": "Plan, implement, maintain, and test ICT readiness to ensure business continuity objectives are met during disruptions."},
    {"clause": "A.5.31", "title": "Legal, statutory, regulatory and contractual requirements", "theme": "Organizational",
     "description": "Identify, document, and keep up to date all relevant legal, statutory, regulatory, and contractual requirements related to information security."},
    {"clause": "A.5.32", "title": "Intellectual property rights", "theme": "Organizational",
     "description": "Implement procedures to ensure compliance with legal, regulatory, and contractual requirements related to intellectual property rights and use of proprietary software."},
    {"clause": "A.5.33", "title": "Protection of records", "theme": "Organizational",
     "description": "Protect records from loss, destruction, falsification, unauthorized access, and unauthorized release in accordance with legal and business requirements."},
    {"clause": "A.5.34", "title": "Privacy and protection of personal identifiable information", "theme": "Organizational",
     "description": "Ensure privacy and protection of personally identifiable information (PII) as required by applicable laws, regulations, and contractual obligations."},
    {"clause": "A.5.35", "title": "Independent review of information security", "theme": "Organizational",
     "description": "Independently review the organization's approach to managing information security at planned intervals or when significant changes occur."},
    {"clause": "A.5.36", "title": "Compliance with policies, rules and standards for information security", "theme": "Organizational",
     "description": "Ensure compliance with the organization's information security policies, topic-specific policies, rules, and standards through regular reviews."},
    {"clause": "A.5.37", "title": "Documented operating procedures", "theme": "Organizational",
     "description": "Document operating procedures for information processing facilities and make them available to personnel who need them."},

    # ── A.6 People controls (8) ───────────────────────────────
    {"clause": "A.6.1", "title": "Screening", "theme": "People",
     "description": "Conduct background verification checks on all candidates for employment proportional to the business requirements and classification of information to be accessed."},
    {"clause": "A.6.2", "title": "Terms and conditions of employment", "theme": "People",
     "description": "State contractual agreements with employees and contractors covering their information security responsibilities before granting access to organizational assets."},
    {"clause": "A.6.3", "title": "Information security awareness, education and training", "theme": "People",
     "description": "Ensure all personnel receive appropriate information security awareness education, training, and regular updates relevant to their job function."},
    {"clause": "A.6.4", "title": "Disciplinary process", "theme": "People",
     "description": "Establish and communicate a formal disciplinary process for personnel who have committed an information security policy violation."},
    {"clause": "A.6.5", "title": "Responsibilities after termination or change of employment", "theme": "People",
     "description": "Define and enforce information security responsibilities and duties that remain valid after termination or change of employment."},
    {"clause": "A.6.6", "title": "Confidentiality or non-disclosure agreements", "theme": "People",
     "description": "Identify, document, regularly review, and have personnel and external parties sign confidentiality or non-disclosure agreements reflecting information protection needs."},
    {"clause": "A.6.7", "title": "Remote working", "theme": "People",
     "description": "Implement security measures for remote working to protect information accessed, processed, or stored outside the organization's premises."},
    {"clause": "A.6.8", "title": "Information security event reporting", "theme": "People",
     "description": "Provide a mechanism for personnel to report observed or suspected information security events through appropriate channels in a timely manner."},

    # ── A.7 Physical controls (14) ────────────────────────────
    {"clause": "A.7.1", "title": "Physical security perimeters", "theme": "Physical",
     "description": "Define and use physical security perimeters to protect areas containing information and information processing facilities."},
    {"clause": "A.7.2", "title": "Physical entry", "theme": "Physical",
     "description": "Secure physical areas by appropriate entry controls and access points to ensure only authorized personnel are permitted access."},
    {"clause": "A.7.3", "title": "Securing offices, rooms and facilities", "theme": "Physical",
     "description": "Design and apply physical security for offices, rooms, and facilities proportional to the classification of information they contain."},
    {"clause": "A.7.4", "title": "Physical security monitoring", "theme": "Physical",
     "description": "Continuously monitor premises for unauthorized physical access using appropriate surveillance and detection mechanisms."},
    {"clause": "A.7.5", "title": "Protecting against physical and environmental threats", "theme": "Physical",
     "description": "Design and implement protection against physical and environmental threats such as natural disasters, fire, flood, and malicious attack."},
    {"clause": "A.7.6", "title": "Working in secure areas", "theme": "Physical",
     "description": "Design and implement security measures and guidelines for working in secure areas to prevent unauthorized access or damage."},
    {"clause": "A.7.7", "title": "Clear desk and clear screen", "theme": "Physical",
     "description": "Define and enforce clear desk rules for papers and removable storage media and clear screen rules for information processing facilities."},
    {"clause": "A.7.8", "title": "Equipment siting and protection", "theme": "Physical",
     "description": "Site and protect equipment to reduce risks from physical and environmental threats and opportunities for unauthorized access."},
    {"clause": "A.7.9", "title": "Security of assets off-premises", "theme": "Physical",
     "description": "Apply security measures to off-site assets taking into account the different risks of working outside the organization's premises."},
    {"clause": "A.7.10", "title": "Storage media", "theme": "Physical",
     "description": "Manage storage media through their lifecycle of acquisition, use, transportation, and disposal in accordance with the classification scheme."},
    {"clause": "A.7.11", "title": "Supporting utilities", "theme": "Physical",
     "description": "Protect information processing facilities from power failures and other disruptions caused by failures in supporting utilities such as electricity and telecommunications."},
    {"clause": "A.7.12", "title": "Cabling security", "theme": "Physical",
     "description": "Protect power and telecommunications cabling carrying data from interception, interference, or damage."},
    {"clause": "A.7.13", "title": "Equipment maintenance", "theme": "Physical",
     "description": "Maintain equipment correctly to ensure continued availability, integrity, and confidentiality of information."},
    {"clause": "A.7.14", "title": "Secure disposal or re-use of equipment", "theme": "Physical",
     "description": "Verify that all items of equipment containing storage media have had sensitive data and licensed software removed or securely overwritten prior to disposal or re-use."},

    # ── A.8 Technological controls (34) ───────────────────────
    {"clause": "A.8.1", "title": "User endpoint devices", "theme": "Technological",
     "description": "Protect information stored on, processed by, or accessible via user endpoint devices through policies, configurations, and technical controls."},
    {"clause": "A.8.2", "title": "Privileged access rights", "theme": "Technological",
     "description": "Restrict and manage the allocation and use of privileged access rights using a formal authorization process."},
    {"clause": "A.8.3", "title": "Information access restriction", "theme": "Technological",
     "description": "Restrict access to information and application system functions in accordance with the access control policy."},
    {"clause": "A.8.4", "title": "Access to source code", "theme": "Technological",
     "description": "Manage read and write access to source code, development tools, and software libraries using appropriate controls."},
    {"clause": "A.8.5", "title": "Secure authentication", "theme": "Technological",
     "description": "Implement secure authentication technologies and procedures based on information access restrictions and the access control policy."},
    {"clause": "A.8.6", "title": "Capacity management", "theme": "Technological",
     "description": "Monitor and adjust the use of resources and project future capacity requirements to ensure required system performance."},
    {"clause": "A.8.7", "title": "Protection against malware", "theme": "Technological",
     "description": "Implement and maintain detection, prevention, and recovery controls combined with user awareness to protect against malware."},
    {"clause": "A.8.8", "title": "Management of technical vulnerabilities", "theme": "Technological",
     "description": "Obtain timely information about technical vulnerabilities of systems in use, evaluate exposure, and take appropriate measures to address the associated risk."},
    {"clause": "A.8.9", "title": "Configuration management", "theme": "Technological",
     "description": "Establish, document, implement, monitor, and review security configurations of hardware, software, services, and networks."},
    {"clause": "A.8.10", "title": "Information deletion", "theme": "Technological",
     "description": "Delete information stored in systems, devices, and any other storage media when no longer required in accordance with legal and business requirements."},
    {"clause": "A.8.11", "title": "Data masking", "theme": "Technological",
     "description": "Use data masking in accordance with the access control policy and business requirements, considering applicable legislation."},
    {"clause": "A.8.12", "title": "Data leakage prevention", "theme": "Technological",
     "description": "Apply data leakage prevention measures to systems, networks, and devices that process, store, or transmit sensitive information."},
    {"clause": "A.8.13", "title": "Information backup", "theme": "Technological",
     "description": "Maintain and regularly test backup copies of information, software, and systems in accordance with the agreed backup policy and recovery objectives."},
    {"clause": "A.8.14", "title": "Redundancy of information processing facilities", "theme": "Technological",
     "description": "Implement information processing facilities with sufficient redundancy to meet availability requirements."},
    {"clause": "A.8.15", "title": "Logging", "theme": "Technological",
     "description": "Produce, store, protect, and analyze logs that record activities, exceptions, faults, and other relevant events."},
    {"clause": "A.8.16", "title": "Monitoring activities", "theme": "Technological",
     "description": "Monitor networks, systems, and applications for anomalous behavior and take appropriate actions to evaluate potential information security incidents."},
    {"clause": "A.8.17", "title": "Clock synchronization", "theme": "Technological",
     "description": "Synchronize the clocks of all information processing systems to approved time sources to support accurate logging and forensic analysis."},
    {"clause": "A.8.18", "title": "Use of privileged utility programs", "theme": "Technological",
     "description": "Restrict and tightly control the use of utility programs that might be capable of overriding system and application controls."},
    {"clause": "A.8.19", "title": "Installation of software on operational systems", "theme": "Technological",
     "description": "Implement procedures and measures to securely manage software installation on operational systems."},
    {"clause": "A.8.20", "title": "Networks security", "theme": "Technological",
     "description": "Secure, manage, and control networks to protect information in systems and applications including data in transit."},
    {"clause": "A.8.21", "title": "Security of network services", "theme": "Technological",
     "description": "Identify, implement, and monitor security mechanisms, service levels, and service requirements of network services."},
    {"clause": "A.8.22", "title": "Segregation of networks", "theme": "Technological",
     "description": "Segregate groups of information services, users, and information systems into separate network segments based on trust levels."},
    {"clause": "A.8.23", "title": "Web filtering", "theme": "Technological",
     "description": "Manage access to external websites to reduce exposure to malicious content and block access to unauthorized web resources."},
    {"clause": "A.8.24", "title": "Use of cryptography", "theme": "Technological",
     "description": "Define and implement rules for the effective use of cryptography including key management to protect information confidentiality, authenticity, and integrity."},
    {"clause": "A.8.25", "title": "Secure development life cycle", "theme": "Technological",
     "description": "Establish and apply rules for the secure development of software and systems throughout the development lifecycle."},
    {"clause": "A.8.26", "title": "Application security requirements", "theme": "Technological",
     "description": "Identify, specify, and approve information security requirements when developing or acquiring applications."},
    {"clause": "A.8.27", "title": "Secure system architecture and engineering principles", "theme": "Technological",
     "description": "Establish, document, maintain, and apply principles for engineering secure systems to all information system development activities."},
    {"clause": "A.8.28", "title": "Secure coding", "theme": "Technological",
     "description": "Apply secure coding principles to software development to reduce the number and impact of potential security vulnerabilities."},
    {"clause": "A.8.29", "title": "Security testing in development and acceptance", "theme": "Technological",
     "description": "Define and implement security testing processes in the development lifecycle to validate that security requirements are met."},
    {"clause": "A.8.30", "title": "Outsourced development", "theme": "Technological",
     "description": "Direct, monitor, and review activities related to outsourced system development to ensure security requirements are addressed."},
    {"clause": "A.8.31", "title": "Separation of development, test and production environments", "theme": "Technological",
     "description": "Separate development, testing, and production environments to reduce the risks of unauthorized access or changes to the production environment."},
    {"clause": "A.8.32", "title": "Change management", "theme": "Technological",
     "description": "Control changes to information processing facilities and systems through formal change management procedures to minimize disruption."},
    {"clause": "A.8.33", "title": "Test information", "theme": "Technological",
     "description": "Select, protect, and manage test information appropriately to ensure representative testing while safeguarding sensitive data."},
    {"clause": "A.8.34", "title": "Protection of information systems during audit testing", "theme": "Technological",
     "description": "Plan and agree audit tests and activities involving verification of operational systems to minimize disruptions to business processes."},
]

assert len(ANNEX_A_CONTROLS) == 93, f"Expected 93 controls, got {len(ANNEX_A_CONTROLS)}"


DEFAULT_ROLES: list[dict] = [
    {"name": "CISO", "description": "Chief Information Security Officer — full access", "permissions": ["*"]},
    {"name": "GRC_Manager", "description": "GRC Manager — manage controls, risks, audits, policies", "permissions": ["controls:*", "risks:*", "audits:*", "policies:*", "soa:*", "assets:*", "evidence:*", "users:read"]},
    {"name": "Risk_Owner", "description": "Risk Owner — manage assigned risks, view controls", "permissions": ["risks:own", "controls:read", "soa:read", "assets:read"]},
    {"name": "Control_Owner", "description": "Control Owner — manage assigned controls, view risks", "permissions": ["controls:own", "risks:read", "soa:read", "evidence:create"]},
    {"name": "Auditor", "description": "Auditor — manage audits and findings, read-only elsewhere", "permissions": ["audits:*", "controls:read", "risks:read", "soa:read", "policies:read", "assets:read", "evidence:read"]},
    {"name": "Viewer", "description": "Read-only access to all modules", "permissions": ["*:read"]},
]


async def seed_controls(session) -> int:
    """Insert Annex A controls if the controls table is empty. Returns count inserted."""
    from ..models.control import Control
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(Control))).scalar()
    if count > 0:
        return 0

    for item in ANNEX_A_CONTROLS:
        session.add(Control(**item))
    await session.flush()
    return len(ANNEX_A_CONTROLS)


async def seed_roles(session) -> int:
    """Insert default RBAC roles if empty. Returns count inserted."""
    from ..models.user import Role
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(Role))).scalar()
    if count > 0:
        return 0

    for role_data in DEFAULT_ROLES:
        session.add(Role(**role_data))
    await session.flush()
    return len(DEFAULT_ROLES)
