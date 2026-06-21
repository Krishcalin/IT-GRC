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


# ─────────────────────────────────────────────────────────────────────────────
#  ISO/IEC 27019:2024 — energy-utility-industry sector controls
#
#  ISO/IEC 27019:2024 is a sector-specific extension of ISO/IEC 27002:2022 for
#  process control systems (SCADA/ICS) in the energy utility industry. It reuses
#  the ISO 27001:2022 Annex A controls above (adding energy-specific guidance to
#  many of them) and introduces NEW sector-specific controls, prefixed "ENR".
#  Those 12 ENR controls are the only controls 27019 adds beyond Annex A, so they
#  are loaded here as a distinct framework ("ISO 27019:2024") that energy-sector
#  organizations can adopt in addition to the base Annex A set.
#
#  Descriptions and guidance below are paraphrased for the application; they are
#  not a reproduction of the copyrighted standard. Refer to ISO/IEC 27019:2024
#  for the authoritative wording. Clause ids use an "ENR." prefix to keep them
#  distinct from the "A." Annex A clauses.
# ─────────────────────────────────────────────────────────────────────────────
ISO27019_CONTROLS: list[dict] = [
    # ── Organizational ────────────────────────────────────────
    {"clause": "ENR.5.38", "title": "Identification of risks related to external business partners",
     "theme": "Organizational", "framework": "ISO 27019:2024",
     "description": "Identify and assess the information security risks that arise when external business partners — vendors, system integrators, interconnected operators — access process control systems or critical-asset information, and implement appropriate controls before access is granted.",
     "implementation_guidance": "Energy process-control environments depend heavily on vendors and integrators for maintenance and on interconnection with other operators. Assess the exposure of the physical process being controlled, require partners to maintain a comparable security level (e.g. through contractual obligations), and tightly control remote-access pathways to critical assets."},
    {"clause": "ENR.5.39", "title": "Addressing security when dealing with customers",
     "theme": "Organizational", "framework": "ISO 27019:2024",
     "description": "Address all identified security requirements before giving customers access to the organization's information or assets, accounting for the complex ownership and demarcation of responsibilities typical of energy supply relationships.",
     "implementation_guidance": "Define responsibility boundaries among asset owners, system operators, service providers and customers. Where equipment is sited on customer or other-utility premises, or where process control systems are interconnected, apply the corresponding physical-protection and interconnection controls (see ENR.7.15–ENR.7.18)."},

    # ── Physical ──────────────────────────────────────────────
    {"clause": "ENR.7.15", "title": "Securing control centres",
     "theme": "Physical", "framework": "ISO 27019:2024",
     "description": "Design, develop and apply measures to physically secure control centres — where control-system servers, HMIs and supporting systems are housed — against unauthorized access and physical and environmental threats.",
     "implementation_guidance": "Consider siting on stable ground away from hazardous-material storage and strong electromagnetic fields; disaster- and fire-resistant construction; adequate structural load capacity; automatic fire detection and suppression; and strict segregation from other ICT where control systems share an externally operated data centre."},
    {"clause": "ENR.7.16", "title": "Securing equipment rooms",
     "theme": "Physical", "framework": "ISO 27019:2024",
     "description": "Design, develop and implement measures to physically secure the rooms in which energy-utility control-system equipment is located.",
     "implementation_guidance": "Locate equipment rooms to minimize exposure to extreme environmental conditions, flooding and electromagnetic interference; keep their purpose unobtrusive; restrict and detect unauthorized access; provide fire detection/suppression, anti-static measures and resilient air-conditioning; and place components with heightened sensitivity in dedicated, hardened rooms."},
    {"clause": "ENR.7.17", "title": "Securing peripheral sites",
     "theme": "Physical", "framework": "ISO 27019:2024",
     "description": "Apply physical security controls to peripheral, frequently unattended sites housing control-system equipment, or apply compensating countermeasures where an adequate level of physical protection is not attainable.",
     "implementation_guidance": "For decentralized substations and distributed-generation sites, consider disaster-proofing, automatic fire control, remote monitoring (component malfunction, power loss, fire, humidity/temperature), secure perimeters and central-monitored alarms. Where protection is limited, weigh asset criticality and existing redundancy/fall-back when selecting countermeasures."},
    {"clause": "ENR.7.18", "title": "Interconnected control and communication systems",
     "theme": "Physical", "framework": "ISO 27019:2024",
     "description": "Where control systems and related communication links are interconnected with external parties, clearly define responsibility boundaries and interfaces so each organization can be disconnected and isolated within an appropriate period to contain identified risks.",
     "implementation_guidance": "Monitor interconnection status; provide a means to isolate and later reconnect links; contractually allow suspension where severe interference affects own services; predefine suspension criteria, assess the impact of suspension and prepare fall-back measures. Applies to both routed network-based and serial communication."},

    # ── Technological ─────────────────────────────────────────
    {"clause": "ENR.8.35", "title": "Treatment of legacy systems",
     "theme": "Technological", "framework": "ISO 27019:2024",
     "description": "Identify legacy process-control technologies, systems and components together with their potential security vulnerabilities, and implement appropriate controls through the risk-treatment process where standard controls cannot be applied.",
     "implementation_guidance": "Many industrial control systems lack basic security features. Where standard controls are infeasible, apply compensating measures: strict network segregation; avoidance of remote access (or, where necessary, isolation via hardened, regularly patched secure proxies at defined monitored interconnection points); and strict access control at network, system and application levels. Secure the equipment used to maintain and configure legacy systems."},
    {"clause": "ENR.8.36", "title": "Integrity and availability of safety functions",
     "theme": "Technological", "framework": "ISO 27019:2024",
     "description": "Protect the integrity and availability of the information, assets, systems, components and functions required to ensure safety functions, in accordance with sector-specific standards and legal requirements.",
     "implementation_guidance": "Use dedicated, isolated communication systems for safety-related data; keep safety functions independent of process-control and automation systems where possible; avoid changing critical safety systems and their safety-related configuration via remote access; and log changes to safety-system configuration."},
    {"clause": "ENR.8.37", "title": "Securing process control data communication",
     "theme": "Technological", "framework": "ISO 27019:2024",
     "description": "Design, develop and implement measures to meet the confidentiality, integrity and availability requirements (identified during risk assessment) of internal and external process-control data communication.",
     "implementation_guidance": "Many process-control protocols (e.g. IEC 60870-5/-6, DNP3, IEC 61850, Modbus) include no built-in security or make it optional. Address the residual risk by enabling supported security features (e.g. per IEC 62351) or adding cryptographic protection — encryption, integrity checks and authentication of communication partners — on the lower communication layers. Applies to networked and serial communication."},
    {"clause": "ENR.8.38", "title": "Logical connection of external process control systems",
     "theme": "Technological", "framework": "ISO 27019:2024",
     "description": "Before logically connecting process-control systems and communication links with external parties, evaluate the resulting risk and ensure only authorized communications and information flows — including control-system commands and messages — can be exchanged over the link.",
     "implementation_guidance": "Connect only where operationally necessary, at defined, securely operated and monitored connection points. Define and approve the type and extent of permitted communications, and use filtering devices such as gateways, proxies or application-level firewalls to allow only the authorized flows."},
    {"clause": "ENR.8.39", "title": "Least functionality",
     "theme": "Technological", "framework": "ISO 27019:2024",
     "description": "Design, configure, operate and maintain process-control systems to provide only the functions required for operation.",
     "implementation_guidance": "Document, then disable and explicitly prohibit unnecessary functions, software, ports, protocols and services; document and explicitly allow the functions, software, ports, protocols and services that are required."},
    {"clause": "ENR.8.40", "title": "Emergency communication",
     "theme": "Technological", "framework": "ISO 27019:2024",
     "description": "During major disturbances, natural disasters, accidents or other emergencies (or where there is a risk of them), ensure that essential communication links are maintained with internal and other-utility emergency staff, essential control systems and the external emergency organizations needed to protect against, handle or recover from such incidents.",
     "implementation_guidance": "Provide for voice and data links with operating and crisis-management staff, power stations and producers, transmission/distribution system operators, meteorological and disaster-relief organizations, authorities and telecommunication providers. Recognize that communication links needed for system restoration can themselves depend on the electricity supply, and plan redundancy accordingly."},
]

