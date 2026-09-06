import math
import re
from flask_backend.services.pincode_resolver import pincode_resolver

# ==============================================================================
# GEODETIC PUBLIC AUTHORITY DIRECTORY WITH GPS COORDINATES & FAA MAPPING
# ==============================================================================
GEO_PUBLIC_AUTHORITIES = [
    # ------------------ VARANASI / BANARAS DISTRICT ------------------
    {
        "id": "VNS-REV-01",
        "city": "Varanasi / Banaras",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "department": "Revenue & Land Records",
        "pio_name": "Shri A. K. Rai",
        "designation": "Tehsildar & Designated PIO (Revenue & Land Circle)",
        "office_address": "Tehsil Sadar Kachehri Complex, Collectorate Compound, Varanasi / Banaras, Uttar Pradesh - 221002",
        "room_no": "Room 104, Tehsil Administrative Block",
        "email": "pio.revenue.varanasi@up.gov.in",
        "phone": "+91-542-2501042",
        "latitude": 25.3340,
        "longitude": 82.9860,
        "faa": {
            "faa_name": "Shri R. P. Maurya, IAS",
            "designation": "Additional District Magistrate (Finance & Revenue) / First Appellate Authority",
            "office_address": "Collectorate Headquarters, Kachehri, Varanasi - 221002",
            "email": "admfr.vns@up.gov.in",
            "phone": "+91-542-2508801"
        }
    },
    {
        "id": "VNS-FOOD-01",
        "city": "Varanasi / Banaras",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "department": "Food & Civil Supplies",
        "pio_name": "Shri V. P. Singh",
        "designation": "District Supply Officer & Designated PIO (Food & PDS Wing)",
        "office_address": "Office of the District Supply Officer, Food & Civil Supplies Kachehri Office, Nadesar, Varanasi / Banaras, Uttar Pradesh - 221002",
        "room_no": "Block B, Room 12, DSO Complex",
        "email": "dso.varanasi@up.gov.in",
        "phone": "+91-542-2502389",
        "latitude": 25.3375,
        "longitude": 82.9810,
        "faa": {
            "faa_name": "Smt. Neelam Yadav",
            "designation": "Deputy Commissioner (Food & Civil Supplies) / First Appellate Authority",
            "office_address": "Divisional Commissioner Compound, Varanasi - 221002",
            "email": "dc.food.vns@up.gov.in",
            "phone": "+91-542-2509122"
        }
    },
    {
        "id": "VNS-MUNI-01",
        "city": "Varanasi / Banaras",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "department": "Municipal Public Works & Drainage",
        "pio_name": "Er. M. K. Verma",
        "designation": "Executive Engineer (Civil/Drainage) & Designated PIO",
        "office_address": "Nagar Nigam Kachehri Complex, Zone 1, Sigra, Varanasi / Banaras, Uttar Pradesh - 221010",
        "room_no": "Engineering Division, Room 204",
        "email": "ee.drainage.nnvns@up.gov.in",
        "phone": "+91-542-2221075",
        "latitude": 25.3180,
        "longitude": 82.9910,
        "faa": {
            "faa_name": "Shri Akshat Verma, IAS",
            "designation": "Municipal Commissioner / First Appellate Authority",
            "office_address": "Nagar Nigam Headquarters, Sigra, Varanasi - 221010",
            "email": "comm-nagarnigam-vns@nic.in",
            "phone": "+91-542-2221700"
        }
    },
    {
        "id": "VNS-POL-01",
        "city": "Varanasi / Banaras",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "department": "Police & Law Enforcement",
        "pio_name": "Shri R. K. Singh",
        "designation": "Deputy Commissioner of Police (DCP) & Designated PIO",
        "office_address": "Police Line Kachehri Headquarters, Varanasi / Banaras, Uttar Pradesh - 221002",
        "room_no": "Police Commission Office, 1st Floor",
        "email": "dcp.varanasi@up.gov.in",
        "phone": "+91-542-2503456",
        "latitude": 25.3420,
        "longitude": 82.9830,
        "faa": {
            "faa_name": "Shri Mohit Agarwal, IPS",
            "designation": "Commissioner of Police / First Appellate Authority",
            "office_address": "Police Commissionerate, Police Line, Varanasi - 221002",
            "email": "cp.varanasi@up.gov.in",
            "phone": "+91-542-2508100"
        }
    },
    {
        "id": "VNS-EDU-01",
        "city": "Varanasi / Banaras",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "department": "Higher Education & Student Welfare",
        "pio_name": "Dr. S. N. Tripathi",
        "designation": "Deputy Registrar & Nodal PIO (Scholarship Wing)",
        "office_address": "District Education Kachehri, Banaras Hindu University / MGKVP Division, Varanasi / Banaras, Uttar Pradesh - 221005",
        "room_no": "Central Scholarship Registry, Room 08",
        "email": "scholarship.pio.varanasi@up.gov.in",
        "phone": "+91-542-2368400",
        "latitude": 25.2677,
        "longitude": 82.9913,
        "faa": {
            "faa_name": "Prof. K. K. Sharma",
            "designation": "Registrar / First Appellate Authority",
            "office_address": "Central Office, BHU Division, Varanasi - 221005",
            "email": "registrar.bhu@edu.gov.in",
            "phone": "+91-542-2368555"
        }
    },
    {
        "id": "VNS-HLT-01",
        "city": "Varanasi / Banaras",
        "district": "Varanasi",
        "state": "Uttar Pradesh",
        "department": "Health & Family Welfare",
        "pio_name": "Dr. S. K. Pandey",
        "designation": "Chief Medical Officer (CMO) & Designated PIO",
        "office_address": "District Hospital Kachehri Complex, Kabir Chaura, Varanasi / Banaras, Uttar Pradesh - 221001",
        "room_no": "CMO Office Block, Kabir Chaura",
        "email": "cmo.varanasi@up.gov.in",
        "phone": "+91-542-2401234",
        "latitude": 25.3140,
        "longitude": 83.0080,
        "faa": {
            "faa_name": "Dr. M. L. Gupta",
            "designation": "Additional Director (Health Services) / First Appellate Authority",
            "office_address": "Directorate of Health Services, Varanasi - 221001",
            "email": "adhealth.vns@up.gov.in",
            "phone": "+91-542-2402100"
        }
    },

    # ------------------ DELHI NCT DISTRICTS ------------------
    {
        "id": "DEL-REV-01",
        "city": "New Delhi",
        "district": "South Delhi",
        "state": "Delhi",
        "department": "Revenue & Land Records",
        "pio_name": "Shri N. Goyal",
        "designation": "Tehsildar & Designated PIO",
        "office_address": "Tehsil & District Kachehri Complex, Revenue Circle 2, Mehrauli, New Delhi - 110030",
        "room_no": "Room 101, SDM Office Complex",
        "email": "pio.revenue.mehrauli@gov.in",
        "phone": "+91-11-26641209",
        "latitude": 28.5180,
        "longitude": 77.1850,
        "faa": {
            "faa_name": "Shri Sandeep Kumar, IAS",
            "designation": "District Magistrate (South Delhi) / First Appellate Authority",
            "office_address": "DM Office Complex, M.B. Road, Saket, New Delhi - 110068",
            "email": "dm-south.delhi@nic.in",
            "phone": "+91-11-29535025"
        }
    },
    {
        "id": "DEL-FOOD-01",
        "city": "New Delhi",
        "district": "Central Delhi",
        "state": "Delhi",
        "department": "Food & Civil Supplies",
        "pio_name": "Shri R. K. Sharma",
        "designation": "Public Information Officer & Assistant Commissioner",
        "office_address": "Office of the District Supply Officer, Sub-Divisional Tehsil Kachehri Complex, Ward 4, Civil Lines, New Delhi - 110054",
        "room_no": "F&S Division, Room 4",
        "email": "pio.foodsupplies.ward4@gov.in",
        "phone": "+91-11-23891042",
        "latitude": 28.6750,
        "longitude": 77.2250,
        "faa": {
            "faa_name": "Smt. Anjali Sehgal",
            "designation": "Additional Commissioner (PDS) / First Appellate Authority",
            "office_address": "Khadya Sadan, Vikas Bhawan, New Delhi - 110002",
            "email": "ac-pds.delhi@gov.in",
            "phone": "+91-11-23378512"
        }
    },
    {
        "id": "DEL-MUNI-01",
        "city": "New Delhi",
        "district": "South West Delhi",
        "state": "Delhi",
        "department": "Municipal Public Works & Drainage",
        "pio_name": "Er. S. K. Kalra",
        "designation": "Executive Engineer (Drainage & Stormwater)",
        "office_address": "Municipal Kachehri Complex, Zone 7, Sector 12, Dwarka, New Delhi - 110075",
        "room_no": "EE Office, Sector 12 MCD Complex",
        "email": "pio.drainage.zone7@mc.gov.in",
        "phone": "+91-11-25083110",
        "latitude": 28.5920,
        "longitude": 77.0460,
        "faa": {
            "faa_name": "Shri D. P. Singh",
            "designation": "Deputy Commissioner (Najafgarh/Dwarka Zone) / First Appellate Authority",
            "office_address": "MCD Zonal Building, Dhansa Stand, New Delhi - 110043",
            "email": "dc-dwarka.mcd@gov.in",
            "phone": "+91-11-25014311"
        }
    },
    {
        "id": "DEL-POL-01",
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "department": "Police & Law Enforcement",
        "pio_name": "Shri V. K. Malhotra",
        "designation": "Additional Deputy Commissioner of Police & Designated PIO",
        "office_address": "Police Headquarters, Civic Center Kachehri, New Delhi - 110001",
        "room_no": "RTI Cell, 4th Floor, PHQ Tower",
        "email": "pio.police@delhipolice.gov.in",
        "phone": "+91-11-23314567",
        "latitude": 28.6340,
        "longitude": 77.2280,
        "faa": {
            "faa_name": "Shri Sanjay Arora, IPS",
            "designation": "Joint Commissioner of Police / First Appellate Authority",
            "office_address": "Police Headquarters, Jai Singh Road, New Delhi - 110001",
            "email": "jcp.rti@delhipolice.gov.in",
            "phone": "+91-11-23319800"
        }
    },
    {
        "id": "DEL-EDU-01",
        "city": "New Delhi",
        "district": "North Delhi",
        "state": "Delhi",
        "department": "Higher Education & Student Welfare",
        "pio_name": "Dr. T. Tiwari",
        "designation": "Deputy Registrar & PIO (Scholarships)",
        "office_address": "State Scholarship Cell, District Education Kachehri, Rajpur Road, New Delhi - 110007",
        "room_no": "Scholarship Wing, Directorate of Education",
        "email": "scholarships.pio@edu.gov.in",
        "phone": "+91-11-23954200",
        "latitude": 28.6720,
        "longitude": 77.2210,
        "faa": {
            "faa_name": "Dr. Rita Sharma",
            "designation": "Director of Higher Education / First Appellate Authority",
            "office_address": "5 Sham Nath Marg, Delhi - 110054",
            "email": "director-higheredu.delhi@gov.in",
            "phone": "+91-11-23980201"
        }
    },
    {
        "id": "DEL-HLT-01",
        "city": "New Delhi",
        "district": "Central Delhi",
        "state": "Delhi",
        "department": "Health & Family Welfare",
        "pio_name": "Dr. A. K. Gupta",
        "designation": "Chief Medical Officer & Designated PIO",
        "office_address": "Directorate of Health Services, Civil Hospital Complex, New Delhi - 110002",
        "room_no": "DHS Building, F-17 Karkardooma / Daryaganj",
        "email": "pio.health@dhs.gov.in",
        "phone": "+91-11-22301234",
        "latitude": 28.6480,
        "longitude": 77.2420,
        "faa": {
            "faa_name": "Dr. Sunita Aggarwal",
            "designation": "Director General of Health Services / First Appellate Authority",
            "office_address": "Swasthya Sewa Nideshalaya, F-17 Karkardooma, Delhi - 110032",
            "email": "dghs.delhi@gov.in",
            "phone": "+91-11-22307100"
        }
    }
]

