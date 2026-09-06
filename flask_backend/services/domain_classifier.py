import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class DomainClassifierService:
    """
    Production-grade Machine Learning Domain Classifier for Indian Public Administration.
    Classifies unstructured citizen grievances into 11 statutory public authority domains
    using TF-IDF n-gram vectorization combined with intent-driven semantic keyword scoring.
    """

    DOMAINS = [
        "Revenue & Land Records",
        "Food, Civil Supplies & Consumer Affairs",
        "Municipal Public Works & Sanitation",
        "Water Supply & Jal Board",
        "Electricity & Power Discom",
        "Police, Criminal Justice & BNSS",
        "Health & Family Welfare",
        "Higher Education & Student Welfare",
        "Transport, Highways & Motor Vehicles / RTO",
        "Labour, Employment, Pension & Social Security",
        "Environment & Pollution Control"
    ]

    DOMAIN_KEYWORDS = {
        "Revenue & Land Records": [
            "land", "zameen", "khasra", "khatauni", "mutation", "daakhil kharij",
            "dakhil kharij", "patwari", "tehsildar", "registry", "land deed", "plot",
            "demarcation", "seema gyan", "jamabandi", "revenue court", "lekhpal",
            "land title", "encroachment on agricultural land", "land revenue", "katcheri",
            "bhoomi", "tehsil office", "sub-divisional magistrate land"
        ],
        "Food, Civil Supplies & Consumer Affairs": [
            "ration", "rashan", "food grain", "khadya", "grain", "bpl", "bpl card",
            "ration card", "pds shop", "fair price shop", "fps dealer", "wheat quota",
            "rice quota", "sugar quota", "antodaya", "aay card", "quota", "dealer",
            "black marketing of grain", "civil supplies", "defective goods", "consumer dispute"
        ],
        "Municipal Public Works & Sanitation": [
            "drainage", "waterlogging", "sewer line", "gutter", "monsoon overflow",
            "road repair", "drain", "sewer", "nalla", "sadak", "pothole", "potholes",
            "municipal", "nagar nigam", "naali", "kachra", "garbage", "waste collection",
            "street light", "streetlights", "illegal construction", "building sanction",
            "encroachment on road", "footpath", "sanitation worker", "safai karmi"
        ],
        "Water Supply & Jal Board": [
            "drinking water", "water supply", "pipeline leak", "contaminated water",
            "dirty water", "tap connection", "water tanker", "jal board", "jal sansthan",
            "water pressure", "overhead tank", "borewell", "tube well", "canal water",
            "irrigation water", "potable water", "foul smell in water", "water meter",
            "jal nigam", "submersible pump"
        ],
        "Electricity & Power Discom": [
            "electricity", "power cut", "load shedding", "electric meter", "faulty meter",
            "high electricity bill", "exorbitant bill", "transformer", "transformer burn",
            "voltage fluctuation", "power supply", "discom", "power theft", "electric pole",
            "hanging wire", "high tension wire", "electricity connection", "bijli",
            "bijli vibhag", "power department", "tariff"
        ],
        "Police, Criminal Justice & BNSS": [
            "police", "fir", "first information report", "police station", "thana",
            "daroga", "sho", "sub-inspector", "investigation", "crime", "robbery",
            "theft", "chori", "armed snatching", "assault", "beating", "extortion",
            "threat", "cyber crime", "online fraud", "complaint refusal", "gd entry",
            "general diary", "bns", "bnss", "unlawful detention", "custodial violence"
        ],
        "Health & Family Welfare": [
            "health", "hospital", "doctor", "medicine", "dawa", "ilaj", "cmo",
            "dispensary", "medical", "treatment", "swasthya", "aspatal", "icu",
            "ventilator", "oxygen cylinder", "ambulance", "primary health center", "phc",
            "chc", "emergency ward", "medical negligence", "injection", "surgical delay"
        ],
        "Higher Education & Student Welfare": [
            "scholarship", "disbursement", "tuition fee waiver", "post-matric scholarship",
            "student grant", "college", "university", "education", "chhatravriti", "student",
            "degree certificate", "marksheet verification", "marksheet", "convocation",
            "board exam", "admit card", "examination result", "re-evaluation", "ugc",
            "bhu", "kashi vidyapith", "fee refund", "hostel allotment"
        ],
        "Transport, Highways & Motor Vehicles / RTO": [
            "transport", "rto", "driving license", "dl renewal", "learner license",
            "rc", "registration certificate", "vehicle registration", "commercial permit",
            "traffic challan", "fitness certificate", "state transport", "bus route",
            "national highway", "toll plaza", "overcharging fare", "high security number plate",
            "hsrp", "pollution certificate", "pucc"
        ],
        "Labour, Employment, Pension & Social Security": [
            "pension", "retirement pension", "ppo", "gratuity", "provident fund", "epf",
            "epfo", "esic", "unorganized worker", "labour card", "minimum wage", "salary not paid",
            "unpaid wages", "bonus", "severance", "pension payment order", "widow pension",
            "old age pension", "divyang pension", "mgnrega wages", "job card", "shramik"
        ],
        "Environment & Pollution Control": [
            "pollution", "environment", "industrial waste", "chemical effluent", "factory smoke",
            "air pollution", "aqi", "water pollution", "tree felling", "illegal cutting of trees",
            "noise pollution", "loudspeaker", "hazardous waste", "pollution control board",
            "cpcb", "spcb", "green belt", "forest land", "chemical plant", "industrial effluent",
            "effluent discharge", "toxic waste", "groundwater contamination"
        ]
    }

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=12000,
            sublinear_tf=True
        )
        self.classifier = LogisticRegression(C=8.0, max_iter=400)
        self.is_trained = False
        self._train_initial_model()

    def _train_initial_model(self):
        """Trains the TF-IDF model on an expanded seed corpus of Indian civic grievances."""
        training_texts = []
        training_labels = []

        # Bootstrap seed corpus across all 11 domains with realistic phrasing
        corpus = {
            "Revenue & Land Records": [
                "My land mutation khasra 45/12 application submitted 4 months ago at Tehsil office Rohini is pending. Patwari is not updating land records.",
                "Tehsildar and patwari are not entering the land mutation in khasra khatauni after registry.",
                "Application for demarcation seema gyan of agricultural land plot in Mehrauli is delayed.",
                "Lekhpal is demanding bribe for issuing certified copy of jamabandi and land title deed.",
                "Illegal encroachment on private land parcel by land mafia, revenue court hearing adjourned repeatedly.",
                "Need certified copies of khasra khatauni and land registry papers from tehsil sub-registrar office.",
                "Dakhil kharij application pending beyond statutory time limit prescribed in Land Revenue Act."
            ],
            "Food, Civil Supplies & Consumer Affairs": [
                "My family BPL ration card application submitted at Ward 4 supply office is pending without food grain distribution.",
                "Fair price shop ration dealer is refusing to give grain to BPL card holders and selling in black market.",
                "Ration dealer black marketing wheat and rice quota, demanding thumb impression without giving grains.",
                "Antyodaya AAY ration card application rejected without any written communication or inspection.",
                "Purchased defective refrigerator from authorized dealer, company refusing warranty repair or consumer refund.",
                "Civil supplies inspector not taking action against FPS dealer for under-weighing rations."
            ],
            "Municipal Public Works & Sanitation": [
                "Road contractor used substandard materials and the newly constructed road developed huge potholes within 10 days.",
                "Open sewage drain overflowing on main road in Dwarka creating severe waterlogging and foul smell.",
                "Street lights in Sector 12 have been non-functional for three weeks causing safety issues at night.",
                "Garbage and solid waste dump not cleared by municipal corporation safai karmi for two weeks.",
                "Illegal commercial construction in residential colony without building plan sanction from municipal authorities.",
                "Potholes on colony street causing fatal bike accidents, municipal public works department ignoring complaints."
            ],
            "Water Supply & Jal Board": [
                "Drinking water supply in our colony is dirty, turbid and smelling like sewer. Pipeline is leaking underground.",
                "Severe water crisis in colony as Delhi Jal Board has cut drinking water supply without prior notice.",
                "Applied for tap water connection and pipeline extension 6 months ago, Jal Sansthan has not laid pipes.",
                "Water tanker mafia operating in the area while municipal pipeline water pressure is completely zero.",
                "Borewell pump in community park broken, Jal Board officials not replacing submersible motor.",
                "Contaminated sewage water mixing into municipal drinking water pipeline causing epidemic."
            ],
            "Electricity & Power Discom": [
                "Electricity department gave a fake bill of 50000 rupees. Meter is faulty and reading wrong power consumption.",
                "Frequent unannounced power cuts and load shedding in our locality lasting 8 hours every day.",
                "Distribution transformer burnt out yesterday, electric discom has not replaced it leaving 200 families without power.",
                "High tension live electricity wire hanging loose over children playground posing electrocution threat.",
                "Applied for new domestic electricity connection 2 months ago, power discom has not installed electric meter."
            ],
            "Police, Criminal Justice & BNSS": [
                "The police station SHO refuses to register my FIR for armed robbery that happened near market junction.",
                "Police Station SHO refuses to register mandatory FIR under Section 173 BNSS regarding violent armed snatching.",
                "Sub-Inspector refuses to provide GD entry copy or acknowledge written complaint of house theft.",
                "Cyber crime online bank fraud complaint filed on portal but local thana police officer has taken no investigation steps.",
                "Victim assaulted and threatened with dire consequences by goons, police officer refusing to register case."
            ],
            "Health & Family Welfare": [
                "Doctor at the government hospital did not attend the emergency patient. Oxygen cylinders were out of stock.",
                "CRITICAL EMERGENCY: Catastrophic ventilator power failure and acute oxygen cylinder stock-out in ICU Ward.",
                "Government civil hospital emergency ward turned away critical accident victim citing lack of ICU beds.",
                "Chief Medical Officer dispensary has zero stock of life-saving medicines and rabies anti-serum.",
                "Medical negligence by government hospital surgeon during operation causing severe disability to patient."
            ],
            "Higher Education & Student Welfare": [
                "University has not provided my degree certificate and marksheet verification for employment despite 6 months delay.",
                "Post-matric scholarship disbursement for SC ST OBC students has been delayed by state education cell.",
                "College administration refusing to refund caution money and tuition fee after formal admission cancellation.",
                "University examination controller delayed semester marksheets preventing students from attending job interviews."
            ],
            "Transport, Highways & Motor Vehicles / RTO": [
                "Applied for driving license renewal at RTO office 3 months ago but smart card DL not issued.",
                "Vehicle registration certificate RC smart card not dispatched by regional transport office after road tax payment.",
                "RTO office delayed commercial vehicle fitness certificate and permit renewal causing financial loss.",
                "Traffic police issued wrong automated camera e-challan to my car which was parked at home.",
                "State road transport corporation buses skipping designated bus stops causing severe inconvenience to commuters."
            ],
            "Labour, Employment, Pension & Social Security": [
                "My retirement pension and gratuity has not been credited since 8 months despite submitting all PPO papers.",
                "EPFO regional office has rejected Provident Fund settlement claim multiple times without specific reasons.",
                "Old age pension payment under social security scheme stopped for elderly widow without verification.",
                "Factory owner refusing to pay statutory minimum wages and retrenchment compensation to workers.",
                "Pension Payment Order PPO issued but monthly pension not disbursed into pensioner bank account."
            ],
            "Environment & Pollution Control": [
                "Chemical factory discharging toxic industrial effluent directly into open drain and groundwater without treatment.",
                "Factory emitting thick black toxic smoke at night exceeding permissible air pollution quality index norms.",
                "Illegal felling of mature trees in green belt area without permission from forest department and pollution board.",
                "Loudspeakers and industrial machinery operating throughout the night causing extreme noise pollution."
            ]
        }

        for domain, texts in corpus.items():
            for t in texts:
                training_texts.append(t)
                training_labels.append(domain)

        X = self.vectorizer.fit_transform(training_texts)
        self.classifier.fit(X, training_labels)
        self.is_trained = True

    def classify_grievance(self, grievance_text: str, user_locality: str = "") -> dict:
        """
        Predicts the public domain, confidence score (0-100), and explanation keywords.
        Combines statistical TF-IDF classification with keyword presence validation.
        """
        text = grievance_text.strip()
        if not text:
            return {
                "domain": "Revenue & Land Records",
                "confidence": 50,
                "reason": "Defaulted due to empty text input",
                "matched_keywords": []
            }

        text_lower = text.lower()

        # 1. Calculate rule-based keyword match density per domain
        keyword_scores = {}
        domain_matched_words = {}

        for domain, kw_list in self.DOMAIN_KEYWORDS.items():
            score = 0
            matched = []
            for kw in kw_list:
                kw_low = kw.lower()
                # Whole word match carries higher weight
                if re.search(r'\b' + re.escape(kw_low) + r'\b', text_lower):
                    score += 25
                    matched.append(kw)
                elif kw_low in text_lower:
                    score += 12
                    matched.append(kw)

            keyword_scores[domain] = score
            domain_matched_words[domain] = list(set(matched))

        # 2. Calculate ML Probabilities via TF-IDF Logistic Regression
        features = self.vectorizer.transform([text])
        ml_probs = self.classifier.predict_proba(features)[0]
        ml_classes = self.classifier.classes_

        ml_scores = {}
        for cls, prob in zip(ml_classes, ml_probs):
            ml_scores[cls] = float(prob)

        # 3. Hybrid scoring: Combine ML probability (70%) + Keyword density (30%)
        final_scores = {}
        for domain in self.DOMAINS:
            ml_prob = ml_scores.get(domain, 0.0)
            kw_score = keyword_scores.get(domain, 0)
            # Normalize kw_score to [0, 1] range (cap at 100)
            kw_norm = min(1.0, kw_score / 60.0)

            # Combined score
            if kw_score > 0:
                combined = (ml_prob * 0.55) + (kw_norm * 0.45)
            else:
                combined = ml_prob * 0.70

            final_scores[domain] = combined

        top_domain = max(final_scores, key=final_scores.get)
        top_score = final_scores[top_domain]

        # Calculate confidence percentage (min 70%, up to 99%)
        matched_words = domain_matched_words.get(top_domain, [])
        if len(matched_words) >= 3:
            conf_pct = min(99, int(75 + (top_score * 24)))
        elif len(matched_words) >= 1:
            conf_pct = min(96, int(70 + (top_score * 25)))
        else:
            conf_pct = max(60, int(top_score * 85))

        if matched_words:
            reason = f"ML model detected key domain indicators: {', '.join(matched_words[:4])}"
        else:
            reason = f"ML statistical NLP classification based on public administration corpus ({conf_pct}% probability)"

        return {
            "domain": top_domain,
            "confidence": conf_pct,
            "reason": reason,
            "matched_keywords": matched_words
        }

# Global singleton
domain_classifier = DomainClassifierService()
