


// ARZI Civic RTI & Statutory Legal Intelligence Platform - Client Interaction Logic

const API_BASE = "/api/v1";

// =========================================================================
// BILINGUAL (ENGLISH / HINDI) TRANSLATION ENGINE & DICTIONARY
// =========================================================================
let savedLang = localStorage.getItem("arzi_lang");
let currentLang = (savedLang === "hi") ? "hi" : "en";
localStorage.setItem("arzi_lang", currentLang);

const I18N_DICT = {
  // Brand & Nav
  "brand_name": { "en": "ARZI", "hi": "अर्जी" },
  "brand_sub": { "en": "Civic Legal Intelligence Desk", "hi": "नागरिक विधिक सहायता डेस्क" },
  "nav_home": { "en": "Home Overview", "hi": "मुख्य पृष्ठ" },
  "nav_about": { "en": "About & Mission", "hi": "उद्देश्य एवं परिचय" },
  "nav_pillars": { "en": "Statutory Pillars", "hi": "कानूनी नियम" },
  "nav_dashboard": { "en": "Operations Dashboard", "hi": "ऑपरेशंस डैशबोर्ड" },
  "nav_dashboard_short": { "en": "Dashboard", "hi": "डैशबोर्ड" },
  "status_operational": { "en": "Operational", "hi": "सक्रिय" },

  // Hero Section
  "hero_tag": { "en": "AUTONOMOUS CIVIC RTI & STATUTORY LEGAL INTELLIGENCE", "hi": "स्वचालित नागरिक आरटीआई एवं कानूनी सहायता डेस्क" },
  "hero_h1_prefix": { "en": "Democratizing Indian Public Law with", "hi": "भारतीय जन-कानून का सरलीकरण" },
  "hero_h1_span": { "en": "Autonomous Statutory Intelligence", "hi": "सटीक एवं पारदर्शी कानूनी प्रणाली" },
  "hero_lead": {
    "en": "ARZI simplifies public legal processes by converting citizen grievances into legally enforceable RTI applications and First Appeals. Automatically map IPC 1860 to Bharatiya Nyaya Sanhita (BNS 2023), locate your designated Public Information Officer via geodesy, and enforce statutory compliance deadlines.",
    "hi": "अर्जी आपकी नागरिक समस्याओं को कानूनी रूप से मान्य आरटीआई और प्रथम अपील में बदलकर त्वरित समाधान दिलाती है। बीएनएस 2023 की धाराएं देखें, अपने जन सूचना अधिकारी (PIO) को खोजें और 30 दिन में जवाब सुनिश्चित करें।"
  },
  "hero_btn_file": { "en": "File RTI Grievance", "hi": "आरटीआई शिकायत दर्ज करें" },
  "hero_btn_codex": { "en": "Statutory Codex", "hi": "कानूनी नियम देखें" },
  "hero_btn_runlog": { "en": "Audit Run Log", "hi": "ऑडिट लॉग" },

  // Snapshot Metrics
  "stat_active": { "en": "Active Cases", "hi": "सक्रिय मामले" },
  "stat_active_sub": { "en": "Pending Review", "hi": "समीक्षा हेतु लंबित" },
  "stat_pio": { "en": "Avg PIO Distance", "hi": "औसत PIO दूरी" },
  "stat_pio_sub": { "en": "Haversine Geodesic Match", "hi": "भू-स्थानिक निकटता" },
  "stat_penalty": { "en": "Sec 20 Liability", "hi": "धारा 20 जुर्माना" },
  "stat_penalty_sub": { "en": "₹250/day Mandatory Penalty", "hi": "₹250/दिन अनिवार्य जुर्माना" },
  "stat_dockets": { "en": "Total Dockets", "hi": "कुल दर्ज मामले" },
  "stat_dockets_sub": { "en": "Cumulative Cases", "hi": "अभिलेख में दर्ज" },

  // Workflow Pipeline
  "pipeline_title": { "en": "4-Stage Grievance-to-Enforcement Pipeline", "hi": "4-चरणीय सरल शिकायत निवारण प्रक्रिया" },
  "pipeline_badge": { "en": "Deterministic SLA", "hi": "समयबद्ध समाधान" },
  "pipeline_s1_title": { "en": "Ingest & Structured Parsing", "hi": "1. शिकायत दर्ज व कानूनी विश्लेषण" },
  "pipeline_s1_desc": { "en": "Translates citizen grievances into legally enforceable questions admissible under Section 2(f) of RTI Act.", "hi": "नागरिक की आम भाषा को आरटीआई अधिनियम की धारा 2(f) के तहत कानूनी प्रश्नों में बदलता है।" },
  "pipeline_s2_title": { "en": "11-Domain ML Classification", "hi": "2. विभाग व बीएनएस धारा चयन" },
  "pipeline_s2_desc": { "en": "Identifies the competent public sector (Power, Water, Transport, Revenue) with confidence scoring.", "hi": "बिजली, पानी, सड़क, राशन, राजस्व आदि में से सही विभाग व बीएनएस 2023 धाराओं का निर्धारण।" },
  "pipeline_s3_title": { "en": "Geodesic PIO Discovery", "hi": "3. संबंधित PIO की खोज" },
  "pipeline_s3_desc": { "en": "Applies Haversine spherical geodesy to map pincodes and coordinates to the verified nodal officer.", "hi": "पिन कोड और भू-स्थानिक तकनीक द्वारा आपके क्षेत्र के सही जन सूचना अधिकारी की खोज।" },
  "pipeline_s4_title": { "en": "Enforceable Instrument & Log", "hi": "4. आरटीआई ड्राफ्ट व ट्रैकिंग" },
  "pipeline_s4_desc": { "en": "Compiles court-admissible Form-A PDFs with SHA-256 digital seals and immutable audit run log.", "hi": "डाउनलोड योग्य आरटीआई फॉर्म-A पीडीएफ तैयार कर 30-दिवसीय समयसीमा की ट्रैकिंग शुरू।" },

  // Quick Triage Launchpad
  "quick_triage_title": { "en": "Instant Civic Sector Triage Launchpad (1-Click Load)", "hi": "सामान्य नागरिक शिकायतें (1-क्लिक में दर्ज करें)" },
  "quick_triage_badge": { "en": "11 Public Domains", "hi": "11 सरकारी विभाग" },
  "preset_power_title": { "en": "Electricity & Power Discom", "hi": "बिजली व पावर डिस्कॉम" },
  "preset_power_sub": { "en": "Transformer burnout & blackout • BSES Delhi (110019)", "hi": "ट्रांसफार्मर खराबी व बिजली कटौती • दिल्ली (110019)" },
  "preset_water_title": { "en": "Drinking Water & Jal Board", "hi": "पेयजल आपूर्ति व जल निगम" },
  "preset_water_sub": { "en": "Sewage contamination • Jal Sansthan Varanasi (221010)", "hi": "गंदे पानी की आपूर्ति व सीवर • वाराणसी (221010)" },
  "preset_transport_title": { "en": "Transport & RTO Vehicles", "hi": "परिवहन विभाग व आरटीओ" },
  "preset_transport_sub": { "en": "Driving license renewal delay • Sarai Kale Khan (110013)", "hi": "ड्राइविंग लाइसेंस में देरी • दिल्ली (110013)" },
  "preset_pension_title": { "en": "Labour, Pension & Security", "hi": "पेंशन एवं भविष्य निधि (EPFO)" },
  "preset_pension_sub": { "en": "EPS-95 monthly pension settlement • EPFO Delhi (110052)", "hi": "मासिक पेंशन का भुगतान न होना • दिल्ली (110052)" },
  "preset_pollution_title": { "en": "Environment & Pollution", "hi": "पर्यावरण व प्रदूषण नियंत्रण" },
  "preset_pollution_sub": { "en": "Illegal industrial toxic effluent • DPCC Delhi (110032)", "hi": "अवैध जहरीला कचरा व प्रदूषण • दिल्ली (110032)" },
  "preset_land_title": { "en": "Revenue & Land Records", "hi": "राजस्व एवं जमीन नामांतरण" },
  "preset_land_sub": { "en": "Mutation & Khasra delay • Sadar Tehsil Varanasi (221002)", "hi": "दाखिल-खारिज व खतौनी में देरी • वाराणसी (221002)" },

  // About Page
  "about_tag": { "en": "ABOUT ARZI • CIVIC ACCOUNTABILITY & MANDATE", "hi": "अर्जी के बारे में • पारदर्शिता व नागरिक अधिकार" },
  "about_h1_prefix": { "en": "Dismantling Administrative Silence", "hi": "प्रशासनिक लेटलतीफी का अंत" },
  "about_h1_span": { "en": "Through Autonomous Legal Engineering", "hi": "सशक्त नागरिक कानूनी तकनीक द्वारा" },
  "about_lead": {
    "en": "ARZI empowers citizens and advocates to dismantle bureaucratic silence by converting informal grievances into binding RTI filings with automatic Section 20 penalty tracking.",
    "hi": "अर्जी नागरिकों और अधिवक्ताओं को यह अधिकार देती है कि वे अपनी समस्याओं को कानूनी रूप से बाध्यकारी आरटीआई में बदलकर सरकारी जवाबदेही सुनिश्चित करें।"
  },
  "about_crisis_title": { "en": "The Administrative Silence Crisis in India", "hi": "सरकारी विभागों में जवाब न मिलने की समस्या" },
  "about_crisis_p1": { "en": "Across municipal corporations, tehsils, and statutory boards, millions of legitimate citizen requests languish unanswered. Bureaucratic delays become the default operating procedure.", "hi": "नगर निगमों, तहसीलों और सरकारी दफ्तरों में लाखों नागरिक आवेदन बिना किसी जवाब के धूल खाते रहते हैं।" },
  "about_crisis_p2": { "en": "When grievances remain informal—without statutory citations—officers face zero legal accountability.", "hi": "जब शिकायतें बिना कानूनी धाराओं के दी जाती हैं, तो अधिकारियों पर कोई जवाबदेही नहीं बनती।" },
  "about_sol_title": { "en": "The ARZI Operational Intervention", "hi": "अर्जी का ठोस समाधान" },
  "about_sol_p1": { "en": "ARZI transforms everyday complaints into precise questions under Section 2(f), finds the nodal PIO via geodesy, and starts the strict 30-day clock.", "hi": "अर्जी आम शिकायतों को धारा 2(f) के तहत कानूनी प्रश्नों में बदलती है, सही अधिकारी खोजती है और 30 दिन की समयसीमा शुरू करती है।" },
  "about_sol_p2": { "en": "By activating the ₹250/day personal salary deduction mandate under Section 20(1), ARZI replaces bureaucratic discretion with enforceable legal liability.", "hi": "धारा 20(1) के तहत लापरवाह अधिकारी के वेतन से ₹250/दिन व्यक्तिगत कटौती का डर जवाबदेही सुनिश्चित करता है।" },
  "about_stake_title": { "en": "Multi-Stakeholder Operational Utility", "hi": "सभी हितधारकों के लिए उपयोगिता" },
  "stake_citizen_title": { "en": "Citizen Complainants", "hi": "आम नागरिक" },
  "stake_citizen_desc": { "en": "File clear, structured RTI questions in under 2 minutes without needing expensive legal representation.", "hi": "बिना किसी वकील के 2 मिनट में सटीक आरटीआई प्रश्न तैयार करें।" },
  "stake_lawyer_title": { "en": "Legal Counsel & Advocates", "hi": "अधिवक्ता एवं विधिक पेशेवर" },
  "stake_lawyer_desc": { "en": "Manage high-volume civic casework with automated IPC ↔ BNS concordance and rapid First Appeal generation.", "hi": "बीएनएस 2023 और प्रथम अपील के साथ नागरिक मामलों को तेजी से निपटाएं।" },
  "stake_gov_title": { "en": "Public Grievance Desks", "hi": "लोक शिकायत प्रकोष्ठ" },
  "stake_gov_desc": { "en": "Public authorities can execute Section 6(3) 5-day transfers seamlessly and avoid Section 20 penalty liabilities.", "hi": "धारा 6(3) के तहत 5 दिन में सही विभाग को फाइल भेजें और जुर्माने से बचें।" },
  "about_rigor_title": { "en": "Engineering Rigor & Cryptographic Verifiability", "hi": "तकनीकी प्रामाणिकता एवं सुरक्षा" },
  "rigor_det_title": { "en": "Deterministic Legal Reasoning", "hi": "सटीक कानूनी तर्क" },
  "rigor_det_desc": { "en": "Zero hallucination risk. Statutory questions, time limits, and fee clauses are compiled via deterministic statutory rule engines verified against official Indian Gazettes.", "hi": "शून्य त्रुटि। कानूनी प्रश्न और समयसीमा आधिकारिक गजट के आधार पर तैयार होते हैं।" },
  "rigor_sha_title": { "en": "SHA-256 Digital Sealing", "hi": "SHA-256 डिजिटल सुरक्षा" },
  "rigor_sha_desc": { "en": "Every generated Form-A embeds an immutable SHA-256 cryptographic hash guaranteeing tamper-evident authenticity.", "hi": "प्रत्येक दस्तावेज में डिजिटल हैश कोड होता है जो उसकी प्रामाणिकता सिद्ध करता है।" },
  "rigor_audit_title": { "en": "Immutable Audit Ledger", "hi": "अपरिवर्तनीय ऑडिट लेजर" },
  "rigor_audit_desc": { "en": "Every intake, transfer, and case update is permanently journaled with microsecond ISO timestamps.", "hi": "प्रत्येक कदम और तारीख का स्थाई रिकॉर्ड दर्ज होता है जिसे बदला नहीं जा सकता।" },

  // Pillars Page
  "pillars_tag": { "en": "LEGAL CODEX & STATUTORY BENCHMARKS", "hi": "कानूनी संहिता एवं समयसीमा" },
  "pillars_h1_prefix": { "en": "Authoritative Statutory Provisions &", "hi": "अधिनियम के मुख्य प्रावधान एवं" },
  "pillars_h1_span": { "en": "Judicial Enforcement Standards", "hi": "न्यायिक निर्णय व मानक" },
  "pillars_lead": {
    "en": "Comprehensive reference guide on Section 20 penalty enforcement, Bharatiya Nyaya Sanhita criminal law transition, statutory escalation ladders, and landmark Supreme Court jurisprudence.",
    "hi": "धारा 20 जुर्माना प्रक्रिया, बीएनएस 2023 में धाराओं का बदलाव, आरटीआई की समयसीमा और सुप्रीम कोर्ट के महत्वपूर्ण फैसलों का संपूर्ण विवरण।"
  },
  "ladder_title": { "en": "Statutory Escalation Ladder & Mandatory Time Limits", "hi": "आरटीआई की कानूनी समयसीमा व चरण" },
  "ladder_day0_title": { "en": "Filing & Fee", "hi": "आवेदन व शुल्क" },
  "ladder_day0_desc": { "en": "Form-A submission with ₹10 court fee / postal order. Receipt acknowledgment legally mandatory.", "hi": "₹10 शुल्क के साथ फॉर्म-A जमा करें; रसीद मिलना अनिवार्य है।" },
  "ladder_day5_title": { "en": "Sec 6(3) Transfer", "hi": "धारा 6(3) अंतरण" },
  "ladder_day5_desc": { "en": "If info held by another public authority, transfer within 5 days with written notice to citizen.", "hi": "दूसरे विभाग का मामला होने पर 5 दिन के भीतर फाइल भेजना अनिवार्य है।" },
  "ladder_day30_title": { "en": "Statutory SLA", "hi": "30-दिवसीय समयसीमा" },
  "ladder_day30_desc": { "en": "Standard 30-day window expires. (48 hours if life/liberty). Day 31 triggers ₹250/day penalty clock.", "hi": "जवाब देने की 30 दिन की सीमा। 31वें दिन से ₹250/दिन जुर्माना शुरू।" },
  "ladder_day60_title": { "en": "First Appeal", "hi": "प्रथम अपील" },
  "ladder_day60_desc": { "en": "File First Appeal under Section 19(1) to First Appellate Authority (FAA) against deemed refusal.", "hi": "जवाब न मिलने पर वरिष्ठ अधिकारी (FAA) के समक्ष प्रथम अपील करें।" },
  "ladder_day150_title": { "en": "Second Appeal", "hi": "द्वितीय अपील" },
  "ladder_day150_desc": { "en": "Escalate to Central / State Information Commission under Section 19(3) with prayer for Section 20 penalties.", "hi": "राज्य या केंद्रीय सूचना आयोग में अपील कर जुर्माना लगाने की मांग करें।" },
  "p1_title": { "en": "Pillar 1: Section 20(1) Personal Penalty Clock", "hi": "स्तंभ 1: धारा 20(1) व्यक्तिगत जुर्माना" },
  "p1_desc": { "en": "Under Section 20(1) of the RTI Act 2005, where the Commission finds that a Public Information Officer (PIO) has refused or delayed information without reasonable cause, it shall impose a penalty of ₹250 each day (up to ₹25,000) deducted from the officer's salary.", "hi": "धारा 20(1) के तहत, 30 दिन में बिना ठोस कारण सूचना न देने पर आयोग अधिकारी के वेतन से प्रतिदिन ₹250 (अधिकतम ₹25,000) जुर्माना काटता है।" },
  "p2_title": { "en": "Pillar 2: IPC 1860 to BNS 2023 Criminal Codex", "hi": "स्तंभ 2: आईपीसी 1860 से बीएनएस 2023" },
  "p3_title": { "en": "Pillar 3: Section 6(3) 5-Day Mandatory Transfer", "hi": "स्तंभ 3: धारा 6(3) 5-दिवसीय अंतरण" },
  "p3_desc": { "en": "Where an application is made to an authority requesting information held by another, the officer shall transfer the application within five days and immediately inform the applicant in writing.", "hi": "यदि मांगी गई सूचना किसी अन्य विभाग से संबंधित है, तो अधिकारी 5 दिन के भीतर आवेदन को सही विभाग को भेजने के लिए बाध्य है।" },
  "p4_title": { "en": "Pillar 4: Haversine Geodetic PIO Mapping", "hi": "स्तंभ 4: भू-स्थानिक अधिकारी मैपिंग" },
  "p4_desc": { "en": "ARZI uses the great-circle Haversine formula across verified municipal coordinates (Delhi NCT, Varanasi, Lucknow) to assign the nearest competent Public Information Officer.", "hi": "अर्जी पिन कोड और निर्देशांकों के आधार पर आपके क्षेत्र के निकटतम सक्षम जन सूचना अधिकारी को चुनती है।" },
  "sc_precedents_title": { "en": "Landmark Supreme Court Jurisprudence on Right to Information", "hi": "सूचना के अधिकार पर सुप्रीम कोर्ट के ऐतिहासिक फैसले" },
  "matrix_title": { "en": "Comprehensive IPC 1860 ↔ BNS 2023 Statutory Comparison Matrix", "hi": "आईपीसी 1860 ↔ बीएनएस 2023 तुलनात्मक तालिका" },
  "table_filter_placeholder": { "en": "Filter by section, crime, or keyword...", "hi": "धारा, अपराध या शब्द से खोजें..." },
  "th_offense": { "en": "Offense Category", "hi": "अपराध / समस्या श्रेणी" },
  "th_ipc": { "en": "Historical IPC (1860)", "hi": "पुराना कानून (IPC 1860)" },
  "th_bns": { "en": "Bharatiya Nyaya Sanhita (2023)", "hi": "नया कानून (BNS 2023)" },
  "th_punishment": { "en": "Maximum Punishment Scope", "hi": "सजा का प्रावधान" },
  "th_status": { "en": "Cognizability & Bail Status", "hi": "संज्ञेयता व जमानत" },

  // Dashboard & Subtabs
  "subnav_casework": { "en": "01. Casework Desk", "hi": "01. शिकायत डेस्क" },
  "subnav_statutory": { "en": "02. Statutory Library & Custom Acts", "hi": "02. कानून व अधिनियम" },
  "subnav_pio": { "en": "03. PIO Geospatial Map", "hi": "03. अधिकारी मैप" },
  "subnav_compliance": { "en": "04. Compliance & SLA", "hi": "04. जुर्माना कैलकुलेटर" },
  "subnav_runlog": { "en": "05. Audit Run Log", "hi": "05. ऑडिट लॉग" },

  "intake_panel_title": { "en": "Citizen Grievance Ingestion", "hi": "नागरिक शिकायत दर्ज करें" },
  "intake_toggle_btn": { "en": "Toggle Form", "hi": "फॉर्म छिपाएं/दिखाएं" },
  "intake_name": { "en": "Complainant / Client Full Name *", "hi": "शिकायतकर्ता का पूरा नाम *" },
  "intake_contact": { "en": "Phone / Contact *", "hi": "फोन / संपर्क नंबर *" },
  "intake_language": { "en": "Language / Locale", "hi": "दस्तावेज़ की भाषा" },
  "intake_addr": { "en": "Address / Locality *", "hi": "पता / मोहल्ला / क्षेत्र *" },
  "intake_pin": { "en": "PIN Code (6-Digit) *", "hi": "पिन कोड (6 अंक) *" },
  "intake_urgent_label": { "en": "48-Hour Urgent Life & Liberty Fast-Track (Section 7(1) Proviso)", "hi": "48 घंटे का आपातकालीन मामला (जीवन व स्वतंत्रता)" },
  "intake_urgent_hint": { "en": "Invokes 48-hour statutory deadline for ICU emergencies, water contamination, unlawful custody, or life threats.", "hi": "अस्पताल आपातकाल, दूषित जल, अवैध हिरासत या जीवन को खतरे के मामलों में 48 घंटे में सूचना का अधिकार।" },
  "intake_ref": { "en": "Original Ref / Ack No.", "hi": "मूल संदर्भ / रसीद संख्या" },
  "intake_date": { "en": "Submission Date", "hi": "आवेदन की तारीख" },
  "intake_narrative": { "en": "Statement of Facts & Grievance Narrative *", "hi": "अपनी शिकायत का संक्षिप्त विवरण *" },
  "intake_narrative_ph": { "en": "Enter or dictate factual details regarding public record request, administrative delay, or refusal...", "hi": "अपनी समस्या विस्तार से लिखें (जैसे राशन न मिलना, जमीन नामांतरण में देरी, सड़क या नाली की समस्या)..." },
  "intake_submit": { "en": "Ingest, Extract Law & Route PIO →", "hi": "शिकायत जमा करें एवं अधिकारी खोजें →" },
  "btn_ml_predict": { "en": "⚡ Predict Domain via ML", "hi": "⚡ श्रेणी जांचें (AI)" },
  "btn_voice_dictate": { "en": "Voice Dictation", "hi": "बोलकर लिखें" },
  "presets_label": { "en": "Common Civic Presets (1-Click):", "hi": "त्वरित उदाहरण (1-क्लिक):" },
  "preset_ration_pill": { "en": "Ration / PDS (Delhi)", "hi": "राशन / कोटेदार (दिल्ली)" },
  "preset_land_pill": { "en": "Land Mutation (Varanasi)", "hi": "जमीन नामांतरण (वाराणसी)" },
  "preset_water_pill": { "en": "Water & Sewer (Jal Board)", "hi": "जल आपूर्ति व सीवर (जल निगम)" },
  "preset_power_pill": { "en": "Electricity Discom (Power)", "hi": "बिजली आपूर्ति (डिस्कॉम)" },
  "preset_emergency_pill": { "en": "48h Urgent (AIIMS)", "hi": "48 घंटे आपातकाल (एम्स)" },

  "queue_panel_title": { "en": "Active Casework Dockets", "hi": "सक्रिय मामले" },
  "queue_search_ph": { "en": "Search Case ID, Citizen, Varanasi, Section...", "hi": "केस आईडी, नाम, शहर या धारा से खोजें..." },
  "queue_filter_btn": { "en": "Filter", "hi": "खोजें" },
  "th_docket": { "en": "Docket", "hi": "केस आईडी" },
  "th_complainant": { "en": "Complainant", "hi": "आवेदक" },
  "th_dept": { "en": "Department", "hi": "विभाग" },
  "th_sections": { "en": "Sections", "hi": "धाराएं" },
  "th_pio": { "en": "Assigned PIO", "hi": "नामित अधिकारी" },
  "th_status": { "en": "Status", "hi": "स्थिति" },
  "th_action": { "en": "Action", "hi": "कार्रवाई" },
  "btn_view": { "en": "View", "hi": "देखें" },

  "no_case_title": { "en": "No Active Case Docket Selected", "hi": "कोई केस चयनित नहीं है" },
  "no_case_desc": { "en": "Select a case file from the left queue, or ingest a citizen brief to open the legal evidence dossier.", "hi": "बाईं ओर की सूची से कोई केस चुनें या नया आवेदन भरें।" },

  // Compliance Calculator
  "calc_panel_title": { "en": "Interactive Section 20(1) Penalty & Statutory SLA Clock", "hi": "धारा 20(1) जुर्माना एवं समयसीमा कैलकुलेटर" },
  "calc_heading_params": { "en": "Case Timeline & SLA Parameters", "hi": "समयसीमा व आवेदन विवरण" },
  "calc_lbl_filing": { "en": "RTI Application Filing Date *", "hi": "आवेदन जमा करने की तिथि *" },
  "calc_lbl_provision": { "en": "Statutory SLA Provision *", "hi": "कानूनी श्रेणी *" },
  "calc_lbl_resp": { "en": "PIO Response Date (Leave empty if still pending)", "hi": "जवाब मिलने की तिथि (लंबित होने पर खाली छोड़ें)" },
  "calc_lbl_dept": { "en": "Target Public Authority / Department", "hi": "संबंधित सरकारी विभाग" },
  "calc_btn_reset_label": { "en": "Reset to 35-Day Overdue Benchmark", "hi": "डिफ़ॉल्ट पर रीसेट करें" },
  "calc_heading_results": { "en": "Live Accrued Personal Penalty Liability", "hi": "अधिकारी पर देय जुर्माना" },
  "calc_lbl_deadline": { "en": "Statutory Deadline", "hi": "अंतिम तिथि" },
  "calc_lbl_elapsed": { "en": "Days Elapsed", "hi": "बीते दिन" },
  "calc_lbl_delinquent": { "en": "Delinquent Days", "hi": "विलंब के दिन" },
  "calc_lbl_accrued": { "en": "Accrued Penalty", "hi": "कुल जुर्माना" },
  "calc_copy_btn": { "en": "Copy Clause", "hi": "क्लॉज कॉपी करें" },

  // PIO Tab
  "pio_geodesy_title": { "en": "Active Complaint Docket Geodesy", "hi": "शिकायत का भू-स्थानिक विवरण" },
  "pio_visualizer_title": { "en": "Geospatial Jurisdictional Visualizer", "hi": "क्षेत्राधिकार मैप व टेलीमेट्री" },
  "pio_nearest_title": { "en": "Nearest PIO Officers in Area", "hi": "क्षेत्र के निकटतम जन सूचना अधिकारी" },

  // RunLog Tab
  "runlog_search_title": { "en": "Search Case Dockets & Audit Trail", "hi": "केस ऑडिट ट्रायल व सर्च" },
  "runlog_table_title": { "en": "Immutable Code-Generated Execution Run Log", "hi": "अपरिवर्तनीय कोड-जनित ऑडिट रन लॉग" },

  // Case Detail Dossier
  "dossier_return_btn": { "en": "← Return to Audit Run Log", "hi": "← वापस ऑडिट लॉग पर जाएं" },
  "dossier_open_workspace": { "en": "Open in Casework Workspace", "hi": "शिकायत डेस्क में खोलें" },
  "dossier_download_pdf": { "en": "Download Form-A PDF", "hi": "फॉर्म-A पीडीएफ डाउनलोड" },
  "dossier_parties_title": { "en": "Citizen Complainant & Designated Public Authority", "hi": "नागरिक आवेदक एवं नामित जन सूचना अधिकारी" },
  "dossier_grievance_title": { "en": "Citizen Grievance & Structured Questions", "hi": "शिकायत विवरण एवं तैयार आरटीआई प्रश्न" },
  "dossier_ml_title": { "en": "ML Domain Classification Intelligence", "hi": "एआई वर्गीकरण व धारा विश्लेषण" },
  "dossier_merge_title": { "en": "Case Deduplication & Docket Consolidation", "hi": "समान मामलों का एकीकरण व दोहराव निवारण" },
  "dossier_update_title": { "en": "Log Official Case Update with Timestamp", "hi": "केस में नया घटनाक्रम / तारीख दर्ज करें" },
  "dossier_timeline_title": { "en": "Chronological Case Timeline & Ledger", "hi": "केस की समयबद्ध प्रगति एवं लेजर" },

  // Extra Utility & Component Keys
  "btn_refresh": { "en": "Refresh", "hi": "ताज़ा करें" },
  "btn_clear": { "en": "Clear", "hi": "हटाएं" },
  "btn_close": { "en": "Close", "hi": "बंद करें" },
  "btn_cancel": { "en": "Cancel", "hi": "रद्द करें" },
  "btn_dismiss": { "en": "Dismiss", "hi": "हटाएं" },
  "btn_print_slip": { "en": "Print Dispatch Slip", "hi": "रसीद प्रिंट करें" },
  "btn_execute_transfer": { "en": "Execute Transfer", "hi": "अंतरण करें" },

  // Statutory Library & Custom Acts
  "statutory_codex_title": { "en": "Statutory Codex & Custom Acts Registration", "hi": "कानून एवं अधिनियम पंजीकरण" },
  "statutory_act_title": { "en": "Act / Legislation Full Title *", "hi": "अधिनियम का पूरा नाम *" },
  "statutory_act_sections": { "en": "Specific Section(s) / Rule *", "hi": "संबंधित धाराएं / नियम *" },
  "statutory_act_domain": { "en": "Statutory Domain / Practice Area *", "hi": "कानूनी विभाग / विषय *" },
  "statutory_act_author": { "en": "Advocate / Author Name *", "hi": "अधिवक्ता / लेखक का नाम *" },
  "statutory_act_grounds": { "en": "Statutory Grounds & Legal Effect *", "hi": "कानूनी आधार व प्रभाव *" },
  "statutory_act_link": { "en": "Link immediately to current active docket", "hi": "वर्तमान केस से तुरंत जोड़ें" },
  "statutory_act_btn": { "en": "Register Custom Act", "hi": "अधिनियम जोड़ें" },
  "statutory_registered_title": { "en": "Registered Legislation", "hi": "पंजीकृत कानून" },

  // PIO Radar & Directory
  "pio_banner_text": { "en": "Complaint Registered & Nearest Domain PIO Assigned!", "hi": "शिकायत दर्ज एवं संबंधित क्षेत्र के PIO का आवंटन सम्पन्न!" },
  "pio_inspect_label": { "en": "Inspect Docket:", "hi": "केस चुनें:" },
  "pio_kpi_docket": { "en": "Docket & Complainant", "hi": "केस व आवेदक" },
  "pio_kpi_domain": { "en": "Complaint Domain", "hi": "शिकायत श्रेणी" },
  "pio_kpi_assigned": { "en": "Assigned Nearest Domain PIO", "hi": "आवंटित जन सूचना अधिकारी" },
  "pio_origin_legend": { "en": "Citizen Origin", "hi": "आवेदक का स्थान" },
  "pio_assigned_legend": { "en": "Assigned Domain PIO", "hi": "आवंटित जन सूचना अधिकारी" },
  "pio_nearby_legend": { "en": "Other Nearby Authorities", "hi": "अन्य निकटतम कार्यालय" },
  "pio_filter_all": { "en": "All Nearby", "hi": "सभी निकटतम" },
  "pio_filter_domain": { "en": "Domain Only", "hi": "केवल विभाग" },
  "pio_filter_close": { "en": "< 3 km", "hi": "3 किमी से कम" },

  // Speed Post & Transfer Modals
  "transfer_modal_title": { "en": "SECTION 6(3) 5-DAY MANDATORY TRANSFER", "hi": "धारा 6(3) 5-दिवसीय अनिवार्य अंतरण" },
  "transfer_modal_desc": { "en": "Transfer this application to the rightful public authority holding records. An automated notice and run log audit will be recorded.", "hi": "इस आवेदन को संबंधित विभाग को 5 दिन में अंतरित करें। इसका रिकॉर्ड ऑडिट लॉग में दर्ज होगा।" },
  "postal_slip_modal_title": { "en": "INDIAN SPEED POST DISPATCH DOCKET & REGISTERED AD", "hi": "भारतीय स्पीड पोस्ट एवं पंजीकृत डाक रसीद" },
  "postal_slip_modal_sub": { "en": "Department of Posts, India • Statutory Proof of Dispatch under Section 27 General Clauses Act", "hi": "डाक विभाग, भारत सरकार • धारा 27 के तहत विधिक प्रेषण प्रमाण" },

  // Footer
  "footer_brand": { "en": "ARZI — Civic RTI & Statutory Legal Intelligence Platform • National Legal Tech Standard", "hi": "अर्जी — नागरिक आरटीआई एवं कानूनी सहायता प्लेटफॉर्म • राष्ट्रीय विधिक सेवा" }
};