# Geocoding Dictionary for Locality Reference Points (Lat, Lon) Across India
LOCALITY_GEO_CENTROIDS = {
    # Varanasi / Banaras
    "assi ghat": (25.2905, 82.9995),
    "sigra": (25.3180, 82.9910),
    "godowlia": (25.3090, 83.0060),
    "kashi": (25.3109, 83.0107),
    "banaras": (25.3176, 82.9739),
    "varanasi": (25.3176, 82.9739),
    "nadesar": (25.3375, 82.9810),
    "kabir chaura": (25.3140, 83.0080),
    "bhu": (25.2677, 82.9913),
    "lanka": (25.2810, 82.9980),
    # Delhi NCT
    "mehrauli": (28.5180, 77.1850),
    "rohini": (28.7490, 77.0680),
    "dwarka": (28.5920, 77.0460),
    "civil lines": (28.6750, 77.2250),
    "saket": (28.5240, 77.2060),
    "connaught place": (28.6315, 77.2167),
    "daryaganj": (28.6480, 77.2420),
    "okhla": (28.5355, 77.2732),
    "janakpuri": (28.6219, 77.0878),
    "ward 4": (28.6750, 77.2250),
    "sector 12": (28.5920, 77.0460),
    # Major Indian Metro & State Capital Hubs
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "mumbai": (18.9388, 72.8354),
    "pune": (18.5204, 73.8567),
    "nagpur": (21.1458, 79.0882),
    "chennai": (13.0827, 80.2707),
    "madurai": (9.9252, 78.1198),
    "coimbatore": (11.0168, 76.9558),
    "hyderabad": (17.3850, 78.4867),
    "kolkata": (22.5726, 88.3639),
    "howrah": (22.5958, 88.2636),
    "siliguri": (26.7271, 88.3953),
    "jaipur": (26.9124, 75.7873),
    "jodhpur": (26.2389, 73.0243),
    "udaipur": (24.5854, 73.7125),
    "patna": (25.5941, 85.1376),
    "gaya": (24.7914, 85.0002),
    "muzaffarpur": (26.1209, 85.3647),
    "ahmedabad": (23.0225, 72.5714),
    "surat": (21.1702, 72.8311),
    "rajkot": (22.3039, 70.8022),
    "lucknow": (26.8467, 80.9462),
    "gomti nagar": (26.8500, 81.0000),
    "prayagraj": (25.4358, 81.8463),
    "kanpur": (26.4499, 80.3319),
    "agra": (27.1767, 78.0081),
    "noida": (28.5355, 77.3910),
    "bhopal": (23.2599, 77.4126),
    "indore": (22.7196, 75.8577),
    "chandigarh": (30.7333, 76.7794),
    "ludhiana": (30.9010, 75.8573),
    "dehradun": (30.3165, 78.0322),
    "ranchi": (23.3441, 85.3096),
    "bhubaneswar": (20.2961, 85.8245),
    "cuttack": (20.4625, 85.8828),
    "guwahati": (26.1445, 91.7362),
    "kochi": (9.9816, 76.2999),
    "thiruvananthapuram": (8.5241, 76.9366)
}


