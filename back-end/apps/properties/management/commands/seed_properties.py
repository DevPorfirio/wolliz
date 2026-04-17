from urllib.request import Request, urlopen

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from apps.properties.models import Property, PropertyImage

# Marker usado para identificar registros de mock (permite limpar sem afetar dados reais)
MOCK_MARKER = "[MOCK]"

# Sample real-estate photos (Unsplash, livres para uso). Baixadas uma vez,
# armazenadas no MinIO em `properties/samples/` e reutilizadas em todos os mocks.
SAMPLE_IMAGE_URLS = [
    # Casa moderna com piscina (cover)
    "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=1600&q=80",
    # Fachada noturna
    "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1600&q=80",
    # Sala de estar moderna
    "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1600&q=80",
    # Cozinha planejada
    "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=1600&q=80",
    # Quarto principal
    "https://images.unsplash.com/photo-1600573472556-e636c2acda88?w=1600&q=80",
]

MOCK_PROPERTIES = [
    # ── Grande Florianópolis — Palhoça / São José / Biguaçu ───────────────────
    {
        "title": "Casa térrea em Palhoça",
        "description": "Casa bem localizada no centro de Palhoça, quintal, 2 vagas e área de serviço.",
        "property_type": "house", "listing_type": "sale",
        "price": 420_000, "area_m2": 130, "bedrooms": 3, "bathrooms": 2, "parking_spots": 2,
        "latitude": -27.6434, "longitude": -48.6694,
        "address_line": "R. Frei Caneca, 320 — Centro", "city": "Palhoça", "state": "SC",
    },
    {
        "title": "Apartamento 2 quartos em Palhoça",
        "description": "Apartamento novo, lazer completo, próximo ao shopping Palladium.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 340_000, "area_m2": 68, "bedrooms": 2, "bathrooms": 2, "parking_spots": 1,
        "latitude": -27.6371, "longitude": -48.6609,
        "address_line": "Av. Benício Figueiredo, 870 — Passa Vinte", "city": "Palhoça", "state": "SC",
    },
    {
        "title": "Casa de alto padrão em Pedra Branca",
        "description": "Casa em condomínio fechado no bairro planejado Pedra Branca, academia, parque e escola.",
        "property_type": "house", "listing_type": "sale",
        "price": 1_200_000, "area_m2": 280, "bedrooms": 4, "bathrooms": 4, "parking_spots": 3,
        "latitude": -27.6208, "longitude": -48.6317,
        "address_line": "R. João Pessoa, 50 — Pedra Branca", "city": "Palhoça", "state": "SC",
    },
    {
        "title": "Kitnet para alugar em Palhoça",
        "description": "Kitnet mobiliada, próxima ao centro e ao Terminal de Ônibus.",
        "property_type": "apartment", "listing_type": "rent",
        "price": 1_400, "area_m2": 25, "bedrooms": 1, "bathrooms": 1, "parking_spots": 0,
        "latitude": -27.6455, "longitude": -48.6617,
        "address_line": "R. Prefeito Acácio Garibaldi São Thiago, 120 — Centro", "city": "Palhoça", "state": "SC",
    },
    {
        "title": "Sobrado 3 suítes em São José",
        "description": "Sobrado reformado em condomínio fechado, churrasqueira, piscina e 3 vagas.",
        "property_type": "house", "listing_type": "sale",
        "price": 780_000, "area_m2": 210, "bedrooms": 3, "bathrooms": 3, "parking_spots": 3,
        "latitude": -27.6136, "longitude": -48.6345,
        "address_line": "R. Frei Eusébio, 400 — Kobrasol", "city": "São José", "state": "SC",
    },
    {
        "title": "Apartamento garden em São José",
        "description": "Apto térreo com garden de 60m², próximo ao centro de São José.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 490_000, "area_m2": 82, "bedrooms": 2, "bathrooms": 2, "parking_spots": 1,
        "latitude": -27.5998, "longitude": -48.6231,
        "address_line": "Av. Presidente Kennedy, 1500 — Campinas", "city": "São José", "state": "SC",
    },
    {
        "title": "Casa à venda em Biguaçu",
        "description": "Casa espaçosa com amplo terreno, ideal para família, próximo à BR-101.",
        "property_type": "house", "listing_type": "sale",
        "price": 310_000, "area_m2": 160, "bedrooms": 3, "bathrooms": 2, "parking_spots": 2,
        "latitude": -27.4934, "longitude": -48.6561,
        "address_line": "R. Cel. Teixeira Oliveira, 200 — Centro", "city": "Biguaçu", "state": "SC",
    },

    # ── São Paulo — Jardins / Itaim / Moema ────────────────────────────────────
    {
        "title": "Apartamento moderno nos Jardins",
        "description": "Apartamento alto padrão com varanda gourmet, vista para a cidade e acabamento premium.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 1_850_000, "area_m2": 120, "bedrooms": 3, "bathrooms": 2, "parking_spots": 2,
        "latitude": -23.5659, "longitude": -46.6567,
        "address_line": "R. Oscar Freire, 1250 — Jardins", "city": "São Paulo", "state": "SP",
    },
    {
        "title": "Cobertura duplex no Itaim Bibi",
        "description": "Cobertura com piscina privativa, terraço gourmet e vista panorâmica do skyline paulistano.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 4_200_000, "area_m2": 280, "bedrooms": 4, "bathrooms": 4, "parking_spots": 3,
        "latitude": -23.5832, "longitude": -46.6777,
        "address_line": "Av. Brigadeiro Faria Lima, 3500 — Itaim Bibi", "city": "São Paulo", "state": "SP",
    },
    {
        "title": "Mansão em condomínio no Morumbi",
        "description": "Residência de luxo em condomínio fechado, com jardim, piscina aquecida, quadra de tênis e segurança 24h.",
        "property_type": "house", "listing_type": "sale",
        "price": 12_500_000, "area_m2": 850, "bedrooms": 6, "bathrooms": 7, "parking_spots": 6,
        "latitude": -23.6044, "longitude": -46.7258,
        "address_line": "Rua Dummont, 50 — Morumbi", "city": "São Paulo", "state": "SP",
    },
    {
        "title": "Studio em Pinheiros",
        "description": "Studio reformado, mobiliado, excelente localização a 500m do metrô Fradique Coutinho.",
        "property_type": "apartment", "listing_type": "rent",
        "price": 3_200, "area_m2": 38, "bedrooms": 1, "bathrooms": 1, "parking_spots": 0,
        "latitude": -23.5636, "longitude": -46.6939,
        "address_line": "R. dos Pinheiros, 820 — Pinheiros", "city": "São Paulo", "state": "SP",
    },
    {
        "title": "Casa com quintal em Vila Madalena",
        "description": "Casa charmosa com quintal, área de churrasco, 2 vagas cobertas e garden privativo.",
        "property_type": "house", "listing_type": "rent",
        "price": 8_500, "area_m2": 180, "bedrooms": 3, "bathrooms": 2, "parking_spots": 2,
        "latitude": -23.5569, "longitude": -46.6906,
        "address_line": "R. Aspicuelta, 430 — Vila Madalena", "city": "São Paulo", "state": "SP",
    },
    {
        "title": "Apartamento 2 quartos em Moema",
        "description": "Apartamento reformado com varanda, 2 quartos sendo 1 suíte, lazer completo no condomínio.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 980_000, "area_m2": 85, "bedrooms": 2, "bathrooms": 2, "parking_spots": 1,
        "latitude": -23.5989, "longitude": -46.6647,
        "address_line": "Av. Ibirapuera, 2800 — Moema", "city": "São Paulo", "state": "SP",
    },
    {
        "title": "Cobertura triplex no Brooklin",
        "description": "Cobertura de 3 andares com rooftop, piscina privativa e vista para o WTC.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 6_800_000, "area_m2": 420, "bedrooms": 5, "bathrooms": 5, "parking_spots": 4,
        "latitude": -23.6108, "longitude": -46.6952,
        "address_line": "Av. das Nações Unidas, 11900 — Brooklin", "city": "São Paulo", "state": "SP",
    },

    # ── Rio de Janeiro ──────────────────────────────────────────────────────────
    {
        "title": "Apartamento frente mar em Ipanema",
        "description": "Vista frontal para o mar, varanda com pôr do sol para o Arpoador, alto padrão.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 5_400_000, "area_m2": 160, "bedrooms": 3, "bathrooms": 3, "parking_spots": 2,
        "latitude": -22.9849, "longitude": -43.1989,
        "address_line": "Av. Vieira Souto, 180 — Ipanema", "city": "Rio de Janeiro", "state": "RJ",
    },
    {
        "title": "Cobertura em Leblon",
        "description": "Cobertura com piscina aquecida, churrasqueira e vista para as Duas Irmãs. Topo de linha.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 9_900_000, "area_m2": 350, "bedrooms": 4, "bathrooms": 4, "parking_spots": 3,
        "latitude": -22.9840, "longitude": -43.2228,
        "address_line": "R. Dias Ferreira, 417 — Leblon", "city": "Rio de Janeiro", "state": "RJ",
    },
    {
        "title": "Mansão em Santa Teresa",
        "description": "Villa histórica reformada com jardim tropical, piscina, ateliê e vista panorâmica para a Baía de Guanabara.",
        "property_type": "house", "listing_type": "sale",
        "price": 7_200_000, "area_m2": 600, "bedrooms": 5, "bathrooms": 5, "parking_spots": 4,
        "latitude": -22.9219, "longitude": -43.1783,
        "address_line": "R. Almirante Alexandrino, 1500 — Santa Teresa", "city": "Rio de Janeiro", "state": "RJ",
    },
    {
        "title": "Kitnet em Copacabana",
        "description": "Kitnet a 2 quadras da praia, totalmente mobiliada, ideal para investimento.",
        "property_type": "apartment", "listing_type": "rent",
        "price": 2_800, "area_m2": 28, "bedrooms": 1, "bathrooms": 1, "parking_spots": 0,
        "latitude": -22.9705, "longitude": -43.1870,
        "address_line": "R. Figueiredo Magalhães, 350 — Copacabana", "city": "Rio de Janeiro", "state": "RJ",
    },

    # ── Florianópolis ───────────────────────────────────────────────────────────
    {
        "title": "Casa à beira-mar em Jurerê Internacional",
        "description": "Casa de alto padrão em condomínio exclusivo, piscina, jardim paisagístico e acesso à praia.",
        "property_type": "house", "listing_type": "sale",
        "price": 8_500_000, "area_m2": 520, "bedrooms": 5, "bathrooms": 5, "parking_spots": 4,
        "latitude": -27.4394, "longitude": -48.4894,
        "address_line": "Alameda Borges de Medeiros, 100 — Jurerê Internacional", "city": "Florianópolis", "state": "SC",
    },
    {
        "title": "Apartamento 3 suítes no Centro",
        "description": "Apartamento reformado, sala ampla, varanda e lazer completo no prédio.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 750_000, "area_m2": 90, "bedrooms": 3, "bathrooms": 2, "parking_spots": 1,
        "latitude": -27.5969, "longitude": -48.5495,
        "address_line": "R. Felipe Schmidt, 680 — Centro", "city": "Florianópolis", "state": "SC",
    },
    {
        "title": "Mansão com vista para o mar em Lagoa da Conceição",
        "description": "Propriedade única com vista 360°, piscina infinity, spa, adega e heliponto.",
        "property_type": "house", "listing_type": "sale",
        "price": 18_000_000, "area_m2": 1200, "bedrooms": 7, "bathrooms": 8, "parking_spots": 8,
        "latitude": -27.5988, "longitude": -48.4648,
        "address_line": "Servidão das Gangorras, 80 — Lagoa da Conceição", "city": "Florianópolis", "state": "SC",
    },
    {
        "title": "Studio mobiliado em Trindade",
        "description": "Studio próximo à UFSC, totalmente mobiliado, ideal para estudantes ou profissionais.",
        "property_type": "apartment", "listing_type": "rent",
        "price": 2_200, "area_m2": 32, "bedrooms": 1, "bathrooms": 1, "parking_spots": 0,
        "latitude": -27.5989, "longitude": -48.5218,
        "address_line": "R. Lauro Linhares, 900 — Trindade", "city": "Florianópolis", "state": "SC",
    },
    {
        "title": "Casa familiar em Coqueiros",
        "description": "Casa em bairro residencial tranquilo, quintal grande, área de lazer e 3 vagas.",
        "property_type": "house", "listing_type": "rent",
        "price": 5_800, "area_m2": 200, "bedrooms": 4, "bathrooms": 3, "parking_spots": 3,
        "latitude": -27.5744, "longitude": -48.5576,
        "address_line": "R. João Pio Duarte, 200 — Coqueiros", "city": "Florianópolis", "state": "SC",
    },
    {
        "title": "Cobertura no Campeche",
        "description": "Cobertura com terraço privativo, vista para o oceano e acabamento de alto padrão.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 1_650_000, "area_m2": 140, "bedrooms": 3, "bathrooms": 3, "parking_spots": 2,
        "latitude": -27.6881, "longitude": -48.4885,
        "address_line": "Av. Campeche, 1500 — Campeche", "city": "Florianópolis", "state": "SC",
    },
    {
        "title": "Apartamento garden no Bairro Jardim Atlântico",
        "description": "Apto térreo com garden privativo de 80m², churrasqueira e 2 vagas.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 620_000, "area_m2": 78, "bedrooms": 2, "bathrooms": 2, "parking_spots": 2,
        "latitude": -27.5720, "longitude": -48.5048,
        "address_line": "R. Desembargador Vitor Lima, 560 — Pantanal", "city": "Florianópolis", "state": "SC",
    },

    # ── Belo Horizonte ─────────────────────────────────────────────────────────
    {
        "title": "Mansão no Belvedere",
        "description": "Mansão com 6 suítes, piscina aquecida, cinema, sauna e quadra poliesportiva em condomínio fechado.",
        "property_type": "house", "listing_type": "sale",
        "price": 9_500_000, "area_m2": 780, "bedrooms": 6, "bathrooms": 7, "parking_spots": 6,
        "latitude": -19.9526, "longitude": -43.9366,
        "address_line": "R. Professor Otávio Coelho de Magalhães, 200 — Belvedere", "city": "Belo Horizonte", "state": "MG",
    },
    {
        "title": "Apartamento 3 quartos no Savassi",
        "description": "Apartamento reformado no coração do Savassi, a 300m do parque e próximo a restaurantes.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 890_000, "area_m2": 95, "bedrooms": 3, "bathrooms": 2, "parking_spots": 2,
        "latitude": -19.9370, "longitude": -43.9384,
        "address_line": "R. Pernambuco, 800 — Savassi", "city": "Belo Horizonte", "state": "MG",
    },
    {
        "title": "Cobertura no Lourdes",
        "description": "Cobertura com piscina privativa, varanda gourmet e vista para a Serra do Curral.",
        "property_type": "apartment", "listing_type": "sale",
        "price": 3_200_000, "area_m2": 240, "bedrooms": 4, "bathrooms": 4, "parking_spots": 3,
        "latitude": -19.9401, "longitude": -43.9302,
        "address_line": "Av. Getúlio Vargas, 1500 — Lourdes", "city": "Belo Horizonte", "state": "MG",
    },
    {
        "title": "Flat mobiliado no Funcionários",
        "description": "Flat completo com serviços de hotel, academia, piscina e restaurante. Ideal para executivos.",
        "property_type": "apartment", "listing_type": "rent",
        "price": 4_500, "area_m2": 55, "bedrooms": 1, "bathrooms": 1, "parking_spots": 1,
        "latitude": -19.9432, "longitude": -43.9273,
        "address_line": "R. Maranhão, 670 — Funcionários", "city": "Belo Horizonte", "state": "MG",
    },
]


