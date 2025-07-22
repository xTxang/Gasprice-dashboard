# Dictionary mapping of categories:
POINT_CATEGORY_MAP = {
    # Format: (pointLabel, direction) : Category



    # --------------------------------NWELNG-----------------------------
    # NWELNG Send-Outs (entry only)
    # France
    ("Dunkerque", "entry"): "NWELNG Send-Outs",
    ("Montoir-de-Bretagne", "entry"): "NWELNG Send-Outs",
    ("Le Havre", "entry"): "NWELNG Send-Outs",

    # Belgium
    ("Zeebrugge", "entry"): "NWELNG Send-Outs",

    # Netherlands
    ("Gate", "entry"): "NWELNG Send-Outs",
    ("Eemshaven", "entry"): "NWELNG Send-Outs",

    # Germany
    ("Wilhelmshaven", "entry"): "NWELNG Send-Outs",
    ("Brunsbüttel", "entry"): "NWELNG Send-Outs",

    # United Kingdom (already covered, but included for completeness)
    ("Isle of Grain", "entry"): "UK LNG Imports",
    ("Milford Haven - South Hook", "entry"): "UK LNG Imports",
    ("Milford Haven - Dragon", "entry"): "UK LNG Imports",






    # -------------------------------------RUSSIAN PIPELINE--------------------------------------------
    # Russian Pipeline (exit only)
    # Note: This list includes all major pipeline exit points, but many are no longer operational.

    # Nord Stream (to Germany) - Inactive
    ("Greifswald", "exit"): "Russian Pipeline",

    # Yamal-Europe (to Poland and Germany) - Inactive
    ("Mallnow", "exit"): "Russian Pipeline",
    ("Kondratki", "exit"): "Russian Pipeline",

    # Ukraine Transit (to EU countries)
    ("Velke Kapusany", "exit"): "Russian Pipeline",        # To Slovakia
    ("Berehove", "exit"): "Russian Pipeline",             # To Hungary
    ("Isaccea 1", "exit"): "Russian Pipeline",             # To Romania
    ("Orlovka", "exit"): "Russian Pipeline",               # To Romania (interconnection with Isaccea)

    # TurkStream (to Turkey and Southeast Europe)
    ("Malkoclar", "exit"): "Russian Pipeline",             # To Turkey, connecting onward to Bulgaria, Serbia, and Hungary
    ("Kiyikoy", "exit"): "Russian Pipeline",               # Alternative landing point in Turkey

    # Blue Stream (to Turkey)
    ("Durusu", "exit"): "Russian Pipeline",

    # Pipelines to Finland and the Baltics - Inactive
    ("Imatra", "exit"): "Russian Pipeline",                # To Finland
    ("Värska", "exit"): "Russian Pipeline",                 # To Estonia











    # ---------------------NORWEGIAN PRODUCTION--------------
    # Norwegian Production (entry only)
    ("Dornum", "entry"): "Norwegian Production",          # Entry point in Germany for the Europipe I and II pipelines
    ("Emden", "entry"): "Norwegian Production",          # Entry point in Germany for the Norpipe pipeline
    ("Zeebrugge", "entry"): "Norwegian Production",        # Entry point in Belgium for the Zeepipe pipeline
    ("Dunkerque", "entry"): "Norwegian Production",        # Entry point in France for the Franpipe
    ("St. Fergus Vesterled", "entry"): "Norwegian Production", # Entry point in the UK for the Vesterled pipeline
    ("Easington Langeled", "entry"): "Norwegian Production", # Entry point in the UK for the Langeled pipeline





    # --------------------UK PRODUCTION----------------

    # UK Production (entry only) - Gas from the UK Continental Shelf
    ("Bacton UKCS", "entry"): "UK Production",
    ("Barrow", "entry"): "UK Production",
    ("Easington", "entry"): "UK Production",
    ("St Fergus", "entry"): "UK Production",
    ("Teesside", "entry"): "UK Production",
    ("Theddlethorpe", "entry"): "UK Production",

    # UK Pipeline Imports (entry only) - Gas from European pipelines
    ("Bacton IUK", "entry"): "UK Pipeline Imports",
    ("Bacton BBL", "entry"): "UK Pipeline Imports",
    ("Easington Langeled", "entry"): "UK Pipeline Imports",
    ("St. Fergus Vesterled", "entry"): "UK Pipeline Imports",

    # UK LNG Imports (entry only) - Liquefied Natural Gas
    ("Isle of Grain", "entry"): "UK LNG Imports",
    ("Milford Haven - South Hook", "entry"): "UK LNG Imports",
    ("Milford Haven - Dragon", "entry"): "UK LNG Imports",



    # -------------------NORTH AFRICAN PIPELINES---------------

    # North African Pipelines (exit only)
    # TODO idk if these are right(the first 3)
    ("Trans-Med", "exit"): "North African Pipelines",
    ("GME (LY→IT)", "exit"): "North African Pipelines",
    ("Medgaz (DZ→ES)", "exit"): "North African Pipelines",
    # North African Pipelines (entry only)
    # Note: These are the European entry points for gas originating in North Africa.
    ("Mazara del Vallo", "entry"): "North African Pipelines",  # Trans-Mediterranean (TransMed) pipeline from Algeria via Tunisia
    ("Gela", "entry"): "North African Pipelines",             # Greenstream pipeline from Libya
    ("Almería", "entry"): "North African Pipelines",         # Medgaz pipeline from Algeria
    ("Tarifa", "entry"): "North African Pipelines",           # Maghreb-Europe (MEG) pipeline from Algeria via Morocco (currently inactive)





        # TAP (Azerbaijan→EU) (entry only)
    ("Kipoi", "entry"): "TAP (Azerbaijan→EU)",              # Entry point from TANAP (Turkey) into TAP (Greece)
    ("Nea Mesimvria", "entry"): "TAP (Azerbaijan→EU)",     # Interconnection point between TAP and the Greek national grid (DESFA)
    ("Melendugno", "entry"): "TAP (Azerbaijan→EU)",         # Entry point from TAP (subsea) into the Italian national grid (Snam Rete Gas)
}