assert len(ISO27019_CONTROLS) == 12, f"Expected 12 ISO 27019:2024 controls, got {len(ISO27019_CONTROLS)}"


# ─────────────────────────────────────────────────────────────────────────────
#  ISO/IEC 27001:2022 mandatory management-system requirements (Clauses 4–10)
#
#  These are the normative ISMS "shall" requirements an organization is audited
#  against — distinct from the Annex A controls above. Per Clause 1 (Scope),
#  excluding any of Clauses 4–10 is NOT acceptable when claiming conformity, so
#  these requirements have no "Not Applicable" status.
#
#  Requirement text below is paraphrased for the application; it is not a
#  reproduction of the copyrighted standard. Refer to ISO/IEC 27001:2022 for the
#  authoritative normative wording.
# ─────────────────────────────────────────────────────────────────────────────
ISMS_CLAUSES: list[dict] = [
    # ── 4 Context of the organization ─────────────────────────
    {"clause": "4.1", "clause_number": 4, "section": "Context of the organization",
     "title": "Understanding the organization and its context",
     "requirement": "Determine the external and internal issues relevant to the organization's purpose that affect its ability to achieve the intended outcomes of the ISMS.",
     "documented_info": None},
    {"clause": "4.2", "clause_number": 4, "section": "Context of the organization",
     "title": "Understanding the needs and expectations of interested parties",
     "requirement": "Identify the interested parties relevant to the ISMS, their relevant requirements (including legal, regulatory, and contractual obligations), and which of those requirements will be addressed through the ISMS.",
     "documented_info": None},
    {"clause": "4.3", "clause_number": 4, "section": "Context of the organization",
     "title": "Determining the scope of the ISMS",
     "requirement": "Determine the boundaries and applicability of the ISMS, taking account of internal/external issues, interested-party requirements, and interfaces and dependencies with other organizations.",
     "documented_info": "ISMS scope (maintained as documented information)."},
    {"clause": "4.4", "clause_number": 4, "section": "Context of the organization",
     "title": "Information security management system",
     "requirement": "Establish, implement, maintain, and continually improve the ISMS, including the processes needed and their interactions, in accordance with the standard.",
     "documented_info": None},

    # ── 5 Leadership ──────────────────────────────────────────
    {"clause": "5.1", "clause_number": 5, "section": "Leadership",
     "title": "Leadership and commitment",
     "requirement": "Top management demonstrates leadership and commitment by aligning the policy and objectives with strategy, integrating ISMS requirements into business processes, providing resources, communicating the importance of information security, ensuring intended outcomes, directing and supporting personnel, promoting continual improvement, and supporting other management roles.",
     "documented_info": None},
    {"clause": "5.2", "clause_number": 5, "section": "Leadership",
     "title": "Policy",
     "requirement": "Top management establishes an information security policy that is appropriate to the organization, provides a framework for objectives, and commits to satisfying applicable requirements and to continual improvement; the policy is documented, communicated internally, and available to interested parties as appropriate.",
     "documented_info": "Information security policy."},
    {"clause": "5.3", "clause_number": 5, "section": "Leadership",
     "title": "Organizational roles, responsibilities and authorities",
     "requirement": "Assign and communicate responsibilities and authorities for ensuring the ISMS conforms to the standard and for reporting on ISMS performance to top management.",
     "documented_info": None},

    # ── 6 Planning ────────────────────────────────────────────
    {"clause": "6.1.1", "clause_number": 6, "section": "Planning",
     "title": "Actions to address risks and opportunities — General",
     "requirement": "Considering the issues (4.1) and requirements (4.2), determine the risks and opportunities to be addressed to ensure the ISMS achieves its outcomes, to prevent or reduce undesired effects, and to achieve continual improvement; plan the actions and how to integrate, implement, and evaluate their effectiveness.",
     "documented_info": None},
    {"clause": "6.1.2", "clause_number": 6, "section": "Planning",
     "title": "Information security risk assessment",
     "requirement": "Define and apply a risk assessment process with risk-acceptance and assessment criteria that yields consistent, valid, comparable results; identify risks to confidentiality, integrity, and availability and their owners; analyze consequences and likelihood to determine risk levels; and evaluate and prioritize risks for treatment.",
     "documented_info": "Information security risk assessment process."},
    {"clause": "6.1.3", "clause_number": 6, "section": "Planning",
     "title": "Information security risk treatment",
     "requirement": "Define and apply a risk treatment process: select treatment options, determine the necessary controls, compare them against Annex A to verify none are omitted, produce a Statement of Applicability (with justifications and implementation status), formulate a risk treatment plan, and obtain risk-owner approval and acceptance of residual risk.",
     "documented_info": "Statement of Applicability; risk treatment plan; risk treatment process."},
    {"clause": "6.2", "clause_number": 6, "section": "Planning",
     "title": "Information security objectives and planning to achieve them",
     "requirement": "Establish measurable, communicated information security objectives consistent with the policy, monitored and updated as appropriate; plan what will be done, the resources, who is responsible, when it will be completed, and how results are evaluated.",
     "documented_info": "Information security objectives."},
    {"clause": "6.3", "clause_number": 6, "section": "Planning",
     "title": "Planning of changes",
     "requirement": "When the organization determines a need for changes to the ISMS, carry out those changes in a planned manner.",
     "documented_info": None},

    # ── 7 Support ─────────────────────────────────────────────
    {"clause": "7.1", "clause_number": 7, "section": "Support",
     "title": "Resources",
     "requirement": "Determine and provide the resources needed to establish, implement, maintain, and continually improve the ISMS.",
     "documented_info": None},
    {"clause": "7.2", "clause_number": 7, "section": "Support",
     "title": "Competence",
     "requirement": "Determine the necessary competence of persons whose work affects information security performance, ensure their competence through education, training, or experience, take action to close gaps and evaluate its effectiveness.",
     "documented_info": "Evidence of competence."},
    {"clause": "7.3", "clause_number": 7, "section": "Support",
     "title": "Awareness",
     "requirement": "Ensure persons doing work under the organization's control are aware of the information security policy, their contribution to ISMS effectiveness, and the implications of not conforming to ISMS requirements.",
     "documented_info": None},
    {"clause": "7.4", "clause_number": 7, "section": "Support",
     "title": "Communication",
     "requirement": "Determine the internal and external communications relevant to the ISMS — on what, when, with whom, and how to communicate.",
     "documented_info": None},
    {"clause": "7.5.1", "clause_number": 7, "section": "Support",
     "title": "Documented information — General",
     "requirement": "Include in the ISMS the documented information required by the standard and that determined by the organization to be necessary for ISMS effectiveness.",
     "documented_info": "Documented information required by the standard and by the organization."},
    {"clause": "7.5.2", "clause_number": 7, "section": "Support",
     "title": "Creating and updating",
     "requirement": "When creating and updating documented information, ensure appropriate identification and description, format and media, and review and approval for suitability and adequacy.",
     "documented_info": None},
    {"clause": "7.5.3", "clause_number": 7, "section": "Support",
     "title": "Control of documented information",
     "requirement": "Control documented information so it is available and adequately protected; address distribution, access, retrieval, storage, version control, retention and disposition, and control of documents of external origin.",
     "documented_info": None},

    # ── 8 Operation ───────────────────────────────────────────
    {"clause": "8.1", "clause_number": 8, "section": "Operation",
     "title": "Operational planning and control",
     "requirement": "Plan, implement, and control the processes needed to meet requirements and the Clause 6 actions by establishing process criteria and controlling the processes accordingly; control planned changes, review unintended changes, and ensure externally provided processes are controlled.",
     "documented_info": "Evidence that processes have been carried out as planned."},
    {"clause": "8.2", "clause_number": 8, "section": "Operation",
     "title": "Information security risk assessment",
     "requirement": "Perform information security risk assessments at planned intervals or when significant changes are proposed or occur, applying the criteria established in 6.1.2.",
     "documented_info": "Results of the information security risk assessments."},
    {"clause": "8.3", "clause_number": 8, "section": "Operation",
     "title": "Information security risk treatment",
     "requirement": "Implement the information security risk treatment plan.",
     "documented_info": "Results of the information security risk treatment."},

    # ── 9 Performance evaluation ──────────────────────────────
    {"clause": "9.1", "clause_number": 9, "section": "Performance evaluation",
     "title": "Monitoring, measurement, analysis and evaluation",
     "requirement": "Determine what to monitor and measure, the methods, and when and by whom monitoring/measurement and analysis/evaluation are performed; evaluate information security performance and the effectiveness of the ISMS.",
     "documented_info": "Evidence of the monitoring and measurement results."},
    {"clause": "9.2.1", "clause_number": 9, "section": "Performance evaluation",
     "title": "Internal audit — General",
     "requirement": "Conduct internal audits at planned intervals to determine whether the ISMS conforms to the organization's own requirements and to the standard, and whether it is effectively implemented and maintained.",
     "documented_info": None},
    {"clause": "9.2.2", "clause_number": 9, "section": "Performance evaluation",
     "title": "Internal audit programme",
     "requirement": "Plan, establish, implement, and maintain audit programme(s) covering frequency, methods, responsibilities, planning, and reporting; define audit criteria and scope, select objective and impartial auditors, and report results to relevant management.",
     "documented_info": "Evidence of the audit programme(s) and audit results."},
    {"clause": "9.3.1", "clause_number": 9, "section": "Performance evaluation",
     "title": "Management review — General",
     "requirement": "Top management reviews the ISMS at planned intervals to ensure its continuing suitability, adequacy, and effectiveness.",
     "documented_info": None},
    {"clause": "9.3.2", "clause_number": 9, "section": "Performance evaluation",
     "title": "Management review inputs",
     "requirement": "The management review considers the status of prior actions, changes in internal/external issues and interested-party needs, performance feedback (nonconformities and corrective actions, monitoring and measurement results, audit results, fulfilment of objectives), feedback from interested parties, risk assessment results and risk-treatment-plan status, and opportunities for continual improvement.",
     "documented_info": None},
    {"clause": "9.3.3", "clause_number": 9, "section": "Performance evaluation",
     "title": "Management review results",
     "requirement": "The results of the management review include decisions on continual improvement opportunities and any needs for changes to the ISMS.",
     "documented_info": "Evidence of the results of management reviews."},

    # ── 10 Improvement ────────────────────────────────────────
    {"clause": "10.1", "clause_number": 10, "section": "Improvement",
     "title": "Continual improvement",
     "requirement": "Continually improve the suitability, adequacy, and effectiveness of the ISMS.",
     "documented_info": None},
    {"clause": "10.2", "clause_number": 10, "section": "Improvement",
     "title": "Nonconformity and corrective action",
     "requirement": "When a nonconformity occurs, react to it and correct it, deal with the consequences, evaluate the need to eliminate its causes, implement any action needed, review the effectiveness of corrective action, and make changes to the ISMS if necessary; corrective actions are appropriate to the effects encountered.",
     "documented_info": "Evidence of the nature of nonconformities, actions taken, and results of corrective action."},
]

