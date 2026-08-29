import math
import re

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

# Geocoding Dictionary for Locality Reference Points (Lat, Lon)
LOCALITY_GEO_CENTROIDS = {
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
    "lucknow": (26.8467, 80.9462),
    "gomti nagar": (26.8500, 81.0000),
    "prayagraj": (25.4358, 81.8463),
    "kanpur": (26.4499, 80.3319),
    "mumbai": (19.0760, 72.8777),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "jaipur": (26.9124, 75.7873),
    "patna": (25.5941, 85.1376)
}


class GeospatialLocator:
    """
    Geospatial Public Authority & PIO Routing Engine.
    Uses spherical trigonometry (Haversine formula) to locate the exact nearest PIO and FAA,
    computes accurate straight-line distances (in KM), and assigns administrative nodal details.
    """

    def haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Computes Great-Circle Distance between two coordinates in Kilometers."""
        R = 6371.0  # Earth radius in kilometers
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    def geocode_location(self, address: str, narrative: str) -> tuple[float, float, str]:
        """Geocodes citizen locality to Latitude, Longitude, and standard locality name."""
        full_text = f"{address} {narrative}".lower()

        for loc_name, coords in LOCALITY_GEO_CENTROIDS.items():
            if re.search(r'\b' + re.escape(loc_name) + r'\b', full_text):
                formatted_name = loc_name.title()
                if loc_name in ("varanasi", "banaras", "kashi", "assi ghat", "sigra", "godowlia", "nadesar", "kabir chaura", "bhu"):
                    formatted_name = "Varanasi / Banaras"
                return coords[0], coords[1], formatted_name

        # Default to Delhi Center
        return 28.6139, 77.2090, "Central Division"

    def find_nearest_public_authority(self, category: str, address: str, narrative: str = "") -> dict:
        """
        Finds the closest designated PIO and First Appellate Authority (FAA) for a given department
        relative to the citizen's geocoded location.
        """
        user_lat, user_lon, locality_name = self.geocode_location(address, narrative)
        
        # Filter candidates matching the target department
        dept_candidates = [
            p for p in GEO_PUBLIC_AUTHORITIES 
            if p["department"].lower() == category.lower()
        ]

        if not dept_candidates:
            # Fallback to any in the city or first available
            dept_candidates = [p for p in GEO_PUBLIC_AUTHORITIES if category.lower() in p["department"].lower()]
            if not dept_candidates:
                dept_candidates = [GEO_PUBLIC_AUTHORITIES[0]]

        # Find closest candidate using Haversine
        best_candidate = None
        min_distance = float('inf')

        for candidate in dept_candidates:
            dist = self.haversine_distance(user_lat, user_lon, candidate["latitude"], candidate["longitude"])
            if dist < min_distance:
                min_distance = dist
                best_candidate = candidate

        # Format distance string
        if min_distance < 1.0:
            dist_str = f"{int(min_distance * 1000)} meters away"
        else:
            dist_str = f"{min_distance} km away"

        return {
            "department": best_candidate["department"],
            "pio_name": best_candidate["pio_name"],
            "designation": best_candidate["designation"],
            "office_address": best_candidate["office_address"],
            "room_no": best_candidate.get("room_no", "Ground Floor RTI Desk"),
            "email": best_candidate["email"],
            "phone": best_candidate["phone"],
            "distance_km": min_distance,
            "distance_label": dist_str,
            "user_coordinates": {"latitude": user_lat, "longitude": user_lon},
            "pio_coordinates": {"latitude": best_candidate["latitude"], "longitude": best_candidate["longitude"]},
            "matched_user_locality": locality_name,
            "faa": best_candidate.get("faa", {}),
            "jurisdiction_radius_km": 15.0,
            "ml_prediction_reason": f"Geospatially matched nearest {category} Public Authority ({dist_str}) in {locality_name}"
        }


geo_locator = GeospatialLocator()