class Command(BaseCommand):
    help = "Cria imóveis mock para desenvolvimento. Controlado pela variável SEED_MOCK_DATA."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Remove todos os imóveis mock antes de criar novos.",
        )

    def _ensure_sample_images(self) -> list[str]:
        """
        Baixa as imagens de exemplo uma única vez e devolve os paths no storage.
        Como todos os mocks compartilham o mesmo conjunto, evitamos N×5 uploads
        no MinIO — gravamos só 5 arquivos e cada PropertyImage referencia o path.
        """
        paths: list[str] = []
        for i, url in enumerate(SAMPLE_IMAGE_URLS):
            path = f"properties/samples/sample_{i}.jpg"
            if not default_storage.exists(path):
                try:
                    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urlopen(req, timeout=15) as resp:
                        default_storage.save(path, ContentFile(resp.read()))
                    self.stdout.write(self.style.SUCCESS(f"  ↓ baixou {path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  ✗ falhou {url}: {e}"))
                    continue
            paths.append(path)
        return paths

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Property.objects.filter(title__startswith=MOCK_MARKER).delete()
            self.stdout.write(self.style.WARNING(f"Removidos {deleted} imóveis mock."))

        # Idempotente: não duplica se já existir
        existing = Property.objects.filter(title__startswith=MOCK_MARKER).count()
        if existing > 0 and not options["clear"]:
            self.stdout.write(self.style.NOTICE(
                f"Mock data já existe ({existing} imóveis). Use --clear para recriar."
            ))
            return

        self.stdout.write("Preparando imagens de exemplo no MinIO…")
        sample_paths = self._ensure_sample_images()
        if not sample_paths:
            self.stdout.write(self.style.WARNING(
                "Nenhuma imagem de exemplo disponível — mocks serão criados sem fotos."
            ))

        created = 0
        for data in MOCK_PROPERTIES:
            prop = Property.objects.create(
                title=f"{MOCK_MARKER} {data['title']}",
                description=data["description"],
                property_type=data["property_type"],
                listing_type=data["listing_type"],
                price=data["price"],
                area_m2=data["area_m2"],
                bedrooms=data["bedrooms"],
                bathrooms=data["bathrooms"],
                parking_spots=data["parking_spots"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                address_line=data["address_line"],
                city=data["city"],
                state=data["state"],
                is_active=True,
            )

            for i, path in enumerate(sample_paths):
                PropertyImage.objects.create(
                    property=prop,
                    image=path,
                    is_cover=(i == 0),
                    order=i,
                )

            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"✓ {created} imóveis mock criados com {len(sample_paths)} fotos cada."
        ))