assert len(ISMS_CLAUSES) == 30, f"Expected 30 ISMS clause requirements, got {len(ISMS_CLAUSES)}"


# ─────────────────────────────────────────────────────────────────────────────
#  Mandatory documented information (Clause 7.5)
#
#  The documents and records an ISO/IEC 27001:2022 ISMS must maintain, drawn from
#  the "Documentation requirements" of Clauses 4–10. Pre-loaded as a checklist so
#  an organization can track each one's owner, version, approval, and review.
# ─────────────────────────────────────────────────────────────────────────────
MANDATORY_DOCUMENTS: list[dict] = [
    {"title": "ISMS Scope", "doc_type": "Statement", "clause_ref": "4.3",
     "description": "Boundaries and applicability of the ISMS — which assets, processes, units, and locations are in or out of scope."},
    {"title": "Register of Interested Parties", "doc_type": "Register", "clause_ref": "4.2",
     "description": "Interested parties relevant to the ISMS, their relevant requirements, and which are addressed by the ISMS."},
    {"title": "Register of Legal, Regulatory and Contractual Requirements", "doc_type": "Register", "clause_ref": "A.5.31",
     "description": "Applicable legal, statutory, regulatory, and contractual information security requirements, kept up to date."},
    {"title": "Information Security Policy", "doc_type": "Policy", "clause_ref": "5.2",
     "description": "Top-management information security policy, including the framework for objectives and commitments to satisfy requirements and continually improve."},
    {"title": "Information Security Risk Assessment Process", "doc_type": "Process", "clause_ref": "6.1.2",
     "description": "Defined process with risk-acceptance and assessment criteria producing consistent, valid, comparable results."},
    {"title": "Information Security Risk Treatment Process", "doc_type": "Process", "clause_ref": "6.1.3",
     "description": "Defined process for selecting treatment options and determining the necessary controls."},
    {"title": "Statement of Applicability (SoA)", "doc_type": "Statement", "clause_ref": "6.1.3",
     "description": "Necessary controls with justification for inclusion, implementation status, and justification for any Annex A exclusions."},
    {"title": "Information Security Risk Treatment Plan", "doc_type": "Plan", "clause_ref": "6.1.3",
     "description": "Risk treatment actions, owners, and risk-owner approval plus acceptance of residual risk."},
    {"title": "Information Security Objectives", "doc_type": "Register", "clause_ref": "6.2",
     "description": "Measurable information security objectives, plans to achieve them, and how results are evaluated."},
    {"title": "Evidence of Competence", "doc_type": "Record", "clause_ref": "7.2",
     "description": "Records demonstrating the competence of persons whose work affects information security performance."},
    {"title": "Operational Planning & Control Evidence", "doc_type": "Record", "clause_ref": "8.1",
     "description": "Evidence giving confidence that ISMS processes have been carried out as planned."},
    {"title": "Risk Assessment Results", "doc_type": "Record", "clause_ref": "8.2",
     "description": "Documented results of the information security risk assessments performed at planned intervals or on significant change."},
    {"title": "Risk Treatment Results", "doc_type": "Record", "clause_ref": "8.3",
     "description": "Documented results of implementing the information security risk treatment plan."},
    {"title": "Monitoring & Measurement Results", "doc_type": "Record", "clause_ref": "9.1",
     "description": "Evidence of monitoring/measurement results used to evaluate information security performance and ISMS effectiveness."},
    {"title": "Internal Audit Programme & Results", "doc_type": "Record", "clause_ref": "9.2",
     "description": "Evidence of the internal audit programme(s) and the results of the audits performed."},
    {"title": "Management Review Results", "doc_type": "Record", "clause_ref": "9.3",
     "description": "Documented results of top-management reviews, including decisions on improvement and ISMS changes."},
    {"title": "Nonconformity & Corrective Action Records", "doc_type": "Record", "clause_ref": "10.2",
     "description": "Records of the nature of nonconformities, actions taken, and the results of corrective action."},
]