function t(key) {
  if (!I18N_DICT[key]) return key;
  if (I18N_DICT[key][currentLang]) {
    return I18N_DICT[key][currentLang];
  }
  return I18N_DICT[key]["en"] || key;
}

function setLanguage(lang) {
  if (lang !== "hi") lang = "en";
  currentLang = lang;
  localStorage.setItem("arzi_lang", lang);

  // Set strict CSS class on <body>
  document.body.classList.remove("lang-en", "lang-hi", "lang-bi");
  document.body.classList.add("lang-" + lang);
  document.documentElement.lang = (lang === "hi" ? "hi" : "en");

  // Update dynamic document title
  document.title = lang === "hi"
    ? "अर्जी — नागरिक आरटीआई एवं विधिक सहायता डेस्क"
    : "ARZI — Civic RTI & Statutory Legal Intelligence Desk";

  // Update switcher button states
  const btnEn = document.getElementById("langEn");
  const btnHi = document.getElementById("langHi");
  if (btnEn) btnEn.classList.toggle("active", lang === "en");
  if (btnHi) btnHi.classList.toggle("active", lang === "hi");

  // Switch all select options having data-en and data-hi
  document.querySelectorAll("option[data-en]").forEach(opt => {
    const en = opt.getAttribute("data-en") || "";
    const hi = opt.getAttribute("data-hi") || "";
    opt.textContent = (lang === "hi" ? (hi || en) : en);
  });

  // Switch all input/textarea placeholders having data-ph-en and data-ph-hi
  document.querySelectorAll("[data-ph-en]").forEach(inp => {
    const en = inp.getAttribute("data-ph-en") || "";
    const hi = inp.getAttribute("data-ph-hi") || "";
    inp.placeholder = (lang === "hi" ? (hi || en) : en);
  });

  // Translate all [data-i18n] text nodes
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (I18N_DICT[key]) {
      el.textContent = t(key);
    }
  });

  // Translate all [data-i18n-html] elements
  document.querySelectorAll("[data-i18n-html]").forEach(el => {
    const key = el.getAttribute("data-i18n-html");
    if (I18N_DICT[key]) {
      el.innerHTML = I18N_DICT[key][lang] || I18N_DICT[key]["en"];
    }
  });

  // Translate all [data-i18n-placeholder] inputs
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (I18N_DICT[key]) {
      el.placeholder = t(key);
    }
  });

  // Update queue table action buttons and titles if rendered
  document.querySelectorAll(".btn-view-docket").forEach(btn => {
    btn.textContent = t("btn_view");
  });

  const repoStatus = document.getElementById("repoStatusText");
  if (repoStatus) {
    repoStatus.textContent = (lang === "hi" ? "सक्रिय" : "Operational");
  }

  // Refresh workspace or queue if active
  if (typeof currentCase !== "undefined" && currentCase) {
    populateWorkspaceFields(currentCase);
  }
  if (typeof loadCaseQueue === "function") {
    loadCaseQueue();
  }
  if (typeof activeDetailCase !== "undefined" && activeDetailCase) {
    openCaseDetailView(activeDetailCase.case_id);
  }
  // Re-run compliance calculator if dates are filled
  const calcFiling = document.getElementById("calcFilingDate");
  if (calcFiling && calcFiling.value && typeof calculateLiveSection20Penalty === "function") {
    calculateLiveSection20Penalty();
  }

  if (typeof renderLucide === "function") {
    renderLucide();
  }
}

function initLanguage() {
  setLanguage(currentLang);
}

window.t = t;
window.setLanguage = setLanguage;
window.initLanguage = initLanguage;

let currentCase = null;
let activePersona = "law_firm"; // 'law_firm' or 'gov_desk'
let currentDocTab = "rti"; // 'rti', 'appeal', 'notice', 'section8', 'slip', 'report'
let radarAnimationId = null;

// Leaflet Map & Speech Recognition Instances
let leafletMap = null;
let leafletMarkersLayer = null;
let speechRecognizer = null;
let isListeningVoice = false;

function renderLucide() {
  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  }
}

function initApp() {
  try { initTheme(); } catch (e) { console.warn("Theme init:", e); }
  try { initLanguage(); } catch (e) { console.warn("Language init:", e); }
  try { setupNavigation(); } catch (e) { console.warn("Nav init:", e); }
  try { loadCaseQueue(); } catch (e) { console.warn("Queue init:", e); }
  try { loadRunLogs(); } catch (e) { console.warn("RunLog init:", e); }
  try { initLeafletPioMap(); } catch (e) { console.warn("Map init:", e); }
  try { initRadarAnimation(); } catch (e) { console.warn("Radar init:", e); }
  try { updatePioMapForCase(); } catch (e) { console.warn("PioMap init:", e); }
  try { loadCustomActs(); } catch (e) { console.warn("Acts init:", e); }
  try { renderLucide(); } catch (e) { console.warn("Lucide init:", e); }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initApp);
} else {
  initApp();
}

// Persona Switcher (Law Firm vs Gov Desk)
function switchPersona(persona) {
  activePersona = persona;
  const btnLaw = document.getElementById("btnPersonaLaw");
  const btnGov = document.getElementById("btnPersonaGov");

  if (persona === "law_firm") {
    btnLaw.classList.add("active");
    btnGov.classList.remove("active");
    const revInput = document.getElementById("reviewerName");
    if (revInput) revInput.value = "Adv. S. Kalra (Advocate on Record / Legal NGO)";
  } else {
    btnGov.classList.add("active");
    btnLaw.classList.remove("active");
    const revInput = document.getElementById("reviewerName");
    if (revInput) revInput.value = "Shri R. P. Maurya, IAS (Designated Public Authority)";
  }

  if (currentCase) {
    updateWorkspacePersonaView(currentCase);
  }
  renderLucide();
}

// Top-Level Site Navigation Router (Home, About, Pillars, Dashboard)
function showPage(pageId) {
  document.querySelectorAll(".nav-link-btn").forEach(b => b.classList.remove("active"));
  const navDashBtn = document.getElementById("navDashboardBtn");
  if (navDashBtn) navDashBtn.classList.remove("active");
  document.querySelectorAll(".site-page").forEach(p => p.classList.remove("active"));

  const navMap = {
    home: "siteNavHome",
    about: "siteNavAbout",
    pillars: "siteNavPillars"
  };

  const navBtn = navMap[pageId] ? document.getElementById(navMap[pageId]) : null;
  const pageEl = document.getElementById(`page-${pageId}`);

  if (navBtn) navBtn.classList.add("active");
  if ((pageId === "dashboard" || pageId === "case-detail") && navDashBtn) navDashBtn.classList.add("active");
  if (pageEl) {
    pageEl.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  if (pageId === "dashboard") {
    loadCaseQueue();
    loadRunLogs();
    loadCustomActs();
  } else if (pageId === "home") {
    loadCaseQueue();
  }

  renderLucide();
}

// Dashboard Sub-Tab Switcher (Casework, Statutory, PIO, Compliance, RunLog)
function switchDashTab(tabId) {
  showPage("dashboard");
  document.querySelectorAll(".desk-subnav-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".dash-module").forEach(m => m.classList.remove("active"));

  const subnavMap = {
    casework: "subnavCasework",
    statutory: "subnavStatutory",
    pio: "subnavPio",
    compliance: "subnavCompliance",
    runlog: "subnavRunlog"
  };

  const targetBtn = subnavMap[tabId] ? document.getElementById(subnavMap[tabId]) : null;
  const targetModule = document.getElementById(`dashtab-${tabId}`);

  if (targetBtn) targetBtn.classList.add("active");
  if (targetModule) targetModule.classList.add("active");

  if (tabId === "casework") loadCaseQueue();
  if (tabId === "statutory") loadCustomActs();
  if (tabId === "compliance") initSlaPenaltyCalculator();
  if (tabId === "pio") {
    updatePioMapForCase(currentCase);
    if (leafletMap) {
      setTimeout(() => leafletMap.invalidateSize(), 150);
    }
  }

  renderLucide();
}

// Backwards compatibility aliases
function switchMainModule(modName) {
  if (modName === "home" || modName === "about" || modName === "pillars") {
    showPage(modName);
  } else {
    switchDashTab(modName);
  }
}

function switchToTab(tabName) {
  if (tabName === "intake" || tabName === "queue" || tabName === "workspace") switchDashTab("casework");
  else if (tabName === "precedents") switchDashTab("statutory");
  else if (tabName === "radar") switchDashTab("pio");
  else if (tabName === "runlog") switchDashTab("runlog");
  else switchDashTab("casework");
}

function toggleIntakeForm() {
  const c = document.getElementById("intakeFormContainer");
  const t = document.getElementById("intakeToggleText");
  if (c) {
    if (c.style.display === "none") {
      c.style.display = "block";
      if (t) t.textContent = "Hide Form";
    } else {
      c.style.display = "none";
      if (t) t.textContent = "+ Expand Form";
    }
  }
}

function setupNavigation() {
  // Navigation setup
}

// Document Sub-Tabs in Legal Workspace
function switchDocTab(tabName) {
  currentDocTab = tabName;
  document.querySelectorAll(".doc-draft-tab, .doc-tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll("[id^='docPanel']").forEach(p => p.classList.add("hidden"));

  const btn = Array.from(document.querySelectorAll(".doc-draft-tab, .doc-tab-btn")).find(b =>
    b.dataset.doctab === tabName || b.textContent.toLowerCase().includes(tabName)
  );
  if (btn) btn.classList.add("active");

  const panelMap = {
    rti: "docPanelRti",
    appeal: "docPanelAppeal",
    notice: "docPanelNotice",
    section8: "docPanelSection8",
    slip: "docPanelSlip",
    report: "docPanelReport"
  };

  const panel = document.getElementById(panelMap[tabName]);
  if (panel) panel.classList.remove("hidden");

  if (tabName === "section8") {
    refreshSection8Shield();
  } else if (tabName === "slip") {
    renderTabPostalSlip();
  }
}

// Postal PIN Code Jurisdiction Resolver Client
let pincodeLookupTimeout = null;

async function handlePincodeInput(val) {
  const pin = (val || "").trim();
  const badge = document.getElementById("pincodeJurisdictionBadge");
  if (!badge) return;

  if (pincodeLookupTimeout) clearTimeout(pincodeLookupTimeout);

  if (pin.length !== 6 || !/^\d{6}$/.test(pin)) {
    badge.style.display = "none";
    badge.innerHTML = "";
    return;
  }

  pincodeLookupTimeout = setTimeout(async () => {
    badge.style.display = "block";
    badge.innerHTML = `<span style="color: var(--gov-navy); font-weight: 600;">Resolving official postal jurisdiction for PIN <b>${pin}</b>...</span>`;
    renderLucide();

    try {
      const res = await fetch(`${API_BASE}/cases/pincode-lookup?pincode=${pin}`);
      const data = await res.json();
      if (res.ok && data.status === "success") {
        const codex = data.land_codex || {};
        const pio = data.assigned_pio || {};
        badge.innerHTML = `
          <div style="display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 4px;">
            <div>
              <b style="color: var(--gov-navy);">✓ Verified Administrative Jurisdiction:</b>
              <span style="font-weight: 600; color: var(--ink-primary);">${data.district}, ${data.state} (${data.block || 'Taluk/Block'})</span>
            </div>
            <span style="font-size: 10px; color: var(--status-active); font-weight: 700;">Center: ${data.latitude?.toFixed(4)}, ${data.longitude?.toFixed(4)}</span>
          </div>
          <div style="margin-top: 3px; color: var(--ink-secondary); font-size: 10.5px;">
            <b>Designated PIO:</b> ${pio.pio_name || 'Tahsildar / Nodal Officer'} &bull; <i>${pio.designation || 'PIO'}</i>
          </div>
          <div style="margin-top: 2px; color: var(--gov-copper); font-size: 10px; font-weight: 600;">
            <b>State Land Law:</b> ${codex.primary_land_act || 'State Land Revenue Act'} &bull; <b>Portal:</b> ${codex.digital_land_portal || 'Digital Land Records'}
          </div>
        `;
      } else {
        badge.innerHTML = `<span style="color: #DC2626;">⚠ Could not resolve PIN ${pin}. Please verify the 6-digit postal code.</span>`;
      }
      renderLucide();
    } catch (err) {
      console.warn("Pincode lookup error:", err);
      badge.style.display = "none";
    }
  }, 250);
}

// Submit Citizen / Advocate Intake
async function submitIntake(event) {
  event.preventDefault();

  const pincodeInput = document.getElementById("complainantPincode");
  const pincode = pincodeInput ? pincodeInput.value.trim() : "";

  const complainant = {
    name: document.getElementById("complainantName").value.trim(),
    contact: document.getElementById("complainantContact").value.trim(),
    address: document.getElementById("complainantAddr").value.trim(),
    pincode: pincode,
    language: document.getElementById("complainantLang").value
  };

  const raw_grievance = document.getElementById("rawGrievance").value.trim();
  const application_ref_no = document.getElementById("intakeRefNo").value.trim();
  const original_submission_date = document.getElementById("intakeSubDate").value.trim();
  const is_urgent = document.getElementById("intakeUrgent") ? document.getElementById("intakeUrgent").checked : false;

  try {
    const res = await fetch(`${API_BASE}/cases/intake`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ complainant, raw_grievance, application_ref_no, original_submission_date, is_urgent, pincode })
    });

    const data = await res.json();
    if (res.ok) {
      document.getElementById("intakeForm").reset();
      const pBadge = document.getElementById("pincodeJurisdictionBadge");
      if (pBadge) { pBadge.style.display = "none"; pBadge.innerHTML = ""; }
      const mlBox = document.getElementById("liveMlPredictionBox");
      if (mlBox) { mlBox.style.display = "none"; mlBox.innerHTML = ""; }
      currentCase = data.case;
      populateWorkspaceFields(data.case);

      // Update PIO map for this registered complaint
      updatePioMapForCase(data.case);

      // Switch to PIO Geospatial Map tab
      showPage("dashboard");
      switchDashTab("pio");

      // Show the banner on the PIO map
      const banner = document.getElementById("pioRegistrationBanner");
      const bannerText = document.getElementById("pioBannerText");
      if (banner && bannerText) {
        const pio = data.case.suggested_pio || {};
        const nearbyCount = data.case.nearby_area_pios ? data.case.nearby_area_pios.length : 5;
        const areaLabel = data.case.district ? `${data.case.district}, ${data.case.state} (${data.case.pincode || ''})` : (pio.matched_user_locality || 'Local Division');
        bannerText.innerHTML = `✓ Docket <b>${data.case.case_id}</b> Registered in <b>${areaLabel}</b>! Assigned nearest domain (<b>${data.case.department}</b>) PIO: <b>${pio.pio_name}</b> (${pio.distance_label}). All ${nearbyCount} district/area public authorities mapped below.`;
        banner.style.display = "block";
      }

      loadCaseQueue();
      loadRunLogs();
    } else {
      alert(`Error: ${data.message || "Failed to create case"}`);
    }
  } catch (err) {
    console.error("Intake error:", err);
    alert("Connection error submitting intake.");
  }
}

