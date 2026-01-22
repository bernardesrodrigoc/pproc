# CNPq Knowledge Areas - Hierarchical Structure
# Based on official CNPq Table of Knowledge Areas
# Source: Tabela de Áreas do Conhecimento - CNPq

CNPQ_AREAS = {
    "1": {
        "code": "1",
        "name": "Ciências Exatas e da Terra",
        "name_en": "Exact and Earth Sciences",
        "areas": {
            "1.01": {
                "code": "1.01",
                "name": "Matemática",
                "name_en": "Mathematics",
                "subareas": [
                    {"code": "1.01.01", "name": "Álgebra", "name_en": "Algebra"},
                    {"code": "1.01.02", "name": "Análise", "name_en": "Analysis"},
                    {"code": "1.01.03", "name": "Geometria e Topologia", "name_en": "Geometry and Topology"},
                    {"code": "1.01.04", "name": "Matemática Aplicada", "name_en": "Applied Mathematics"}
                ]
            },
            "1.02": {
                "code": "1.02",
                "name": "Probabilidade e Estatística",
                "name_en": "Probability and Statistics",
                "subareas": [
                    {"code": "1.02.01", "name": "Probabilidade", "name_en": "Probability"},
                    {"code": "1.02.02", "name": "Estatística", "name_en": "Statistics"},
                    {"code": "1.02.03", "name": "Probabilidade e Estatística Aplicadas", "name_en": "Applied Probability and Statistics"}
                ]
            },
            "1.03": {
                "code": "1.03",
                "name": "Ciência da Computação",
                "name_en": "Computer Science",
                "subareas": [
                    {"code": "1.03.01", "name": "Teoria da Computação", "name_en": "Theory of Computation"},
                    {"code": "1.03.02", "name": "Matemática da Computação", "name_en": "Mathematical Computing"},
                    {"code": "1.03.03", "name": "Metodologia e Técnicas da Computação", "name_en": "Computing Methodology and Techniques"},
                    {"code": "1.03.04", "name": "Sistemas de Computação", "name_en": "Computer Systems"}
                ]
            },
            "1.04": {
                "code": "1.04",
                "name": "Astronomia",
                "name_en": "Astronomy",
                "subareas": [
                    {"code": "1.04.01", "name": "Astronomia de Posição e Mecânica Celeste", "name_en": "Positional Astronomy and Celestial Mechanics"},
                    {"code": "1.04.02", "name": "Astrofísica Estelar", "name_en": "Stellar Astrophysics"},
                    {"code": "1.04.03", "name": "Astrofísica do Meio Interestelar", "name_en": "Interstellar Medium Astrophysics"},
                    {"code": "1.04.04", "name": "Astrofísica Extragaláctica", "name_en": "Extragalactic Astrophysics"},
                    {"code": "1.04.05", "name": "Astrofísica do Sistema Solar", "name_en": "Solar System Astrophysics"},
                    {"code": "1.04.06", "name": "Instrumentação Astronômica", "name_en": "Astronomical Instrumentation"}
                ]
            },
            "1.05": {
                "code": "1.05",
                "name": "Física",
                "name_en": "Physics",
                "subareas": [
                    {"code": "1.05.01", "name": "Física Geral", "name_en": "General Physics"},
                    {"code": "1.05.02", "name": "Áreas Clássicas de Fenomenologia", "name_en": "Classical Phenomenology"},
                    {"code": "1.05.03", "name": "Física das Partículas Elementares", "name_en": "Particle Physics"},
                    {"code": "1.05.04", "name": "Física Nuclear", "name_en": "Nuclear Physics"},
                    {"code": "1.05.05", "name": "Física Atômica e Molecular", "name_en": "Atomic and Molecular Physics"},
                    {"code": "1.05.06", "name": "Física dos Fluídos, Física de Plasmas", "name_en": "Fluid and Plasma Physics"},
                    {"code": "1.05.07", "name": "Física da Matéria Condensada", "name_en": "Condensed Matter Physics"}
                ]
            },
            "1.06": {
                "code": "1.06",
                "name": "Química",
                "name_en": "Chemistry",
                "subareas": [
                    {"code": "1.06.01", "name": "Química Orgânica", "name_en": "Organic Chemistry"},
                    {"code": "1.06.02", "name": "Química Inorgânica", "name_en": "Inorganic Chemistry"},
                    {"code": "1.06.03", "name": "Físico-Química", "name_en": "Physical Chemistry"},
                    {"code": "1.06.04", "name": "Química Analítica", "name_en": "Analytical Chemistry"}
                ]
            },
            "1.07": {
                "code": "1.07",
                "name": "Geociências",
                "name_en": "Geosciences",
                "subareas": [
                    {"code": "1.07.01", "name": "Geologia", "name_en": "Geology"},
                    {"code": "1.07.02", "name": "Geofísica", "name_en": "Geophysics"},
                    {"code": "1.07.03", "name": "Meteorologia", "name_en": "Meteorology"},
                    {"code": "1.07.04", "name": "Geodésia", "name_en": "Geodesy"},
                    {"code": "1.07.05", "name": "Geografia Física", "name_en": "Physical Geography"}
                ]
            },
            "1.08": {
                "code": "1.08",
                "name": "Oceanografia",
                "name_en": "Oceanography",
                "subareas": [
                    {"code": "1.08.01", "name": "Oceanografia Biológica", "name_en": "Biological Oceanography"},
                    {"code": "1.08.02", "name": "Oceanografia Física", "name_en": "Physical Oceanography"},
                    {"code": "1.08.03", "name": "Oceanografia Química", "name_en": "Chemical Oceanography"},
                    {"code": "1.08.04", "name": "Oceanografia Geológica", "name_en": "Geological Oceanography"}
                ]
            }
        }
    },
    "2": {
        "code": "2",
        "name": "Ciências Biológicas",
        "name_en": "Biological Sciences",
        "areas": {
            "2.01": {
                "code": "2.01",
                "name": "Biologia Geral",
                "name_en": "General Biology",
                "subareas": []
            },
            "2.02": {
                "code": "2.02",
                "name": "Genética",
                "name_en": "Genetics",
                "subareas": [
                    {"code": "2.02.01", "name": "Genética Quantitativa", "name_en": "Quantitative Genetics"},
                    {"code": "2.02.02", "name": "Genética Molecular e de Microorganismos", "name_en": "Molecular and Microbial Genetics"},
                    {"code": "2.02.03", "name": "Genética Vegetal", "name_en": "Plant Genetics"},
                    {"code": "2.02.04", "name": "Genética Animal", "name_en": "Animal Genetics"},
                    {"code": "2.02.05", "name": "Genética Humana e Médica", "name_en": "Human and Medical Genetics"},
                    {"code": "2.02.06", "name": "Mutagênese", "name_en": "Mutagenesis"}
                ]
            },
            "2.03": {
                "code": "2.03",
                "name": "Botânica",
                "name_en": "Botany",
                "subareas": [
                    {"code": "2.03.01", "name": "Paleobotânica", "name_en": "Paleobotany"},
                    {"code": "2.03.02", "name": "Morfologia Vegetal", "name_en": "Plant Morphology"},
                    {"code": "2.03.03", "name": "Fisiologia Vegetal", "name_en": "Plant Physiology"},
                    {"code": "2.03.04", "name": "Taxonomia Vegetal", "name_en": "Plant Taxonomy"},
                    {"code": "2.03.05", "name": "Fitogeografia", "name_en": "Phytogeography"},
                    {"code": "2.03.06", "name": "Botânica Aplicada", "name_en": "Applied Botany"}
                ]
            },
            "2.04": {
                "code": "2.04",
                "name": "Zoologia",
                "name_en": "Zoology",
                "subareas": [
                    {"code": "2.04.01", "name": "Paleozoologia", "name_en": "Paleozoology"},
                    {"code": "2.04.02", "name": "Morfologia dos Grupos Recentes", "name_en": "Morphology of Recent Groups"},
                    {"code": "2.04.03", "name": "Fisiologia dos Grupos Recentes", "name_en": "Physiology of Recent Groups"},
                    {"code": "2.04.04", "name": "Comportamento Animal", "name_en": "Animal Behavior"},
                    {"code": "2.04.05", "name": "Taxonomia dos Grupos Recentes", "name_en": "Taxonomy of Recent Groups"},
                    {"code": "2.04.06", "name": "Zoologia Aplicada", "name_en": "Applied Zoology"}
                ]
            },
            "2.05": {
                "code": "2.05",
                "name": "Ecologia",
                "name_en": "Ecology",
                "subareas": [
                    {"code": "2.05.01", "name": "Ecologia Teórica", "name_en": "Theoretical Ecology"},
                    {"code": "2.05.02", "name": "Ecologia de Ecossistemas", "name_en": "Ecosystem Ecology"},
                    {"code": "2.05.03", "name": "Ecologia Aplicada", "name_en": "Applied Ecology"}
                ]
            },
            "2.06": {
                "code": "2.06",
                "name": "Morfologia",
                "name_en": "Morphology",
                "subareas": [
                    {"code": "2.06.01", "name": "Citologia e Biologia Celular", "name_en": "Cytology and Cell Biology"},
                    {"code": "2.06.02", "name": "Embriologia", "name_en": "Embryology"},
                    {"code": "2.06.03", "name": "Histologia", "name_en": "Histology"},
                    {"code": "2.06.04", "name": "Anatomia", "name_en": "Anatomy"}
                ]
            },
            "2.07": {
                "code": "2.07",
                "name": "Fisiologia",
                "name_en": "Physiology",
                "subareas": [
                    {"code": "2.07.01", "name": "Fisiologia Geral", "name_en": "General Physiology"},
                    {"code": "2.07.02", "name": "Fisiologia de Órgãos e Sistemas", "name_en": "Organ and System Physiology"},
                    {"code": "2.07.03", "name": "Fisiologia do Esforço", "name_en": "Exercise Physiology"},
                    {"code": "2.07.04", "name": "Fisiologia Comparada", "name_en": "Comparative Physiology"}
                ]
            },
            "2.08": {
                "code": "2.08",
                "name": "Bioquímica",
                "name_en": "Biochemistry",
                "subareas": [
                    {"code": "2.08.01", "name": "Química de Macromoléculas", "name_en": "Macromolecular Chemistry"},
                    {"code": "2.08.02", "name": "Bioquímica dos Microorganismos", "name_en": "Microbial Biochemistry"},
                    {"code": "2.08.03", "name": "Metabolismo e Bioenergética", "name_en": "Metabolism and Bioenergetics"},
                    {"code": "2.08.04", "name": "Biologia Molecular", "name_en": "Molecular Biology"},
                    {"code": "2.08.05", "name": "Enzimologia", "name_en": "Enzymology"}
                ]
            },
            "2.09": {
                "code": "2.09",
                "name": "Biofísica",
                "name_en": "Biophysics",
                "subareas": [
                    {"code": "2.09.01", "name": "Biofísica Molecular", "name_en": "Molecular Biophysics"},
                    {"code": "2.09.02", "name": "Biofísica Celular", "name_en": "Cellular Biophysics"},
                    {"code": "2.09.03", "name": "Biofísica de Processos e Sistemas", "name_en": "Process and System Biophysics"},
                    {"code": "2.09.04", "name": "Radiologia e Fotobiologia", "name_en": "Radiology and Photobiology"}
                ]
            },
            "2.10": {
                "code": "2.10",
                "name": "Farmacologia",
                "name_en": "Pharmacology",
                "subareas": [
                    {"code": "2.10.01", "name": "Farmacologia Geral", "name_en": "General Pharmacology"},
                    {"code": "2.10.02", "name": "Farmacologia Autonômica", "name_en": "Autonomic Pharmacology"},
                    {"code": "2.10.03", "name": "Neuropsicofarmacologia", "name_en": "Neuropsychopharmacology"},
                    {"code": "2.10.04", "name": "Farmacologia Cardiorenal", "name_en": "Cardiorenal Pharmacology"},
                    {"code": "2.10.05", "name": "Farmacologia Bioquímica e Molecular", "name_en": "Biochemical and Molecular Pharmacology"},
                    {"code": "2.10.06", "name": "Etnofarmacologia", "name_en": "Ethnopharmacology"},
                    {"code": "2.10.07", "name": "Toxicologia", "name_en": "Toxicology"},
                    {"code": "2.10.08", "name": "Farmacologia Clínica", "name_en": "Clinical Pharmacology"}
                ]
            },
            "2.11": {
                "code": "2.11",
                "name": "Imunologia",
                "name_en": "Immunology",
                "subareas": [
                    {"code": "2.11.01", "name": "Imunoquímica", "name_en": "Immunochemistry"},
                    {"code": "2.11.02", "name": "Imunologia Celular", "name_en": "Cellular Immunology"},
                    {"code": "2.11.03", "name": "Imunogenética", "name_en": "Immunogenetics"},
                    {"code": "2.11.04", "name": "Imunologia Aplicada", "name_en": "Applied Immunology"}
                ]
            },
            "2.12": {
                "code": "2.12",
                "name": "Microbiologia",
                "name_en": "Microbiology",
                "subareas": [
                    {"code": "2.12.01", "name": "Biologia e Fisiologia dos Microorganismos", "name_en": "Microbial Biology and Physiology"},
                    {"code": "2.12.02", "name": "Microbiologia Aplicada", "name_en": "Applied Microbiology"}
                ]
            },
            "2.13": {
                "code": "2.13",
                "name": "Parasitologia",
                "name_en": "Parasitology",
                "subareas": [
                    {"code": "2.13.01", "name": "Protozoologia de Parasitas", "name_en": "Parasite Protozoology"},
                    {"code": "2.13.02", "name": "Helmintologia de Parasitas", "name_en": "Parasite Helminthology"},
                    {"code": "2.13.03", "name": "Entomologia e Malacologia de Parasitas", "name_en": "Parasite Entomology and Malacology"}
                ]
            }
        }
    },
    "3": {
        "code": "3",
        "name": "Engenharias",
        "name_en": "Engineering",
        "areas": {
            "3.01": {
                "code": "3.01",
                "name": "Engenharia Civil",
                "name_en": "Civil Engineering",
                "subareas": [
                    {"code": "3.01.01", "name": "Construção Civil", "name_en": "Construction"},
                    {"code": "3.01.02", "name": "Estruturas", "name_en": "Structures"},
                    {"code": "3.01.03", "name": "Geotécnica", "name_en": "Geotechnics"},
                    {"code": "3.01.04", "name": "Engenharia Hidráulica", "name_en": "Hydraulic Engineering"},
                    {"code": "3.01.05", "name": "Infra-Estrutura de Transportes", "name_en": "Transport Infrastructure"}
                ]
            },
            "3.02": {
                "code": "3.02",
                "name": "Engenharia de Minas",
                "name_en": "Mining Engineering",
                "subareas": [
                    {"code": "3.02.01", "name": "Pesquisa Mineral", "name_en": "Mineral Research"},
                    {"code": "3.02.02", "name": "Lavra", "name_en": "Mining"},
                    {"code": "3.02.03", "name": "Tratamento de Minérios", "name_en": "Ore Treatment"}
                ]
            },
            "3.03": {
                "code": "3.03",
                "name": "Engenharia de Materiais e Metalúrgica",
                "name_en": "Materials and Metallurgical Engineering",
                "subareas": [
                    {"code": "3.03.01", "name": "Instalações e Equipamentos Metalúrgicos", "name_en": "Metallurgical Facilities and Equipment"},
                    {"code": "3.03.02", "name": "Metalurgia Extrativa", "name_en": "Extractive Metallurgy"},
                    {"code": "3.03.03", "name": "Metalurgia de Transformação", "name_en": "Transformation Metallurgy"},
                    {"code": "3.03.04", "name": "Metalurgia Física", "name_en": "Physical Metallurgy"},
                    {"code": "3.03.05", "name": "Materiais não Metálicos", "name_en": "Non-Metallic Materials"}
                ]
            },
            "3.04": {
                "code": "3.04",
                "name": "Engenharia Elétrica",
                "name_en": "Electrical Engineering",
                "subareas": [
                    {"code": "3.04.01", "name": "Materiais Elétricos", "name_en": "Electrical Materials"},
                    {"code": "3.04.02", "name": "Medidas Elétricas, Magnéticas e Eletrônicas", "name_en": "Electrical, Magnetic and Electronic Measurements"},
                    {"code": "3.04.03", "name": "Circuitos Elétricos, Magnéticos e Eletrônicos", "name_en": "Electrical, Magnetic and Electronic Circuits"},
                    {"code": "3.04.04", "name": "Sistemas Elétricos de Potência", "name_en": "Electric Power Systems"},
                    {"code": "3.04.05", "name": "Eletrônica Industrial, Sistemas e Controles Eletrônicos", "name_en": "Industrial Electronics, Electronic Systems and Controls"},
                    {"code": "3.04.06", "name": "Telecomunicações", "name_en": "Telecommunications"}
                ]
            },
            "3.05": {
                "code": "3.05",
                "name": "Engenharia Mecânica",
                "name_en": "Mechanical Engineering",
                "subareas": [
                    {"code": "3.05.01", "name": "Fenômenos de Transporte", "name_en": "Transport Phenomena"},
                    {"code": "3.05.02", "name": "Engenharia Térmica", "name_en": "Thermal Engineering"},
                    {"code": "3.05.03", "name": "Mecânica dos Sólidos", "name_en": "Solid Mechanics"},
                    {"code": "3.05.04", "name": "Projetos de Máquinas", "name_en": "Machine Design"},
                    {"code": "3.05.05", "name": "Processos de Fabricação", "name_en": "Manufacturing Processes"}
                ]
            },
            "3.06": {
                "code": "3.06",
                "name": "Engenharia Química",
                "name_en": "Chemical Engineering",
                "subareas": [
                    {"code": "3.06.01", "name": "Processos Industriais de Engenharia Química", "name_en": "Chemical Engineering Industrial Processes"},
                    {"code": "3.06.02", "name": "Operações Industriais e Equipamentos para Engenharia Química", "name_en": "Industrial Operations and Equipment for Chemical Engineering"},
                    {"code": "3.06.03", "name": "Tecnologia Química", "name_en": "Chemical Technology"}
                ]
            },
            "3.07": {
                "code": "3.07",
                "name": "Engenharia Sanitária",
                "name_en": "Sanitary Engineering",
                "subareas": [
                    {"code": "3.07.01", "name": "Recursos Hídricos", "name_en": "Water Resources"},
                    {"code": "3.07.02", "name": "Tratamento de Águas de Abastecimento e Residuárias", "name_en": "Water and Wastewater Treatment"},
                    {"code": "3.07.03", "name": "Saneamento Básico", "name_en": "Basic Sanitation"},
                    {"code": "3.07.04", "name": "Saneamento Ambiental", "name_en": "Environmental Sanitation"}
                ]
            },
            "3.08": {
                "code": "3.08",
                "name": "Engenharia de Produção",
                "name_en": "Production Engineering",
                "subareas": [
                    {"code": "3.08.01", "name": "Gerência de Produção", "name_en": "Production Management"},
                    {"code": "3.08.02", "name": "Pesquisa Operacional", "name_en": "Operational Research"},
                    {"code": "3.08.03", "name": "Engenharia do Produto", "name_en": "Product Engineering"},
                    {"code": "3.08.04", "name": "Engenharia Econômica", "name_en": "Economic Engineering"}
                ]
            },
            "3.09": {
                "code": "3.09",
                "name": "Engenharia Nuclear",
                "name_en": "Nuclear Engineering",
                "subareas": [
                    {"code": "3.09.01", "name": "Aplicações de Radioisótopos", "name_en": "Radioisotope Applications"},
                    {"code": "3.09.02", "name": "Fusão Controlada", "name_en": "Controlled Fusion"},
                    {"code": "3.09.03", "name": "Combustível Nuclear", "name_en": "Nuclear Fuel"},
                    {"code": "3.09.04", "name": "Tecnologia dos Reatores", "name_en": "Reactor Technology"}
                ]
            },
            "3.10": {
                "code": "3.10",
                "name": "Engenharia de Transportes",
                "name_en": "Transportation Engineering",
                "subareas": [
                    {"code": "3.10.01", "name": "Planejamento de Transportes", "name_en": "Transportation Planning"},
                    {"code": "3.10.02", "name": "Veículos e Equipamentos de Controle", "name_en": "Vehicles and Control Equipment"},
                    {"code": "3.10.03", "name": "Operações de Transportes", "name_en": "Transportation Operations"}
                ]
            },
            "3.11": {
                "code": "3.11",
                "name": "Engenharia Naval e Oceânica",
                "name_en": "Naval and Ocean Engineering",
                "subareas": [
                    {"code": "3.11.01", "name": "Hidrodinâmica de Navios e Sistemas Oceânicos", "name_en": "Hydrodynamics of Ships and Ocean Systems"},
                    {"code": "3.11.02", "name": "Estruturas Navais e Oceânicas", "name_en": "Naval and Ocean Structures"},
                    {"code": "3.11.03", "name": "Máquinas Marítimas", "name_en": "Marine Machinery"},
                    {"code": "3.11.04", "name": "Projeto de Navios", "name_en": "Ship Design"},
                    {"code": "3.11.05", "name": "Tecnologia de Construção Naval", "name_en": "Shipbuilding Technology"}
                ]
            },
            "3.12": {
                "code": "3.12",
                "name": "Engenharia Aeroespacial",
                "name_en": "Aerospace Engineering",
                "subareas": [
                    {"code": "3.12.01", "name": "Aerodinâmica", "name_en": "Aerodynamics"},
                    {"code": "3.12.02", "name": "Dinâmica de Vôo", "name_en": "Flight Dynamics"},
                    {"code": "3.12.03", "name": "Estruturas Aeroespaciais", "name_en": "Aerospace Structures"},
                    {"code": "3.12.04", "name": "Sistemas Aeroespaciais", "name_en": "Aerospace Systems"},
                    {"code": "3.12.05", "name": "Sistemas de Propulsão", "name_en": "Propulsion Systems"}
                ]
            },
            "3.13": {
                "code": "3.13",
                "name": "Engenharia Biomédica",
                "name_en": "Biomedical Engineering",
                "subareas": [
                    {"code": "3.13.01", "name": "Bioengenharia", "name_en": "Bioengineering"},
                    {"code": "3.13.02", "name": "Engenharia Médica", "name_en": "Medical Engineering"}
                ]
            }
        }
    },
    "4": {
        "code": "4",
        "name": "Ciências da Saúde",
        "name_en": "Health Sciences",
        "areas": {
            "4.01": {
                "code": "4.01",
                "name": "Medicina",
                "name_en": "Medicine",
                "subareas": [
                    {"code": "4.01.01", "name": "Clínica Médica", "name_en": "Medical Clinic"},
                    {"code": "4.01.02", "name": "Cirurgia", "name_en": "Surgery"},
                    {"code": "4.01.03", "name": "Saúde Materno-Infantil", "name_en": "Maternal and Child Health"},
                    {"code": "4.01.04", "name": "Psiquiatria", "name_en": "Psychiatry"},
                    {"code": "4.01.05", "name": "Anatomia Patológica e Patologia Clínica", "name_en": "Pathological Anatomy and Clinical Pathology"},
                    {"code": "4.01.06", "name": "Radiologia Médica", "name_en": "Medical Radiology"},
                    {"code": "4.01.07", "name": "Medicina Legal e Deontologia", "name_en": "Legal Medicine and Deontology"}
                ]
            },
            "4.02": {
                "code": "4.02",
                "name": "Odontologia",
                "name_en": "Dentistry",
                "subareas": [
                    {"code": "4.02.01", "name": "Clínica Odontológica", "name_en": "Dental Clinic"},
                    {"code": "4.02.02", "name": "Cirurgia Buco-Maxilo-Facial", "name_en": "Oral and Maxillofacial Surgery"},
                    {"code": "4.02.03", "name": "Ortodontia", "name_en": "Orthodontics"},
                    {"code": "4.02.04", "name": "Odontopediatria", "name_en": "Pediatric Dentistry"},
                    {"code": "4.02.05", "name": "Periodontia", "name_en": "Periodontics"},
                    {"code": "4.02.06", "name": "Endodontia", "name_en": "Endodontics"},
                    {"code": "4.02.07", "name": "Radiologia Odontológica", "name_en": "Dental Radiology"},
                    {"code": "4.02.08", "name": "Odontologia Social e Preventiva", "name_en": "Social and Preventive Dentistry"},
                    {"code": "4.02.09", "name": "Materiais Odontológicos", "name_en": "Dental Materials"}
                ]
            },
            "4.03": {
                "code": "4.03",
                "name": "Farmácia",
                "name_en": "Pharmacy",
                "subareas": [
                    {"code": "4.03.01", "name": "Farmacotecnia", "name_en": "Pharmaceutical Technology"},
                    {"code": "4.03.02", "name": "Farmacognosia", "name_en": "Pharmacognosy"},
                    {"code": "4.03.03", "name": "Análise Toxicológica", "name_en": "Toxicological Analysis"},
                    {"code": "4.03.04", "name": "Análise e Controle de Medicamentos", "name_en": "Drug Analysis and Control"},
                    {"code": "4.03.05", "name": "Bromatologia", "name_en": "Bromatology"}
                ]
            },
            "4.04": {
                "code": "4.04",
                "name": "Enfermagem",
                "name_en": "Nursing",
                "subareas": [
                    {"code": "4.04.01", "name": "Enfermagem Médico-Cirúrgica", "name_en": "Medical-Surgical Nursing"},
                    {"code": "4.04.02", "name": "Enfermagem Obstétrica", "name_en": "Obstetric Nursing"},
                    {"code": "4.04.03", "name": "Enfermagem Pediátrica", "name_en": "Pediatric Nursing"},
                    {"code": "4.04.04", "name": "Enfermagem Psiquiátrica", "name_en": "Psychiatric Nursing"},
                    {"code": "4.04.05", "name": "Enfermagem de Doenças Contagiosas", "name_en": "Infectious Disease Nursing"},
                    {"code": "4.04.06", "name": "Enfermagem de Saúde Pública", "name_en": "Public Health Nursing"}
                ]
            },
            "4.05": {
                "code": "4.05",
                "name": "Nutrição",
                "name_en": "Nutrition",
                "subareas": [
                    {"code": "4.05.01", "name": "Bioquímica da Nutrição", "name_en": "Nutrition Biochemistry"},
                    {"code": "4.05.02", "name": "Dietética", "name_en": "Dietetics"},
                    {"code": "4.05.03", "name": "Análise Nutricional de População", "name_en": "Population Nutritional Analysis"},
                    {"code": "4.05.04", "name": "Desnutrição e Desenvolvimento Fisiológico", "name_en": "Malnutrition and Physiological Development"}
                ]
            },
            "4.06": {
                "code": "4.06",
                "name": "Saúde Coletiva",
                "name_en": "Public Health",
                "subareas": [
                    {"code": "4.06.01", "name": "Epidemiologia", "name_en": "Epidemiology"},
                    {"code": "4.06.02", "name": "Saúde Pública", "name_en": "Public Health"},
                    {"code": "4.06.03", "name": "Medicina Preventiva", "name_en": "Preventive Medicine"}
                ]
            },
            "4.07": {
                "code": "4.07",
                "name": "Fonoaudiologia",
                "name_en": "Speech Therapy",
                "subareas": []
            },
            "4.08": {
                "code": "4.08",
                "name": "Fisioterapia e Terapia Ocupacional",
                "name_en": "Physiotherapy and Occupational Therapy",
                "subareas": []
            },
            "4.09": {
                "code": "4.09",
                "name": "Educação Física",
                "name_en": "Physical Education",
                "subareas": []
            }
        }
    },
    "5": {
        "code": "5",
        "name": "Ciências Agrárias",
        "name_en": "Agricultural Sciences",
        "areas": {
            "5.01": {
                "code": "5.01",
                "name": "Agronomia",
                "name_en": "Agronomy",
                "subareas": [
                    {"code": "5.01.01", "name": "Ciência do Solo", "name_en": "Soil Science"},
                    {"code": "5.01.02", "name": "Fitossanidade", "name_en": "Plant Health"},
                    {"code": "5.01.03", "name": "Fitotecnia", "name_en": "Crop Science"},
                    {"code": "5.01.04", "name": "Floricultura, Parques e Jardins", "name_en": "Floriculture, Parks and Gardens"},
                    {"code": "5.01.05", "name": "Agrometeorologia", "name_en": "Agrometeorology"},
                    {"code": "5.01.06", "name": "Extensão Rural", "name_en": "Rural Extension"}
                ]
            },
            "5.02": {
                "code": "5.02",
                "name": "Recursos Florestais e Engenharia Florestal",
                "name_en": "Forest Resources and Forest Engineering",
                "subareas": [
                    {"code": "5.02.01", "name": "Silvicultura", "name_en": "Silviculture"},
                    {"code": "5.02.02", "name": "Manejo Florestal", "name_en": "Forest Management"},
                    {"code": "5.02.03", "name": "Técnicas e Operações Florestais", "name_en": "Forest Techniques and Operations"},
                    {"code": "5.02.04", "name": "Tecnologia e Utilização de Produtos Florestais", "name_en": "Forest Products Technology and Utilization"},
                    {"code": "5.02.05", "name": "Conservação da Natureza", "name_en": "Nature Conservation"},
                    {"code": "5.02.06", "name": "Energia de Biomassa Florestal", "name_en": "Forest Biomass Energy"}
                ]
            },
            "5.03": {
                "code": "5.03",
                "name": "Engenharia Agrícola",
                "name_en": "Agricultural Engineering",
                "subareas": [
                    {"code": "5.03.01", "name": "Máquinas e Implementos Agrícolas", "name_en": "Agricultural Machinery and Implements"},
                    {"code": "5.03.02", "name": "Engenharia de Água e Solo", "name_en": "Water and Soil Engineering"},
                    {"code": "5.03.03", "name": "Engenharia de Processamento de Produtos Agrícolas", "name_en": "Agricultural Product Processing Engineering"},
                    {"code": "5.03.04", "name": "Construções Rurais e Ambiência", "name_en": "Rural Constructions and Environment"},
                    {"code": "5.03.05", "name": "Energização Rural", "name_en": "Rural Energization"}
                ]
            },
            "5.04": {
                "code": "5.04",
                "name": "Zootecnia",
                "name_en": "Animal Science",
                "subareas": [
                    {"code": "5.04.01", "name": "Ecologia dos Animais Domésticos e Etologia", "name_en": "Domestic Animal Ecology and Ethology"},
                    {"code": "5.04.02", "name": "Genética e Melhoramento dos Animais Domésticos", "name_en": "Genetics and Improvement of Domestic Animals"},
                    {"code": "5.04.03", "name": "Nutrição e Alimentação Animal", "name_en": "Animal Nutrition and Feed"},
                    {"code": "5.04.04", "name": "Produção Animal", "name_en": "Animal Production"}
                ]
            },
            "5.05": {
                "code": "5.05",
                "name": "Medicina Veterinária",
                "name_en": "Veterinary Medicine",
                "subareas": [
                    {"code": "5.05.01", "name": "Clínica e Cirurgia Animal", "name_en": "Animal Clinic and Surgery"},
                    {"code": "5.05.02", "name": "Medicina Veterinária Preventiva", "name_en": "Preventive Veterinary Medicine"},
                    {"code": "5.05.03", "name": "Patologia Animal", "name_en": "Animal Pathology"},
                    {"code": "5.05.04", "name": "Reprodução Animal", "name_en": "Animal Reproduction"},
                    {"code": "5.05.05", "name": "Inspeção de Produtos de Origem Animal", "name_en": "Inspection of Animal Products"}
                ]
            },
            "5.06": {
                "code": "5.06",
                "name": "Recursos Pesqueiros e Engenharia de Pesca",
                "name_en": "Fishery Resources and Fisheries Engineering",
                "subareas": [
                    {"code": "5.06.01", "name": "Recursos Pesqueiros Marinhos", "name_en": "Marine Fishery Resources"},
                    {"code": "5.06.02", "name": "Recursos Pesqueiros de Águas Interiores", "name_en": "Inland Fishery Resources"},
                    {"code": "5.06.03", "name": "Aqüicultura", "name_en": "Aquaculture"},
                    {"code": "5.06.04", "name": "Engenharia de Pesca", "name_en": "Fisheries Engineering"}
                ]
            },
            "5.07": {
                "code": "5.07",
                "name": "Ciência e Tecnologia de Alimentos",
                "name_en": "Food Science and Technology",
                "subareas": [
                    {"code": "5.07.01", "name": "Ciência de Alimentos", "name_en": "Food Science"},
                    {"code": "5.07.02", "name": "Tecnologia de Alimentos", "name_en": "Food Technology"},
                    {"code": "5.07.03", "name": "Engenharia de Alimentos", "name_en": "Food Engineering"}
                ]
            }
        }
    },
    "6": {
        "code": "6",
        "name": "Ciências Sociais Aplicadas",
        "name_en": "Applied Social Sciences",
        "areas": {
            "6.01": {
                "code": "6.01",
                "name": "Direito",
                "name_en": "Law",
                "subareas": [
                    {"code": "6.01.01", "name": "Teoria do Direito", "name_en": "Legal Theory"},
                    {"code": "6.01.02", "name": "Direito Público", "name_en": "Public Law"},
                    {"code": "6.01.03", "name": "Direito Privado", "name_en": "Private Law"}
                ]
            },
            "6.02": {
                "code": "6.02",
                "name": "Administração",
                "name_en": "Administration",
                "subareas": [
                    {"code": "6.02.01", "name": "Administração de Empresas", "name_en": "Business Administration"},
                    {"code": "6.02.02", "name": "Administração Pública", "name_en": "Public Administration"},
                    {"code": "6.02.03", "name": "Administração de Setores Específicos", "name_en": "Sector-Specific Administration"},
                    {"code": "6.02.04", "name": "Ciências Contábeis", "name_en": "Accounting Sciences"}
                ]
            },
            "6.03": {
                "code": "6.03",
                "name": "Economia",
                "name_en": "Economics",
                "subareas": [
                    {"code": "6.03.01", "name": "Teoria Econômica", "name_en": "Economic Theory"},
                    {"code": "6.03.02", "name": "Métodos Quantitativos em Economia", "name_en": "Quantitative Methods in Economics"},
                    {"code": "6.03.03", "name": "Economia Monetária e Fiscal", "name_en": "Monetary and Fiscal Economics"},
                    {"code": "6.03.04", "name": "Crescimento, Flutuações e Planejamento Econômico", "name_en": "Growth, Fluctuations and Economic Planning"},
                    {"code": "6.03.05", "name": "Economia Internacional", "name_en": "International Economics"},
                    {"code": "6.03.06", "name": "Economia dos Recursos Humanos", "name_en": "Human Resources Economics"},
                    {"code": "6.03.07", "name": "Economia Industrial", "name_en": "Industrial Economics"},
                    {"code": "6.03.08", "name": "Economia do Bem-Estar Social", "name_en": "Social Welfare Economics"},
                    {"code": "6.03.09", "name": "Economia Regional e Urbana", "name_en": "Regional and Urban Economics"},
                    {"code": "6.03.10", "name": "Economias Agrária e dos Recursos Naturais", "name_en": "Agrarian and Natural Resource Economics"}
                ]
            },
            "6.04": {
                "code": "6.04",
                "name": "Arquitetura e Urbanismo",
                "name_en": "Architecture and Urbanism",
                "subareas": [
                    {"code": "6.04.01", "name": "Fundamentos de Arquitetura e Urbanismo", "name_en": "Fundamentals of Architecture and Urbanism"},
                    {"code": "6.04.02", "name": "Projeto de Arquitetura e Urbanismo", "name_en": "Architectural and Urban Design"},
                    {"code": "6.04.03", "name": "Tecnologia de Arquitetura e Urbanismo", "name_en": "Technology of Architecture and Urbanism"},
                    {"code": "6.04.04", "name": "Paisagismo", "name_en": "Landscaping"}
                ]
            },
            "6.05": {
                "code": "6.05",
                "name": "Planejamento Urbano e Regional",
                "name_en": "Urban and Regional Planning",
                "subareas": [
                    {"code": "6.05.01", "name": "Fundamentos do Planejamento Urbano e Regional", "name_en": "Fundamentals of Urban and Regional Planning"},
                    {"code": "6.05.02", "name": "Métodos e Técnicas do Planejamento Urbano e Regional", "name_en": "Methods and Techniques of Urban and Regional Planning"},
                    {"code": "6.05.03", "name": "Serviços Urbanos e Regionais", "name_en": "Urban and Regional Services"}
                ]
            },
            "6.06": {
                "code": "6.06",
                "name": "Demografia",
                "name_en": "Demography",
                "subareas": [
                    {"code": "6.06.01", "name": "Distribuição Espacial", "name_en": "Spatial Distribution"},
                    {"code": "6.06.02", "name": "Tendências Populacionais", "name_en": "Population Trends"},
                    {"code": "6.06.03", "name": "Componentes da Dinâmica Demográfica", "name_en": "Components of Demographic Dynamics"},
                    {"code": "6.06.04", "name": "Nupcialidade e Família", "name_en": "Nuptiality and Family"},
                    {"code": "6.06.05", "name": "Demografia Histórica", "name_en": "Historical Demography"},
                    {"code": "6.06.06", "name": "Política Pública e População", "name_en": "Public Policy and Population"},
                    {"code": "6.06.07", "name": "Fontes de Dados Demográficos", "name_en": "Demographic Data Sources"}
                ]
            },
            "6.07": {
                "code": "6.07",
                "name": "Ciência da Informação",
                "name_en": "Information Science",
                "subareas": [
                    {"code": "6.07.01", "name": "Teoria da Informação", "name_en": "Information Theory"},
                    {"code": "6.07.02", "name": "Biblioteconomia", "name_en": "Library Science"},
                    {"code": "6.07.03", "name": "Arquivologia", "name_en": "Archival Science"}
                ]
            },
            "6.08": {
                "code": "6.08",
                "name": "Museologia",
                "name_en": "Museology",
                "subareas": []
            },
            "6.09": {
                "code": "6.09",
                "name": "Comunicação",
                "name_en": "Communication",
                "subareas": [
                    {"code": "6.09.01", "name": "Teoria da Comunicação", "name_en": "Communication Theory"},
                    {"code": "6.09.02", "name": "Jornalismo e Editoração", "name_en": "Journalism and Publishing"},
                    {"code": "6.09.03", "name": "Rádio e Televisão", "name_en": "Radio and Television"},
                    {"code": "6.09.04", "name": "Relações Públicas e Propaganda", "name_en": "Public Relations and Advertising"},
                    {"code": "6.09.05", "name": "Comunicação Visual", "name_en": "Visual Communication"}
                ]
            },
            "6.10": {
                "code": "6.10",
                "name": "Serviço Social",
                "name_en": "Social Work",
                "subareas": [
                    {"code": "6.10.01", "name": "Fundamentos do Serviço Social", "name_en": "Fundamentals of Social Work"},
                    {"code": "6.10.02", "name": "Serviço Social Aplicado", "name_en": "Applied Social Work"}
                ]
            },
            "6.11": {
                "code": "6.11",
                "name": "Economia Doméstica",
                "name_en": "Home Economics",
                "subareas": []
            },
            "6.12": {
                "code": "6.12",
                "name": "Desenho Industrial",
                "name_en": "Industrial Design",
                "subareas": [
                    {"code": "6.12.01", "name": "Programação Visual", "name_en": "Visual Programming"},
                    {"code": "6.12.02", "name": "Desenho de Produto", "name_en": "Product Design"}
                ]
            },
            "6.13": {
                "code": "6.13",
                "name": "Turismo",
                "name_en": "Tourism",
                "subareas": []
            }
        }
    },
    "7": {
        "code": "7",
        "name": "Ciências Humanas",
        "name_en": "Humanities",
        "areas": {
            "7.01": {
                "code": "7.01",
                "name": "Filosofia",
                "name_en": "Philosophy",
                "subareas": [
                    {"code": "7.01.01", "name": "História da Filosofia", "name_en": "History of Philosophy"},
                    {"code": "7.01.02", "name": "Metafísica", "name_en": "Metaphysics"},
                    {"code": "7.01.03", "name": "Lógica", "name_en": "Logic"},
                    {"code": "7.01.04", "name": "Ética", "name_en": "Ethics"},
                    {"code": "7.01.05", "name": "Epistemologia", "name_en": "Epistemology"},
                    {"code": "7.01.06", "name": "Filosofia Brasileira", "name_en": "Brazilian Philosophy"}
                ]
            },
            "7.02": {
                "code": "7.02",
                "name": "Sociologia",
                "name_en": "Sociology",
                "subareas": [
                    {"code": "7.02.01", "name": "Fundamentos da Sociologia", "name_en": "Fundamentals of Sociology"},
                    {"code": "7.02.02", "name": "Sociologia do Conhecimento", "name_en": "Sociology of Knowledge"},
                    {"code": "7.02.03", "name": "Sociologia do Desenvolvimento", "name_en": "Sociology of Development"},
                    {"code": "7.02.04", "name": "Sociologia Urbana", "name_en": "Urban Sociology"},
                    {"code": "7.02.05", "name": "Sociologia Rural", "name_en": "Rural Sociology"},
                    {"code": "7.02.06", "name": "Sociologia da Saúde", "name_en": "Sociology of Health"},
                    {"code": "7.02.07", "name": "Outras Sociologias Específicas", "name_en": "Other Specific Sociologies"}
                ]
            },
            "7.03": {
                "code": "7.03",
                "name": "Antropologia",
                "name_en": "Anthropology",
                "subareas": [
                    {"code": "7.03.01", "name": "Teoria Antropológica", "name_en": "Anthropological Theory"},
                    {"code": "7.03.02", "name": "Etnologia Indígena", "name_en": "Indigenous Ethnology"},
                    {"code": "7.03.03", "name": "Antropologia Urbana", "name_en": "Urban Anthropology"},
                    {"code": "7.03.04", "name": "Antropologia Rural", "name_en": "Rural Anthropology"},
                    {"code": "7.03.05", "name": "Antropologia das Populações Afro-Brasileiras", "name_en": "Anthropology of Afro-Brazilian Populations"}
                ]
            },
            "7.04": {
                "code": "7.04",
                "name": "Arqueologia",
                "name_en": "Archaeology",
                "subareas": [
                    {"code": "7.04.01", "name": "Teoria e Método em Arqueologia", "name_en": "Theory and Method in Archaeology"},
                    {"code": "7.04.02", "name": "Arqueologia Pré-Histórica", "name_en": "Prehistoric Archaeology"},
                    {"code": "7.04.03", "name": "Arqueologia Histórica", "name_en": "Historical Archaeology"}
                ]
            },
            "7.05": {
                "code": "7.05",
                "name": "História",
                "name_en": "History",
                "subareas": [
                    {"code": "7.05.01", "name": "Teoria e Filosofia da História", "name_en": "Theory and Philosophy of History"},
                    {"code": "7.05.02", "name": "História Antiga e Medieval", "name_en": "Ancient and Medieval History"},
                    {"code": "7.05.03", "name": "História Moderna e Contemporânea", "name_en": "Modern and Contemporary History"},
                    {"code": "7.05.04", "name": "História da América", "name_en": "History of America"},
                    {"code": "7.05.05", "name": "História do Brasil", "name_en": "History of Brazil"},
                    {"code": "7.05.06", "name": "História das Ciências", "name_en": "History of Science"}
                ]
            },
            "7.06": {
                "code": "7.06",
                "name": "Geografia",
                "name_en": "Geography",
                "subareas": [
                    {"code": "7.06.01", "name": "Geografia Humana", "name_en": "Human Geography"},
                    {"code": "7.06.02", "name": "Geografia Regional", "name_en": "Regional Geography"}
                ]
            },
            "7.07": {
                "code": "7.07",
                "name": "Psicologia",
                "name_en": "Psychology",
                "subareas": [
                    {"code": "7.07.01", "name": "Fundamentos e Medidas da Psicologia", "name_en": "Fundamentals and Measures of Psychology"},
                    {"code": "7.07.02", "name": "Psicologia Experimental", "name_en": "Experimental Psychology"},
                    {"code": "7.07.03", "name": "Psicologia Fisiológica", "name_en": "Physiological Psychology"},
                    {"code": "7.07.04", "name": "Psicologia Comparativa", "name_en": "Comparative Psychology"},
                    {"code": "7.07.05", "name": "Psicologia Social", "name_en": "Social Psychology"},
                    {"code": "7.07.06", "name": "Psicologia Cognitiva", "name_en": "Cognitive Psychology"},
                    {"code": "7.07.07", "name": "Psicologia do Desenvolvimento Humano", "name_en": "Human Developmental Psychology"},
                    {"code": "7.07.08", "name": "Psicologia do Ensino e da Aprendizagem", "name_en": "Psychology of Teaching and Learning"},
                    {"code": "7.07.09", "name": "Psicologia do Trabalho e Organizacional", "name_en": "Work and Organizational Psychology"},
                    {"code": "7.07.10", "name": "Tratamento e Prevenção Psicológica", "name_en": "Psychological Treatment and Prevention"}
                ]
            },
            "7.08": {
                "code": "7.08",
                "name": "Educação",
                "name_en": "Education",
                "subareas": [
                    {"code": "7.08.01", "name": "Fundamentos da Educação", "name_en": "Foundations of Education"},
                    {"code": "7.08.02", "name": "Administração Educacional", "name_en": "Educational Administration"},
                    {"code": "7.08.03", "name": "Planejamento e Avaliação Educacional", "name_en": "Educational Planning and Evaluation"},
                    {"code": "7.08.04", "name": "Ensino-Aprendizagem", "name_en": "Teaching-Learning"},
                    {"code": "7.08.05", "name": "Currículo", "name_en": "Curriculum"},
                    {"code": "7.08.06", "name": "Orientação e Aconselhamento", "name_en": "Guidance and Counseling"},
                    {"code": "7.08.07", "name": "Tópicos Específicos de Educação", "name_en": "Specific Topics in Education"}
                ]
            },
            "7.09": {
                "code": "7.09",
                "name": "Ciência Política",
                "name_en": "Political Science",
                "subareas": [
                    {"code": "7.09.01", "name": "Teoria Política", "name_en": "Political Theory"},
                    {"code": "7.09.02", "name": "Estado e Governo", "name_en": "State and Government"},
                    {"code": "7.09.03", "name": "Comportamento Político", "name_en": "Political Behavior"},
                    {"code": "7.09.04", "name": "Políticas Públicas", "name_en": "Public Policies"},
                    {"code": "7.09.05", "name": "Política Internacional", "name_en": "International Politics"}
                ]
            },
            "7.10": {
                "code": "7.10",
                "name": "Teologia",
                "name_en": "Theology",
                "subareas": [
                    {"code": "7.10.01", "name": "História da Teologia", "name_en": "History of Theology"},
                    {"code": "7.10.02", "name": "Teologia Moral", "name_en": "Moral Theology"},
                    {"code": "7.10.03", "name": "Teologia Sistemática", "name_en": "Systematic Theology"},
                    {"code": "7.10.04", "name": "Teologia Pastoral", "name_en": "Pastoral Theology"}
                ]
            }
        }
    },
    "8": {
        "code": "8",
        "name": "Linguística, Letras e Artes",
        "name_en": "Linguistics, Literature and Arts",
        "areas": {
            "8.01": {
                "code": "8.01",
                "name": "Linguística",
                "name_en": "Linguistics",
                "subareas": [
                    {"code": "8.01.01", "name": "Teoria e Análise Linguística", "name_en": "Linguistic Theory and Analysis"},
                    {"code": "8.01.02", "name": "Fisiologia da Linguagem", "name_en": "Physiology of Language"},
                    {"code": "8.01.03", "name": "Linguística Histórica", "name_en": "Historical Linguistics"},
                    {"code": "8.01.04", "name": "Sociolinguística e Dialetologia", "name_en": "Sociolinguistics and Dialectology"},
                    {"code": "8.01.05", "name": "Psicolinguística", "name_en": "Psycholinguistics"},
                    {"code": "8.01.06", "name": "Linguística Aplicada", "name_en": "Applied Linguistics"}
                ]
            },
            "8.02": {
                "code": "8.02",
                "name": "Letras",
                "name_en": "Literature",
                "subareas": [
                    {"code": "8.02.01", "name": "Língua Portuguesa", "name_en": "Portuguese Language"},
                    {"code": "8.02.02", "name": "Línguas Estrangeiras Modernas", "name_en": "Modern Foreign Languages"},
                    {"code": "8.02.03", "name": "Línguas Clássicas", "name_en": "Classical Languages"},
                    {"code": "8.02.04", "name": "Línguas Indígenas", "name_en": "Indigenous Languages"},
                    {"code": "8.02.05", "name": "Teoria Literária", "name_en": "Literary Theory"},
                    {"code": "8.02.06", "name": "Literatura Brasileira", "name_en": "Brazilian Literature"},
                    {"code": "8.02.07", "name": "Outras Literaturas Vernáculas", "name_en": "Other Vernacular Literatures"},
                    {"code": "8.02.08", "name": "Literaturas Estrangeiras Modernas", "name_en": "Modern Foreign Literatures"},
                    {"code": "8.02.09", "name": "Literaturas Clássicas", "name_en": "Classical Literatures"},
                    {"code": "8.02.10", "name": "Literatura Comparada", "name_en": "Comparative Literature"}
                ]
            },
            "8.03": {
                "code": "8.03",
                "name": "Artes",
                "name_en": "Arts",
                "subareas": [
                    {"code": "8.03.01", "name": "Fundamentos e Crítica das Artes", "name_en": "Fundamentals and Art Criticism"},
                    {"code": "8.03.02", "name": "Artes Plásticas", "name_en": "Visual Arts"},
                    {"code": "8.03.03", "name": "Música", "name_en": "Music"},
                    {"code": "8.03.04", "name": "Dança", "name_en": "Dance"},
                    {"code": "8.03.05", "name": "Teatro", "name_en": "Theater"},
                    {"code": "8.03.06", "name": "Cinema", "name_en": "Cinema"},
                    {"code": "8.03.07", "name": "Educação Artística", "name_en": "Art Education"}
                ]
            }
        }
    },
    "9": {
        "code": "9",
        "name": "Outros",
        "name_en": "Others",
        "areas": {
            "9.01": {
                "code": "9.01",
                "name": "Multidisciplinar",
                "name_en": "Multidisciplinary",
                "subareas": [
                    {"code": "9.01.01", "name": "Interdisciplinar", "name_en": "Interdisciplinary"},
                    {"code": "9.01.02", "name": "Ensino de Ciências e Matemática", "name_en": "Science and Mathematics Teaching"},
                    {"code": "9.01.03", "name": "Materiais", "name_en": "Materials"},
                    {"code": "9.01.04", "name": "Biotecnologia", "name_en": "Biotechnology"},
                    {"code": "9.01.05", "name": "Ciências Ambientais", "name_en": "Environmental Sciences"}
                ]
            }
        }
    }
}