assert len(MANDATORY_DOCUMENTS) == 17, f"Expected 17 mandatory documents, got {len(MANDATORY_DOCUMENTS)}"


# Representative interested parties (Clause 4.2) — generic starting set; tailor per organization.
SAMPLE_INTERESTED_PARTIES: list[dict] = [
    {"name": "Customers", "party_type": "External", "category": "Customer", "addressed_in_isms": True,
     "requirements": "Protection of their data, contractual security obligations, and timely breach notification."},
    {"name": "Regulatory Authorities", "party_type": "External", "category": "Regulator", "addressed_in_isms": True,
     "requirements": "Compliance with applicable laws and regulations (e.g. data protection, sector-specific rules)."},
    {"name": "Employees", "party_type": "Internal", "category": "Employee", "addressed_in_isms": True,
     "requirements": "Clear security policies, awareness and training, and workable, non-disruptive processes."},
    {"name": "Suppliers & Service Providers", "party_type": "External", "category": "Supplier", "addressed_in_isms": True,
     "requirements": "Agreed information security requirements in contracts, right-to-audit, and incident reporting channels."},
    {"name": "Top Management & Owners", "party_type": "Internal", "category": "Owner", "addressed_in_isms": True,
     "requirements": "Protection of business value, risk kept within appetite, and effective, efficient use of resources."},
]


