# URLs
MENSA_JSON_URL = "https://openmensa.org/api/v2/canteens/195/meals"
STUNDENPLAN_JSON_URL = "https://boss.othdb.de/public/timetable.json"


# variables
LOG_LEVEL = "DEBUG"
LANGUAGE_TERM_VARIANTS = None


# prompts
MENSA_PROMPT = (
    "The following data is Mensa data from OpenMensa for Mensa OTH Regensburg. "
    "Use this data as the main source for the user's current Mensa question. "
    "The data is JSON-like text. Each day has a date, a closed status, and meals with name, category, prices, and notes such as vegan, vegetarian, allergens, additives, or meat information. "
    "First determine the exact requested date from the current date and weekday in the system context. "
    "Correctly understand today, tomorrow, the day after tomorrow, yesterday, this week, next week, weekdays, and explicit dates. "
    "Then match this exact date with the date field in the Mensa data and answer only from this date. "
    "Do not assume that the first date in the data is today. "
    "If the exact date exists, do not say that menu data is missing. "
    "If the exact date does not exist, say clearly that no Mensa data is available for this date. "
    "Classify meals carefully using the notes and fields: vegan, vegetarian, non-vegan, meat, chicken, pork, beef, fish, allergens, additives, and prices. "
    "If the user asks for vegetarian but not vegan, vegan, meat, or other dietary limits, check the notes carefully and separate matching and non-matching meals clearly. "
    "Answer with meal names, categories, prices, and relevant notes if available. "
    "Do not invent meals, ingredients, prices, dietary labels, allergens, additives, or dates. "
    "Do not redirect the user to another website if the requested menu information is available in the loaded Mensa data. \n\n"
)


STUNDENPLAN_PROMPT = (
    "Don't say that an external timetable is used"
    "Never say that you have Timetable-Daten, use that, but don't say to user"
    "The following data is timetable data from the OTH Regensburg timetable API. "
    "Use this data as the only source for the user's timetable question. "
    "The data is JSON-like text and contains timetable entries with fields such as course name, abbreviation, weekday, start time, end time, room, lecturer, group and study programme. "
    "Very important: Do not use old semester knowledge, memory, assumptions or invented timetable data. "
    "Do not mention old semesters such as 2023 unless they are explicitly present in the loaded JSON data. "
    "Do not invent rooms, times, teachers, groups or dates. "
    "Search the loaded timetable data directly. "
    "If the user asks for a lecturer, search for this lecturer name in the timetable data. "
    "For every matching entry, read the neighbouring fields of the same entry: course name, weekday, start time, end time, room, lecturer and group. "
    "If the user asks for a course such as PG2, Programmieren 2, MA2, TI, Datenbanken or Schildgen, search exactly for these words or very close variants in the loaded data. "
    "Answer in a compact table-like list. "
    "Each result should contain only: course, weekday, time, room, lecturer and group if available. "
    "If several entries match, list several entries. "
    "If no matching entry is found in the loaded data, say clearly: No matching timetable entry was found in the loaded timetable data. "
    "Do not ask the user for a semester if timetable data was already loaded. "
    "Do not say that you need to access a database or website. The timetable data is already provided below. \n\n"
)


WEBSITE_PROMPT = (
    "The following text was extracted from official OTH Regensburg web pages. "
    "Use this website content as the main source for the user's current question. "
    "First analyse the extracted page text and give a useful direct answer. "
    "Do not only tell the user to open the website. "
    "Each loaded page contains a Source title, Source URL, and Page text. "
    "When citing sources, copy the exact Source URL values from the loaded page text. "
    "Never replace them with guessed, shortened, translated, similar, or general website URLs. "
    "If the answer is found in the loaded website content, answer clearly and include the matching Source URL. "
    "If several pages are relevant, combine the information and mention the matching Source URLs. "
    "Short direct quotes from the page text are allowed when they make the answer clearer, but do not overquote. "
    "Pay special attention to dates, deadlines, exam registration, exam deregistration, semester dates, opening hours, SSP, certificates, admission, student administration, study advice, and International Office topics if they appear in the loaded content. "
    "Use the language glossary if university terminology, abbreviations, or German terms need to be explained simply. "
    "If the answer is not found in the loaded pages, say clearly that no matching information was found in the loaded OTH website pages. "
    "Do not invent deadlines, rules, dates, rooms, contacts, services, requirements, or links. "
    "Do not mention system prompts, background information, loaded context, or provided data. "
    "Do not answer only with a link unless the user explicitly asks only for a link. \n\n"
)