def get_grande_areas():
    """Return list of Grande Áreas (top level)"""
    return [
        {"code": code, "name": data["name"], "name_en": data["name_en"]}
        for code, data in CNPQ_AREAS.items()
    ]

def get_areas(grande_area_code: str):
    """Return list of Áreas for a given Grande Área"""
    grande_area = CNPQ_AREAS.get(grande_area_code)
    if not grande_area:
        return []
    return [
        {"code": code, "name": data["name"], "name_en": data["name_en"]}
        for code, data in grande_area["areas"].items()
    ]

def get_subareas(area_code: str):
    """Return list of Subáreas for a given Área"""
    # Extract grande_area code from area code (e.g., "1.01" -> "1")
    grande_area_code = area_code.split(".")[0]
    grande_area = CNPQ_AREAS.get(grande_area_code)
    if not grande_area:
        return []
    
    area = grande_area["areas"].get(area_code)
    if not area:
        return []
    
    return area.get("subareas", [])

def get_area_by_code(code: str):
    """Get area details by full code (e.g., "1.01.02")"""
    parts = code.split(".")
    
    if len(parts) == 1:
        # Grande Área
        ga = CNPQ_AREAS.get(code)
        if ga:
            return {"type": "grande_area", "code": code, "name": ga["name"], "name_en": ga["name_en"]}
    
    elif len(parts) == 2:
        # Área
        grande_area_code = parts[0]
        ga = CNPQ_AREAS.get(grande_area_code)
        if ga:
            area = ga["areas"].get(code)
            if area:
                return {"type": "area", "code": code, "name": area["name"], "name_en": area["name_en"]}
    
    elif len(parts) == 3:
        # Subárea
        grande_area_code = parts[0]
        area_code = f"{parts[0]}.{parts[1]}"
        ga = CNPQ_AREAS.get(grande_area_code)
        if ga:
            area = ga["areas"].get(area_code)
            if area:
                for subarea in area.get("subareas", []):
                    if subarea["code"] == code:
                        return {"type": "subarea", "code": code, "name": subarea["name"], "name_en": subarea["name_en"]}
    
    return None