# Sample information security objectives (Clause 6.2) — tailor per organization.
SAMPLE_OBJECTIVES: list[dict] = [
    {"title": "Reduce workforce phishing susceptibility", "measure": "Phishing simulation click-through rate",
     "target_value": "<= 5%", "unit": "%", "status": "On Track",
     "description": "Lower the proportion of staff who click simulated phishing links through targeted awareness campaigns."},
    {"title": "Remediate critical vulnerabilities within SLA", "measure": "% of critical vulnerabilities remediated within 14 days",
     "target_value": ">= 95%", "unit": "%", "status": "At Risk",
     "description": "Ensure critical technical vulnerabilities are remediated within the defined service level."},
    {"title": "Maintain security awareness coverage", "measure": "% of in-scope staff completing annual training",
     "target_value": ">= 98%", "unit": "%", "status": "On Track",
     "description": "Sustain high completion of mandatory annual information security awareness training."},
]

# Sample KPI/KRI/KCI metrics (Clause 9.1). objective_ref links to a seeded objective.
SAMPLE_METRICS: list[dict] = [
    {"name": "Phishing simulation click-through rate", "metric_type": "KRI", "objective_ref": "OBJ-001",
     "target_value": 5, "current_value": 8, "unit": "%", "direction": "lower_is_better", "frequency": "Quarterly",
     "description": "Percentage of recipients clicking a simulated phishing link during the campaign."},
    {"name": "Critical vulnerabilities remediated within SLA", "metric_type": "KPI", "objective_ref": "OBJ-002",
     "target_value": 95, "current_value": 91, "unit": "%", "direction": "higher_is_better", "frequency": "Monthly",
     "description": "Percentage of critical vulnerabilities closed within the 14-day SLA window."},
    {"name": "Critical vulnerabilities past SLA (open)", "metric_type": "KRI", "objective_ref": "OBJ-002",
     "target_value": 0, "current_value": 4, "unit": "count", "direction": "lower_is_better", "frequency": "Monthly",
     "description": "Number of critical vulnerabilities still open beyond the remediation SLA."},
    {"name": "Annual awareness training completion", "metric_type": "KCI", "objective_ref": "OBJ-003",
     "target_value": 98, "current_value": 99, "unit": "%", "direction": "higher_is_better", "frequency": "Annual",
     "description": "Percentage of in-scope personnel who completed the mandatory awareness training."},
    {"name": "Mean time to detect (MTTD)", "metric_type": "KPI", "objective_ref": None,
     "target_value": 60, "current_value": 45, "unit": "minutes", "direction": "lower_is_better", "frequency": "Continuous",
     "description": "Average time from a security event occurring to its detection."},
]