// All-India Civic Presets Loader (28 States & 8 UTs)
function loadPreset(num) {
  switchMainModule("casework");
  const c = document.getElementById("intakeFormContainer");
  if (c) c.style.display = "block";

  const urgentCheckbox = document.getElementById("intakeUrgent");
  if (urgentCheckbox) urgentCheckbox.checked = false;

  let pinToResolve = "";

  if (num === 1) {
    // 1. Delhi PDS Ration
    document.getElementById("complainantName").value = "Sunita Devi";
    document.getElementById("complainantContact").value = "+91-9876543210";
    document.getElementById("complainantAddr").value = "House No. 45, BPL Cluster, Civil Lines, Delhi";
    document.getElementById("complainantPincode").value = "110054";
    document.getElementById("intakeRefNo").value = "RC-88492";
    document.getElementById("intakeSubDate").value = "15-Feb-2026";
    document.getElementById("rawGrievance").value = "My family's BPL ration card application (Ref No. RC-88492) was submitted on 15-Feb-2026 at Civil Lines supply office. We have not received the card or food grains. Staff refuses to disclose stock registers.";
    pinToResolve = "110054";
  } else if (num === 2) {
    // 2. Karnataka Bhoomi Land Mutation (Bengaluru North)
    document.getElementById("complainantName").value = "Basavaraj Gowda";
    document.getElementById("complainantContact").value = "+91-9845012345";
    document.getElementById("complainantAddr").value = "Indiranagar, Bengaluru North, Karnataka";
    document.getElementById("complainantPincode").value = "560001";
    document.getElementById("intakeRefNo").value = "BLR-MUT-7701";
    document.getElementById("intakeSubDate").value = "18-Jan-2026";
    document.getElementById("rawGrievance").value = "My application for land title mutation and RTC Pahani extract transfer on the Karnataka Bhoomi portal (Ref BLR-MUT-7701) was submitted on 18-Jan-2026. Tahsildar office Bangalore North has kept the file pending past 30 days without reasons. Revenue Inspector refuses inspection.";
    pinToResolve = "560001";
  } else if (num === 3) {
    // 3. Maharashtra 7/12 Satbara Land Title (Mumbai)
    document.getElementById("complainantName").value = "Sachin Deshmukh";
    document.getElementById("complainantContact").value = "+91-9820011223";
    document.getElementById("complainantAddr").value = "Fort, South Mumbai, Maharashtra";
    document.getElementById("complainantPincode").value = "400001";
    document.getElementById("intakeRefNo").value = "MH-FER-4521";
    document.getElementById("intakeSubDate").value = "05-Jan-2026";
    document.getElementById("rawGrievance").value = "Application for Ferfar mutation entry and Satbara 7/12 extract on MahaBhulekh portal (Ref MH-FER-4521) registered under Section 149 & 150 Maharashtra Land Revenue Code 1966. Talathi and Tahsildar have failed to issue certified extract or show cause notice.";
    pinToResolve = "400001";
  } else if (num === 4) {
    // 4. Rajasthan Land Demarcation (Jaipur)
    document.getElementById("complainantName").value = "Kailash Choudhary";
    document.getElementById("complainantContact").value = "+91-9414055667";
    document.getElementById("complainantAddr").value = "C-Scheme, Jaipur, Rajasthan";
    document.getElementById("complainantPincode").value = "302001";
    document.getElementById("intakeRefNo").value = "RJ-JAM-9912";
    document.getElementById("intakeSubDate").value = "12-Dec-2025";
    document.getElementById("rawGrievance").value = "Application for land demarcation and Namantaran mutation under Section 133 & 135 Rajasthan Land Revenue Act 1956 and Apna Khata portal. Patwari is refusing field measurement and boundary verification despite receipt of demarcation fee.";
    pinToResolve = "302001";
  } else if (num === 5) {
    // 5. Varanasi Land Khasra (Varanasi / Banaras)
    document.getElementById("complainantName").value = "Shivanshu Pandey";
    document.getElementById("complainantContact").value = "+91-9988776655";
    document.getElementById("complainantAddr").value = "Assi Ghat, Varanasi / Banaras, Uttar Pradesh";
    document.getElementById("complainantPincode").value = "221005";
    document.getElementById("intakeRefNo").value = "VNS-99401";
    document.getElementById("intakeSubDate").value = "10-Jan-2026";
    document.getElementById("rawGrievance").value = "My land mutation khasra 88/14 application (Ref VNS-99401) submitted on 10-Jan-2026 at Tehsil Kachehri Varanasi under UP Revenue Code 2006 is pending beyond the 30-day statutory limit. Lekhpal is refusing to update the revenue registry on UP Bhulekh.";
    pinToResolve = "221005";
  } else if (num === 6) {
    // 6. Bihar Land Mutation (Patna)
    document.getElementById("complainantName").value = "Pradeep Kumar Yadav";
    document.getElementById("complainantContact").value = "+91-9709012345";
    document.getElementById("complainantAddr").value = "Kankarbagh, Patna, Bihar";
    document.getElementById("complainantPincode").value = "800001";
    document.getElementById("intakeRefNo").value = "BR-RTPS-6621";
    document.getElementById("intakeSubDate").value = "20-Jan-2026";
    document.getElementById("rawGrievance").value = "Dakhil Kharij mutation application under Section 6 & 9 of the Bihar Land Mutation Act 2011 and Bihar RTPS portal (Ref BR-RTPS-6621). Circle Officer (Anchal Adhikari) Patna has failed to dispose mutation petition within the prescribed statutory period.";
    pinToResolve = "800001";
  } else if (num === 7) {
    // 7. 48h ICU Emergency (AIIMS Delhi)
    document.getElementById("complainantName").value = "Dr. Anil Sharma";
    document.getElementById("complainantContact").value = "+91-9811223344";
    document.getElementById("complainantAddr").value = "Trauma Center, AIIMS, Ansari Nagar, New Delhi";
    document.getElementById("complainantPincode").value = "110029";
    document.getElementById("intakeRefNo").value = "MED-91142";
    document.getElementById("intakeSubDate").value = "Today 08:00 AM";
    document.getElementById("rawGrievance").value = "CRITICAL EMERGENCY: Catastrophic ventilator power failure and acute oxygen cylinder stock-out in ICU Ward 3B posing imminent threat to human life. Demanding immediate maintenance logbooks, cylinder delivery challans, and duty roasters under Section 7(1) Proviso (48-Hour SLA).";
    if (urgentCheckbox) urgentCheckbox.checked = true;
    pinToResolve = "110029";
  } else if (num === 8) {
    // 8. Police FIR Inaction (Prayagraj)
    document.getElementById("complainantName").value = "Kavita Verma";
    document.getElementById("complainantContact").value = "+91-9871100223";
    document.getElementById("complainantAddr").value = "Civil Lines, Prayagraj, Uttar Pradesh";
    document.getElementById("complainantPincode").value = "211001";
    document.getElementById("intakeRefNo").value = "FIR-552";
    document.getElementById("intakeSubDate").value = "02-Mar-2026";
    document.getElementById("rawGrievance").value = "Police Station SHO refuses to register mandatory FIR under Section 173 BNSS (old Section 154 CrPC) regarding violent armed snatching incident at market junction. Sub-Inspector refuses to provide GD entry copy or acknowledge complaint.";
    pinToResolve = "211001";
  } else if (num === 9) {
    // 9. Delhi Electricity Outage / Discom
    document.getElementById("complainantName").value = "Virender Gupta";
    document.getElementById("complainantContact").value = "+91-9810234567";
    document.getElementById("complainantAddr").value = "Kalkaji, South Delhi, Delhi";
    document.getElementById("complainantPincode").value = "110019";
    document.getElementById("intakeRefNo").value = "DISCOM-PWR-44910";
    document.getElementById("intakeSubDate").value = "28-Feb-2026";
    document.getElementById("rawGrievance").value = "Severe recurrent unscheduled power outage and burned distribution transformer causing blackout for 5 days. BSES / Discom division junior engineer refuses to restore power grid or provide breakdown inspection logbook.";
    pinToResolve = "110019";
  } else if (num === 10) {
    // 10. Varanasi Jal Board / Water Contamination
    document.getElementById("complainantName").value = "Manoj Tripathy";
    document.getElementById("complainantContact").value = "+91-9793112244";
    document.getElementById("complainantAddr").value = "Bhelupur, Varanasi, Uttar Pradesh";
    document.getElementById("complainantPincode").value = "221010";
    document.getElementById("intakeRefNo").value = "JAL-SAN-78219";
    document.getElementById("intakeSubDate").value = "01-Mar-2026";
    document.getElementById("rawGrievance").value = "Severe water pipeline contamination with sewage backflow into municipal drinking water supply lines. Varanasi Jal Sansthan executive engineer has ignored repeated samples and lab test reports.";
    pinToResolve = "221010";
  } else if (num === 11) {
    // 11. Delhi Transport / RTO License Renewal
    document.getElementById("complainantName").value = "Rajesh Narang";
    document.getElementById("complainantContact").value = "+91-9811445566";
    document.getElementById("complainantAddr").value = "Mayur Vihar Phase 1, East Delhi, Delhi";
    document.getElementById("complainantPincode").value = "110013";
    document.getElementById("intakeRefNo").value = "DL-RTO-55201";
    document.getElementById("intakeSubDate").value = "12-Jan-2026";
    document.getElementById("rawGrievance").value = "Commercial driving license renewal and vehicle fitness RC endorsement application pending at Sarai Kale Khan RTO for over 60 days. Motor Licensing Officer refusing to issue smart card without illicit speed money.";
    pinToResolve = "110013";
  } else if (num === 12) {
    // 12. Delhi EPFO Pension Delay
    document.getElementById("complainantName").value = "Harcharan Singh";
    document.getElementById("complainantContact").value = "+91-9871556677";
    document.getElementById("complainantAddr").value = "Ashok Vihar, North West Delhi, Delhi";
    document.getElementById("complainantPincode").value = "110052";
    document.getElementById("intakeRefNo").value = "EPFO-PPO-33019";
    document.getElementById("intakeSubDate").value = "05-Nov-2025";
    document.getElementById("rawGrievance").value = "Retired senior citizen EPS-95 pension claim and PPO Pension Payment Order disbursal settlement pending at EPFO Wazirpur Regional Office for 120 days. Assistant Provident Fund Commissioner has failed to release accumulated superannuation pension arrears.";
    pinToResolve = "110052";
  } else if (num === 13) {
    // 13. Delhi Environment & Chemical Pollution
    document.getElementById("complainantName").value = "Anita Saxena";
    document.getElementById("complainantContact").value = "+91-9899887711";
    document.getElementById("complainantAddr").value = "Shahdara Industrial Area, Delhi";
    document.getElementById("complainantPincode").value = "110032";
    document.getElementById("intakeRefNo").value = "DPCC-ENV-90214";
    document.getElementById("intakeSubDate").value = "15-Jan-2026";
    document.getElementById("rawGrievance").value = "Illegal chemical electroplating factory emitting toxic noxious fumes and releasing untreated acidic effluent directly into residential open drains in violation of Air and Water Acts. DPCC pollution control board has failed to seal units.";
    pinToResolve = "110032";
  }

  if (pinToResolve) {
    handlePincodeInput(pinToResolve);
  }

  // Auto-run ML Domain Prediction on the loaded preset
  triggerLiveMlPrediction();

  // Scroll to intake form smoothly
  const intakeForm = document.getElementById("intakeForm");
  if (intakeForm) intakeForm.scrollIntoView({ behavior: "smooth", block: "center" });
}

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// Live ML Domain & Public Authority Prediction
async function triggerLiveMlPrediction() {
  const grievanceEl = document.getElementById("rawGrievance");
  const box = document.getElementById("liveMlPredictionBox");
  if (!grievanceEl || !box) return;

  const text = grievanceEl.value.trim();
  if (!text) {
    box.style.display = "block";
    box.innerHTML = `
      <div style="background:#fffbeb; border:1px solid #fef3c7; border-left:4px solid #f59e0b; border-radius:6px; padding:8px 12px; font-size:12px; color:#92400e; display:flex; align-items:center; gap:8px;">
        <span>⚠️</span>
        <span>Please enter or load grievance details first to run the ML domain prediction model.</span>
      </div>
    `;
    return;
  }

  box.style.display = "block";
  box.innerHTML = `
    <div style="background:#f0fdfa; border:1px solid #ccfbf1; border-radius:6px; padding:8px 12px; font-size:12px; color:#0f766e; display:flex; align-items:center; gap:8px;">
      <span class="spinner-border spinner-border-sm" role="status" style="width:14px; height:14px; border-width:2px;"></span>
      <span>Running ML civic classification algorithms (TF-IDF keyword matching & domain heuristics)...</span>
    </div>
  `;

  try {
    const res = await fetch(`${API_BASE}/cases/classify-domain`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    if (!res.ok) {
      box.innerHTML = `
        <div style="background:#fef2f2; border:1px solid #fee2e2; border-left:4px solid #ef4444; border-radius:6px; padding:8px 12px; font-size:12px; color:#991b1b;">
          ❌ ML Prediction error: ${escapeHtml(data.detail || data.error || "Failed to classify grievance")}
        </div>
      `;
      return;
    }

    const conf = Math.round(data.confidence || 0);
    const domain = escapeHtml(data.domain || "general");
    const domainUpper = domain.toUpperCase();
    const triggers = (data.triggers || []).map(t => `<span class="badge" style="font-size:10px; background:#e6fffa; color:#0d9488; border:1px solid #99f6e4; padding:2px 6px; border-radius:4px; margin-right:4px;">${escapeHtml(t)}</span>`).join("");
    const pio = data.pio || {};
    const pioInfo = pio.name ? `<div style="margin-top:5px; font-size:11px; color:#475569; border-top:1px dashed #ccfbf1; padding-top:4px;"><strong>Target Public Authority / PIO:</strong> ${escapeHtml(pio.name)} (${escapeHtml(pio.department || pio.public_authority || "")}) &bull; <em>${escapeHtml(pio.designation || "Public Information Officer")}</em></div>` : "";

    box.innerHTML = `
      <div style="background:#f0fdfa; border:1px solid #5eead4; border-left:4px solid #0d9488; border-radius:6px; padding:10px 14px; font-size:12px; color:#134e4a; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
          <span style="font-weight:700; font-size:13px; color:#0f766e;">
            🤖 ML Classified Domain: <span style="background:#0d9488; color:#fff; padding:2px 8px; border-radius:12px; font-size:11px;">${domainUpper}</span>
          </span>
          <span style="font-weight:700; color:#0d9488; font-size:12px;">Confidence: ${conf}%</span>
        </div>
        <div style="color:#334155; font-size:11px; margin-bottom:4px;">${escapeHtml(data.reason || "")}</div>
        ${triggers ? `<div style="margin-top:4px; display:flex; align-items:center; flex-wrap:wrap; gap:4px;"><span style="font-size:10px; color:#64748b; font-weight:600;">Trigger Keywords:</span> ${triggers}</div>` : ""}
        ${pioInfo}
      </div>
    `;
  } catch (err) {
    box.innerHTML = `
      <div style="background:#fef2f2; border:1px solid #fee2e2; border-left:4px solid #ef4444; border-radius:6px; padding:8px 12px; font-size:12px; color:#991b1b;">
        ❌ Connection error connecting to ML service: ${escapeHtml(err.message)}
      </div>
    `;
  }
}

// Queue Listing & Global Multi-Field Search
async function loadCaseQueue() {
  const searchQuery = document.getElementById("caseSearchInput") ? document.getElementById("caseSearchInput").value.trim() : "";
  const filter = document.getElementById("queueFilter") ? document.getElementById("queueFilter").value : "";

  let url = `${API_BASE}/cases?`;
  if (filter) url += `status=${encodeURIComponent(filter)}&`;
  if (searchQuery) url += `search=${encodeURIComponent(searchQuery)}`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    if (!res.ok) return;

    // Update Counts
    const statInbox = document.getElementById("statInbox");
    if (statInbox) statInbox.textContent = data.counts.inbox;
    const statApproved = document.getElementById("statApproved");
    if (statApproved) statApproved.textContent = data.counts.approved;
    const statAtRisk = document.getElementById("statAtRisk");
    if (statAtRisk) statAtRisk.textContent = data.counts.at_risk;
    const statTotal = document.getElementById("statTotal");
    if (statTotal) statTotal.textContent = data.counts.total;
    const inboxCount = document.getElementById("inboxCount");
    if (inboxCount) inboxCount.textContent = data.counts.inbox;
    const homeBadge = document.getElementById("homeQueueBadge");
    if (homeBadge) homeBadge.textContent = data.counts.inbox;
    const homeInboxEl = document.getElementById("homeStatInbox");
    if (homeInboxEl) homeInboxEl.textContent = data.counts.inbox;
    const homeTotalEl = document.getElementById("homeStatTotal");
    if (homeTotalEl) homeTotalEl.textContent = data.counts.total;

    const tbody = document.getElementById("caseQueueBody");
    tbody.innerHTML = "";

    if (data.cases.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 24px;">No matching cases found for keyword "${searchQuery}".</td></tr>`;
      return;
    }

    allCasesCache = data.cases || [];

    // Auto-select first case if none is selected yet
    if (!currentCase && data.cases.length > 0) {
      currentCase = data.cases[0];
      populateWorkspaceFields(data.cases[0]);
      updatePioMapForCase(data.cases[0]);
    }

    data.cases.forEach(c => {
      const tr = document.createElement("tr");
      tr.style.cursor = "pointer";
      tr.onclick = () => openCaseById(c.case_id);

      const pio = c.suggested_pio || {};
      const legal = c.statutory_legal_analysis || {};
      const ipcBrief = legal.ipc_sections ? legal.ipc_sections[0] : "IPC Sec 420";
      const bnsBrief = legal.bns_sections ? legal.bns_sections[0] : "BNS Sec 318(4)";
      const distLabel = pio.distance_label || (c.geospatial_meta ? c.geospatial_meta.distance_label : "1.5 km away");
            const statusMap = {
        "APPROVED": currentLang === "hi" ? "स्वीकृत" : (currentLang === "bi" ? "APPROVED • स्वीकृत" : "APPROVED"),
        "TRANSFERRED_SEC_6_3": currentLang === "hi" ? "अंतरित (धारा 6(3))" : (currentLang === "bi" ? "TRANSFERRED • अंतरित" : "TRANSFERRED (SEC 6(3))"),
        "NEEDS_REVIEW": currentLang === "hi" ? "समीक्षाधीन" : (currentLang === "bi" ? "UNDER REVIEW • समीक्षाधीन" : "UNDER REVIEW"),
        "UNDER_REVIEW": currentLang === "hi" ? "समीक्षाधीन" : (currentLang === "bi" ? "UNDER REVIEW • समीक्षाधीन" : "UNDER REVIEW"),
        "REJECTED": currentLang === "hi" ? "अस्वीकृत" : (currentLang === "bi" ? "REJECTED • अस्वीकृत" : "REJECTED")
      };
      const displayStatus = statusMap[c.status] || c.status;
      tr.innerHTML = `
        <td><b style="font-family: var(--font-mono); color: var(--gov-navy); font-size: 11.5px;">${c.case_id}</b></td>
        <td><b>${c.complainant.name}</b><br/><span style="font-size: 10px; color: var(--ink-muted);">${c.complainant.address || 'Local'}${c.pincode ? ' (' + c.pincode + ')' : ''}</span></td>
        <td><b>${c.department}</b><br/><span style="font-size: 10px; color: var(--gov-copper);">${legal.statutory_infraction || 'Administrative Infraction'}</span></td>
        <td><span class="statutory-tag bns" style="font-size: 9.5px; padding: 1px 4px;">${bnsBrief}</span><br/><span class="statutory-tag ipc" style="font-size: 9.5px; padding: 1px 4px; margin-top: 2px;">${ipcBrief}</span></td>
        <td><b>${pio.pio_name || 'Designated PIO'}</b><br/><span style="font-size: 9.5px; color: var(--status-active); font-family: var(--font-mono);">${distLabel}</span></td>
        <td><span class="status-pill ${c.status === 'APPROVED' ? 'approved' : (c.status === 'TRANSFERRED_SEC_6_3' ? 'transferred' : 'under-review')}">● ${displayStatus}</span></td>
        <td><button class="btn-gov-outline btn-view-docket" style="padding: 3px 8px; font-size: 10.5px;" onclick="event.stopPropagation(); openCaseById('${c.case_id}')">${t("btn_view")}</button></td>
      `;
      tbody.appendChild(tr);
    });
    renderLucide();
  } catch (err) {
    console.error("Queue load error:", err);
  }
}