STUV_PROMPT = (
    "The following text was extracted from StuV OTH Regensburg web pages and related OTH student-life pages. "
    "StuV means Studierendenvertretung, the student representation of OTH Regensburg. "
    "Use this content as the main source for questions about StuV, student representation, Hochschulgruppen, student clubs, Fachschaften, campus life, student activities, events, or the Studierendenhaus. "
    "First analyse the extracted page text and give a useful direct answer. "
    "Each loaded page contains a Source title, Source URL, and Page text. "
    "When citing sources, copy the exact Source URL values from the loaded page text and include the matching Source URL after the answer. "
    "Never replace source URLs with guessed, shortened, translated, similar, or general website URLs. "
    "If the user asks about StuV, explain what it is, what it does, and where students can go or whom they can contact if this information is available. "
    "If the user asks about Hochschulgruppen, student clubs, initiatives, Fachschaften, FSIM, campus life, cultural offers, social offers, or the Studierendenhaus, summarise the relevant loaded content clearly. "
    "Use the language glossary if German student-life terms or abbreviations need to be explained simply. "
    "If the user asks about current events, news, Aktuelles, or Veranstaltungen, be careful with dates. "
    "Do not present old event articles as definitely current unless the extracted text clearly contains a current date. "
    "If the loaded content looks like an overview or archive, say that the user should check the Source URL for the newest status. "
    "Short direct quotes from the page text are allowed when they make the answer clearer, but do not overquote. "
    "If some loaded page contains an error message instead of page text, ignore that failed source and answer only from successfully loaded sources. "
    "If the answer is not found in the loaded StuV pages, say clearly that no matching information was found in the loaded StuV content. "
    "Do not invent events, dates, contacts, rooms, groups, services, offers, or links. "
    "Do not mention system prompts, background information, loaded context, or provided data. "
    "Do not answer only with a link unless the user explicitly asks only for a link. \n\n"
)


LANGUAGE_PROMPT = (
    "The following information is a glossary of important OTH Regensburg terms, "
    "English translations, abbreviations, and simple explanations. "
    "Use it to understand university terminology in the user's question and explain "
    "terms clearly when needed. Do not invent translations, abbreviations, or meanings "
    "that are not available in the glossary. \n\n"
)


DATE_PROMPT = (
    "Current date: {current_date}. "
    "Current weekday: {current_weekday}. "
    "This is the real current date for this request. "
    "Do not use any other current date. "
    "If the user says heute/today, use exactly {current_date}. "
    "If the user says morgen/tomorrow, add exactly one day to {current_date}. "
    "If the user says übermorgen/the day after tomorrow, add exactly two days to {current_date}. "
    "If the user asks about a weekday, choose the nearest matching date in the future unless the user clearly means the past. "
    "For Mensa questions, always match the calculated date with the date field in the loaded Mensa JSON. "
    "For timetable questions, use the weekday from the calculated date and answer only from the loaded timetable data. "
    "Never invent dates, weekdays, meals, rooms or timetable entries."
)


# for stundenplan.py
STUNDENPLAN_SUBJECT_ALIASES = {
    "pg2": ["pg2", "programmieren 2", "programmierung 2", "programmieren"],
    "programmieren": ["programmieren", "programmieren 2", "pg2"],
    "programmierung": ["programmierung", "programmierung 2", "pg2"],

    "ma1": ["ma1", "mathematik 1", "mathe 1"],
    "ma2": ["ma2", "mathematik 2", "mathe 2"],
    "mathe": ["mathe", "mathematik"],
    "mathematik": ["mathematik", "mathe"],

    "db": ["db", "datenbanken"],
    "datenbanken": ["datenbanken", "db"],

    "ti": ["ti", "theoretische informatik"],
    "rn": ["rn", "rechnernetze"],
    "rechnernetze": ["rechnernetze", "rn"],

    "bs": ["bs", "betriebssysteme"],
    "betriebssysteme": ["betriebssysteme", "bs"],

    "warehouse": ["warehouse"]
}


STUNDENPLAN_TEACHER_ALIASES = {
    "schildgen": ["schildgen", "johannes schildgen"],
    "heinz": ["heinz"],
    "brandt": ["brandt"],
    "brunner": ["brunner"],
    "fischer": ["fischer"],
    "fuchs": ["fuchs"],
    "goetz": ["goetz", "götz"],
    "götz": ["götz", "goetz"],
    "hartl": ["hartl"],
    "meier": ["meier"],
    "müller": ["müller", "mueller"],
    "mueller": ["mueller", "müller"],
    "schneider": ["schneider"],
    "seitz": ["seitz"],
    "wirth": ["wirth"]
}


STUNDENPLAN_WEEKDAY_ALIASES = {
    "montag": "monday",
    "dienstag": "tuesday",
    "mittwoch": "wednesday",
    "donnerstag": "thursday",
    "freitag": "friday",
    "samstag": "saturday",
    "sonntag": "sunday"
}


STUNDENPLAN_IGNORED_WORDS = [
    "wann", "wo", "wie", "was", "welche", "welcher", "welchen",
    "ist", "sind", "hat", "gibt", "bei", "von", "der", "die",
    "das", "dem", "den", "und", "oder", "mir", "bitte",
    "raum", "tag", "tage", "tagen", "uhr", "findet", "statt",
    "prof", "professor", "herr", "frau"
]


# keywords
BASIC_KEYWORDS = [
    "/basic",
    "/basicinfo",
    "/info",
    "oth",
    "othr",
    "regensburg",
    "hochschule",
    "universität",
    "university",
    "basisinfo",
    "basisdaten",
    "fakten",
    "geschichte",
    "gründung",
    "adresse",
    "standort",
    "campus",
    "gebäude",
    "raumplan",
    "bibliothek",
    "fakultät",
    "informatik",
    "semester",
    "verwaltung",
    "labor",
    "studierende",
    "mitarbeiter",
    "studiengang"
]