# Sample suppliers / third parties (Clauses 5.19–5.23) — generic; tailor per organization.
SAMPLE_SUPPLIERS: list[dict] = [
    {"name": "Primary Cloud Platform (IaaS)", "category": "Cloud Service", "criticality": "Critical",
     "data_classification": "Confidential", "status": "Active", "is_requirements_agreed": True,
     "right_to_audit": False, "processes_pii": True, "certifications": "ISO 27001, SOC 2 Type II",
     "service_description": "Hosts production workloads and customer data.",
     "notes": "Right-to-audit not granted in standard cloud terms — rely on SOC 2 Type II report."},
    {"name": "Managed IT Services Provider", "category": "Service", "criticality": "High",
     "data_classification": "Confidential", "status": "Active", "is_requirements_agreed": True,
     "right_to_audit": True, "processes_pii": True, "certifications": "ISO 27001",
     "service_description": "Endpoint management, helpdesk, and patching."},
    {"name": "Payroll SaaS Vendor", "category": "Cloud Service", "criticality": "High",
     "data_classification": "Restricted", "status": "Active", "is_requirements_agreed": True,
     "right_to_audit": False, "processes_pii": True, "certifications": "ISO 27001, ISAE 3402",
     "service_description": "Processes employee payroll and personal data (DPA in place)."},
    {"name": "Network Hardware Vendor", "category": "ICT Supply Chain", "criticality": "Medium",
     "data_classification": "Internal", "status": "Active", "is_requirements_agreed": False,
     "right_to_audit": False, "processes_pii": False, "certifications": "",
     "service_description": "Supplies firewalls and switches; firmware supply-chain risk."},
]


# Sample information security incidents (Clauses 5.24–5.28) — generic; illustrative only.
SAMPLE_INCIDENTS: list[dict] = [
    {"title": "Phishing email reported by staff", "category": "Phishing", "severity": "Medium", "status": "Resolved",
     "reporter": "Service Desk", "data_breach": False,
     "description": "Several staff reported a credential-harvesting email impersonating the IT helpdesk.",
     "affected_assets": "Email service; 3 user mailboxes",
     "containment_actions": "Blocked sender domain and URL at the gateway; reset 2 affected accounts; sent awareness reminder.",
     "lessons_learned": "Add the lookalike domain to the blocklist; reinforce reporting via the phishing button."},
    {"title": "Malware detected on a laptop", "category": "Malware", "severity": "High", "status": "In Progress",
     "reporter": "EDR Alert", "data_breach": False,
     "description": "Endpoint protection flagged and quarantined a trojan dropper on a field laptop.",
     "affected_assets": "1 corporate laptop (LAP-0345)",
     "containment_actions": "Isolated the host from the network; quarantined the file; investigation ongoing."},
    {"title": "Public storage bucket misconfiguration", "category": "Misconfiguration", "severity": "High", "status": "Triaged",
     "reporter": "Cloud Security Scan", "data_breach": False,
     "description": "A cloud storage bucket was found with overly permissive public read access.",
     "affected_assets": "Cloud storage bucket (non-production)"},
    {"title": "Lost company mobile phone", "category": "Lost/Stolen Device", "severity": "Low", "status": "Closed",
     "reporter": "Employee", "data_breach": False,
     "description": "An employee reported a lost corporate mobile phone while travelling.",
     "affected_assets": "1 corporate mobile device",
     "containment_actions": "Remote-wiped via MDM; revoked sessions.",
     "lessons_learned": "Confirm MDM enrolment coverage for all mobile devices."},
]


# Sample awareness & training campaigns with participation records (Clauses 7.2/7.3).
SAMPLE_TRAINING: list[dict] = [
    {"title": "Annual Security Awareness 2026", "training_type": "Awareness Campaign", "topic": "General security",
     "status": "In Progress", "audience": "All staff",
     "description": "Mandatory annual information security awareness training for all personnel.",
     "records": [
         {"participant": "Alex Morgan", "status": "Completed", "score": 95},
         {"participant": "Jordan Lee", "status": "Completed", "score": 88},
         {"participant": "Priya Sharma", "status": "Completed", "score": 100},
         {"participant": "Sam Carter", "status": "Assigned"},
     ]},
    {"title": "Q2 Phishing Simulation", "training_type": "Phishing Simulation", "topic": "Phishing",
     "status": "Completed", "audience": "All staff",
     "description": "Simulated phishing campaign measuring click-through and reporting rates.",
     "records": [
         {"participant": "Alex Morgan", "status": "Completed", "score": 100},
         {"participant": "Jordan Lee", "status": "Completed", "score": 100},
         {"participant": "Sam Carter", "status": "Overdue"},
     ]},
    {"title": "Developer Secure Coding Onboarding", "training_type": "Role-based Training", "topic": "Secure development",
     "status": "Planned", "audience": "Engineering team",
     "description": "Role-based secure coding training for new engineering hires.",
     "records": []},
]