async function openCaseById(caseId) {
  try {
    const res = await fetch(`${API_BASE}/cases/${caseId}`);
    const data = await res.json();
    if (res.ok) {
      openCaseWorkspace(data.case);
      switchMainModule("casework");
    }
  } catch (err) {
    console.error("Open case error:", err);
  }
}

// Workspace Renderer
function openCaseWorkspace(c) {
  currentCase = c;
  populateWorkspaceFields(c);
  updatePioMapForCase(c);
  switchMainModule("casework");
}

function populateWorkspaceFields(c) {
  const emptyState = document.getElementById("noCaseSelected");
  const workspaceView = document.getElementById("caseWorkspaceView");
  if (emptyState) emptyState.classList.add("hidden");
  if (workspaceView) workspaceView.classList.remove("hidden");

  document.getElementById("viewCaseId").textContent = c.case_id;

        const statusMap = {
        "APPROVED": currentLang === "hi" ? "स्वीकृत" : (currentLang === "bi" ? "APPROVED • स्वीकृत" : "APPROVED"),
        "TRANSFERRED_SEC_6_3": currentLang === "hi" ? "अंतरित (धारा 6(3))" : (currentLang === "bi" ? "TRANSFERRED • अंतरित" : "TRANSFERRED (SEC 6(3))"),
        "NEEDS_REVIEW": currentLang === "hi" ? "समीक्षाधीन" : (currentLang === "bi" ? "UNDER REVIEW • समीक्षाधीन" : "UNDER REVIEW"),
        "UNDER_REVIEW": currentLang === "hi" ? "समीक्षाधीन" : (currentLang === "bi" ? "UNDER REVIEW • समीक्षाधीन" : "UNDER REVIEW"),
        "REJECTED": currentLang === "hi" ? "अस्वीकृत" : (currentLang === "bi" ? "REJECTED • अस्वीकृत" : "REJECTED")
      };

  const statusEl = document.getElementById("viewCaseStatus");
  if (statusEl) {
    statusEl.textContent = `● ${statusMap[c.status] || c.status}`;
    statusEl.className = `status-pill ${c.status === 'APPROVED' ? 'approved' : (c.status === 'TRANSFERRED_SEC_6_3' ? 'transferred' : 'under-review')}`;
  }

  document.getElementById("viewComplainant").textContent = c.complainant.name;
  document.getElementById("viewRawGrievance").textContent = `"${c.raw_grievance}"`;

  // Pan-India Jurisdiction & State Land Codex Banner
  const jurisBanner = document.getElementById("viewJurisdictionBanner");
  const jurisArea = document.getElementById("viewJurisdictionArea");
  const portalLink = document.getElementById("viewDigitalPortalLink");
  const landActEl = document.getElementById("viewPrimaryLandAct");

  const pio = c.suggested_pio || {};
  const faa = c.suggested_faa || pio.faa || {};
  const juris = c.statutory_jurisdiction || pio.statutory_jurisdiction || {};
  const district = c.district || pio.district;
  const state = c.state || pio.state;
  const pin = c.pincode || pio.pincode;

  if (jurisBanner) {
    if (district || state || pin || juris.primary_land_act || juris.substantive_act) {
      jurisBanner.style.display = "block";
      const areaParts = [];
      if (district) areaParts.push(district);
      if (state) areaParts.push(state);
      const pinStr = pin ? ` [PIN: ${pin}]` : "";
      if (jurisArea) jurisArea.textContent = `${areaParts.join(", ")}${pinStr}`;

      const portal = juris.digital_portal || juris.digital_land_portal;
      const rtiPortal = juris.state_rti_portal || juris.rti_portal_url;
      let portalTxt = "";
      if (portal) portalTxt += `Portal: ${portal}`;
      if (rtiPortal) portalTxt += `${portal ? ' • ' : ''}RTI: ${rtiPortal}`;
      if (portalLink) portalLink.textContent = portalTxt || "State Civic Records";

      const landAct = juris.primary_land_act || juris.substantive_act || "Citizen Charter & Public Service Guarantee Act";
      if (landActEl) landActEl.textContent = landAct;
    } else {
      jurisBanner.style.display = "none";
    }
  }

  const legal = c.statutory_legal_analysis || {};
  document.getElementById("viewMeritBadge").textContent = `${legal.case_merit_score || 92}/100 Merit • योग्यता (${legal.win_probability || 'High'} • उच्च)`;

  const pen = legal.section_20_penalty_liability_inr || 0;
  document.getElementById("viewPenaltyBadge").textContent = `Section 20(1) Penalty Liability: ₹${pen} (Mandatory ₹250/day deduction applicable on delinquent PIO) • धारा 20(1) जुर्माना: ₹${pen} (अधिकारी के वेतन से ₹250/दिन अनिवार्य कटौती)`;

  // 48-Hour Urgent Life & Liberty Status
  const isUrgent = !!(c.is_life_liberty || c.is_urgent_48h);
  const urgencyBadge = document.getElementById("viewUrgencyBadge");
  const urgencyBtn = document.getElementById("dossierUrgencyToggleBtn");
  const urgencyLabel = document.getElementById("dossierUrgencyLabel");
  const dueDateEl = document.getElementById("viewDueDate");
  const slaEl = document.getElementById("viewSla");

  if (isUrgent) {
    if (urgencyBadge) urgencyBadge.style.display = "inline-block";
    if (urgencyBtn) urgencyBtn.classList.add("active");
    if (urgencyLabel) urgencyLabel.textContent = "Fast-Track Active (48-Hr SLA) • 48 घंटे आपातकालीन";
    if (slaEl) slaEl.textContent = "🚨 48 Hours (URGENT LIFE & LIBERTY) • 48 घंटे आपातकाल";
    if (dueDateEl) dueDateEl.textContent = `Statutory Deadline: ${c.statutory_deadline_date || c.calculated_due_date || "Within 48 Hours"} • अंतिम तिथि (48 घंटे)`;
  } else {
    if (urgencyBadge) urgencyBadge.style.display = "none";
    if (urgencyBtn) urgencyBtn.classList.remove("active");
    if (urgencyLabel) urgencyLabel.textContent = "Fast-Track (48-Hr Life & Liberty) • 48 घंटे आपातकाल";
    if (slaEl) slaEl.textContent = `${c.sla_days_remaining || 30} Days Remaining • दिन शेष`;
    if (dueDateEl) dueDateEl.textContent = `Statutory Deadline: ${c.statutory_deadline_date || c.calculated_due_date || "30 Days"} • विधिक समयसीमा`;
  }

  document.getElementById("viewRefNo").textContent = c.application_ref_no || "Not Provided";
  document.getElementById("viewSubDate").textContent = c.original_submission_date || "Unconfirmed";

  // PIO & FAA Block
  document.getElementById("viewDistanceLabel").textContent = pio.distance_label || "1.5 km away";
  document.getElementById("viewPioName").textContent = pio.pio_name || "Designated PIO";
  document.getElementById("viewPioDept").textContent = pio.department || c.department;
  document.getElementById("viewPioAddr").textContent = pio.office_address || "District Kachehri";
  document.getElementById("viewPioRoom").textContent = `Room: ${pio.room_no || 'Room 101, Ground Floor'} &middot; Email: ${pio.email || 'N/A'}`;

  document.getElementById("viewFaaName").textContent = faa.faa_name || "Additional District Magistrate (Revenue)";

  // Statutory Pills (IPC & BNS)
  const ipcPillsBox = document.getElementById("viewIpcPills");
  const bnsPillsBox = document.getElementById("viewBnsPills");
  ipcPillsBox.innerHTML = "";
  bnsPillsBox.innerHTML = "";

  (legal.ipc_sections || ["IPC Section 420 (Cheating)", "IPC Section 166 (Disobedience of Law)"]).forEach(s => {
    const span = document.createElement("span");
    span.className = "statutory-tag ipc";
    span.style.cssText = "margin-right: 4px; margin-bottom: 4px; display: inline-block;";
    span.textContent = s;
    ipcPillsBox.appendChild(span);
  });

  (legal.bns_sections || ["BNS Section 318(4) (Cheating)", "BNS Section 198 (Public Servant Disobedience)"]).forEach(s => {
    const span = document.createElement("span");
    span.className = "statutory-tag bns";
    span.style.cssText = "margin-right: 4px; margin-bottom: 4px; display: inline-block;";
    span.textContent = s;
    bnsPillsBox.appendChild(span);
  });

  const ipcCountEl = document.getElementById("viewIpcCount");
  const bnsCountEl = document.getElementById("viewBnsCount");
  if (ipcCountEl) ipcCountEl.textContent = `${(legal.ipc_sections || []).length} Sections`;
  if (bnsCountEl) bnsCountEl.textContent = `${(legal.bns_sections || []).length} Sections`;
  const maxPunEl = document.getElementById("viewMaxPunishment");
  if (maxPunEl) maxPunEl.textContent = legal.maximum_punishment || "Rigorous Imprisonment + Fine";

  const groundsList = document.getElementById("viewLegalGrounds");
  groundsList.innerHTML = "";
  (legal.legal_grounds || ["Statutory failure under Citizen Charter"]).forEach(g => {
    const li = document.createElement("li");
    li.textContent = g;
    groundsList.appendChild(li);
  });

  // Draft RTI Inputs
  document.getElementById("editDraftSubject").value = c.draft_rti?.application_subject || "";
  document.getElementById("editDraftQuestions").value = (c.draft_rti?.questions || []).join("\n");
  document.getElementById("editDraftFees").value = c.draft_rti?.fees_paid || "Rs. 10 IPO under Rule 3 Central RTI Rules 2012";

  // First Appeal Panel
  const appeal = c.first_appeal_draft || {};
  document.getElementById("viewAppealSubject").value = appeal.subject || `FIRST APPEAL UNDER SECTION 19(1) IN CASE ${c.case_id}`;
  document.getElementById("viewAppealGrounds").value = (appeal.grounds_of_appeal || []).join("\n\n");
  document.getElementById("viewAppealPrayers").value = (appeal.prayers_sought || []).join("\n");

  // Legal Notice Panel
  const notice = c.legal_notice_draft || {};
  document.getElementById("viewLegalNoticeText").value = notice.notice_text || "";

  // ML Dossier
  document.getElementById("viewMlReportFormat").value = c.ml_report_format || "";

  // Timeline
  renderCaseTimeline(c);

  // Dispatch Proof
  const proofBox = document.getElementById("dispatchProofBox");
  if (c.dispatch_info) {
    proofBox.classList.remove("hidden");
    document.getElementById("proofDetails").innerHTML = `
      <div>DISPATCH ID / प्रेषण संख्या: <b>${c.dispatch_info.dispatch_id}</b></div>
      <div>TRACKING ID / ट्रैकिंग नंबर: <b>${c.dispatch_info.tracking_id}</b></div>
      <div>DISPATCHED AT / प्रेषण तिथि: <b>${c.dispatch_info.dispatched_at}</b></div>
      <div>RECIPIENT / प्राप्तकर्ता: <b>${c.dispatch_info.recipient_name} (${c.dispatch_info.recipient_email})</b></div>
    `;
    document.getElementById("approveBtn").disabled = true;
    document.getElementById("approveBtn").textContent = "CASE DISPATCHED & SEALED ✓ • प्रेषण सम्पन्न एवं मुहरबंद";
  } else {
    proofBox.classList.add("hidden");
    document.getElementById("approveBtn").disabled = false;
    document.getElementById("approveBtn").textContent = "⚖️ APPROVE & EXECUTE DISPATCH • विधिक प्रेषण स्वीकृत करें →";
  }

  updateRadarTelemetry(c);
  updateWorkspacePersonaView(c);
}

function updateWorkspacePersonaView(c) {
  if (activePersona === "gov_desk") {
    document.getElementById("approveBtn").innerHTML = `<i data-lucide="check-check"></i> <span>Dispose / Approve on Gov Desk • सरकारी डेस्क पर निस्तारण</span>`;
  } else {
    document.getElementById("approveBtn").innerHTML = `<i data-lucide="send"></i> <span>Approve & Execute Dispatch • विधिक प्रेषण स्वीकृत करें</span>`;
  }
  renderLucide();
}

function renderCaseTimeline(c) {
  const container = document.getElementById("caseTimelineContainer");
  const tbody = document.getElementById("caseHistoryBody");
  container.innerHTML = "";
  tbody.innerHTML = "";

  if (c.update_history && c.update_history.length > 0) {
    c.update_history.forEach((h, idx) => {
      const isLatest = idx === c.update_history.length - 1;
      const card = document.createElement("div");
      card.style.cssText = `display: flex; gap: 12px; padding: 8px 12px; background: var(--bg-primary); border: 1px solid var(--border-color); border-left: 3px solid ${isLatest ? 'var(--accent-gold)' : 'var(--text-muted)'}; border-radius: 4px; margin-bottom: 6px; font-size: 11px;`;
      card.innerHTML = `
        <div class="text-mono" style="min-width: 130px; color: var(--text-muted);">${h.timestamp}</div>
        <div>
          <b>${h.update_type}</b> — <span style="color: var(--text-secondary);">${h.actor}</span>
          <div style="color: var(--text-secondary); margin-top: 2px;">Field: <b>${h.field_changed}</b> &nbsp;|&nbsp; <code>${h.old_value}</code> &rarr; <code>${h.new_value}</code></div>
          ${h.remarks ? `<div style="color: var(--text-muted); font-style: italic; margin-top: 2px;">"${h.remarks}"</div>` : ''}
        </div>
      `;
      container.appendChild(card);

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="text-mono">${h.timestamp}</td>
        <td><span class="badge badge-gold">${h.update_type}</span></td>
        <td><b>${h.actor}</b></td>
        <td>${h.field_changed}</td>
        <td><small class="text-mono">Old: ${h.old_value}<br/>New: <b>${h.new_value}</b></small></td>
      `;
      tbody.appendChild(tr);
    });
  } else {
    container.innerHTML = `<div class="text-mono" style="font-size: 11px; color: var(--text-muted);">No prior timeline events.</div>`;
  }
}

// Section 6(3) Transfer Modal & Execution
function openTransferModal() {
  if (!currentCase) return;
  document.getElementById("transferModal").classList.remove("hidden");
}

function closeTransferModal() {
  document.getElementById("transferModal").classList.add("hidden");
}

async function submitTransferSec6_3() {
  if (!currentCase) return;
  const targetDept = document.getElementById("transferDeptSelect").value;
  const reason = document.getElementById("transferReason").value.trim();
  const reviewer = document.getElementById("reviewerName").value.trim();

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/transfer-sec6-3`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_department: targetDept, transfer_reason: reason, reviewer })
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Section 6(3) 5-Day Mandatory Transfer Executed!\n\n• Transferred to: ${targetDept}\n• Transferee PIO: ${data.case.suggested_pio?.pio_name}\n• Transfer ID: ${data.case.section_6_3_transfer?.transfer_id}`);
      closeTransferModal();
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Transfer error:", err);
  }
}

// Approve & Dispatch
async function approveCurrentCase() {
  if (!currentCase) return;

  const reviewer = document.getElementById("reviewerName").value.trim();
  const action = document.getElementById("reviewActionSelect").value;
  const subject = document.getElementById("editDraftSubject").value.trim();
  const questions = document.getElementById("editDraftQuestions").value.trim().split("\n").filter(q => q.trim());

  const payload = {
    reviewer: reviewer || "Adv. S. Kalra",
    notes: `Approved under action: ${action}`,
    draft_rti: {
      application_subject: subject,
      questions: questions
    }
  };

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Case ${currentCase.case_id} approved and dispatched!\n\n• Dispatch Tracking ID: ${data.case.dispatch_info?.tracking_id}\n• Status: APPROVED & DISPATCHED`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Approval error:", err);
  }
}

// View / Download PDF
function viewPdf(type = "rti") {
  if (!currentCase) {
    alert("Please select a case first.");
    return;
  }
  window.open(`${API_BASE}/cases/${currentCase.case_id}/pdf?type=${type}`, "_blank");
}

// Immutable Run Logs & Multi-Field Search Cache
let allRunLogsCache = [];
let allCasesCache = [];

async function loadRunLogs() {
  try {
    const res = await fetch(`${API_BASE}/run-log`);
    const data = await res.json();
    if (!res.ok) return;

    allRunLogsCache = data.run_logs || [];

    // Also load cases to cross-reference keywords across Name, Place, Subject, Address, Officer
    try {
      const caseRes = await fetch(`${API_BASE}/cases`);
      const caseData = await caseRes.json();
      if (caseRes.ok) {
        allCasesCache = caseData.cases || [];
      }
    } catch (e) {
      console.warn("Could not preload cases for run log search:", e);
    }

    const searchInput = document.getElementById("runLogSearchInput");
    if (searchInput && searchInput.value.trim()) {
      handleRunLogSearch(searchInput.value.trim());
    } else {
      renderRunLogsTable(allRunLogsCache);
      const countBadge = document.getElementById("runLogCountBadge");
      if (countBadge) countBadge.textContent = allRunLogsCache.length;
      const matchedCasesPanel = document.getElementById("matchedCasesPanel");
      if (matchedCasesPanel) matchedCasesPanel.style.display = "none";
      const filterBadge = document.getElementById("runLogFilterBadge");
      if (filterBadge) {
        filterBadge.textContent = "All Events";
        filterBadge.className = "status-pill approved";
      }
      const searchStatus = document.getElementById("runLogSearchStatus");
      if (searchStatus) {
        searchStatus.textContent = "All Logs Active";
        searchStatus.className = "status-pill approved";
      }
    }
  } catch (err) {
    console.error("Run log error:", err);
  }
}

function renderRunLogsTable(logs) {
  const tbody = document.getElementById("runLogBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (!logs || logs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--ink-muted); padding: 24px;">No execution run logs match the active query.</td></tr>`;
    return;
  }

  logs.forEach(log => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-family: var(--font-mono); font-size: 11px;">${log.timestamp}</td>
      <td><span class="statutory-tag" style="font-size: 10px;">${log.event_type}</span></td>
      <td>
        <a href="#" style="font-family: var(--font-mono); color: var(--gov-navy); font-weight: 700; font-size: 11.5px; text-decoration: underline;" onclick="event.preventDefault(); inspectCaseFromRunLog('${log.case_id}')">
          ${log.case_id}
        </a>
      </td>
      <td><b>${log.actor}</b></td>
      <td>${log.action}<br/><span style="font-family: var(--font-mono); font-size: 10px; color: var(--status-active);">Result: ${log.result}</span></td>
      <td style="font-family: var(--font-mono); font-size: 10.5px; color: var(--ink-muted);">${log.correlation_id}</td>
    `;
    tbody.appendChild(tr);
  });
  renderLucide();
}