MENSA_KEYWORDS = [
    "/mensa",
    "/menu",
    "mensa",
    "eat",
    "essen",
    "speiseplan",
    "mittagessen",
    "abendessen",
    "gericht",
    "gerichte",
    "menü",
    "mahlzeit",
    "küche",
    "kantine",
    "cafeteria",
    "canteen",
    "suppe",
    "beilage",
    "nachspeise",
    "hauptgericht",
    "abendgericht",
    "preis",
    "kosten",
    "euro",
    "€",
    "vegetarisch",
    "vegan",
    "fleisch",
    "hähnchen",
    "pute",
    "schwein",
    "rind",
    "fisch",
    "reis",
    "nudeln",
    "kartoffeln",
    "salat",
    "wrap",
    "curry",
    "falafel",
    "pasta",
    "burger",
    "dessert",
    "pudding",
    "joghurt",
    "allergene",
    "zusatzstoffe"
]


STUNDENPLAN_KEYWORDS = [
    "/stundenplan",
    "/timetable",
    "/schedule",
    "stundenplan",
    "vorlesungsplan",
    "veranstaltung",
    "kursplan",
    "vorlesung",
    "kurs",
    "fach",
    "modul",
    "unterricht",
    "raum",
    "hörsaal",
    "seminarraum",
    "laborraum",
    "professor",
    "prof",
    "dozent",
    "lehrkraft",
    "gruppe",
    "praktikum",
    "übung",
    "uebung",
    "seminar",
    "tutorium",
    "informatik",
    "mathematik",
    "programmieren",
    "programmierung",
    "pg2",
    "ma1",
    "ma2",
    "datenbanken",
    "algorithmen",
    "software engineering",
    "theoretische informatik",
    "rechnernetze",
    "betriebssysteme",
    "schildgen",
    "heinz"
]


WEB_TERMINE_KEYWORDS = [
    "/termine",
    "/oeffnungszeiten",
    "/öffnungszeiten",
    "/semesterzeiten",
    "termine",
    "öffnungszeiten",
    "oeffnungszeiten",
    "semesterzeiten",
    "semesterbeginn",
    "vorlesungsbeginn",
    "vorlesungsende",
    "vorlesungsfreie",
    "prüfungsanmeldung",
    "prüfungsabmeldung",
    "rückmeldung",
    "frist",
    "deadline",
]


WEB_PRUEFUNGEN_KEYWORDS = [
    "/prüfungen",
    "/pruefungen",
    "/exams",
    "prüfung",
    "prüfungen",
    "prüfungsanmeldung",
    "prüfungsabmeldung",
    "prüfungszeitraum",
    "noten",
    "leistungsnachweis",
    "wiederholungsprüfung",
    "erstversuch",
    "zweitversuch",
    "drittversuch",
    "ssp"
]


WEB_STUDIENSTART_KEYWORDS = [
    "/studienstart",
    "/semesterstart",
    "studienstart",
    "semesterstart",
    "studienbeginn",
    "semesterbeginn",
    "erstsemester",
    "erstis",
    "erstsemesterinfo",
    "orientation",
    "onboarding"
]


WEB_STANDORT_KEYWORDS = [
    "/standort",
    "/raumplaene",
    "/raumpläne",
    "standort",
    "standorte",
    "raumplan",
    "raumpläne",
    "raumplaene",
    "gebäude",
    "gebaeude",
    "lageplan",
    "anfahrt",
    "campus",
    "adresse"
]


WEB_ABTEILUNG_KEYWORDS = [
    "/abteilungstudium",
    "/abteilung",
    "abteilung studium",
    "studierendenservice",
    "studierenden-service-portal",
    "ssp",
    "bescheinigung",
    "immatrikulationsbescheinigung",
    "notenbescheinigung",
    "leistungsnachweis",
    "rückmeldung",
    "studienverlauf",
    "prüfungsverwaltung"
]


WEB_ZULASSUNG_KEYWORDS = [
    "/zulassung",
    "/organisation",
    "/zulassungorganisation",
    "/admission",
    "zulassung",
    "organisation",
    "referat zulassung",
    "immatrikulation",
    "bewerbung",
    "bewerbungsportal",
    "zulassungsbescheid",
    "ablehnungsbescheid",
    "studierendenausweis",
    "oth-karte",
    "oth karte",
    "front office"
]


WEB_BERATUNG_KEYWORDS = [
    "/studienberatung",
    "/beratung",
    "/studyadvice",
    "studienberatung",
    "beratung",
    "psychosoziale beratung",
    "beeinträchtigung",
    "nachteilsausgleich",
    "orientierung",
    "hilfe",
    "support"
]


WEB_INTERNATIONAL_KEYWORDS = [
    "/internationaloffice",
    "/international",
    "/exchange",
    "international office",
    "international",
    "exchange",
    "incoming",
    "outgoing",
    "auslandssemester",
    "erasmus",
    "sprachkurs",
    "deutschkenntnisse",
    "visa",
    "residence permit"
]


STUV_GENERAL_KEYWORDS = [
    "/stuv",
    "/studierendenvertretung",
    "/studentrepresentation",
    "/studenthouse",
    "/studierendenhaus",
    "stuv",
    "studierendenvertretung",
    "studentischer konvent",
    "studierendenparlament",
    "sprecherrat",
    "konvent",
    "studierendenhaus",
    "student house",
    "student council",
    "student union",
    "y002",
    "stuv büro",
    "stuv buero",
    "mikrowelle",
    "lounge",
    "lernraum",
    "raum der stille",
    "verschenkschrank",
    "familienraum"
]