# Sample workflow tasks (assignment / approval / remediation) — generic demo set.
# `due_offset_days` is resolved to an absolute date at seed time; assignee/creator
# default to the first available user.
SAMPLE_TASKS: list[dict] = [
    {"title": "Review and approve Information Security Policy", "task_type": "Approval", "priority": "High",
     "status": "Open", "resource_type": "document", "resource_label": "Information Security Policy",
     "due_offset_days": 7,
     "description": "Top-management sign-off required before publication (Clause 5.2 / 7.5.2)."},
    {"title": "Complete Statement of Applicability sign-off", "task_type": "Approval", "priority": "High",
     "status": "Open", "resource_type": "soa", "resource_label": "Statement of Applicability",
     "due_offset_days": 14,
     "description": "Risk owner to approve the SoA and accept residual risk (Clause 6.1.3)."},
    {"title": "Remediate critical vulnerabilities past SLA", "task_type": "Remediation", "priority": "Critical",
     "status": "In Progress", "resource_type": "metric", "resource_label": "Critical vulns past SLA (open)",
     "due_offset_days": -3,
     "description": "Four critical vulnerabilities remain open beyond the 14-day SLA."},
    {"title": "Quarterly access-rights review", "task_type": "Review", "priority": "Medium",
     "status": "Open", "resource_type": "control", "resource_label": "A.5.18 Access rights",
     "due_offset_days": 21,
     "description": "Recertify privileged and application access rights for the quarter."},
    {"title": "Vendor security assessment — Payroll SaaS", "task_type": "Action", "priority": "Medium",
     "status": "Open", "resource_type": "supplier", "resource_label": "Payroll SaaS Vendor",
     "due_offset_days": 30,
     "description": "Issue and review the security questionnaire for the payroll provider."},
]


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


async def seed_iso27019_controls(session) -> int:
    """Insert ISO 27019:2024 energy-sector controls if not already present.

    Gated on the absence of *ISO 27019:2024* controls specifically (not on an
    empty table) so the set can be added to a database that already holds the
    base Annex A controls. Returns count inserted.
    """
    from ..models.control import Control
    from sqlalchemy import select, func

    count = (await session.execute(
        select(func.count()).select_from(Control).where(Control.framework == "ISO 27019:2024")
    )).scalar()
    if count > 0:
        return 0

    for item in ISO27019_CONTROLS:
        session.add(Control(**item))
    await session.flush()
    return len(ISO27019_CONTROLS)


async def seed_clauses(session) -> int:
    """Insert ISMS clause requirements (Clauses 4–10) if the table is empty. Returns count inserted."""
    from ..models.clause_requirement import ClauseRequirement
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(ClauseRequirement))).scalar()
    if count > 0:
        return 0

    for item in ISMS_CLAUSES:
        session.add(ClauseRequirement(**item))
    await session.flush()
    return len(ISMS_CLAUSES)


async def seed_documents(session) -> int:
    """Insert mandatory documented information (Clause 7.5) if the table is empty. Returns count inserted."""
    from ..models.documented_information import DocumentedInformation
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(DocumentedInformation))).scalar()
    if count > 0:
        return 0

    for i, item in enumerate(MANDATORY_DOCUMENTS, start=1):
        session.add(DocumentedInformation(
            ref_id=f"DOC-{i:03d}", mandatory=True, version="1.0", status="Draft", classification="Internal", **item,
        ))
    await session.flush()
    return len(MANDATORY_DOCUMENTS)


async def seed_interested_parties(session) -> int:
    """Insert sample interested parties (Clause 4.2) if the table is empty. Returns count inserted."""
    from ..models.interested_party import InterestedParty
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(InterestedParty))).scalar()
    if count > 0:
        return 0

    for i, item in enumerate(SAMPLE_INTERESTED_PARTIES, start=1):
        session.add(InterestedParty(ref_id=f"PARTY-{i:03d}", **item))
    await session.flush()
    return len(SAMPLE_INTERESTED_PARTIES)


async def seed_objectives(session) -> int:
    """Insert sample information security objectives (Clause 6.2) if empty. Returns count inserted."""
    from ..models.objective import Objective
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(Objective))).scalar()
    if count > 0:
        return 0

    for i, item in enumerate(SAMPLE_OBJECTIVES, start=1):
        session.add(Objective(ref_id=f"OBJ-{i:03d}", **item))
    await session.flush()
    return len(SAMPLE_OBJECTIVES)


async def seed_metrics(session) -> int:
    """Insert sample KPI/KRI/KCI metrics (Clause 9.1) if empty, linked to objectives. Returns count inserted."""
    from ..models.metric import Metric
    from ..models.objective import Objective
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(Metric))).scalar()
    if count > 0:
        return 0

    rows = (await session.execute(select(Objective.ref_id, Objective.id))).all()
    ref_to_id = {ref: oid for ref, oid in rows}

    for i, item in enumerate(SAMPLE_METRICS, start=1):
        data = dict(item)
        obj_ref = data.pop("objective_ref", None)
        session.add(Metric(ref_id=f"MET-{i:03d}", objective_id=ref_to_id.get(obj_ref), **data))
    await session.flush()
    return len(SAMPLE_METRICS)