function handleRunLogSearch(rawQuery) {
  const query = (rawQuery || "").trim().toLowerCase();
  const matchedCasesContainer = document.getElementById("matchedCasesContainer");
  const matchedCasesPanel = document.getElementById("matchedCasesPanel");
  const matchedCasesCount = document.getElementById("matchedCasesCount");
  const runLogFilterBadge = document.getElementById("runLogFilterBadge");
  const runLogSearchStatus = document.getElementById("runLogSearchStatus");
  const countBadge = document.getElementById("runLogCountBadge");

  if (!query) {
    if (matchedCasesPanel) matchedCasesPanel.style.display = "none";
    if (runLogFilterBadge) {
      runLogFilterBadge.textContent = "All Events";
      runLogFilterBadge.className = "status-pill approved";
    }
    if (runLogSearchStatus) {
      runLogSearchStatus.textContent = "All Logs Active";
      runLogSearchStatus.className = "status-pill approved";
    }
    renderRunLogsTable(allRunLogsCache);
    if (countBadge) countBadge.textContent = allRunLogsCache.length;
    return;
  }

  // Synonym expansions (Varanasi / Banaras / Kashi)
  const synonyms = query.includes("varanasi") || query.includes("banaras") || query.includes("kashi")
    ? ["varanasi", "banaras", "kashi"]
    : [query];

  // 1. Search cases across: Complainant Name, Place/Address, Subject/Grievance/Department, Officer Name
  const matchedCases = allCasesCache.filter(c => {
    const complainantName = (c.complainant?.name || "").toLowerCase();
    const complainantAddr = (c.complainant?.address || "").toLowerCase();
    const userLocality = (c.confidence?.user_locality || "").toLowerCase();
    const department = (c.department || c.category || "").toLowerCase();
    const rawGrievance = (c.raw_grievance || "").toLowerCase();
    const draftSubject = (c.draft_rti?.application_subject || "").toLowerCase();
    const refNo = (c.application_ref_no || "").toLowerCase();
    const pioName = (c.suggested_pio?.pio_name || "").toLowerCase();
    const pioAddr = (c.suggested_pio?.office_address || "").toLowerCase();
    const pioDesig = (c.suggested_pio?.designation || "").toLowerCase();
    const caseId = (c.case_id || "").toLowerCase();

    const fullSearchText = `${caseId} ${complainantName} ${complainantAddr} ${userLocality} ${department} ${rawGrievance} ${draftSubject} ${refNo} ${pioName} ${pioAddr} ${pioDesig}`;

    return synonyms.some(term => fullSearchText.includes(term));
  });

  const matchedCaseIds = new Set(matchedCases.map(c => c.case_id.toUpperCase()));

  // 2. Render Matched Case Dockets
  if (matchedCasesPanel && matchedCasesContainer) {
    matchedCasesPanel.style.display = "block";
    if (matchedCasesCount) matchedCasesCount.textContent = matchedCases.length;

    if (matchedCases.length === 0) {
      matchedCasesContainer.innerHTML = `
        <div style="grid-column: 1 / -1; padding: 18px; text-align: center; color: var(--ink-muted); font-size: 12px; background: var(--bg-surface); border: 1px dashed var(--border-medium); border-radius: 4px;">
          <i data-lucide="info" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle; margin-right: 4px; color: var(--gov-copper);"></i>
          No case dockets matched the keyword "<b>${rawQuery}</b>". Checking audit event trail below...
        </div>
      `;
    } else {
      matchedCasesContainer.innerHTML = matchedCases.map(c => {
        const pio = c.suggested_pio || {};
        const pioOfficer = pio.pio_name ? `${pio.pio_name} (${pio.designation || 'PIO'})` : 'Designation Pending';
        const locality = c.confidence?.user_locality || c.complainant?.address?.split(',').slice(-2).join(',').trim() || 'Jurisdiction Assigned';
        const subjectBrief = c.draft_rti?.application_subject || c.raw_grievance || 'Public Record Inquiry';
        const truncatedSubject = subjectBrief.length > 95 ? subjectBrief.substring(0, 92) + '...' : subjectBrief;
        const statusClass = c.status === 'APPROVED' ? 'approved' : (c.status === 'TRANSFERRED_SEC_6_3' ? 'neutral' : 'under-review');

        return `
          <div class="matched-case-card">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                  <b style="font-family: var(--font-mono); color: var(--gov-navy); font-size: 12.5px;">${c.case_id}</b>
                  <span class="status-pill ${statusClass}" style="font-size: 9.5px;">${c.status.replace(/_/g, ' ')}</span>
                </div>
                <span style="font-family: var(--font-mono); font-size: 10.5px; color: var(--gov-copper); font-weight: 700;">SLA: ${c.sla_days_remaining ?? 14}d</span>
              </div>
              
              <div style="font-size: 12px; font-weight: 700; color: var(--ink-primary); margin-bottom: 3px; display: flex; align-items: center; gap: 4px;">
                <i data-lucide="user" style="width: 12px; height: 12px; color: var(--gov-navy);"></i>
                <span>${c.complainant?.name || 'Anonymous Citizen'}</span>
                <span style="font-weight: 400; color: var(--ink-muted); font-size: 11px;">&bull; ${locality}</span>
              </div>

              <div style="font-size: 11px; color: var(--ink-secondary); margin-bottom: 6px; line-height: 1.35;">
                <b>Subject:</b> ${truncatedSubject}
              </div>

              <div style="font-size: 10.5px; color: var(--ink-secondary); background: var(--bg-subtle); padding: 6px 8px; border-radius: 2px; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 4px; color: var(--gov-navy); font-weight: 600;">
                  <i data-lucide="building-2" style="width: 11px; height: 11px;"></i>
                  <span>${c.department || 'Public Authority'}</span>
                </div>
                <div style="margin-top: 2px; color: var(--ink-muted);">
                  <b>Officer:</b> ${pioOfficer}
                </div>
                <div style="margin-top: 1px; color: var(--ink-muted);">
                  <b>Address:</b> ${pio.office_address || c.complainant?.address || 'Designated Administrative Complex'}
                </div>
              </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px; padding-top: 6px; border-top: 1px dashed var(--border-subtle);">
              <span style="font-size: 10.5px; color: var(--ink-muted);">Ref: <b>${c.application_ref_no || 'Standard Docket'}</b></span>
              <button class="btn-gov-outline" style="font-size: 11px; padding: 3px 8px; background: #FFFFFF;" onclick="inspectCaseFromRunLog('${c.case_id}')">
                <span>Inspect Dossier &rarr;</span>
              </button>
            </div>
          </div>
        `;
      }).join("");
    }
  }

  // 3. Filter Run Log table rows: match log directly OR match case ID of matched cases
  const filteredLogs = allRunLogsCache.filter(log => {
    const caseId = (log.case_id || "").toUpperCase();
    if (matchedCaseIds.has(caseId)) return true;

    const actor = (log.actor || "").toLowerCase();
    const action = (log.action || "").toLowerCase();
    const eventType = (log.event_type || "").toLowerCase();
    const result = (log.result || "").toLowerCase();
    const correlationId = (log.correlation_id || "").toLowerCase();
    const logCaseId = (log.case_id || "").toLowerCase();

    const logText = `${logCaseId} ${actor} ${action} ${eventType} ${result} ${correlationId}`;
    return synonyms.some(term => logText.includes(term));
  });

  renderRunLogsTable(filteredLogs);

  if (runLogFilterBadge) {
    runLogFilterBadge.textContent = `Filtered: ${filteredLogs.length} Rows (${matchedCases.length} Cases)`;
    runLogFilterBadge.className = "status-pill under-review";
  }
  if (runLogSearchStatus) {
    runLogSearchStatus.textContent = `${matchedCases.length} Cases Matched`;
    runLogSearchStatus.className = matchedCases.length > 0 ? "status-pill approved" : "status-pill under-review";
  }
  if (countBadge) {
    countBadge.textContent = filteredLogs.length;
  }
  renderLucide();
}

// ==========================================================================
// DEDICATED CASE DOSSIER, AUDIT & TIMELINE VIEW (OPENED FROM AUDIT RUN LOG)
// ==========================================================================
let activeDetailCase = null;

function inspectCaseFromRunLog(caseId) {
  openCaseDetailView(caseId);
}

function getStatusClass(status) {
  if (!status) return "under-review";
  const s = String(status).toUpperCase();
  if (s === "APPROVED") return "approved";
  if (s === "TRANSFERRED_SEC_6_3" || s === "TRANSFERRED") return "transferred";
  if (s === "MERGED_DUPLICATE" || s === "MERGED") return "merged";
  if (s === "NEEDS_REVIEW" || s === "UNDER_REVIEW") return "under-review";
  if (s.includes("APPROV")) return "approved";
  if (s.includes("TRANSF")) return "transferred";
  if (s.includes("MERG")) return "merged";
  return "under-review";
}

async function openCaseDetailView(caseId) {
  try {
    let caseData = (typeof allCasesCache !== "undefined" ? allCasesCache : []).find(c => c.case_id === caseId);
    if (!caseData) {
      const res = await fetch(`${API_BASE}/cases/${encodeURIComponent(caseId)}`);
      if (res.ok) {
        const json = await res.json();
        caseData = json.case;
      }
    }
    if (!caseData) {
      alert(`Could not find case docket ${caseId}.`);
      return;
    }
    activeDetailCase = caseData;

    // 1. Header & Summary Banner
    const docketIdEl = document.getElementById("detailDocketId");
    if (docketIdEl) docketIdEl.textContent = caseData.case_id;
    const breadcrumbEl = document.getElementById("detailCaseBreadcrumb");
    if (breadcrumbEl) breadcrumbEl.textContent = `${caseData.case_id} Dossier`;
    const subjectEl = document.getElementById("detailDocketSubject");
    if (subjectEl) subjectEl.textContent = caseData.draft_rti?.application_subject || "Right to Information Application";
    const dateEl = document.getElementById("detailDocketDate");
    if (dateEl) dateEl.textContent = caseData.original_submission_date || caseData.created_at || "—";
    const refEl = document.getElementById("detailDocketRef");
    if (refEl) refEl.textContent = caseData.application_ref_no || "Standard Filing";
    const deptEl = document.getElementById("detailDocketDept");
    if (deptEl) deptEl.textContent = caseData.department || "Revenue & Land Records";
    const compNameEl = document.getElementById("detailDocketComplainantName");
    if (compNameEl) compNameEl.textContent = caseData.complainant?.name || "Citizen Applicant";
    const locEl = document.getElementById("detailDocketLocation");
    if (locEl) locEl.textContent = caseData.district ? `${caseData.district}, ${caseData.state || ''}` : (caseData.confidence?.user_locality || "Local Jurisdiction");
    const pinEl = document.getElementById("detailPincodeBadge");
    if (pinEl) pinEl.textContent = `PIN: ${caseData.pincode || caseData.complainant?.pincode || '—'}`;

    // Status & SLA
          const statusMap = {
        "APPROVED": currentLang === "hi" ? "स्वीकृत" : (currentLang === "bi" ? "APPROVED • स्वीकृत" : "APPROVED"),
        "TRANSFERRED_SEC_6_3": currentLang === "hi" ? "अंतरित (धारा 6(3))" : (currentLang === "bi" ? "TRANSFERRED • अंतरित" : "TRANSFERRED (SEC 6(3))"),
        "NEEDS_REVIEW": currentLang === "hi" ? "समीक्षाधीन" : (currentLang === "bi" ? "UNDER REVIEW • समीक्षाधीन" : "UNDER REVIEW"),
        "UNDER_REVIEW": currentLang === "hi" ? "समीक्षाधीन" : (currentLang === "bi" ? "UNDER REVIEW • समीक्षाधीन" : "UNDER REVIEW"),
        "REJECTED": currentLang === "hi" ? "अस्वीकृत" : (currentLang === "bi" ? "REJECTED • अस्वीकृत" : "REJECTED")
      };
    const statusPill = document.getElementById("detailDocketStatusPill");
    if (statusPill) {
      statusPill.textContent = statusMap[caseData.status] || caseData.status;
      statusPill.className = `status-pill ${getStatusClass(caseData.status)}`;
    }
    const slaBadge = document.getElementById("detailDocketSlaBadge");
    const urgentBadge = document.getElementById("detailDocketUrgentBadge");
    const isUrgent = Boolean(caseData.is_life_liberty);
    if (urgentBadge) urgentBadge.style.display = isUrgent ? "inline-block" : "none";
    if (slaBadge) {
      if (currentLang === "hi") {
        slaBadge.textContent = isUrgent ? "48 घंटे आपातकालीन समयसीमा" : "30-दिवसीय समयसीमा";
      } else if (currentLang === "bi") {
        slaBadge.textContent = isUrgent ? "48-Hour Urgent SLA • 48 घंटे आपातकालीन समयसीमा" : "30-Day Standard SLA • 30-दिवसीय समयसीमा";
      } else {
        slaBadge.textContent = isUrgent ? "48-Hour Urgent SLA" : "30-Day Standard SLA";
      }
    }

    const daysRemaining = caseData.sla_days_remaining !== undefined ? caseData.sla_days_remaining : 30;
    const slaCountdown = document.getElementById("detailDocketSlaCountdown");
    if (slaCountdown) {
      if (currentLang === "hi") {
        slaCountdown.textContent = isUrgent ? "48 घंटे" : `${daysRemaining} दिन शेष`;
      } else if (currentLang === "bi") {
        slaCountdown.textContent = isUrgent ? "48 Hours • 48 घंटे" : `${daysRemaining} Days • दिन शेष`;
      } else {
        slaCountdown.textContent = isUrgent ? "48 Hours" : `${daysRemaining} Days Remaining`;
      }
      slaCountdown.style.color = daysRemaining <= 5 ? "var(--status-risk)" : "var(--gov-navy)";
    }
    const dueDateEl = document.getElementById("detailDocketDueDate");
    if (dueDateEl) {
      if (currentLang === "hi") {
        dueDateEl.textContent = `अंतिम तिथि: ${caseData.due_date || 'विधिक अवधि में'}`;
      } else if (currentLang === "bi") {
        dueDateEl.textContent = `Due / अंतिम तिथि: ${caseData.due_date || 'Within Statutory Period • विधिक अवधि में'}`;
      } else {
        dueDateEl.textContent = `Due: ${caseData.due_date || 'Within Statutory Period'}`;
      }
    }

    // 2. Complainant & PIO Details
    const cName = document.getElementById("detailCompName");
    if (cName) cName.textContent = caseData.complainant?.name || "—";
    const cContact = document.getElementById("detailCompContact");
    if (cContact) cContact.textContent = caseData.complainant?.contact || "Contact not specified";
    const cAddress = document.getElementById("detailCompAddress");
    if (cAddress) cAddress.textContent = caseData.complainant?.address || "Address not provided";

    const pio = caseData.suggested_pio || caseData.assigned_pio || {};
    const pioName = document.getElementById("detailPioName");
    if (pioName) pioName.textContent = pio.pio_name || "Designated PIO Officer";
    const pioDept = document.getElementById("detailPioDept");
    if (pioDept) pioDept.textContent = pio.department || caseData.department || "Public Authority";
    const pioAddress = document.getElementById("detailPioAddress");
    if (pioAddress) pioAddress.textContent = pio.office_address || "Tehsil / District Collectorate Complex";
    const pioDist = document.getElementById("detailPioDistance");
    if (pioDist) pioDist.textContent = pio.distance_label ? `📍 ${pio.distance_label} • भू-स्थानिक निकटता` : "📍 1.2 km away • 1.2 किमी निकट";

    // 3. Grievance & Questions
    const grievanceText = document.getElementById("detailGrievanceText");
    if (grievanceText) grievanceText.textContent = caseData.raw_grievance || "No grievance narrative recorded.";
    const questionsList = document.getElementById("detailQuestionsList");
    if (questionsList) {
      const qArr = caseData.draft_rti?.questions || [];
      if (qArr.length > 0) {
        questionsList.innerHTML = qArr.map(q => `<li style="margin-bottom: 6px;">${q}</li>`).join("");
      } else {
        questionsList.innerHTML = `<li style="color: var(--ink-muted);">Standard certified inspection and dispatch status questions drafted.</li>`;
      }
    }

    // 4. ML Domain Classification Intelligence
    const mlConf = caseData.confidence?.overall || 95;
    const mlConfBadge = document.getElementById("detailMlConfidenceBadge");
    if (mlConfBadge) {
      mlConfBadge.textContent = `${mlConf}% ML Confidence • एआई सटीकता`;
      mlConfBadge.className = `status-pill ${mlConf >= 80 ? "approved" : "under-review"}`;
    }
    const domainTitle = document.getElementById("detailMlDomainTitle");
    if (domainTitle) domainTitle.textContent = caseData.department || "Revenue & Land Records";
    const mlReason = document.getElementById("detailMlReason");
    if (mlReason) mlReason.textContent = caseData.confidence?.ml_prediction_reason || "Classified via multi-gram TF-IDF domain scoring with authentic statutory keyword triggers.";

    const triggersEl = document.getElementById("detailMlTriggers");
    if (triggersEl) {
      const keywords = (caseData.statutory_legal_analysis?.matched_keywords || ["RTI 2005", caseData.department]).slice(0, 4);
      triggersEl.innerHTML = keywords.map(kw => `<span class="statutory-tag" style="font-size: 10px;">${kw}</span>`).join("");
    }

    const bnsMapping = document.getElementById("detailBnsMapping");
    if (bnsMapping) {
      const primaryStatute = caseData.statutory_legal_analysis?.primary_bns_statute;
      bnsMapping.textContent = primaryStatute ? `${primaryStatute.ipc_section} → ${primaryStatute.bns_section}` : "Section 6(1) RTI Act 2005";
    }

    const penaltyEl = document.getElementById("detailSec20Penalty");
    if (penaltyEl) {
      const pen = caseData.statutory_legal_analysis?.section_20_penalty_liability_inr || 0;
      penaltyEl.textContent = `₹${pen.toLocaleString('en-IN')}`;
    }

    // 5. Initialize Timestamp input to live local ISO
    const timestampInput = document.getElementById("updateTimestampInput");
    if (timestampInput) {
      const now = new Date();
      const localIso = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
      timestampInput.value = localIso;
    }

    // 6. Populate Deduplication Select Options
    populateMergeDuplicateSelect(caseData.case_id);

    // 7. Render Previously Merged Dockets
    renderPreviouslyMergedList(caseData);

    // 8. Render Chronological Timeline Ledger
    renderCaseDetailTimeline(caseData);

    // 9. Navigate to page
    showPage("case-detail");
    renderLucide();
  } catch (err) {
    console.error("Error opening case details view:", err);
    alert("Could not load case details: " + err.message);
  }
}

function populateMergeDuplicateSelect(currentCaseId) {
  const select = document.getElementById("mergeDuplicateSelect");
  if (!select) return;
  select.innerHTML = '<option value="">-- Choose a duplicate case to consolidate --</option>';

  const cache = typeof allCasesCache !== "undefined" ? allCasesCache : [];
  const candidates = cache.filter(c => c.case_id !== currentCaseId && c.status !== "MERGED_DUPLICATE");
  if (candidates.length === 0) {
    const opt = document.createElement("option");
    opt.value = "";
    opt.disabled = true;
    opt.textContent = "No other active dockets available for merging";
    select.appendChild(opt);
    return;
  }

  candidates.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c.case_id;
    const name = c.complainant?.name || "Applicant";
    const dept = c.department || "Civic";
    const ref = c.application_ref_no ? `(Ref: ${c.application_ref_no})` : "";
    opt.textContent = `${c.case_id} — ${name} — ${dept} ${ref} [${c.status}]`;
    select.appendChild(opt);
  });
}

function renderPreviouslyMergedList(caseData) {
  const section = document.getElementById("previouslyMergedSection");
  const list = document.getElementById("previouslyMergedList");
  if (!section || !list) return;

  const mergedIds = caseData.merged_duplicate_cases || [];
  const cache = typeof allCasesCache !== "undefined" ? allCasesCache : [];
  const otherMerged = cache.filter(c => c.merged_into_case_id === caseData.case_id).map(c => c.case_id);
  const allMerged = Array.from(new Set([...mergedIds, ...otherMerged]));

  if (allMerged.length === 0) {
    section.style.display = "none";
    list.innerHTML = "";
    return;
  }

  section.style.display = "block";
  list.innerHTML = allMerged.map(id => `
    <span class="statutory-tag" style="background: #FEE2E2; color: #991B1B; border-color: #FCA5A5; font-size: 11px;">
      <b>${id}</b> (Merged Duplicate)
    </span>
  `).join("");
}

function renderCaseDetailTimeline(caseData) {
  const container = document.getElementById("detailTimelineContainer");
  const countEl = document.getElementById("detailTimelineCount");
  if (!container) return;

  const history = caseData.update_history || [];
  if (countEl) countEl.textContent = history.length;

  if (history.length === 0) {
    container.innerHTML = `
      <div style="color: var(--ink-muted); font-size: 12px; padding: 12px 0;">
        No historical update logs found on this docket. Initializing audit trail...
      </div>
    `;
    return;
  }

  // Render in reverse chronological order (newest first)
  const sorted = [...history].reverse();
  container.innerHTML = sorted.map((entry, idx) => {
    const isNewest = idx === 0;
    const uType = (entry.update_type || "").toUpperCase();
    const borderCol = uType.includes("MERGE") ? "var(--gov-copper)" :
      uType.includes("HEARING") ? "var(--gov-navy)" :
        uType.includes("TRANSFER") ? "var(--gov-amber)" :
          "var(--status-active)";

    return `
      <div class="audit-timeline-entry" style="margin-bottom: 12px;">
        <div class="timeline-entry-card" style="${isNewest ? 'border-left: 3px solid ' + borderCol + ';' : ''}">
          <div class="timeline-meta-row">
            <span style="font-family: var(--font-mono); font-size: 10.5px; color: var(--ink-muted); font-weight: 600;">
              ${entry.timestamp || 'Recorded'}
            </span>
            <span class="statutory-tag" style="font-size: 9.5px; text-transform: uppercase;">
              ${entry.update_type || 'CASE_UPDATE'}
            </span>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 11.5px; color: var(--gov-navy);">
              ${entry.actor || 'Legal Desk Officer'}
            </span>
            ${entry.field_changed ? `<span style="font-size: 10px; color: var(--ink-muted);">${entry.field_changed}</span>` : ''}
          </div>
          <div style="font-size: 11.5px; color: var(--ink-secondary); line-height: 1.5; white-space: pre-wrap;">
            ${entry.remarks || 'Status / information updated.'}
          </div>
        </div>
      </div>
    `;
  }).join("");
}