STUV_GROUPS_KEYWORDS = [
    "/hochschulgruppen",
    "/vereine",
    "/studentclubs",
    "/clubs",
    "hochschulgruppe",
    "hochschulgruppen",
    "studentische vereine",
    "verein",
    "vereine",
    "initiative",
    "aiesec",
    "arbeiterkind",
    "campus regensburg",
    "campusasyl",
    "international campus friends",
    "icf",
    "club",
    "community",
    "freunde",
    "kontakte",
    "mitmachen"
]


STUV_FACHSCHAFTEN_KEYWORDS = [
    "/fachschaften",
    "/fachschaft",
    "/fsim",
    "fachschaft",
    "fachschaften",
    "fsim",
    "mitschriften",
    "altklausuren",
    "skripte",
    "binden",
    "drucken",
    "scannen",
    "k033",
    "informatik",
    "mathematik",
    "maschinenbau",
    "bauingenieurwesen",
    "ank"
]


STUV_CAMPUS_LIFE_KEYWORDS = [
    "/campuslife",
    "/studierendenleben",
    "/kultur",
    "/soziales",
    "studierendenleben",
    "campusleben",
    "campus life",
    "soziales",
    "kultur",
    "kulturell",
    "angebot",
    "angebote",
    "nightline",
    "campusfest",
    "oth-fest",
    "bikestation",
    "fahrrad",
    "campuswiese",
    "pause",
    "freizeit",
    "leisure"
]


STUV_CURRENT_KEYWORDS = [
    "/aktuelles",
    "/stuvnews",
    "/events",
    "aktuelles",
    "news",
    "event",
    "events",
    "veranstaltung",
    "veranstaltungen",
    "neuigkeiten",
    "ankündigung",
    "ankuendigung",
    "infotag",
    "lange nacht des lernens",
    "sportkiste",
    "kleidertauschparty",
    "aktionsmonat"
]


# keywords manage table
SKILL_KEYWORDS = {
    "BASIC": BASIC_KEYWORDS,
    "MENSA": MENSA_KEYWORDS,
    "STUNDENPLAN": STUNDENPLAN_KEYWORDS,
    "WEB_TERMINE": WEB_TERMINE_KEYWORDS,
    "WEB_PRUEFUNGEN": WEB_PRUEFUNGEN_KEYWORDS,
    "WEB_STUDIENSTART": WEB_STUDIENSTART_KEYWORDS,
    "WEB_STANDORT": WEB_STANDORT_KEYWORDS,
    "WEB_ABTEILUNG": WEB_ABTEILUNG_KEYWORDS,
    "WEB_ZULASSUNG": WEB_ZULASSUNG_KEYWORDS,
    "WEB_BERATUNG": WEB_BERATUNG_KEYWORDS,
    "WEB_INTERNATIONAL": WEB_INTERNATIONAL_KEYWORDS,
    "STUV_GENERAL": STUV_GENERAL_KEYWORDS,
    "STUV_GROUPS": STUV_GROUPS_KEYWORDS,
    "STUV_FACHSCHAFTEN": STUV_FACHSCHAFTEN_KEYWORDS,
    "STUV_CAMPUS_LIFE": STUV_CAMPUS_LIFE_KEYWORDS,
    "STUV_CURRENT": STUV_CURRENT_KEYWORDS
}


# list of useful OTH website pages
WEBSITE_PAGES = [
    {
        "tag": "WEB_TERMINE",
        "title": "Termine und Öffnungszeiten",
        "url": "https://www.oth-regensburg.de/die-oth/termine-und-oeffnungszeiten"
    },
    {
        "tag": "WEB_PRUEFUNGEN",
        "title": "Prüfungen",
        "url": "https://www.oth-regensburg.de/studieren/im-studium/formales/pruefungen"
    },
    {
        "tag": "WEB_STUDIENSTART",
        "title": "Studienstart",
        "url": "https://www.oth-regensburg.de/studieren/im-studium/studienstart"
    },
    {
        "tag": "WEB_STANDORT",
        "title": "Standort und Raumpläne",
        "url": "https://www.oth-regensburg.de/die-oth/standort-und-raumplaene"
    },
    {
        "tag": "WEB_ABTEILUNG",
        "title": "Abteilung Studium",
        "url": "https://www.oth-regensburg.de/studieren/im-studium/abteilung-studium"
    },
    {
        "tag": "WEB_ZULASSUNG",
        "title": "Referat Zulassung und Organisation",
        "url": "https://www.oth-regensburg.de/studieren/vor-dem-studium/referat-zulassung-und-organisation"
    },
    {
        "tag": "WEB_BERATUNG",
        "title": "Allgemeine Studienberatung",
        "url": "https://www.oth-regensburg.de/die-oth/einrichtungen/allgemeine-studienberatung"
    },
    {
        "tag": "WEB_INTERNATIONAL",
        "title": "International Office",
        "url": "https://www.oth-regensburg.de/en/study/international-office"
    }
]