async def seed_metric_history(session) -> int:
    """Backfill ~6 monthly measurements per metric so trend charts render. Returns points inserted."""
    from ..models.metric import Metric, MetricMeasurement
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(MetricMeasurement))).scalar()
    if count > 0:
        return 0

    metrics = (await session.execute(select(Metric))).scalars().all()
    today = datetime.now(timezone.utc).date()
    points = 0
    for m in metrics:
        if m.current_value is None:
            continue
        current = float(m.current_value)
        # Start from a plausibly "worse" baseline and trend toward the current value.
        start = current * (1.3 if m.direction == "lower_is_better" else 0.7)
        n = 6
        for i in range(n):
            frac = i / (n - 1)
            value = round(start + (current - start) * frac, 1)
            captured = today - timedelta(days=(n - 1 - i) * 30)
            session.add(MetricMeasurement(metric_id=m.id, value=value, captured_at=captured, note="seed backfill"))
            points += 1
    await session.flush()
    return points


async def seed_posture_snapshots(session) -> int:
    """Seed a handful of historical posture snapshots so the trend line shows immediately."""
    from ..models.posture import PostureSnapshot
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(PostureSnapshot))).scalar()
    if count > 0:
        return 0

    today = datetime.now(timezone.utc).date()
    # (days_ago, compliance, conformity, readiness, training)
    history = [
        (150, 22.0, 30.0, 18.0, 60.0),
        (120, 31.0, 43.0, 24.0, 68.0),
        (90, 45.0, 57.0, 41.0, 75.0),
        (60, 58.0, 70.0, 53.0, 82.0),
        (30, 67.0, 80.0, 65.0, 90.0),
    ]
    for days_ago, comp, conf, ready, train in history:
        session.add(PostureSnapshot(
            snapshot_date=today - timedelta(days=days_ago),
            compliance_score=comp, isms_conformity_score=conf,
            document_readiness_score=ready, training_completion_rate=train,
            implemented_controls=int(round(105 * comp / 100)), total_controls=105,
            open_risks=max(0, int(12 - comp / 10)), critical_risks=max(0, int(4 - comp / 30)),
            open_findings=max(0, int(8 - comp / 15)), open_tasks=max(0, int(10 - comp / 12)),
            overdue_tasks=max(0, int(4 - comp / 30)),
        ))
    await session.flush()
    return len(history)


async def seed_suppliers(session) -> int:
    """Insert sample suppliers (Clauses 5.19–5.23) if the table is empty. Returns count inserted."""
    from ..models.supplier import Supplier
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(Supplier))).scalar()
    if count > 0:
        return 0

    for i, item in enumerate(SAMPLE_SUPPLIERS, start=1):
        session.add(Supplier(ref_id=f"SUP-{i:03d}", **item))
    await session.flush()
    return len(SAMPLE_SUPPLIERS)


async def seed_incidents(session) -> int:
    """Insert sample incidents (Clauses 5.24–5.28) if the table is empty. Returns count inserted."""
    from ..models.incident import Incident
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(Incident))).scalar()
    if count > 0:
        return 0

    for i, item in enumerate(SAMPLE_INCIDENTS, start=1):
        session.add(Incident(ref_id=f"INC-{i:03d}", **item))
    await session.flush()
    return len(SAMPLE_INCIDENTS)


async def seed_training(session) -> int:
    """Insert sample training campaigns + records (Clauses 7.2/7.3) if empty. Returns campaigns inserted."""
    from ..models.training import TrainingCampaign, TrainingRecord
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(TrainingCampaign))).scalar()
    if count > 0:
        return 0

    rec_no = 0
    for i, item in enumerate(SAMPLE_TRAINING, start=1):
        data = dict(item)
        records = data.pop("records", [])
        campaign = TrainingCampaign(ref_id=f"TRN-{i:03d}", **data)
        session.add(campaign)
        await session.flush()  # assign campaign.id
        for rec in records:
            rec_no += 1
            session.add(TrainingRecord(ref_id=f"TRR-{rec_no:03d}", campaign_id=campaign.id, **rec))
    await session.flush()
    return len(SAMPLE_TRAINING)


async def seed_tasks(session) -> int:
    """Insert sample workflow tasks if the table is empty. Returns count inserted.

    Assigns tasks to the first available user; resolves relative due dates to
    absolute dates. Call after users have been seeded.
    """
    from ..models.task import Task
    from ..models.user import User
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import select, func

    count = (await session.execute(select(func.count()).select_from(Task))).scalar()
    if count > 0:
        return 0

    user = (await session.execute(select(User).order_by(User.created_at))).scalars().first()
    user_id = user.id if user else None
    today = datetime.now(timezone.utc).date()

    for i, item in enumerate(SAMPLE_TASKS, start=1):
        data = dict(item)
        offset = data.pop("due_offset_days", None)
        due = today + timedelta(days=offset) if offset is not None else None
        session.add(Task(
            ref_id=f"TASK-{i:03d}", assignee_id=user_id, created_by_id=user_id, due_date=due, **data,
        ))
    await session.flush()
    return len(SAMPLE_TASKS)


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