async function submitCaseUpdateFromDetail(event) {
  event.preventDefault();
  if (!activeDetailCase) {
    alert("No active case selected.");
    return;
  }

  const updateType = document.getElementById("updateTypeSelect").value;
  const actor = (document.getElementById("updateActorInput")?.value || "").trim() || "Adv. S. Kalra (Legal Counsel)";
  const rawTime = document.getElementById("updateTimestampInput")?.value;
  const newStatus = document.getElementById("updateStatusSelect")?.value;
  const remarks = (document.getElementById("updateRemarksTextarea")?.value || "").trim();
  const statusMsg = document.getElementById("updateFormStatusMsg");
  const submitBtn = document.getElementById("btnSubmitCaseUpdate");

  if (!remarks) {
    alert("Please enter remarks / hearing minutes for this case update.");
    return;
  }

  const formattedTime = rawTime ? rawTime.replace("T", " ") + ":00" : undefined;

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.innerHTML = "<span>Recording Update...</span>";
  }
  if (statusMsg) {
    statusMsg.style.color = "var(--ink-muted)";
    statusMsg.textContent = "Recording update to case docket...";
  }

  try {
    const payload = {
      update_type: updateType,
      actor: actor,
      timestamp: formattedTime,
      new_status: newStatus || undefined,
      remarks: remarks
    };

    const res = await fetch(`${API_BASE}/cases/${encodeURIComponent(activeDetailCase.case_id)}/updates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || "Failed to record case update");
    }

    // Success! Update active case
    activeDetailCase = data.case;
    if (typeof allCasesCache !== "undefined") {
      const idx = allCasesCache.findIndex(c => c.case_id === activeDetailCase.case_id);
      if (idx !== -1) allCasesCache[idx] = data.case;
    }

    // Refresh timeline & status
    renderCaseDetailTimeline(activeDetailCase);
    if (newStatus) {
      const statusPill = document.getElementById("detailDocketStatusPill");
      if (statusPill) {
        statusPill.textContent = newStatus;
        statusPill.className = `status-pill ${getStatusClass(newStatus)}`;
      }
    }

    // Clear textarea
    const remarksEl = document.getElementById("updateRemarksTextarea");
    if (remarksEl) remarksEl.value = "";
    const statusSel = document.getElementById("updateStatusSelect");
    if (statusSel) statusSel.value = "";

    // Show feedback
    if (statusMsg) {
      statusMsg.style.color = "var(--status-active)";
      statusMsg.textContent = "✓ Timestamped update recorded successfully!";
      setTimeout(() => { if (statusMsg) statusMsg.textContent = ""; }, 4000);
    }

    // Refresh run logs & cases list in background
    loadRunLogs();
    loadCaseQueue();
  } catch (err) {
    console.error("Error submitting case update:", err);
    if (statusMsg) {
      statusMsg.style.color = "var(--status-risk)";
      statusMsg.textContent = `Error: ${err.message}`;
    }
    alert(`Could not record case update: ${err.message}`);
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i data-lucide="plus-circle" style="width: 13px; height: 13px;"></i><span>Record Timestamped Update</span>`;
    }
    renderLucide();
  }
}

async function submitCaseMergeFromDetail(event) {
  event.preventDefault();
  if (!activeDetailCase) {
    alert("No active case selected.");
    return;
  }

  const dupSelect = document.getElementById("mergeDuplicateSelect");
  const duplicateId = dupSelect ? dupSelect.value : "";
  const remarks = (document.getElementById("mergeRemarksInput")?.value || "").trim();
  const statusMsg = document.getElementById("mergeStatusMsg");

  if (!duplicateId) {
    alert("Please select a duplicate case to consolidate into this docket.");
    return;
  }

  if (!confirm(`Are you sure you want to merge duplicate case ${duplicateId} into Master Docket ${activeDetailCase.case_id}?\n\nThis will mark ${duplicateId} as MERGED_DUPLICATE and consolidate all facts.`)) {
    return;
  }

  if (statusMsg) {
    statusMsg.style.color = "var(--ink-muted)";
    statusMsg.textContent = "Executing deduplication merge...";
  }

  try {
    const actorName = (typeof currentPersona !== "undefined" && currentPersona === "counsel") ? "Adv. S. Kalra (Legal NGO)" : "Designated PIO Desk Officer";
    const payload = {
      master_case_id: activeDetailCase.case_id,
      duplicate_case_id: duplicateId,
      actor: actorName,
      remarks: remarks || "Consolidated duplicate docket to eliminate deduplicacy."
    };

    const res = await fetch(`${API_BASE}/cases/merge-duplicates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || "Failed to merge cases");
    }

    // Success! Update active case
    activeDetailCase = data.master_case;

    if (typeof allCasesCache !== "undefined") {
      const mIdx = allCasesCache.findIndex(c => c.case_id === activeDetailCase.case_id);
      if (mIdx !== -1) allCasesCache[mIdx] = data.master_case;
      const dIdx = allCasesCache.findIndex(c => c.case_id === duplicateId);
      if (dIdx !== -1) allCasesCache[dIdx] = data.duplicate_case;
    }

    // Re-populate merge select and previously merged list
    populateMergeDuplicateSelect(activeDetailCase.case_id);
    renderPreviouslyMergedList(activeDetailCase);

    // Refresh timeline
    renderCaseDetailTimeline(activeDetailCase);

    // Clear remarks input
    const remarksInput = document.getElementById("mergeRemarksInput");
    if (remarksInput) remarksInput.value = "";

    if (statusMsg) {
      statusMsg.style.color = "var(--status-active)";
      statusMsg.textContent = `✓ Successfully merged ${duplicateId} into ${activeDetailCase.case_id}!`;
      setTimeout(() => { if (statusMsg) statusMsg.textContent = ""; }, 5000);
    }

    // Refresh background data
    loadRunLogs();
    loadCaseQueue();
  } catch (err) {
    console.error("Error executing case merge:", err);
    if (statusMsg) {
      statusMsg.style.color = "var(--status-risk)";
      statusMsg.textContent = `Error: ${err.message}`;
    }
    alert(`Could not merge cases: ${err.message}`);
  } finally {
    renderLucide();
  }
}

function returnToAuditRunLog() {
  showPage("dashboard");
  switchDashTab("runlog");
}

function openCaseInCaseworkDesk() {
  if (activeDetailCase) {
    openCaseById(activeDetailCase.case_id);
    showPage("dashboard");
    switchDashTab("casework");
  }
}

function downloadActiveCasePdf() {
  if (activeDetailCase) {
    window.open(`${API_BASE}/cases/${encodeURIComponent(activeDetailCase.case_id)}/pdf?type=rti`, "_blank");
  } else if (typeof currentCase !== "undefined" && currentCase) {
    viewPdf("rti");
  }
}

function refreshActiveCaseDetailTimeline() {
  if (activeDetailCase) {
    openCaseDetailView(activeDetailCase.case_id);
  }
}

function clearRunLogSearch() {
  const input = document.getElementById("runLogSearchInput");
  if (input) input.value = "";
  handleRunLogSearch("");
}

function setRunLogSearchQuery(term) {
  const input = document.getElementById("runLogSearchInput");
  if (input) {
    input.value = term;
    handleRunLogSearch(term);
  }
}

// Live Canvas Radar Animation with Multi-PIO Geodesic Telemetry
let sweepAngle = 0;
let currentPioFilter = "all";

function initRadarAnimation() {
  const canvas = document.getElementById("radarCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const radius = cx - 15;

  function draw() {
    ctx.fillStyle = "#F8FAFC";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Outer Range Boundary
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#CBD5E1";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Concentric Range Rings (1.5km, 3.5km, 7.5km, 12km)
    const rings = [0.25, 0.5, 0.75, 1.0];
    const ringLabels = ["1.5km", "3.5km", "7.5km", "12km"];
    rings.forEach((r, idx) => {
      ctx.beginPath();
      ctx.arc(cx, cy, radius * r, 0, Math.PI * 2);
      ctx.strokeStyle = "#E2E8F0";
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = "#64748B";
      ctx.font = "9.5px Segoe UI, Arial, sans-serif";
      ctx.fillText(ringLabels[idx], cx + 6, cy - radius * r + 13);
    });

    // Radar Crosshairs
    ctx.beginPath();
    ctx.moveTo(cx, cy - radius);
    ctx.lineTo(cx, cy + radius);
    ctx.moveTo(cx - radius, cy);
    ctx.lineTo(cx + radius, cy);
    ctx.strokeStyle = "#E2E8F0";
    ctx.lineWidth = 1;
    ctx.stroke();

    // Rotating Sweep Line
    sweepAngle += 0.035;
    const sweepX = cx + Math.cos(sweepAngle) * radius;
    const sweepY = cy + Math.sin(sweepAngle) * radius;

    // Sweep cone gradient
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, radius, sweepAngle - 0.45, sweepAngle);
    ctx.closePath();
    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
    grad.addColorStop(0, "rgba(37, 99, 235, 0)");
    grad.addColorStop(1, "rgba(37, 99, 235, 0.18)");
    ctx.fillStyle = grad;
    ctx.fill();

    // Sweep leading line
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(sweepX, sweepY);
    ctx.strokeStyle = "rgba(37, 99, 235, 0.7)";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // 1. Center Blip: Citizen Complainant Origin
    ctx.beginPath();
    ctx.arc(cx, cy, 6, 0, Math.PI * 2);
    ctx.fillStyle = "#D97706";
    ctx.fill();
    ctx.strokeStyle = "#FFFFFF";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = "#0F172A";
    ctx.font = "bold 10px Segoe UI, Arial, sans-serif";
    ctx.fillText("YOU (CITIZEN)", cx - 34, cy + 18);

    // 2. Multi-PIO Blips for Nearest Area Officers
    const c = currentCase;
    const areaPios = c?.nearby_area_pios || c?.geospatial_meta?.nearby_pios || [];
    const citizenCoords = c?.geospatial_meta?.user_coords || c?.suggested_pio?.user_coordinates || { latitude: 25.2905, longitude: 82.9995 };

    if (areaPios.length === 0) {
      // Fallback single target blip
      let pioOffsetX = 45;
      let pioOffsetY = -35;
      if (currentCase?.geospatial_meta?.distance_km) {
        const d = currentCase.geospatial_meta.distance_km;
        pioOffsetX = Math.min(radius - 20, (d / 15) * radius * 0.8 + 25);
        pioOffsetY = -pioOffsetX * 0.7;
      }
      ctx.beginPath();
      ctx.arc(cx + pioOffsetX, cy + pioOffsetY, 7, 0, Math.PI * 2);
      ctx.fillStyle = "#1D4ED8";
      ctx.fill();
      ctx.fillStyle = "#1D4ED8";
      ctx.font = "bold 10px Segoe UI, Arial, sans-serif";
      ctx.fillText("PIO (NEAREST)", cx + pioOffsetX - 30, cy + pioOffsetY - 10);
    } else {
      const maxDist = Math.max(8.0, ...areaPios.map(p => p.distance_km || 4.0));

      areaPios.forEach((p, idx) => {
        const isAssigned = p.is_assigned || (c.suggested_pio && c.suggested_pio.pio_name === p.pio_name);
        const dist = p.distance_km || 1.5;
        const rDist = Math.min(radius - 22, (dist / maxDist) * (radius - 40) + 24);

        // Calculate angular offset based on coordinate delta
        const dLat = (p.latitude || 0) - citizenCoords.latitude;
        const dLon = (p.longitude || 0) - citizenCoords.longitude;
        let angle = Math.atan2(dLat, dLon);
        if (Math.abs(dLat) < 0.0001 && Math.abs(dLon) < 0.0001) {
          angle = (idx * (2 * Math.PI / areaPios.length)) - (Math.PI / 2);
        }

        const bx = cx + Math.cos(angle) * rDist;
        const by = cy - Math.sin(angle) * rDist;

        if (isAssigned) {
          // Pulsing Halo for Assigned Domain PIO
          const pulse = Math.sin(sweepAngle * 4) * 2.5;
          ctx.beginPath();
          ctx.arc(bx, by, 9 + pulse, 0, Math.PI * 2);
          ctx.strokeStyle = "rgba(29, 78, 216, 0.45)";
          ctx.lineWidth = 2;
          ctx.stroke();

          // Main Blip
          ctx.beginPath();
          ctx.arc(bx, by, 7, 0, Math.PI * 2);
          ctx.fillStyle = "#1D4ED8";
          ctx.fill();
          ctx.strokeStyle = "#FFFFFF";
          ctx.lineWidth = 1.5;
          ctx.stroke();

          // Label
          ctx.fillStyle = "#1D4ED8";
          ctx.font = "bold 10.5px Segoe UI, Arial, sans-serif";
          ctx.fillText(`★ ${p.pio_name} (${p.distance_label})`, bx - 40, by - 12);
        } else {
          // Other Area Authorities
          ctx.beginPath();
          ctx.arc(bx, by, 4.5, 0, Math.PI * 2);
          ctx.fillStyle = "#64748B";
          ctx.fill();
          ctx.strokeStyle = "#FFFFFF";
          ctx.lineWidth = 1;
          ctx.stroke();

          ctx.fillStyle = "#475569";
          ctx.font = "9px Segoe UI, Arial, sans-serif";
          const shortDept = (p.department || "").split("&")[0].trim();
          ctx.fillText(`${shortDept} (${p.distance_label})`, bx + 7, by + 3);
        }
      });
    }

    radarAnimationId = requestAnimationFrame(draw);
  }

  draw();
}

function updateRadarTelemetry(c) {
  const geo = c.geospatial_meta || {};
  const pio = c.suggested_pio || {};

  const uCoords = geo.user_coords || pio.user_coordinates || { latitude: 25.2905, longitude: 82.9995 };
  const pCoords = geo.pio_coords || pio.pio_coordinates || { latitude: 25.3340, longitude: 82.9860 };

  const uEl = document.getElementById("radarUserCoords");
  const pEl = document.getElementById("radarPioCoords");
  const dEl = document.getElementById("radarDistance");

  if (uEl) uEl.textContent = `${uCoords.latitude?.toFixed(4)}° N, ${uCoords.longitude?.toFixed(4)}° E`;
  if (pEl) pEl.textContent = `${pCoords.latitude?.toFixed(4)}° N, ${pCoords.longitude?.toFixed(4)}° E`;
  if (dEl) dEl.textContent = geo.distance_label || pio.distance_label || "1.42 km away";
}

// Full PIO Geospatial Map & Directory Controller for Active Docket
async function updatePioMapForCase(c) {
  if (!c) {
    if (allCasesCache && allCasesCache.length > 0) {
      c = allCasesCache[0];
      currentCase = c;
    } else {
      try {
        const res = await fetch(`${API_BASE}/cases`);
        const data = await res.json();
        if (data.cases && data.cases.length > 0) {
          c = data.cases[0];
          currentCase = c;
          allCasesCache = data.cases;
        }
      } catch (e) {
        console.warn("Could not fetch case for PIO map:", e);
      }
    }
  }
  if (!c) return;

  // Preload nearby area PIOs if not already cached on the docket
  if (!c.nearby_area_pios || c.nearby_area_pios.length === 0) {
    try {
      const geoRes = await fetch(`${API_BASE}/cases/${c.case_id}/nearby-pios`);
      const geoData = await geoRes.json();
      if (geoRes.ok && geoData.nearby_area_pios) {
        c.nearby_area_pios = geoData.nearby_area_pios;
        if (geoData.assigned_pio) c.suggested_pio = geoData.assigned_pio;
      }
    } catch (e) {
      console.warn("Could not fetch nearby area PIOs:", e);
    }
  }

  // 1. Update Active Docket Context Bar
  const caseIdEl = document.getElementById("pioMapCaseId");
  const compEl = document.getElementById("pioMapComplainant");
  const locEl = document.getElementById("pioMapLocality");
  const domainEl = document.getElementById("pioMapDomain");
  const assignedNameEl = document.getElementById("pioMapAssignedName");
  const assignedDistEl = document.getElementById("pioMapAssignedDist");

  const pio = c.suggested_pio || {};
  const locality = c.confidence?.user_locality || c.complainant?.address || "Administrative Jurisdiction";

  if (caseIdEl) caseIdEl.textContent = c.case_id;
  if (compEl) compEl.textContent = c.complainant?.name || "Citizen Applicant";
  if (locEl) locEl.textContent = locality;
  if (domainEl) domainEl.textContent = c.department || c.category || "General Administration";
  if (assignedNameEl) assignedNameEl.textContent = `${pio.pio_name || 'Designated PIO'} (${pio.designation || 'PIO'})`;
  if (assignedDistEl) assignedDistEl.textContent = `${pio.distance_label || 'Jurisdiction Assigned'} • ${pio.department || c.department}`;

  // Populate Dropdown Selector
  populatePioCaseSelector(c.case_id);

  // 2. Update Radar Telemetry
  updateRadarTelemetry(c);

  // 2b. Update Interactive Leaflet OpenStreetMap
  renderLeafletMapMarkers(c);

  // 3. Render Nearest Area PIOs in Directory List
  renderAreaPiosDirectory(c, currentPioFilter);

  renderLucide();
}

function populatePioCaseSelector(selectedCaseId) {
  const sel = document.getElementById("pioMapCaseSelect");
  if (!sel) return;

  const cases = (allCasesCache && allCasesCache.length > 0) ? allCasesCache : (currentCase ? [currentCase] : []);
  sel.innerHTML = cases.map(cs => {
    const isSel = cs.case_id === selectedCaseId ? "selected" : "";
    return `<option value="${cs.case_id}" ${isSel}>${cs.case_id} - ${cs.complainant?.name || 'Citizen'} (${cs.department || 'Public Authority'})</option>`;
  }).join("");
}

async function switchPioMapCase(caseId) {
  try {
    const res = await fetch(`${API_BASE}/cases/${caseId}`);
    const data = await res.json();
    if (res.ok) {
      currentCase = data.case;
      populateWorkspaceFields(data.case);
      updatePioMapForCase(data.case);
    }
  } catch (e) {
    console.error("Error switching PIO map case:", e);
  }
}

function filterRadarDirectory(filterType) {
  currentPioFilter = filterType;
  ["pioFilterAll", "pioFilterDomain", "pioFilterClose"].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) btn.classList.remove("active");
  });
  if (filterType === "all" && document.getElementById("pioFilterAll")) document.getElementById("pioFilterAll").classList.add("active");
  if (filterType === "domain" && document.getElementById("pioFilterDomain")) document.getElementById("pioFilterDomain").classList.add("active");
  if (filterType === "close" && document.getElementById("pioFilterClose")) document.getElementById("pioFilterClose").classList.add("active");

  if (currentCase) {
    renderAreaPiosDirectory(currentCase, filterType);
  }
}

function renderAreaPiosDirectory(c, filterType = "all") {
  const list = document.getElementById("radarDirectoryList");
  const countBadge = document.getElementById("radarAreaCount");
  if (!list) return;

  let areaPios = c.nearby_area_pios || c.geospatial_meta?.nearby_pios || [];

  if (filterType === "domain") {
    const dept = (c.department || "").toLowerCase();
    areaPios = areaPios.filter(p => (p.department || "").toLowerCase().includes(dept) || dept.includes((p.department || "").toLowerCase()));
  } else if (filterType === "close") {
    areaPios = areaPios.filter(p => (p.distance_km || 0) <= 3.0);
  }

  if (countBadge) countBadge.textContent = areaPios.length;

  if (areaPios.length === 0) {
    list.innerHTML = `<div style="text-align: center; color: var(--ink-muted); padding: 24px; font-size: 12px; background: var(--bg-surface); border: 1px dashed var(--border-medium); border-radius: 4px;">No PIO officers match the filter "${filterType}".</div>`;
    return;
  }

  list.innerHTML = areaPios.map(p => {
    const isAssigned = p.is_assigned || (c.suggested_pio && c.suggested_pio.pio_name === p.pio_name);
    const cardClass = isAssigned ? "nearby-pio-card assigned-domain-pio" : "nearby-pio-card";
    const faa = p.faa || {};

    let badgeHtml = "";
    if (isAssigned) {
      badgeHtml = `<span class="status-pill approved" style="font-size: 9.5px; font-weight: 700; background: #DCFCE7; color: #15803D; border: 1px solid #86EFAC;">★ ASSIGNED DOMAIN PIO</span>`;
    } else if (p.is_domain_match || (c.department && p.department && p.department.toLowerCase().includes(c.department.toLowerCase()))) {
      badgeHtml = `<span class="statutory-tag bns" style="font-size: 9.5px;">Domain Match &bull; ${p.department}</span>`;
    } else {
      badgeHtml = `<span class="statutory-tag" style="font-size: 9.5px; background: var(--bg-subtle); color: var(--ink-secondary);">${p.department}</span>`;
    }

    return `
      <div class="${cardClass}" id="pio-card-${p.id || p.latitude}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
          <div>${badgeHtml}</div>
          <span style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--gov-copper);">${p.distance_label || (p.distance_km ? p.distance_km + ' km away' : 'Near')}</span>
        </div>

        <div style="font-size: 13px; font-weight: 700; color: var(--ink-primary); margin-bottom: 2px;">
          ${p.pio_name}
          <span style="font-weight: 400; font-size: 11.5px; color: var(--ink-muted);">&mdash; ${p.designation}</span>
        </div>

        <div style="font-size: 11px; color: var(--ink-secondary); margin-bottom: 6px;">
          <i data-lucide="building" style="width: 11px; height: 11px; display: inline-block; vertical-align: middle; color: var(--gov-navy);"></i>
          <span>${p.office_address} &bull; ${p.room_no || 'RTI Nodal Office'}</span>
        </div>

        <div style="display: flex; gap: 12px; font-size: 10.5px; color: var(--ink-muted); margin-bottom: 8px;">
          <span><b>Email:</b> ${p.email || 'pio@gov.in'}</span>
          <span><b>Phone:</b> ${p.phone || '+91-XX-XXXX'}</span>
        </div>

        <!-- First Appellate Authority Information -->
        <div style="background: var(--bg-subtle); padding: 6px 8px; border-radius: 3px; font-size: 10.5px; margin-bottom: 8px; border-left: 2px solid var(--gov-navy);">
          <div style="color: var(--gov-navy); font-weight: 600;">
            First Appellate Authority (FAA):
          </div>
          <div style="color: var(--ink-secondary); margin-top: 1px;">
            <b>${faa.faa_name || 'Designated Appellate Authority'}</b> &bull; ${faa.designation || 'Appellate Officer'}
          </div>
        </div>

        <!-- Action Controls -->
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed var(--border-subtle); padding-top: 6px;">
          <span style="font-family: var(--font-mono); font-size: 10px; color: var(--ink-muted);">ID: ${p.id || 'GOV-PIO'} &bull; (${p.latitude?.toFixed(4)}, ${p.longitude?.toFixed(4)})</span>
          <div style="display: flex; gap: 6px;">
            ${isAssigned
        ? `<button class="btn-gov-primary" style="font-size: 10.5px; padding: 3px 8px; background: #16A34A; cursor: default; border: none;">✓ Assigned PIO</button>`
        : `<button class="btn-gov-outline" style="font-size: 10.5px; padding: 3px 8px;" onclick="assignPioFromMap('${p.id}')"><span>Assign as Docket PIO</span></button>
                 <button class="btn-gov-outline" style="font-size: 10.5px; padding: 3px 8px;" onclick="openTransferModalForDept('${p.department}')"><span>Transfer Sec 6(3)</span></button>`
      }
          </div>
        </div>
      </div>
    `;
  }).join("");

  renderLucide();
}

async function assignPioFromMap(pioId) {
  if (!currentCase) return;
  const areaPios = currentCase.nearby_area_pios || [];
  const selected = areaPios.find(p => p.id === pioId);
  if (!selected) return;

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/assign-pio`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pio: selected, reviewer: "Counsel / Citizen Desk" })
    });
    const data = await res.json();
    if (res.ok) {
      currentCase = data.case;
      populateWorkspaceFields(data.case);
      updatePioMapForCase(data.case);
      alert(`✓ PIO Assigned Successfully!\n\n• Docket: ${data.case.case_id}\n• Designated PIO: ${selected.pio_name} (${selected.designation})\n• Department: ${selected.department}\n• Distance: ${selected.distance_label}`);
    } else {
      alert(`Error: ${data.message || "Failed to assign PIO"}`);
    }
  } catch (err) {
    console.error("Assign PIO error:", err);
  }
}