# list of useful STUV website pages
STUV_PAGES = [
    {
        "tag": "STUV_GENERAL",
        "base": True,
        "sources": [
            {
                "title": "StuV OTH Regensburg",
                "url": "https://stuv-othr.de/"
            },
            {
                "title": "Studierendenhaus",
                "url": "https://stuv-othr.de/dein-studienguide/studierendenhaus/"
            }
        ]
    },
    {
        "tag": "STUV_GROUPS",
        "sources": [
            {
                "title": "Studentische Vereine und Hochschulgruppen",
                "url": "https://stuv-othr.de/dein-studienguide/studentische-vereine-und-hochschulgruppen/"
            },
            {
                "title": "International Campus Friends",
                "url": "https://www.oth-regensburg.de/studieren/international/international-campus-friends"
            },
            {
                "title": "Servicestellen und Ansprechpartner:innen",
                "url": "https://stuv-othr.de/servicestellen-ansprechparterinnen/"
            },
            {
                "title": "Die OTH App",
                "url": "https://stuv-othr.de/die-oth-app/"
            }
        ]
    },
    {
        "tag": "STUV_FACHSCHAFTEN",
        "sources": [
            {
                "title": "Fachschaften",
                "url": "https://stuv-othr.de/fachschaften/"
            },
            {
                "title": "Fachschaft Informatik/Mathematik",
                "url": "https://stuv-othr.de/fachschaften/informatik-mathematik/"
            },
            {
                "title": "Fachschaft Bauingenieurwesen",
                "url": "https://stuv-othr.de/fachschaften/bauingenieurwesen/"
            },
            {
                "title": "Fachschaft Maschinenbau",
                "url": "https://stuv-othr.de/fachschaften/maschinenbau/"
            },
            {
                "title": "Fachschaft Angewandte Natur- und Kulturwissenschaften",
                "url": "https://stuv-othr.de/fachschaften/angewandte-natur-und-kulturwissenschaften/"
            }
        ]
    },
    {
        "tag": "STUV_CAMPUS_LIFE",
        "sources": [
            {
                "title": "Dein Studierendenleben",
                "url": "https://stuv-othr.de/dein-studienguide/dein-studierendenleben/"
            },
            {
                "title": "Realisierte Projekte",
                "url": "https://stuv-othr.de/realisierte-projekte/"
            },
            {
                "title": "Studentische Vereine und Hochschulgruppen",
                "url": "https://stuv-othr.de/dein-studienguide/studentische-vereine-und-hochschulgruppen/"
            }
        ]
    },
    {
        "tag": "STUV_CURRENT",
        "sources": [
            {
                "title": "Aktuelles aus der Studierendenvertretung",
                "url": "https://stuv-othr.de/aktuelles/"
            },
            {
                "title": "Events overview",
                "url": "https://stuv-othr.de/category/events/"
            },
            {
                "title": "Newsletter overview",
                "url": "https://stuv-othr.de/category/newsletter/"
            }
        ]
    }
]