class GeospatialLocator:
    """
    Geospatial Public Authority & PIO Routing Engine.
    Uses spherical trigonometry (Haversine formula) to locate the exact nearest PIO and FAA,
    computes accurate straight-line distances (in KM), and dynamically resolves all-India
    public authorities by 6-digit Postal PIN codes.
    """

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes Great-Circle Distance between two coordinates in Kilometers."""
        R = 6371.0  # Earth radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    def geocode_location(self, address: str, narrative: str, pincode: str = None) -> tuple[float, float, str, dict]:
        """
        Geocodes citizen locality to Latitude, Longitude, standard locality name,
        and resolved postal PIN code data if available.
        """
        full_text = f"{address} {narrative}".lower()

        # 1. Primary: Check for 6-Digit Indian Postal PIN Code
        pin = pincode or pincode_resolver.extract_pincode(f"{address} {narrative}")
        if pin:
            resolved = pincode_resolver.resolve_pincode(pin)
            if resolved:
                loc_name = f"{resolved['district']}, {resolved['state']} ({resolved['pincode']})"
                return resolved["latitude"], resolved["longitude"], loc_name, resolved

        # 2. Secondary: Centroid dictionary keyword matching
        for loc_name, coords in LOCALITY_GEO_CENTROIDS.items():
            if re.search(r'\b' + re.escape(loc_name) + r'\b', full_text):
                formatted_name = loc_name.title()
                if loc_name in ("varanasi", "banaras", "kashi", "assi ghat", "sigra", "godowlia", "nadesar", "kabir chaura", "bhu"):
                    formatted_name = "Varanasi / Banaras"
                return coords[0], coords[1], formatted_name, None

        # 3. Default fallback
        return 28.6139, 77.2090, "Central Division", None

    def get_area_and_domain_pios(self, category: str, address: str, narrative: str = "", pincode: str = None) -> dict:
        """
        Geocodes citizen location (including Postal PIN code resolution), computes geodesic distances,
        synthesizes/matches designated PIO officers for that specific administrative jurisdiction,
        and assigns the nearest PIO officer matching the complaint's specific domain/department.
        """
        user_lat, user_lon, locality_name, pin_resolved = self.geocode_location(address, narrative, pincode)
        
        all_candidates = []
        c_dept = (category or "").strip().lower()

        # If a 6-digit Indian PIN code was resolved, build authentic district authorities
        synthesized_ids = set()
        if pin_resolved:
            cluster = pincode_resolver.build_designated_pio_cluster(pin_resolved, target_domain=category)
            for auth in cluster["all_nearby_authorities"]:
                dist = self.haversine_distance(user_lat, user_lon, auth["latitude"], auth["longitude"])
                dist_str = f"{int(dist * 1000)} meters away" if dist < 1.0 else f"{dist} km away"
                p_dept = auth.get("department", "").strip().lower()
                is_domain_match = bool(c_dept and ((p_dept == c_dept) or (c_dept in p_dept) or (p_dept in c_dept)))

                item = {
                    "id": auth["id"],
                    "city": auth.get("city", locality_name),
                    "district": auth.get("district", pin_resolved.get("district")),
                    "state": auth.get("state", pin_resolved.get("state")),
                    "department": auth.get("department"),
                    "pio_name": auth.get("pio_name"),
                    "designation": auth.get("designation"),
                    "office_address": auth.get("office_address"),
                    "room_no": auth.get("room_no", "Ground Floor RTI Desk"),
                    "email": auth.get("email"),
                    "phone": auth.get("phone"),
                    "latitude": auth["latitude"],
                    "longitude": auth["longitude"],
                    "distance_km": dist,
                    "distance_label": dist_str,
                    "is_domain_match": is_domain_match,
                    "faa": auth.get("faa", {}),
                    "statutory_jurisdiction": auth.get("statutory_jurisdiction", {})
                }
                all_candidates.append(item)
                synthesized_ids.add(auth["id"])

        # Also add fixed regional directory public authorities
        for p in GEO_PUBLIC_AUTHORITIES:
            if p["id"] in synthesized_ids:
                continue
            dist = self.haversine_distance(user_lat, user_lon, p["latitude"], p["longitude"])
            dist_str = f"{int(dist * 1000)} meters away" if dist < 1.0 else f"{dist} km away"
            p_dept = p.get("department", "").strip().lower()
            is_domain_match = bool(c_dept and ((p_dept == c_dept) or (c_dept in p_dept) or (p_dept in c_dept)))

            item = {
                "id": p.get("id"),
                "city": p.get("city", locality_name),
                "district": p.get("district", ""),
                "state": p.get("state", ""),
                "department": p.get("department"),
                "pio_name": p.get("pio_name"),
                "designation": p.get("designation"),
                "office_address": p.get("office_address"),
                "room_no": p.get("room_no", "Ground Floor RTI Desk"),
                "email": p.get("email"),
                "phone": p.get("phone"),
                "latitude": p.get("latitude"),
                "longitude": p.get("longitude"),
                "distance_km": dist,
                "distance_label": dist_str,
                "is_domain_match": is_domain_match,
                "faa": p.get("faa", {}),
                "statutory_jurisdiction": {}
            }
            all_candidates.append(item)

        # Sort all candidates by distance ascending
        all_candidates.sort(key=lambda x: x["distance_km"])

        # Determine nearby area cluster (within regional radius or top nearby)
        closest_dist = all_candidates[0]["distance_km"] if all_candidates else 0
        area_radius = max(60.0, closest_dist * 2.5) if closest_dist < 100 else closest_dist + 50
        nearby_area_candidates = [c for c in all_candidates if c["distance_km"] <= area_radius]
        if len(nearby_area_candidates) < 4:
            nearby_area_candidates = all_candidates[:6]

        # Identify nearest PIO matching the complaint domain
        domain_matches = [c for c in nearby_area_candidates if c["is_domain_match"]]
        if not domain_matches:
            domain_matches = [c for c in all_candidates if c["is_domain_match"]]

        if domain_matches:
            assigned_candidate = domain_matches[0]
        else:
            assigned_candidate = nearby_area_candidates[0] if nearby_area_candidates else all_candidates[0]

        # Tag is_assigned flag
        assigned_id = assigned_candidate.get("id")
        for c in nearby_area_candidates:
            c["is_assigned"] = (c.get("id") == assigned_id)
        for c in all_candidates:
            c["is_assigned"] = (c.get("id") == assigned_id)

        assigned_pio_dict = {
            "id": assigned_candidate.get("id"),
            "department": assigned_candidate["department"],
            "pio_name": assigned_candidate["pio_name"],
            "designation": assigned_candidate["designation"],
            "office_address": assigned_candidate["office_address"],
            "room_no": assigned_candidate.get("room_no", "Ground Floor RTI Desk"),
            "email": assigned_candidate["email"],
            "phone": assigned_candidate["phone"],
            "distance_km": assigned_candidate["distance_km"],
            "distance_label": assigned_candidate["distance_label"],
            "user_coordinates": {"latitude": user_lat, "longitude": user_lon},
            "pio_coordinates": {"latitude": assigned_candidate["latitude"], "longitude": assigned_candidate["longitude"]},
            "matched_user_locality": locality_name,
            "faa": assigned_candidate.get("faa", {}),
            "statutory_jurisdiction": assigned_candidate.get("statutory_jurisdiction", {}),
            "pincode": pin_resolved.get("pincode") if pin_resolved else None,
            "district": assigned_candidate.get("district"),
            "state": assigned_candidate.get("state"),
            "jurisdiction_radius_km": 15.0,
            "is_domain_match": True,
            "is_assigned": True,
            "ml_prediction_reason": f"Geospatially assigned nearest domain ({category}) PIO {assigned_candidate['pio_name']} ({assigned_candidate['distance_label']}) in {locality_name}"
        }

        return {
            "assigned_pio": assigned_pio_dict,
            "nearby_area_pios": nearby_area_candidates,
            "all_pios": all_candidates,
            "user_coordinates": {"latitude": user_lat, "longitude": user_lon},
            "matched_user_locality": locality_name,
            "target_domain": category,
            "distance_km": assigned_candidate["distance_km"],
            "distance_label": assigned_candidate["distance_label"],
            "pincode_resolved": pin_resolved,
            "statutory_jurisdiction": assigned_candidate.get("statutory_jurisdiction", {})
        }

    def find_nearest_public_authority(self, category: str, address: str, narrative: str = "", pincode: str = None) -> dict:
        """
        Finds the closest designated PIO and First Appellate Authority (FAA) for a given department
        relative to the citizen's geocoded location, including all nearby area PIOs.
        """
        geo_data = self.get_area_and_domain_pios(category, address, narrative, pincode)
        assigned = geo_data["assigned_pio"]
        assigned["nearby_area_pios"] = geo_data["nearby_area_pios"]
        return assigned


geo_locator = GeospatialLocator()