function openTransferModalForDept(targetDept) {
  if (!currentCase) return;
  const modal = document.getElementById("transferModal");
  if (modal) modal.style.display = "flex";
  const deptSelect = document.getElementById("transferDeptSelect");
  if (deptSelect && targetDept) deptSelect.value = targetDept;
}

// ----------------------------------------------------
// LAWYER CUSTOM ACTS & STATUTORY INGESTION METHODS
// ----------------------------------------------------

async function loadCustomActs() {
  const container = document.getElementById("customActsContainer");
  const countEl = document.getElementById("customActsCount");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/cases/custom-acts`);
    const data = await res.json();
    if (!res.ok) return;

    const acts = data.custom_acts || [];
    if (countEl) countEl.textContent = acts.length;

    container.innerHTML = "";
    if (acts.length === 0) {
      container.innerHTML = `<div style="grid-column: 1 / -1; color: var(--text-muted); font-size: 12px; padding: 16px;">No custom acts registered yet. Use the form above to add an Act.</div>`;
      return;
    }

    acts.forEach(act => {
      const card = document.createElement("div");
      card.className = "statutory-card";
      card.style.cssText = "display: flex; flex-direction: column; justify-content: space-between; border-left: 3px solid var(--accent-gold);";

      card.innerHTML = `
        <div>
          <div class="statutory-card-header">
            <span>${act.act_title}</span>
            <span class="badge badge-gold">${act.act_id}</span>
          </div>
          <div style="font-family: var(--font-mono); font-size: 11px; color: var(--accent-cyan); margin-bottom: 6px;">
            <b>${act.section}</b>
          </div>
          <div style="margin-bottom: 6px;">
            <span class="badge badge-blue">${act.domain}</span>
          </div>
          <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
            ${act.statutory_grounds}
          </p>
          ${act.punishment_or_relief ? `<div class="text-mono" style="font-size: 10.5px; color: var(--accent-terracotta); margin-bottom: 8px;"><b>Scope:</b> ${act.punishment_or_relief}</div>` : ''}
          <div class="text-mono" style="font-size: 10px; color: var(--text-muted); margin-bottom: 12px;">
            Registered by: <b>${act.added_by}</b> &middot; ${act.created_at}
          </div>
        </div>

        <div style="display: flex; gap: 8px; border-top: 1px solid var(--border-color); padding-top: 10px;">
          <button class="btn btn-sm btn-primary framer-button" style="flex: 1;" onclick="applyCustomActToActiveCase('${act.act_id}')">
            <i data-lucide="link"></i>
            <span>Link to Case</span>
          </button>
          <button class="btn btn-sm btn-outline framer-button" style="color: var(--color-rose); border-color: #FECDD3;" onclick="deleteCustomAct('${act.act_id}')">
            <i data-lucide="trash-2"></i>
          </button>
        </div>
      `;
      container.appendChild(card);
    });
    renderLucide();
  } catch (err) {
    console.error("Error loading custom acts:", err);
  }
}

async function submitCustomAct(event) {
  event.preventDefault();

  const actTitle = document.getElementById("customActTitle").value.trim();
  const section = document.getElementById("customActSection").value.trim();
  const domain = document.getElementById("customActDomain").value;
  const author = document.getElementById("customActAuthor").value.trim();
  const grounds = document.getElementById("customActGrounds").value.trim();
  const relief = document.getElementById("customActRelief").value.trim();
  const linkActive = document.getElementById("customActLinkActive").checked;

  const payload = {
    act_title: actTitle,
    section: section,
    domain: domain,
    added_by: author || "Advocate Legal Counsel",
    statutory_grounds: grounds,
    punishment_or_relief: relief,
    linked_case_id: linkActive && currentCase ? currentCase.case_id : null
  };

  try {
    const res = await fetch(`${API_BASE}/cases/custom-acts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Custom Act Registered into Legal Codex!\n\n• Act ID: ${data.custom_act.act_id}\n• Act: ${data.custom_act.act_title}\n• Section: ${data.custom_act.section}\n${linkActive && currentCase ? `• Linked to Active Case: ${currentCase.case_id}` : ''}`);
      document.getElementById("customActForm").reset();
      loadCustomActs();
      loadRunLogs();

      if (linkActive && currentCase) {
        openCaseById(currentCase.case_id);
      }
    } else {
      alert(`Error: ${data.message || "Failed to register custom act."}`);
    }
  } catch (err) {
    console.error("Custom act submit error:", err);
    alert("Connection error registering custom act.");
  }
}

async function deleteCustomAct(actId) {
  if (!confirm(`Are you sure you want to remove custom act ${actId} from the legal library?`)) {
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cases/custom-acts/${actId}`, {
      method: "DELETE"
    });

    const data = await res.json();
    if (res.ok) {
      loadCustomActs();
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Delete custom act error:", err);
  }
}