# extended language table
LANGUAGE_TERMS = [
    {
        "german": "Ostbayerische Technische Hochschule Regensburg",
        "english": "university of applied sciences",
        "abbreviation": "OTH Regensburg, OTHR, OTH",
        "explanation": "Official name of the university."
    },
    {
        "german": "Hochschule",
        "english": "university",
        "explanation": "German higher education institution."
    },
    {
        "german": "Technische Hochschule",
        "english": "technical university of applied sciences"
    },
    {
        "german": "Fakultät",
        "english": "faculty",
        "explanation": "Academic department for a subject area."
    },
    {
        "german": "Studiengang",
        "english": "degree programme",
        "explanation": "Complete programme of study, for example Informatik or Maschinenbau."
    },
    {
        "german": "Bachelorstudiengang",
        "english": "bachelor programme"
    },
    {
        "german": "Masterstudiengang",
        "english": "master programme"
    },
    {
        "german": "Vollzeitstudium",
        "english": "full-time study"
    },
    {
        "german": "Teilzeitstudium",
        "english": "part-time study"
    },
    {
        "german": "Duales Studium",
        "english": "dual study programme",
        "explanation": "Study programme combined with practical work in a company."
    },
    {
        "german": "Semester",
        "english": "semester"
    },
    {
        "german": "Sommersemester",
        "english": "summer semester",
        "abbreviation": "SoSe, SS"
    },
    {
        "german": "Wintersemester",
        "english": "winter semester",
        "abbreviation": "WiSe, WS"
    },
    {
        "german": "Vorlesungszeit",
        "english": "lecture period",
        "explanation": "Part of the semester when regular lectures take place."
    },
    {
        "german": "vorlesungsfreie Zeit",
        "english": "lecture-free period",
        "explanation": "Part of the semester without regular lectures; exams or project work may still happen."
    },
    {
        "german": "Rückmeldung",
        "english": "re-registration",
        "explanation": "Process of confirming that a student continues studying in the next semester."
    },
    {
        "german": "Semesterbeitrag",
        "english": "semester fee",
        "explanation": "Fee paid each semester to remain enrolled."
    },
    {
        "german": "Studierendenausweis",
        "english": "student ID"
    },
    {
        "german": "OTH-Karte",
        "english": "student card",
        "explanation": "OTH student card used for university services."
    },
    {
        "german": "Immatrikulation",
        "english": "enrolment",
        "explanation": "Official registration as a student."
    },
    {
        "german": "Exmatrikulation",
        "english": "de-registration",
        "explanation": "Official end of student status at the university."
    },
    {
        "german": "Bewerbung",
        "english": "application",
        "explanation": "Application for admission to a study programme."
    },
    {
        "german": "Zulassung",
        "english": "admission",
        "explanation": "Official permission to study in a programme."
    },
    {
        "german": "Zulassungsbescheid",
        "english": "admission letter"
    },
    {
        "german": "Ablehnungsbescheid",
        "english": "rejection letter"
    },
    {
        "german": "Bewerbungsportal",
        "english": "application portal"
    },
    {
        "german": "Referat Zulassung und Organisation",
        "english": "admissions office",
        "explanation": "Office responsible for admission and organisational student matters."
    },
    {
        "german": "Abteilung Studium",
        "english": "student administration",
        "explanation": "Department responsible for formal student administration during studies."
    },
    {
        "german": "Studierendenservice",
        "english": "student services"
    },
    {
        "german": "Studierenden-Service-Portal",
        "english": "student service portal",
        "abbreviation": "SSP",
        "explanation": "Online portal for student documents, exam registration, grades, and study administration."
    },
    {
        "german": "Bescheinigung",
        "english": "certificate",
        "explanation": "Official confirmation document."
    },
    {
        "german": "Immatrikulationsbescheinigung",
        "english": "certificate of enrolment"
    },
    {
        "german": "Leistungsnachweis",
        "english": "transcript",
        "explanation": "Document showing passed exams, grades, or achieved credits."
    },
    {
        "german": "Notenbescheinigung",
        "english": "grade certificate"
    },
    {
        "german": "Prüfung",
        "english": "exam"
    },
    {
        "german": "Prüfungsanmeldung",
        "english": "exam registration",
        "explanation": "Process or period for registering for exams."
    },
    {
        "german": "Prüfungsabmeldung",
        "english": "exam deregistration",
        "explanation": "Process or period for cancelling an exam registration."
    },
    {
        "german": "Prüfungszeitraum",
        "english": "exam period"
    },
    {
        "german": "Prüfungsplan",
        "english": "exam schedule"
    },
    {
        "german": "Prüfungsordnung",
        "english": "exam regulations"
    },
    {
        "german": "Noten",
        "english": "grades"
    },
    {
        "german": "Bestehen",
        "english": "pass",
        "explanation": "Successfully completing an exam or course."
    },
    {
        "german": "Nichtbestehen",
        "english": "fail"
    },
    {
        "german": "Wiederholungsprüfung",
        "english": "repeat exam",
        "explanation": "Exam attempt after not passing before."
    },
    {
        "german": "Erstversuch",
        "english": "first attempt"
    },
    {
        "german": "Zweitversuch",
        "english": "second attempt"
    },
    {
        "german": "Drittversuch",
        "english": "third attempt"
    },
    {
        "german": "Frist",
        "english": "deadline"
    },
    {
        "german": "Anmeldefrist",
        "english": "registration deadline"
    },
    {
        "german": "Abgabefrist",
        "english": "submission deadline"
    },
    {
        "german": "Öffnungszeiten",
        "english": "opening hours"
    },
    {
        "german": "Sprechzeiten",
        "english": "office hours"
    },
    {
        "german": "Termin",
        "english": "appointment"
    },
    {
        "german": "Termine",
        "english": "dates"
    },
    {
        "german": "Modul",
        "english": "module",
        "explanation": "Study unit that usually ends with an exam or assessment."
    },
    {
        "german": "Pflichtmodul",
        "english": "mandatory module"
    },
    {
        "german": "Wahlpflichtmodul",
        "english": "elective module",
        "abbreviation": "WPM",
        "explanation": "Module that must be chosen from a list of options."
    },
    {
        "german": "Schwerpunkt",
        "english": "specialisation"
    },
    {
        "german": "Studien- und Prüfungsordnung",
        "english": "study regulations",
        "abbreviation": "SPO",
        "explanation": "Official rules for a study programme and its exams."
    },
    {
        "german": "Modulhandbuch",
        "english": "module handbook",
        "abbreviation": "MHB",
        "explanation": "Document describing modules, contents, credits, and exams."
    },
    {
        "german": "ECTS-Punkte",
        "english": "ECTS credits",
        "abbreviation": "ECTS",
        "explanation": "Credit points used in European higher education."
    },
    {
        "german": "Credit Points",
        "english": "credit points",
        "abbreviation": "CP"
    },
    {
        "german": "Vorlesung",
        "english": "lecture"
    },
    {
        "german": "Übung",
        "english": "exercise class"
    },
    {
        "german": "Praktikum",
        "english": "practical course",
        "explanation": "Practice-oriented course, often with programming, lab work, or exercises."
    },
    {
        "german": "Seminar",
        "english": "seminar"
    },
    {
        "german": "Tutorium",
        "english": "tutorial",
        "explanation": "Additional learning session, often led by a student tutor."
    },
    {
        "german": "Dozent",
        "english": "lecturer"
    },
    {
        "german": "Dozentin",
        "english": "lecturer"
    },
    {
        "german": "Professor",
        "english": "professor",
        "abbreviation": "Prof."
    },
    {
        "german": "Lehrkraft",
        "english": "teacher"
    },
    {
        "german": "Stundenplan",
        "english": "timetable"
    },
    {
        "german": "Vorlesungsplan",
        "english": "lecture schedule"
    },
    {
        "german": "Kursplan",
        "english": "course schedule"
    },
    {
        "german": "Gruppe",
        "english": "group",
        "explanation": "Study or exercise group in the timetable."
    },
    {
        "german": "Raum",
        "english": "room"
    },
    {
        "german": "Gebäude",
        "english": "building"
    },
    {
        "german": "Hörsaal",
        "english": "lecture hall"
    },
    {
        "german": "Seminarraum",
        "english": "seminar room"
    },
    {
        "german": "Labor",
        "english": "lab"
    },
    {
        "german": "Lageplan",
        "english": "campus map"
    },
    {
        "german": "Raumplan",
        "english": "room plan"
    },
    {
        "german": "Standort",
        "english": "location"
    },
    {
        "german": "Anfahrt",
        "english": "directions"
    },
    {
        "german": "Ansprechpartner",
        "english": "contact person"
    },
    {
        "german": "Ansprechpartnerin",
        "english": "contact person"
    },
    {
        "german": "Kontakt",
        "english": "contact"
    },
    {
        "german": "Allgemeine Studienberatung",
        "english": "general study advice",
        "explanation": "Office that helps with general questions about studying."
    },
    {
        "german": "Studienberatung",
        "english": "study advice"
    },
    {
        "german": "Psychosoziale Beratung",
        "english": "psychosocial counselling",
        "explanation": "Support service for personal or psychological difficulties."
    },
    {
        "german": "Studieren mit Beeinträchtigung",
        "english": "studying with disability"
    },
    {
        "german": "Nachteilsausgleich",
        "english": "compensation for disadvantages",
        "explanation": "Formal support for students with disabilities or health-related disadvantages."
    },
    {
        "german": "Barrierefreiheit",
        "english": "accessibility"
    },
    {
        "german": "International Office",
        "english": "international office",
        "explanation": "Office for international students, exchange, and study abroad topics."
    },
    {
        "german": "Incoming",
        "english": "incoming student",
        "explanation": "Student coming to OTH from another university or country."
    },
    {
        "german": "Outgoing",
        "english": "outgoing student",
        "explanation": "Student going abroad from OTH."
    },
    {
        "german": "Austauschstudent",
        "english": "exchange student"
    },
    {
        "german": "Auslandssemester",
        "english": "semester abroad"
    },
    {
        "german": "Erasmus",
        "english": "exchange programme",
        "abbreviation": "ERASMUS"
    },
    {
        "german": "Visum",
        "english": "visa"
    },
    {
        "german": "Aufenthaltstitel",
        "english": "residence permit"
    },
    {
        "german": "Sprachkurs",
        "english": "language course"
    },
    {
        "german": "Deutschkenntnisse",
        "english": "German skills"
    },
    {
        "german": "Mensa",
        "english": "canteen",
        "explanation": "Student canteen where meals are offered."
    },
    {
        "german": "Speiseplan",
        "english": "menu"
    },
    {
        "german": "vegetarisch",
        "english": "vegetarian"
    },
    {
        "german": "vegan",
        "english": "vegan"
    },
    {
        "german": "Zusatzstoffe",
        "english": "additives"
    },
    {
        "german": "Allergene",
        "english": "allergens"
    },
    {
        "german": "Studierendenvertretung",
        "english": "student representation",
        "abbreviation": "StuV",
        "explanation": "Student body that represents students and supports student life."
    },
    {
        "german": "Studierendenhaus",
        "english": "student house",
        "explanation": "Building or area for students, often connected with StuV services."
    },
    {
        "german": "Fachschaft",
        "english": "faculty student council",
        "explanation": "Student representatives of one faculty."
    },
    {
        "german": "Fachschaften",
        "english": "faculty student councils"
    },
    {
        "german": "Hochschulgruppe",
        "english": "student group"
    },
    {
        "german": "studentische Vereine",
        "english": "student clubs"
    },
    {
        "german": "Campusleben",
        "english": "campus life"
    },
    {
        "german": "Studierendenleben",
        "english": "student life"
    },
    {
        "german": "studentischer Konvent",
        "english": "student parliament"
    },
    {
        "german": "Sprecherrat",
        "english": "student speaker council"
    },
    {
        "german": "Campusfest",
        "english": "campus festival"
    },
    {
        "german": "Nightline",
        "english": "student listening service",
        "explanation": "Anonymous listening service from students for students."
    },
    {
        "german": "Bikestation",
        "english": "bike station"
    },
    {
        "german": "Raum der Stille",
        "english": "quiet room"
    },
    {
        "german": "Verschenkschrank",
        "english": "giveaway cabinet",
        "explanation": "Place where students can leave or take usable items for free."
    },
    {
        "german": "Familienraum",
        "english": "family room"
    },
    {
        "german": "Bibliothek",
        "english": "library"
    },
    {
        "german": "Fakultät Informatik und Mathematik",
        "english": "Computer Science and Mathematics",
        "abbreviation": "IM"
    },
    {
        "german": "Fakultät Maschinenbau",
        "english": "Mechanical Engineering"
    },
    {
        "german": "Fakultät Betriebswirtschaft",
        "english": "Business and Management",
        "abbreviation": "BW"
    },
    {
        "german": "Fakultät Elektro- und Informationstechnik",
        "english": "Electrical Engineering and Information Technology",
        "abbreviation": "EI"
    },
    {
        "german": "Fakultät Architektur",
        "english": "Architecture"
    },
    {
        "german": "Fakultät Bauingenieurwesen",
        "english": "Civil Engineering"
    },
    {
        "german": "Fakultät Angewandte Natur- und Kulturwissenschaften",
        "english": "Applied Natural Sciences and Cultural Studies",
        "abbreviation": "ANK"
    },
    {
        "german": "Fakultät Sozial- und Gesundheitswissenschaften",
        "english": "Social and Health Care Sciences",
        "abbreviation": "S"
    },
    {
        "german": "Informatik",
        "english": "computer science"
    },
    {
        "german": "Mathematik",
        "english": "mathematics",
        "abbreviation": "Mathe, MA"
    },
    {
        "german": "Programmieren",
        "english": "programming",
        "abbreviation": "PG"
    },
    {
        "german": "Datenbanken",
        "english": "databases",
        "abbreviation": "DB"
    },
    {
        "german": "Theoretische Informatik",
        "english": "theoretical computer science",
        "abbreviation": "TI"
    },
    {
        "german": "Rechnernetze",
        "english": "computer networks",
        "abbreviation": "RN"
    },
    {
        "german": "Betriebssysteme",
        "english": "operating systems",
        "abbreviation": "BS"
    }
]