async function applyCustomActToActiveCase(actId) {
  if (!currentCase) {
    alert("Please select or open an active case docket first from Command Center.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/apply-custom-act`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ act_id: actId, reviewer: "Adv. S. Kalra" })
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Custom Act ${actId} successfully linked to active case ${currentCase.case_id}!\n\nCheck '03. LEGAL & COMPLIANCE WORKSPACE' to see the added statutory section and grounds.`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Apply custom act error:", err);
  }
}

// ----------------------------------------------------
// EXECUTIVE THEME CONTROLLER (DARK / LIGHT PARCHMENT)
// ----------------------------------------------------

function initTheme() {
  const saved = localStorage.getItem("arzi_theme") || "light";
  applyTheme(saved);
}

function applyTheme(theme) {
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("arzi_theme", theme);
  const icon = document.getElementById("themeIcon");
  const btn = document.getElementById("themeToggleBtn");
  if (icon) {
    if (theme === "dark") {
      icon.setAttribute("data-lucide", "sun");
      if (btn) btn.title = "Switch to Supreme Court Parchment Light Theme";
    } else {
      icon.setAttribute("data-lucide", "moon");
      if (btn) btn.title = "Switch to Executive Dark Theme";
    }
    renderLucide();
  }
}

function toggleExecutiveTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "light";
  const next = current === "dark" ? "light" : "dark";
  applyTheme(next);
}

// ----------------------------------------------------
// WEB SPEECH API VOICE DICTATION
// ----------------------------------------------------

function toggleVoiceDictation() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  const btn = document.getElementById("btnVoiceDictate");
  const status = document.getElementById("voiceStatusText");
  const liveTranscript = document.getElementById("voiceLiveTranscript");
  const textarea = document.getElementById("rawGrievance");

  if (!SpeechRec) {
    alert("Web Speech API is not supported in this browser. Please use Google Chrome, Microsoft Edge, or Safari to dictate grievances.");
    return;
  }

  if (isListeningVoice) {
    if (speechRecognizer) {
      try { speechRecognizer.stop(); } catch (e) { }
    }
    isListeningVoice = false;
    if (btn) btn.classList.remove("recording");
    if (status) status.textContent = "Voice Dictation";
    if (liveTranscript) liveTranscript.style.display = "none";
    return;
  }

  try {
    speechRecognizer = new SpeechRec();
    speechRecognizer.continuous = true;
    speechRecognizer.interimResults = true;
    speechRecognizer.lang = "en-IN"; // Configured for Indian English / Hinglish speech cadence

    speechRecognizer.onstart = () => {
      isListeningVoice = true;
      if (btn) btn.classList.add("recording");
      if (status) status.textContent = "Listening (Speak)...";
      if (liveTranscript) {
        liveTranscript.style.display = "block";
        liveTranscript.textContent = "Listening to microphone...";
      }
    };

    speechRecognizer.onresult = (event) => {
      let interim = "";
      let final = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          final += event.results[i][0].transcript;
        } else {
          interim += event.results[i][0].transcript;
        }
      }

      if (final && textarea) {
        const existing = textarea.value.trim();
        textarea.value = existing ? `${existing} ${final.trim()}` : final.trim();
      }
      if (liveTranscript) {
        liveTranscript.textContent = interim ? `Live: "${interim}"` : (final ? `Dictated: "${final}"` : "Listening...");
      }
    };

    speechRecognizer.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      isListeningVoice = false;
      if (btn) btn.classList.remove("recording");
      if (status) status.textContent = "Voice Dictation";
      if (liveTranscript) {
        liveTranscript.textContent = `Dictation ended (${event.error})`;
        setTimeout(() => { if (liveTranscript) liveTranscript.style.display = "none"; }, 3000);
      }
    };

    speechRecognizer.onend = () => {
      isListeningVoice = false;
      if (btn) btn.classList.remove("recording");
      if (status) status.textContent = "Voice Dictation";
      setTimeout(() => { if (liveTranscript) liveTranscript.style.display = "none"; }, 2500);
    };

    speechRecognizer.start();
  } catch (err) {
    console.error("Speech start error:", err);
    alert("Could not access microphone for voice dictation.");
    isListeningVoice = false;
    if (btn) btn.classList.remove("recording");
    if (status) status.textContent = "Voice Dictation";
  }
}

// ----------------------------------------------------
// 48-HOUR URGENT LIFE & LIBERTY TOGGLE CONTROLLER
// ----------------------------------------------------

async function toggleCurrentCaseUrgency() {
  if (!currentCase) {
    alert("Please select an active docket first.");
    return;
  }
  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/toggle-urgency`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    const data = await res.json();
    if (res.ok) {
      currentCase = data.case;
      populateWorkspaceFields(data.case);
      loadCaseQueue();
      loadRunLogs();
      const statusMsg = data.is_life_liberty
        ? "🚨 Case elevated to 48-Hour Urgent Life & Liberty Fast-Track under Section 7(1) Proviso!\n• Statutory SLA: Compressed to 48 Hours\n• Section 20(1) Penalty: Multiplied for acute life risk\n• Life & Liberty Red Banner stamped across PDF instruments."
        : "✓ Case restored to standard 30-day statutory SLA.";
      alert(statusMsg);
    } else {
      alert(`Error: ${data.message || "Failed to toggle urgency"}`);
    }
  } catch (err) {
    console.error("Toggle urgency error:", err);
    alert("Network error toggling urgency.");
  }
}

// ----------------------------------------------------
// SECTION 8 EXEMPTION SHIELD & NEUTRALIZER CONTROLLER
// ----------------------------------------------------

async function refreshSection8Shield() {
  if (!currentCase) return;
  const body = document.getElementById("section8ShieldBody");
  if (!body) return;

  body.innerHTML = `<div style="text-align: center; padding: 20px; color: var(--ink-muted);">Auditing Section 8 exemptions & generating pre-emptive statutory shields...</div>`;

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/section8-shield`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    const data = await res.json();
    if (!res.ok) {
      body.innerHTML = `<div style="color: var(--status-urgent); padding: 12px;">Failed to audit Section 8 exemptions.</div>`;
      return;
    }

    const shield = data.section_8_shield || {};
    const risks = shield.section_8_risks_identified || [];

    let riskCards = risks.map(r => {
      return `
        <div style="border: 1px solid var(--border-medium); border-left: 3px solid #DC2626; padding: 10px; margin-bottom: 8px; background: var(--bg-surface); border-radius: 2px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <b style="color: var(--gov-navy); font-size: 11.5px;">${r.exemption_section}: ${r.clause_title}</b>
            <span class="status-pill urgent" style="font-size: 9.5px;">POTENTIAL REFUSAL EXCUSE</span>
          </div>
          <div style="font-size: 10.5px; color: var(--ink-muted); margin-bottom: 4px; font-style: italic;">
            <b>Delinquent PIO Claim:</b> "${r.delinquent_pio_excuse}"
          </div>
          <div style="font-size: 10.5px; color: var(--ink-secondary); margin-bottom: 4px;">
            <b>Statutory Neutralizer:</b> ${r.statutory_neutralizer}
          </div>
          <div style="font-size: 10px; color: var(--gov-copper); font-style: italic; margin-bottom: 2px;">
            <b>Judicial Authority:</b> ${r.landmark_precedent}
          </div>
          <div style="font-size: 10px; color: #15803D; font-weight: 600;">
            <b>Legal Ground:</b> ${r.rebuttal_ground}
          </div>
        </div>
      `;
    }).join("");

    body.innerHTML = `
      <div style="margin-bottom: 10px; padding: 8px 10px; background: rgba(30, 58, 138, 0.05); border: 1px solid var(--border-medium); border-radius: 2px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span style="font-weight: 700; color: var(--gov-navy);">Section 8 Exemption Neutralizer Active</span>
          <span class="status-pill approved" style="font-size: 9.5px;">${risks.length} Risk Clauses Audited</span>
        </div>
        <div style="font-size: 10px; color: var(--ink-secondary); margin-top: 4px;">
          <b>${shield.section_8_2_override_text || "Section 8(2) Public Interest Override Active"}</b>
        </div>
        <div style="font-size: 10px; color: #15803D; margin-top: 2px;">
          <b>${shield.section_8_1_j_proviso_text || "Proviso to Section 8(1)(j) Applied"}</b>
        </div>
      </div>

      <div style="margin-bottom: 10px;">
        <label class="form-label" style="font-size: 10px; margin-bottom: 2px;">Pre-emptive Statutory Rebuttal Notice</label>
        <textarea id="section8RebuttalNotice" rows="5" style="width: 100%; font-family: var(--font-mono); font-size: 10px; background: var(--bg-subtle); padding: 6px;" readonly>${shield.statutory_rebuttal_draft || ""}</textarea>
        <button class="btn-gov-outline" style="font-size: 9.5px; padding: 2px 8px; margin-top: 4px;" onclick="navigator.clipboard.writeText(document.getElementById('section8RebuttalNotice').value); alert('Rebuttal notice copied to clipboard!');">📋 Copy Rebuttal Notice</button>
      </div>

      <div>
        <label class="form-label" style="font-size: 10px; margin-bottom: 4px;">Audited Exemption Clauses & Statutory Counter-Measures</label>
        ${riskCards}
      </div>
    `;
  } catch (e) {
    console.error("Section 8 Shield error:", e);
    body.innerHTML = `<div style="color: var(--status-urgent); padding: 12px;">Error contacting Section 8 auditor.</div>`;
  }
}

// ----------------------------------------------------
// INDIAN SPEED POST BARCODE SLIP CONTROLLERS
// ----------------------------------------------------

async function fetchPostalSlipData(caseId) {
  try {
    const res = await fetch(`${API_BASE}/cases/${caseId}/postal-slip`);
    if (res.ok) {
      const data = await res.json();
      return data.postal_slip || data;
    }
  } catch (e) {
    console.error("Error fetching postal slip:", e);
  }
  return null;
}

function buildPostalSlipHtml(slipData) {
  const isUrgent = slipData.statutory_sla?.includes("48") || currentCase?.is_life_liberty;
  const recipient = slipData.addressee || slipData.recipient || {};
  const sender = slipData.sender || {};

  return `
    <div class="postal-slip-card" style="border: 2px solid #0F172A; padding: 16px; background: #FFFFFF; font-family: var(--font-mono); color: #0F172A;">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #0F172A; padding-bottom: 8px; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div style="background: #991B1B; color: #FFFFFF; font-weight: 800; font-size: 15px; padding: 3px 8px; border-radius: 2px; line-height: 1.2;">
            INDIA POST<br/><span style="font-size: 11px; font-weight: 600;">भारतीय डाक</span>
          </div>
          <div>
            <div style="font-weight: 700; font-size: 12.5px; letter-spacing: 0.5px;">SPEED POST & REGISTERED AD • स्पीड पोस्ट एवं पंजीकृत डाक</div>
            <div style="font-size: 9px; color: #475569;">DEPARTMENT OF POSTS, GOVT. OF INDIA • डाक विभाग, भारत सरकार</div>
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 9.5px; font-weight: 700; color: #0F172A;">CONSIGNMENT NO / कंसाइनमेंट नंबर:</div>
          <div style="font-size: 13.5px; font-weight: 800; letter-spacing: 1px; color: #1E3A8A;">${slipData.consignment_number}</div>
        </div>
      </div>

      ${isUrgent ? `
        <div style="background: #FEE2E2; border: 2px dashed #DC2626; color: #991B1B; font-weight: 800; font-size: 10.5px; padding: 6px 10px; margin-bottom: 12px; text-align: center; text-transform: uppercase;">
          🚨 URGENT: 48-HOUR STATUTORY LIFE & LIBERTY DISPATCH — SECTION 7(1) RTI ACT 2005 🚨<br/>
          <span style="font-size: 9.5px; font-weight: 700;">आपातकालीन 48-घंटे विधिक प्रेषण — धारा 7(1) सूचना का अधिकार अधिनियम 2005</span>
        </div>
      ` : ''}

      <div style="text-align: center; margin: 10px 0; background: #FFFFFF; padding: 8px; border: 1px solid #E2E8F0;">
        <div style="display: inline-block;">
          ${slipData.barcode_svg}
        </div>
        <div style="font-size: 11.5px; font-weight: 700; letter-spacing: 2px; margin-top: 4px;">${slipData.consignment_number}</div>
      </div>

      <div class="postal-parties-grid">
        <div>
          <div style="font-size: 9px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 3px;">TO / सेवा में (RECIPIENT PIO):</div>
          <div style="font-size: 11px; font-weight: 700;">${recipient.name || recipient.pio_name || 'Designated PIO'} (${recipient.designation || 'PIO'})</div>
          <div style="font-size: 10px; color: #1E293B;">Department: ${recipient.department || 'Public Authority'}</div>
          <div style="font-size: 10px; color: #334155;">${recipient.office_address || recipient.address || 'N/A'}</div>
          <div style="font-size: 9.5px; color: #334155;">Room: ${recipient.room_no || 'N/A'}</div>
        </div>
        <div>
          <div style="font-size: 9px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 3px;">FROM / प्रेषक (CITIZEN / COUNSEL):</div>
          <div style="font-size: 11px; font-weight: 700;">${sender.name || 'Citizen Applicant'}</div>
          <div style="font-size: 10px; color: #334155;">${sender.address || 'N/A'}</div>
          <div style="font-size: 10px; color: #334155;">Contact: ${sender.contact || 'N/A'}</div>
          <div style="font-size: 9.5px; color: #334155;">Case Docket: <b>${slipData.case_id}</b></div>
        </div>
      </div>

      <div class="postal-meta-grid">
        <div><b>Booking Date / तिथि:</b><br/>${slipData.booking_date}</div>
        <div><b>Weight / वजन:</b><br/>${slipData.article_weight_grams || 45}g</div>
        <div><b>Postage Tariff / शुल्क:</b><br/>₹${slipData.tariff_inr || 41.00}</div>
        <div><b>Category / श्रेणी:</b><br/>Speed Post + AD</div>
      </div>

      <div style="margin-top: 10px; padding-top: 6px; border-top: 1px dashed #94A3B8; font-size: 8px; color: #64748B; line-height: 1.3;">
        <b>STATUTORY PROOF NOTICE / विधिक प्रेषण साक्ष्य:</b> ${slipData.legal_notice || 'Section 27 General Clauses Act presumption applies. धारा 27 साधारण खंड अधिनियम के अंतर्गत विधिक तामीली मानी जाएगी।'}
      </div>
    </div>
  `;
}

async function openPostalSlipModal() {
  if (!currentCase) {
    alert("Please select a case first.");
    return;
  }
  const modal = document.getElementById("postalSlipModal");
  const content = document.getElementById("postalSlipModalContent");
  if (!modal || !content) return;

  content.innerHTML = `<div style="text-align: center; padding: 24px;">Generating Indian Speed Post Dispatch Slip with Code-128 Barcode...</div>`;
  modal.classList.remove("hidden");

  const slipData = await fetchPostalSlipData(currentCase.case_id);
  if (slipData) {
    content.innerHTML = buildPostalSlipHtml(slipData);
  } else {
    content.innerHTML = `<div style="color: var(--status-urgent); padding: 20px;">Could not generate Speed Post dispatch slip.</div>`;
  }
  renderLucide();
}

function closePostalSlipModal() {
  const modal = document.getElementById("postalSlipModal");
  if (modal) modal.classList.add("hidden");
}

function printPostalSlip() {
  window.print();
}

function downloadSlipPdf() {
  if (!currentCase) return;
  window.open(`${API_BASE}/cases/${currentCase.case_id}/pdf?type=slip`, "_blank");
}

async function renderTabPostalSlip() {
  if (!currentCase) return;
  const container = document.getElementById("tabPostalSlipContainer");
  if (!container) return;

  container.innerHTML = `<div style="text-align: center; padding: 20px; color: var(--ink-muted);">Loading Speed Post Dispatch Slip...</div>`;
  const slipData = await fetchPostalSlipData(currentCase.case_id);
  if (slipData) {
    container.innerHTML = buildPostalSlipHtml(slipData);
  } else {
    container.innerHTML = `<div style="color: var(--status-urgent); padding: 12px;">Could not load Speed Post slip.</div>`;
  }
}

// ----------------------------------------------------
// LEAFLET.JS INTERACTIVE OPENSTREETMAP VISUALIZER
// ----------------------------------------------------

function initLeafletPioMap() {
  const mapEl = document.getElementById("pioLeafletMap");
  if (!mapEl || typeof L === "undefined") return;

  if (leafletMap) {
    try { leafletMap.remove(); } catch (e) { }
    leafletMap = null;
  }

  try {
    leafletMap = L.map("pioLeafletMap", {
      center: [25.3176, 82.9739], // Default Varanasi
      zoom: 13,
      zoomControl: true
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '© <a href="https://openstreetmap.org">OpenStreetMap</a>'
    }).addTo(leafletMap);

    leafletMarkersLayer = L.layerGroup().addTo(leafletMap);
  } catch (err) {
    console.error("Leaflet init error:", err);
  }
}

function renderLeafletMapMarkers(c) {
  if (!leafletMap || !leafletMarkersLayer || typeof L === "undefined") return;

  leafletMarkersLayer.clearLayers();

  const citizenCoords = c?.geospatial_meta?.user_coords || c?.suggested_pio?.user_coordinates || { latitude: 25.2905, longitude: 82.9995 };
  const assignedPio = c?.suggested_pio || {};
  const pioCoords = c?.geospatial_meta?.pio_coords || assignedPio.pio_coordinates || { latitude: 25.3340, longitude: 82.9860 };
  const areaPios = c?.nearby_area_pios || c?.geospatial_meta?.nearby_pios || [];

  const bounds = [];

  // 1. Citizen Complainant Marker (Orange CircleMarker)
  if (citizenCoords.latitude && citizenCoords.longitude) {
    const cPt = [citizenCoords.latitude, citizenCoords.longitude];
    bounds.push(cPt);
    const citizenMarker = L.circleMarker(cPt, {
      radius: 9,
      fillColor: "#D97706",
      color: "#FFFFFF",
      weight: 2,
      opacity: 1,
      fillOpacity: 0.95
    }).addTo(leafletMarkersLayer);

    citizenMarker.bindPopup(`
      <div style="font-family: var(--font-ui); font-size: 11px;">
        <b style="color: #D97706;">Citizen Complainant Origin</b><br/>
        <b>${c?.complainant?.name || "Complainant"}</b><br/>
        <span style="font-size: 10px; color: #64748B;">${c?.complainant?.address || "Local Jurisdiction"}</span>
      </div>
    `);
  }

  // 2. Assigned PIO Marker (Royal Blue with Gold border)
  if (pioCoords.latitude && pioCoords.longitude) {
    const pPt = [pioCoords.latitude, pioCoords.longitude];
    bounds.push(pPt);
    const pioMarker = L.circleMarker(pPt, {
      radius: 11,
      fillColor: "#1D4ED8",
      color: "#FEF08A",
      weight: 3,
      opacity: 1,
      fillOpacity: 1
    }).addTo(leafletMarkersLayer);

    pioMarker.bindPopup(`
      <div style="font-family: var(--font-ui); font-size: 11px;">
        <b style="color: #1D4ED8;">★ ASSIGNED DOMAIN PIO</b><br/>
        <b>${assignedPio.pio_name || "Designated PIO"}</b><br/>
        <span style="font-size: 10px; color: #475569;">${assignedPio.designation || "PIO"} &bull; ${assignedPio.department || c?.department}</span><br/>
        <span style="font-size: 10px; font-weight: 700; color: #15803D;">Distance: ${assignedPio.distance_label || "Nearest"}</span>
      </div>
    `);

    // Draw dashed connecting path between citizen and assigned PIO
    if (citizenCoords.latitude && citizenCoords.longitude) {
      const poly = L.polyline([
        [citizenCoords.latitude, citizenCoords.longitude],
        [pioCoords.latitude, pioCoords.longitude]
      ], {
        color: "#1D4ED8",
        weight: 2.5,
        dashArray: "6, 6",
        opacity: 0.8
      }).addTo(leafletMarkersLayer);

      poly.bindTooltip(`${assignedPio.distance_label || "Direct Line"}`, { permanent: false });
    }
  }

  // 3. Other Area Authorities (Slate Markers)
  areaPios.forEach(p => {
    const isAssigned = p.is_assigned || (assignedPio.pio_name === p.pio_name);
    if (isAssigned) return;
    if (p.latitude && p.longitude) {
      const pt = [p.latitude, p.longitude];
      bounds.push(pt);
      const m = L.circleMarker(pt, {
        radius: 6,
        fillColor: "#64748B",
        color: "#FFFFFF",
        weight: 1.5,
        opacity: 0.9,
        fillOpacity: 0.85
      }).addTo(leafletMarkersLayer);

      m.bindPopup(`
        <div style="font-family: var(--font-ui); font-size: 10.5px;">
          <b>${p.pio_name}</b><br/>
          <span style="color: #64748B;">${p.department} &bull; ${p.distance_label}</span><br/>
          <button style="margin-top: 4px; font-size: 9.5px; padding: 2px 6px; cursor: pointer;" onclick="assignPioFromMap('${p.id}')">Reassign Docket to this PIO</button>
        </div>
      `);
    }
  });

  if (bounds.length > 0) {
    try {
      leafletMap.fitBounds(bounds, { padding: [35, 35], maxZoom: 15 });
    } catch (e) {
      console.warn("fitBounds failed:", e);
    }
  }
}

function switchGeoView(viewType) {
  const mapContainer = document.getElementById("leafletMapContainer");
  const radarContainer = document.getElementById("radarCanvasContainer");
  const btnMap = document.getElementById("btnViewMap");
  const btnRadar = document.getElementById("btnViewRadar");

  if (viewType === "map") {
    if (mapContainer) mapContainer.style.display = "block";
    if (radarContainer) radarContainer.style.display = "none";
    if (btnMap) btnMap.classList.add("active");
    if (btnRadar) btnRadar.classList.remove("active");
    if (leafletMap) {
      setTimeout(() => leafletMap.invalidateSize(), 150);
    }
  } else {
    if (mapContainer) mapContainer.style.display = "none";
    if (radarContainer) radarContainer.style.display = "block";
    if (btnRadar) btnRadar.classList.add("active");
    if (btnMap) btnMap.classList.remove("active");
  }
}

// ----------------------------------------------------
// GLOBAL WINDOW SCOPE EXPOSURES FOR HTML ONCLICK BINDINGS
// ----------------------------------------------------
window.showPage = showPage;
window.switchDashTab = switchDashTab;
window.switchDocTab = switchDocTab;
window.switchPersona = switchPersona;
window.switchMainModule = switchMainModule;
window.switchToTab = switchToTab;
window.toggleExecutiveTheme = toggleExecutiveTheme;
window.toggleIntakeForm = toggleIntakeForm;
window.toggleVoiceDictation = toggleVoiceDictation;
window.loadPreset = loadPreset;
window.loadCaseQueue = loadCaseQueue;
window.openCaseById = openCaseById;
window.openCaseWorkspace = openCaseWorkspace;
window.approveCurrentCase = approveCurrentCase;
window.toggleCurrentCaseUrgency = toggleCurrentCaseUrgency;
window.openTransferModal = openTransferModal;
window.closeTransferModal = closeTransferModal;
window.openTransferModalForDept = openTransferModalForDept;
window.submitTransferSec6_3 = submitTransferSec6_3;
window.openPostalSlipModal = openPostalSlipModal;
window.closePostalSlipModal = closePostalSlipModal;
window.printPostalSlip = printPostalSlip;
window.downloadSlipPdf = downloadSlipPdf;
window.viewPdf = viewPdf;
window.refreshSection8Shield = refreshSection8Shield;
window.switchGeoView = switchGeoView;
window.filterRadarDirectory = filterRadarDirectory;
window.loadCustomActs = loadCustomActs;
window.loadRunLogs = loadRunLogs;
window.clearRunLogSearch = clearRunLogSearch;
window.setRunLogSearchQuery = setRunLogSearchQuery;
window.handleRunLogSearch = handleRunLogSearch;
window.inspectCaseFromRunLog = inspectCaseFromRunLog;
window.submitIntake = submitIntake;
window.submitCustomAct = submitCustomAct;
window.handlePincodeInput = handlePincodeInput;
window.assignPioFromMap = assignPioFromMap;
window.deleteCustomAct = deleteCustomAct;
window.applyCustomActToActiveCase = applyCustomActToActiveCase;
window.switchPioMapCase = switchPioMapCase;
window.openCaseDetailView = openCaseDetailView;
window.returnToAuditRunLog = returnToAuditRunLog;
window.openCaseInCaseworkDesk = openCaseInCaseworkDesk;
window.downloadActiveCasePdf = downloadActiveCasePdf;
window.submitCaseUpdateFromDetail = submitCaseUpdateFromDetail;
window.submitCaseMergeFromDetail = submitCaseMergeFromDetail;
window.refreshActiveCaseDetailTimeline = refreshActiveCaseDetailTimeline;
window.populateMergeDuplicateSelect = populateMergeDuplicateSelect;
window.triggerLiveMlPrediction = triggerLiveMlPrediction;
window.getStatusClass = getStatusClass;

// ----------------------------------------------------
// SECTION 20(1) STATUTORY SLA & PENALTY CLOCK CALCULATOR
// ----------------------------------------------------
function initSlaPenaltyCalculator() {
  const filingInput = document.getElementById("slaFilingDate");
  if (!filingInput) return;
  if (!filingInput.value) {
    // Default to 35 days ago to demonstrate overdue penalty calculations immediately
    const d = new Date();
    d.setDate(d.getDate() - 35);
    filingInput.value = d.toISOString().split("T")[0];
  }
  calculateSlaPenalty();
}

function resetSlaCalculator() {
  const filingInput = document.getElementById("slaFilingDate");
  const provSelect = document.getElementById("slaProvisionType");
  const respInput = document.getElementById("slaResponseDate");
  const deptInput = document.getElementById("slaPioDepartment");

  if (filingInput) {
    const d = new Date();
    d.setDate(d.getDate() - 35);
    filingInput.value = d.toISOString().split("T")[0];
  }
  if (provSelect) provSelect.value = "30";
  if (respInput) respInput.value = "";
  if (deptInput) deptInput.value = "Delhi Jal Board / BSES Power Discom";
  calculateSlaPenalty();
}

function calculateSlaPenalty() {
  const filingVal = document.getElementById("slaFilingDate")?.value;
  if (!filingVal) return;

  const filingDate = new Date(filingVal);
  const provVal = document.getElementById("slaProvisionType")?.value || "30";
  let slaDays = 30;
  if (provVal === "2") slaDays = 2;
  else if (provVal === "35_apio" || provVal === "35_transfer") slaDays = 35;
  else if (provVal === "45") slaDays = 45;

  const deadlineDate = new Date(filingDate);
  deadlineDate.setDate(deadlineDate.getDate() + slaDays);

  const respVal = document.getElementById("slaResponseDate")?.value;
  const endDate = respVal ? new Date(respVal) : new Date();

  const diffTime = endDate.getTime() - filingDate.getTime();
  const elapsedDays = Math.max(0, Math.floor(diffTime / (1000 * 60 * 60 * 24)));

  const overdueDays = Math.max(0, elapsedDays - slaDays);
  const penaltyAmount = Math.min(25000, overdueDays * 250);

  const fmtOpts = { day: "2-digit", month: "short", year: "numeric" };
  const deadlineStr = deadlineDate.toLocaleDateString("en-IN", fmtOpts);
  const filingStr = filingDate.toLocaleDateString("en-IN", fmtOpts);
  const targetDept = document.getElementById("slaPioDepartment")?.value || "Public Authority";

  const elDeadline = document.getElementById("slaDeadlineDisplay");
  const elElapsed = document.getElementById("slaElapsedDaysDisplay");
  const elOverdue = document.getElementById("slaOverdueDaysDisplay");
  const elPenalty = document.getElementById("slaPenaltyAmountDisplay");
  const elPill = document.getElementById("slaClockStatusPill");
  const elGuidanceBox = document.getElementById("slaGuidanceBox");
  const elGuidanceTitle = document.getElementById("slaGuidanceTitle");
  const elGuidanceText = document.getElementById("slaGuidanceText");
  const elClause = document.getElementById("slaGeneratedClause");

  if (elDeadline) elDeadline.textContent = deadlineStr;
  if (elElapsed) elElapsed.textContent = `${elapsedDays} Days`;
  if (elOverdue) {
    elOverdue.textContent = `${overdueDays} Days`;
    elOverdue.style.color = overdueDays > 0 ? "var(--status-review)" : "var(--status-active)";
  }
  if (elPenalty) {
    elPenalty.textContent = `₹${penaltyAmount.toLocaleString("en-IN")}`;
    elPenalty.style.color = overdueDays > 0 ? "var(--status-review)" : "var(--status-active)";
  }

  if (elPill) {
    elPill.className = "status-pill";
    if (overdueDays > 0) {
      elPill.classList.add("needs-review");
      elPill.textContent = `Statutory Overdue (₹${penaltyAmount.toLocaleString("en-IN")})`;
    } else if (elapsedDays >= slaDays - 5) {
      elPill.classList.add("under-review");
      elPill.textContent = "Approaching Deadline";
    } else {
      elPill.classList.add("approved");
      elPill.textContent = "Within Statutory Window";
    }
  }

  if (elGuidanceBox && elGuidanceTitle && elGuidanceText) {
    if (overdueDays > 0) {
      elGuidanceBox.style.borderLeftColor = "var(--status-review)";
      elGuidanceTitle.style.color = "var(--status-review)";
      if (currentLang === "hi") {
        elGuidanceTitle.textContent = `⚠️ वैधानिक डिफ़ॉल्ट: वेतन से कटौती प्रारंभ (${overdueDays} दिन का विलंब)`;
        elGuidanceText.innerHTML = `<b>${escapeHtml(targetDept)}</b> के जन सूचना अधिकारी ने कानूनी 30-दिवसीय सीमा का <b>${overdueDays} दिन</b> उल्लंघन किया है। आरटीआई अधिनियम की धारा 20(1) के तहत ₹250/दिन की दर से कुल <b>₹${penaltyAmount.toLocaleString("en-IN")}</b> जुर्माना देय है जो अधिकारी के वेतन से काटा जाएगा। तुरंत धारा 19(1) के तहत प्रथम अपील दर्ज करें।`;
      } else if (currentLang === "bi") {
        elGuidanceTitle.textContent = `⚠️ Statutory Default: Personal Salary Deduction Triggered (${overdueDays} Days Overdue) • वैधानिक विलंब: वेतन कटौती लागू`;
        elGuidanceText.innerHTML = `The Designated PIO at <b>${escapeHtml(targetDept)}</b> has exceeded statutory SLA by <b>${overdueDays} days</b>. Under Section 20(1), a mandatory ₹250/day penalty (Total: <b>₹${penaltyAmount.toLocaleString("en-IN")}</b>) has accrued.<br/><span style="color: var(--ink-secondary); font-size: 11px; display: inline-block; margin-top: 4px;">संबंधित जन सूचना अधिकारी ने तय सीमा से <b>${overdueDays} दिन</b> का विलंब किया है। धारा 20(1) के तहत कुल <b>₹${penaltyAmount.toLocaleString("en-IN")}</b> जुर्माना अधिकारी के वेतन से काटा जाएगा।</span>`;
      } else {
        elGuidanceTitle.textContent = `⚠️ Statutory Default: Personal Salary Deduction Triggered (${overdueDays} Days Overdue)`;
        elGuidanceText.innerHTML = `The Designated Public Information Officer at <b>${escapeHtml(targetDept)}</b> has exceeded the statutory deadline by <b>${overdueDays} days</b> without lawful order. Under Section 20(1) of the RTI Act 2005 and Supreme Court precedent <i>Manohar Anchule (2013)</i>, a mandatory penalty of ₹250/day (Total: <b>₹${penaltyAmount.toLocaleString("en-IN")}</b>) has accrued and is deductible directly from the officer's salary. Recommended action: Immediately file First Appeal under Section 19(1) or penalty complaint under Section 18.`;
      }
    } else {
      elGuidanceBox.style.borderLeftColor = "var(--status-active)";
      elGuidanceTitle.style.color = "var(--status-active)";
      if (currentLang === "hi") {
        elGuidanceTitle.textContent = "✓ आवेदन वैधानिक समयसीमा के भीतर";
        elGuidanceText.innerHTML = `<b>${filingStr}</b> को दर्ज आवेदन अभी निर्धारित ${slaDays}-दिवसीय समयसीमा में है। अधिकारी को <b>${deadlineStr}</b> तक जानकारी देनी होगी।`;
      } else if (currentLang === "bi") {
        elGuidanceTitle.textContent = "✓ Within Statutory Window • वैधानिक समयसीमा के भीतर";
        elGuidanceText.innerHTML = `Application filed on <b>${filingStr}</b> is within lawful ${slaDays}-day window. PIO has until <b>${deadlineStr}</b> to furnish information.<br/><span style="color: var(--ink-secondary); font-size: 11px; display: inline-block; margin-top: 4px;">आवेदन अभी निर्धारित सीमा में है। अधिकारी को <b>${deadlineStr}</b> तक जवाब देना अनिवार्य है।</span>`;
      } else {
        elGuidanceTitle.textContent = "✓ Application Within Lawful SLA Window";
        elGuidanceText.innerHTML = `Application filed on <b>${filingStr}</b> is currently within the lawful ${slaDays}-day SLA window. The PIO has until <b>${deadlineStr}</b> to furnish the certified information or issue a Section 6(3) transfer notice.`;
      }
    }
  }

  if (elClause) {
    if (overdueDays > 0) {
      elClause.value = `TAKE NOTICE that the Applicant submitted RTI Application dated ${filingStr} before the Designated PIO, ${targetDept}. In terms of Section 7(1) of the RTI Act 2005, the statutory 30-day window expired on ${deadlineStr}. The PIO has defaulted for ${overdueDays} days without reasonable cause. Under Section 20(1) and the law declared in Manohar s/o Manikrao Anchule v. State of Maharashtra (AIR 2013 SC 681), the PIO is personally liable for a penalty of ₹250 per day amounting to ₹${penaltyAmount.toLocaleString("en-IN")}, deductible directly from the officer's personal salary.`;
    } else {
      elClause.value = `IN RE: RTI Application dated ${filingStr} submitted before Designated PIO, ${targetDept}. Statutory compliance deadline under Section 7(1) of RTI Act 2005 expires on ${deadlineStr}.`;
    }
  }
}

function copySlaNoticeClause() {
  const elClause = document.getElementById("slaGeneratedClause");
  const btnText = document.getElementById("copyClauseBtnText");
  if (!elClause) return;

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(elClause.value).then(() => {
      if (btnText) {
        const orig = btnText.textContent;
        btnText.textContent = "Copied!";
        setTimeout(() => { btnText.textContent = orig; }, 2000);
      }
    }).catch(() => {
      fallbackCopy(elClause, btnText);
    });
  } else {
    fallbackCopy(elClause, btnText);
  }
}

function fallbackCopy(elClause, btnText) {
  elClause.select();
  document.execCommand("copy");
  if (btnText) {
    const orig = btnText.textContent;
    btnText.textContent = "Copied!";
    setTimeout(() => { btnText.textContent = orig; }, 2000);
  }
}

// ----------------------------------------------------
// STATUTORY CODEX REAL-TIME MATRIX FILTER (PAGE 3)
// ----------------------------------------------------
function filterStatutoryMatrix() {
  const query = (document.getElementById("statutorySearchInput")?.value || "").toLowerCase().trim();
  const table = document.getElementById("statutoryCodexTable");
  if (!table) return;
  const rows = table.querySelectorAll("tbody tr");
  let matchCount = 0;

  rows.forEach(r => {
    const text = r.textContent.toLowerCase();
    if (!query || text.includes(query)) {
      r.style.display = "";
      matchCount++;
    } else {
      r.style.display = "none";
    }
  });

  const countEl = document.getElementById("statutoryFilterCount");
  if (countEl) {
    countEl.textContent = `${matchCount} Provision${matchCount === 1 ? "" : "s"} Active`;
  }
}

// Window bindings
window.initSlaPenaltyCalculator = initSlaPenaltyCalculator;
window.resetSlaCalculator = resetSlaCalculator;
window.calculateSlaPenalty = calculateSlaPenalty;
window.copySlaNoticeClause = copySlaNoticeClause;
window.filterStatutoryMatrix = filterStatutoryMatrix;

// Auto-initialize calculator on DOM load
document.addEventListener("DOMContentLoaded", () => {
  initSlaPenaltyCalculator();
});