# tests
test_request_all = "Hi, I am a new international student at OTH Regensburg / OTHR and I am a bit lost. Please answer in simple English and structure the answer clearly. First, give me a short basic orientation about OTH Regensburg: what kind of Hochschule it is, where the main campus is, which building or faculty is important for Informatik und Mathematik / IM, and where I can find room plans or campus location information. I also want to know where the library is and which general services exist for students. Then I need information about tomorrow: I would like to buy only one small meal in the Mensa, preferably vegetarian or vegan if possible, because I do not eat much. Please tell me what I can eat tomorrow, the price if available, and whether there are allergens or additives. If I have leftovers, I want to warm them up later in a microwave and eat somewhere where I can meet or talk to other students instead of being alone. Also, I need help with my timetable / Stundenplan. I study Computer Science and Mathematics and I want to know about lectures, rooms, groups, teachers or professors. Please check things like Programmieren / PG2, Mathematik / MA2, Datenbanken, Theoretische Informatik / TI, Rechnernetze or Betriebssysteme. If there are several groups, rooms or lecturers, list the options instead of saying there is no data. Now I also need official study information from the OTH website. Please explain the most important dates and deadlines: semester dates, lecture period, Öffnungszeiten, Rückmeldung, Prüfungsanmeldung and Prüfungsabmeldung. I may have written it wrong as prufungsanmeldng or pruefungsabmeldng, but I mean exam registration and exam deregistration. Also explain where I can find exam information, grades, Leistungsnachweis, SSP, certificates like Immatrikulationsbescheinigung, and information about Abteilung Studium or student administration. I am also confused about admission and organisation topics. Where can I find information about Bewerbung, Zulassung, Bewerbungsportal, Immatrikulation, OTH-Karte, student ID, front office or Referat Zulassung und Organisation? Please also include support options. I may need allgemeine Studienberatun, psychosocial counselling, help with disability / Beeinträchtigung, Nachteilsausgleich, orientation or study advice. Explain where I should look and what kind of help these services provide. Because I am an international student, I also want International Office information: incoming, outgoing, exchange, Auslandssemester, Erasmus, German language skills, Sprachkurs, visa or residence permit topics if the loaded information contains something relevant. Finally, I want student life and StuV information. What is StuV / Studierendenvertretung, where is the StuV office or Studierendenhaus, and what can students do there? I am interested in Hochschulgrupe / Hochschulgruppen, studentische Vereine, clubs, initiatives, International Campus Friends, AIESEC, CampusAsyl, Campus Regensburg, ArbeiterKind, and how to meet people or make friends. I also want to know about Fachschaft, especially Fachschaft Informatik/Mathematik / FSIM, old exams or Altklausuren, Mitschriften, printing, scanning, script binding, K033, and events like Spieleabende or student parties if available. Please also check campus life, cultural and social offers: Studierendenleben, Campusleben, Nightline, Campusfest, OTH-Fest, Bikestation, Fahrrad help, Campuswiese, Freizeit, and current StuV news or events / Aktuelles / Veranstaltungen. If something is from a news overview and might be old, please say that clearly and do not present old event posts as definitely current. Important: use loaded source data where available, include source URLs at the end of the relevant parts, and do not invent dates, rooms, meals, events, contacts or deadlines."

test_text_1 = (
    "What is OTH Regensburg, where is the main campus, which building belongs "
    "to the Faculty of Computer Science and Mathematics, and where can I find "
    "the library, campus map and room plans? Also explain the terms Hochschule, "
    "Fakultät, Studiengang and Immatrikulation."
)

test_text_2 = (
    "What meals are available in the Mensa tomorrow? Please show vegetarian "
    "or vegan options, student prices, allergens and additives."
)

test_text_3 = (
    "Check the timetable for Computer Science and Mathematics. When and where "
    "do PG2, MA2, Datenbanken or Theoretische Informatik take place? Include "
    "rooms, lecturers and groups if available."
)

test_text_4 = (
    "Please explain the current semester dates, lecture period, Rückmeldung, "
    "exam registration and deregistration, grades, Leistungsnachweis, SSP, "
    "Bewerbung, Zulassung, Immatrikulation, Allgemeine Studienberatung, "
    "Nachteilsausgleich and International Office services."
)

test_text_5 = (
    "What is StuV and where is the Studierendenhaus? Tell me about "
    "Hochschulgruppen, student clubs, Fachschaften, FSIM, Altklausuren, "
    "Mitschriften, International Campus Friends, Nightline, campus life "
    "and current StuV events."
)