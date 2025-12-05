"""
Configuración de la base de datos
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# -------------------------
# Clase base para modelos SQLAlchemy
# -------------------------
class Base(DeclarativeBase):
    pass

# -------------------------
# Motor de conexión a la base de datos
# -------------------------
engine = create_engine(
    "sqlite:///videogames.db",
    echo=True,
    connect_args={"check_same_thread": False}
)

# -------------------------
# Fábrica de sesiones
# -------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=True,
    expire_on_commit=False
)

# -------------------------
# Dependencia para FastAPI
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# Inicialización de la base de datos
# -------------------------
def init_db():
    # Importar modelos aquí dentro para evitar circular imports
    from app.models.genre import GenreORM
    from app.models.videogame import VideogameORM
    from app.models.developer import DevORM
    from app.models.user import UserORM
    from app.models.review import ReviewORM

    # Crear todas las tablas
    Base.metadata.create_all(engine)

    db = SessionLocal()
    try:
        # Si ya hay géneros, asumimos que la DB ya tiene datos
        if db.query(GenreORM).first():
            return

        # -------------------------
        # Crear géneros de ejemplo
        # -------------------------
        action = GenreORM(name="Acción", description="Se centran en la destreza física y la reacción rápida del jugador, como juegos de lucha o plataformas.", image_url="/static/genre/action.png")
        adventure = GenreORM(name="Aventura", description="Se enfocan en la exploración, la resolución de acertijos y una narrativa", image_url="/static/genre/adventure.png")
        rpg = GenreORM(name="RPG", description="El jugador controla un personaje que evoluciona y mejora a lo largo de la historia, ya sea por niveles o habilidades.", image_url="/static/genre/rpg.png")
        strategy = GenreORM(name="Estrategia", description="Requieren planificación y pensamiento táctico para superar a los oponentes, ya sea en tiempo real (RTS) o por turnos.", image_url="/static/genre/strategy.png")
        simulation = GenreORM(name="Simulación", description="Buscan recrear una actividad del mundo real, desde pilotar aviones hasta gestionar una ciudad o una vida.", image_url="/static/genre/simulation.png")
        sport = GenreORM(name="Deportes", description="Simulan deportes reales como fútbol o tenis.", image_url="/static/genre/sport.png")
        arcade = GenreORM(name="Arcade", description="Juegos de acción y habilidad de ritmo rápido, a menudo con objetivos simples como superar niveles.", image_url="/static/genre/arcade.png")
        sandbox = GenreORM(name="Sandbox", description="Ofrecen un mundo abierto donde el jugador tiene gran libertad para explorar y crear.", image_url="/static/genre/sandbox.png")
        puzzle = GenreORM(name="Puzzle", description="Se centran en la resolución de acertijos lógicos y rompecabezas. ", image_url="/static/genre/puzzle.png")
        shooters = GenreORM(name="Shooter", description="Incluyen los First-Person Shooter (FPS) y Third-Person Shooter (TPS), donde se usan armas de fuego.", image_url="/static/genre/shooter.png")
        indie = GenreORM(name="Indie", description="Los videojuegos 'indie' son aquellos creados por individuos o pequeños equipos de desarrollo, sin el apoyo financiero ni la supervisión de un gran distribuidor o editor (publisher) de videojuegos comercial establecido.", image_url="/static/genre/indie.png")
        db.add_all([action, adventure, rpg, strategy, simulation, sport, arcade, sandbox, puzzle, shooters, indie])
        db.commit()

        # -------------------------
        # Crear developers de ejemplo
        # -------------------------
        dev1 = DevORM(name="Dev Studio 1")
        dev2 = DevORM(name="Dev Studio 2")
        dev3 = DevORM(name="Dev Studio 3")
        db.add_all([dev1, dev2, dev3])
        db.commit()

        # -------------------------
        # Crear videojuegos de ejemplo
        # -------------------------
        default_videogames =[
            VideogameORM(title="Doom Eternal", description="Shooter en primera persona frenético donde encarnas al Doom Slayer. Combina velocidad, armas devastadoras y combates contra hordas de demonios, con un diseño de niveles vertical y dinámico que exige reflejos y estrategia..", cover_url="https://files.gamesfull.app/uploads/image/2020/06/doom-eternal-12757-poster.jpg", genre_id=1),
            VideogameORM(title="Devil May Cry 5", description="Es un juego de acción tipo hack & slash: controlas personajes como Nero, Dante o “V”, cada uno con su estilo, para enfrentarte a hordas de demonios.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/devil-may-cry-5-deluxe-edition-9589-poster.jpg", genre_id=1 ),
            VideogameORM(title="Sekiro: Shadows Die Twice", description="Acción táctica y desafiante ambientada en Japón feudal. El juego combina sigilo, exploración vertical y duelos de espada precisos, con un sistema de muerte y resurrección que permite afrontar los combates de manera estratégica.", cover_url="/static/videogames/", genre_id=1 ),
            VideogameORM(title="Bayonetta", description="Hack & slash extravagante con ritmo vertiginoso y estilo visual único. Juegas como la bruja Bayonetta, usando armas, magia y combos aéreos para derrotar hordas de ángeles y enemigos sobrenaturales en escenarios espectaculares.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/bayonetta-digital-deluxe-edition-3675-poster.jpg", genre_id=1 ),
            
            VideogameORM(title="Uncharted 4 Legacy of Thieves Collection", description="Aventura cinematográfica con énfasis en narrativa, exploración y resolución de puzzles. Sigues a Nathan Drake en una épica búsqueda de tesoros, mezclando tiroteos, parkour y entornos detallados que cuentan su historia de manera inmersiva.", cover_url="https://files.gamesfull.app/uploads/image/2022/10/Uncharted-4-Legacy-of-Thieves-Collection.jpg", genre_id=2 ),
            VideogameORM(title="Shadow of the Tomb Raider Croft Edition", description="Vive el momento más crucial de la vida de Lara Croft, en el que se convierte en saqueadora de tumbas. En Shadow of the Tomb Raider, Lara debe dominar una selva mortal, superar tumbas aterradoras y perseverar en su hora más aciaga. Mientras trata de detener un apocalipsis maya, Lara terminará por convertirse en la saqueadora de tumbas que está destinada a", cover_url="https://files.gamesfull.app/uploads/image/2020/05/shadow-of-the-tomb-raider-digital-deluxe-edition-8477-poster.jpg", genre_id=2 ),
            VideogameORM(title="Subnautica", description="Juego de aventura y supervivencia en un planeta oceánico alienígena. Exploras profundidades submarinas llenas de criaturas exóticas, recolectas recursos para construir bases y sobrevives a un ecosistema peligroso mientras descubres la historia del planeta.", cover_url="https://files.gamesfull.app/uploads/image/2020/06/subnautica-2272-poster.jpg", genre_id=2),
            VideogameORM(title="The Last of Us Part I Deluxe Edition", description="En The Last of Us Part I Deluxe Edition la civilización devastada donde se enfrentan infectados e insensibilizados sobrevivientes, alguien contrata a Joel, el cansado protagonista, para que escabulla en secreto a Ellie, de 14 años, fuera de una zona militar de cuarentena. Sin embargo, lo que comienza como un pequeño trabajo, se convierte en un viaje brutal a través del país.", cover_url="https://files.gamesfull.app/uploads/image/2023/03/The-Last-of-Us-Part-I-Deluxe-Edition-1.jpg", genre_id=2 ),
            
            VideogameORM(title="The Witcher 3: Wild Hunt", description="RPG de mundo abierto con una historia rica y ramificada. Interpretas a Geralt de Rivia, cazador de monstruos, enfrentando decisiones morales complejas mientras exploras un continente lleno de personajes, misiones secundarias y combates tácticos con espadas y magia.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/the-witcher-3-wild-hunt-goty-2923-poster.jpg", genre_id=3 ),
            VideogameORM(title="The Elder Scrolls V Skyrim Enderal Forgotten Stories", description="The Elder Scrolls V Skyrim Enderal Forgotten Stories ElAmigos por googledrive – Enderal: Forgotten Stories ElAmigos es una conversión total para TES V: Skyrim: una modificación del juego que se desarrolla en su propio mundo con su propio paisaje e historia. Ofrece un mundo abierto inmersivo, todo para que el jugador lo explore, revise los sistemas de habilidades y las mecánicas del juego y una historia oscura y psicológica con personajes", cover_url="https://files.gamesfull.app/uploads/image/2020/05/enderal-forgotten-stories-9327-poster.jpg", genre_id=3 ),
            VideogameORM(title="Dragon Age Inquisition", description="RPG táctico con narrativa profunda y decisiones que afectan a tu mundo. Gestionas a un grupo de héroes mientras lideras la Inquisición para detener una amenaza que podría destruir el reino, combinando exploración, diplomacia y combates estratégicos.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/dragon-age-inquisition-game-of-the-year-edition-2437-poster.jpg", genre_id=3 ),
            VideogameORM(title="Persona 5", description="RPG japonés que mezcla la vida cotidiana con combates por turnos en mundos alternativos. Controlas a un grupo de estudiantes con habilidades sobrenaturales mientras desarrollas relaciones, gestionas tiempo y tomas decisiones que impactan la historia y los finales posibles.", cover_url="https://files.gamesfull.app/uploads/image/2021/02/persona-5-strikers-deluxe-edition.jpg", genre_id=3 ),
            
            VideogameORM(title="StarCraft II", description="Estrategia en tiempo real con tres razas únicas (Terran, Protoss y Zerg). Gestionas recursos, construyes bases y despliegas unidades en combates tácticos competitivos con alta demanda de reflejos y planificación estratégica.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/starcraft-ii-the-complete-collection-4459-poster.jpg", genre_id=4 ),
            VideogameORM(title="Civilization VI", description="Estrategia por turnos donde construyes y gestionas un imperio desde la antigüedad hasta la era moderna. Exploras, desarrollas tecnologías, negocias diplomáticamente y enfrentas a otras civilizaciones para alcanzar la victoria mediante guerra, cultura o ciencia.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/sid-meiers-civilization-vi-digital-deluxe-2699-poster.jpg", genre_id=4 ),
            VideogameORM(title="Age of Empires IV", description="Estrategia histórica en tiempo real donde controlas civilizaciones medievales. Gestionas recursos, construyes ejércitos y participas en campañas épicas, combinando tácticas de combate y planificación económica.", cover_url="https://files.gamesfull.app/uploads/image/2025/04/Age-of-Empires-IV-Anniversary-Edition.jpg", genre_id=4 ),
            VideogameORM(title="XCOM 2", description="Estrategia táctica por turnos con soldados personalizables y combates desafiantes. Lideras a la resistencia contra una ocupación alienígena, tomando decisiones críticas que afectan la moral y supervivencia de tu escuadrón.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/xcom-2-digital-deluxe-edition-2238-poster.jpg", genre_id=4 ),
            
            VideogameORM(title="The Sims 4", description="Simulación de vida donde creas personajes, construyes hogares y gestionas relaciones, carreras y aspiraciones. Cada elección afecta la personalidad y la vida de los Sims, ofreciendo infinitas posibilidades de narrativa emergente.", cover_url="https://files.gamesfull.app/uploads/image/2020/06/the-sims-4-digital-deluxe-edition-2806-poster.jpg", genre_id=5 ),
            VideogameORM(title="Microsoft Flight Simulator", description="Simulador de vuelo ultra realista que recrea el mundo completo con satélites y mapas en tiempo real. Pilotas aviones de distintos tipos, enfrentando condiciones climáticas reales y trayectos detallados.", cover_url="https://files.gamesfull.app/uploads/image/2020/08/Microsoft-Flight-Simulator-2020-Deluxe-Edition.jpg", genre_id=5 ),
            VideogameORM(title="Cities: Skylines", description="Simulación urbana donde diseñas y gestionas una ciudad completa. Administras recursos, tráfico, servicios y políticas, mientras equilibras crecimiento, economía y felicidad de los ciudadanos.", cover_url="https://files.gamesfull.app/uploads/image/2020/06/cities-skylines-deluxe-edition-2158-poster.jpg", genre_id=5 ),
            VideogameORM(title="Farming Simulator 25", description="Simulación agrícola detallada donde cultivas, crías animales y gestionas maquinaria. Incluye estaciones, mercados y contratos, ofreciendo una experiencia completa de granja moderna.", cover_url="https://files.gamesfull.app/uploads/image/2024/11/Farming-Simulator-25.jpg", genre_id=5 ),
            
            VideogameORM(title="FIFA 23", description="Simulación de fútbol con licencias de equipos reales, ligas y competiciones. Permite modos de juego en solitario, multijugador online y gestión de clubes, con física y tácticas muy realistas.", cover_url="https://files.gamesfull.app/uploads/image/2023/08/FIFA-23.jpg", genre_id=6 ),
            VideogameORM(title="NBA 2K21", description="Baloncesto realista que combina jugabilidad, gestión de franquicias y modos carrera. Incluye gráficos detallados, movimientos auténticos de jugadores y narrativa deportiva.", cover_url="https://files.gamesfull.app/uploads/image/2020/09/NBA-2K21.jpg", genre_id=6 ),
            VideogameORM(title="Tony Hawks Pro Skater 3 plus 4", description="Skateboarding arcade con trucos combinables y niveles clásicos remasterizados. Es un juego de ritmo y precisión, ideal para lograr combos y explorar mapas llenos de", cover_url="https://files.gamesfull.app/uploads/image/2025/07/tony-hawks-pro-skater-3-plus-4-deluxe-edition-1752015958924.jpg", genre_id=6 ),
            VideogameORM(title="Madden NFL 20", description="Fútbol americano con control total de jugadores, estrategias de equipo y ligas completas. Combina simulación de partidos con gestión táctica y creación de franquicias.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/madden-nfl-20-11387-poster.jpg", genre_id=6 ),
            
            VideogameORM(title="Pac-Man Championship Edition DX", description="Modernización del clásico Pac-Man con laberintos dinámicos, velocidad creciente y efectos visuales llamativos que amplifican la experiencia arcade.", cover_url="/static/videogames/", genre_id=7 ),
            VideogameORM(title="Cuphead", description="Shooter-runner con estética de dibujos animados de los años 30. Combates exigentes contra jefes, patrones complejos y animaciones dibujadas a mano hacen de cada nivel un reto artístico y", cover_url="https://files.gamesfull.app/uploads/image/2020/05/cuphead-deluxe-edition-2133-poster.jpg", genre_id=7 ),
            VideogameORM(title="Geometry Wars 3", description="Shooter arcade con acción frenética en gráficos neón. Controlas una nave contra hordas de enemigos mientras buscas sobrevivir el mayor tiempo posible y acumular puntuación.", cover_url="/static/videogames/", genre_id=7 ),
            VideogameORM(title="Super Meat Boy", description="Plataformas rápidas y desafiantes donde cada salto debe ser preciso. Los niveles cortos, con obstáculos mortales, hacen que la habilidad y la repetición sean la clave del éxito.", cover_url="https://files.gamesfull.app/uploads/image/2021/01/Super-Meat-Boy-Forever.jpg", genre_id=7 ),
            
            VideogameORM(title="Minecraft Dungeons", description=" ¡Ábrete camino en un juego de acción y aventura completamente nuevo inspirado en los clásicos juegos de mazmorras y ambientado en el universo de Minecraft! Pueden jugar juntos hasta cuatro amigos o también puedes aventurarte en las mazmorras en solitario. ¡Combate a nuevas y desagradables hordas en niveles increíblemente variados repletos de acción y llenos de tesoros.", cover_url="https://files.gamesfull.app/uploads/image/2021/01/Minecraft-Dungeons.jpg", genre_id=8 ),
            VideogameORM(title="Terraria", description="Aventura 2D con crafting, combate, minería y exploración. Enfrentas jefes, descubres biomas y construyes estructuras complejas con libertad creativa.", cover_url="https://data.xxlgamer.com/products/2762/o2hv7ukmhGY7SB-medium.jpg", genre_id=8 ),
            VideogameORM(title="Grand Theft Auto V", description="Mundo abierto donde alternas entre tres protagonistas en Los Santos. Combina misiones narrativas, conducción, acción y libertad total para explorar, robar y crear caos urbano.", cover_url="https://files.gamesfull.app/uploads/image/2020/06/grand-theft-auto-v-1006-poster.jpg", genre_id=8 ),
            VideogameORM(title="Red Dead Redemption 2", description="Plataforma social de juegos y creación, donde jugadores diseñan experiencias propias y participan en mundos creados por otros, con infinitas posibilidades de diversión y colaboración.", cover_url="https://files.gamesfull.app/uploads/image/2020/10/Red-Dead-Redemption-2.jpg", genre_id=8 ),
            
            VideogameORM(title="Portal 2", description="Combina resolución de puzzles y narrativa humorística. Usas un dispositivo de portales para atravesar cámaras de prueba, resolviendo desafíos lógicos y explorando una historia con inteligencia artificial sarcástica.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/portal-2-complete-3774-poster.jpg", genre_id=10 ),
            VideogameORM(title="The Witness", description="Juego de exploración en mundo abierto centrado en puzzles lógicos. Cada enigma se integra con el entorno, incentivando observación, reflexión y patrones de pensamiento creativo.", cover_url="https://data.xxlgamer.com/products/3681/HFzSnpOY9UIWX9-medium.jpg", genre_id=10 ),
            VideogameORM(title="Tetris Effect", description="Clásico Tetris con música y visuales envolventes. Cada movimiento se sincroniza con efectos de sonido y luz, creando una experiencia meditativa y adictiva.", cover_url="https://files.gamesfull.app/uploads/image/2020/06/tetris-effect-12355-poster.jpg", genre_id=10 ),
            VideogameORM(title="Escape Simulator 2", description="Escape Simulator 2 es un juego de simulación y aventura en primera persona donde debes escapar de habitaciones resolviendo acertijos y rompecabezas. La historia se desarrolla en diferentes entornos y escenarios, como mazmorras, naves espaciales y otros lugares misteriosos, donde debes usar tu lógica y habilidades para encontrar la salida.", cover_url="https://files.gamesfull.app/uploads/image/2025/10/escape-simulator-2-1761605598554.jpg", genre_id=10 ),

            VideogameORM(title="Call of Duty: Modern Warfare II", description="Shooter en primera persona con campañas cinematográficas y multijugador competitivo. Combina acción intensa, narrativa realista y modos cooperativos.", cover_url="https://data.xxlgamer.com/products/1428/CeiOxjPwMuQLl0-medium.jpg", genre_id=11 ),
            VideogameORM(title="Overwatch", description="Shooter por equipos con héroes únicos y habilidades estratégicas. Cada personaje aporta estilo de juego distinto, fomentando la cooperación y la planificación táctica.", cover_url="https://data.xxlgamer.com/products/3467/38XaoUR9SvWQtY-medium.jpg", genre_id=11 ),
            VideogameORM(title="Valorant", description="ArmA III es la tercera parte de la saga de acción bélica de Bohemia Interactive, “heredera” de Operation Flashpoint, y que ha permitido sobre su base mods como DayZ. Esta tercera parte sigue la filosofía de “siempre en construcción”, y en un primer momento solo se ha lanzado con su modo cooperativo y multijugador.", cover_url="https://files.gamesfull.app/uploads/image/2020/06/arma-3-complete-campaign-edition-988-poster.jpg", genre_id=11 ),
            VideogameORM(title="Halo 2", description="Halo 2 es un videojuego de disparos en primera persona desarrollado por Bungie Studios y lanzado para la consola Xbox el 9 de noviembre de 2004.4 Es la segunda entrega en la franquicia de Halo así como la continuación del exitoso Halo: Combat Evolved. Los acontecimientos de Halo 2 se sitúan en el siglo XXVI, donde los seres humanos bajo los auspicios del Comando Espacial de Naciones Unidas", cover_url="https://files.gamesfull.app/uploads/image/2020/05/halo-2-6887-poster.jpg", genre_id=11 ),

            VideogameORM(title="Hades", description="Roguelike con narrativa profunda, combate rápido y personajes carismáticos. Cada intento de escapar del inframundo combina estrategia, habilidades y diálogos dinámicos.", cover_url="https://files.gamesfull.app/uploads/image/2020/09/Hades-Battle-out-of-Hell.jpg", genre_id=12 ),
            VideogameORM(title="Hollow Knight", description="Metroidvania con mundo oscuro, plataformas precisas y combates desafiantes. Exploras Hallownest, desbloqueas habilidades y descubres secretos mientras enfrentas enemigos únicos.", cover_url="https://files.gamesfull.app/uploads/image/2020/05/hollow-knight-5055-poster.jpg", genre_id=12 ),
            VideogameORM(title="Little Nightmares Enhanced Edition", description="¡Sumérgete en la enigmática atmósfera de Little Nightmares y enfréntate a los miedos de tu infancia! Ayuda a Seis a escapar de Las Fauces, un misterioso navío donde moran ánimas corrompidas en busca de su próxima comida... Explora la casita de muñecas más perturbadora que jamás hayas visto: escapa de su prisión y diviértete en su patio de recreo.", cover_url="https://files.gamesfull.app/uploads/image/2025/10/little-nightmares-enhanced-edition-1760068160017.jpg", genre_id=12 ),
            VideogameORM(title="Stardew Valley", description="Simulación relajante de granja con agricultura, minería y relaciones sociales. Construyes tu comunidad, mejoras tu granja y participas en festivales y actividades del pueblo.", cover_url="https://files.gamesfull.app/uploads/image/2020/06/stardew-valley-collectors-edition-4995-poster.jpg", genre_id=12 ),
        ]
        db.add_all(default_videogames)
        db.commit()



        # -------------------------
        # Crear videojuegos de ejemplo
        # -------------------------
        vg1 = VideogameORM(title="Super Action Game", description="Juego de acción épico", genre_id=action.id, developer_id=dev1.id)
        vg2 = VideogameORM(title="Adventure Quest", description="Explora mundos fantásticos", genre_id=adventure.id, developer_id=dev2.id)
        vg3 = VideogameORM(title="RPG Legends", description="RPG clásico con héroes y mazmorras", genre_id=rpg.id, developer_id=dev3.id)
        db.add_all([vg1, vg2, vg3])
        db.commit()


        # -------------------------
        # Crear usuarios de ejemplo
        # -------------------------
        user1 = UserORM(nick="admin", email="admin@hotmail.es", nif="1231231231", password="admin1234")
        user2 = UserORM(nick="player1", email="player1@gmail.com", nif="111111111A", password="player1234")
        user3 = UserORM(nick="player2", email="player2@gmail.com", nif="222222222B", password="player2345")
        db.add_all([user1, user2, user3])
        db.commit()
        
        # -------------------------
        # Asignar videojuegos a los usuarios (bibliotecas)
        # -------------------------
        # user1.videogames.append(vg1)
        # user1.videogames.append(vg2)

        # user2.videogames.append(vg2)
        # user2.videogames.append(vg3)

        # user3.videogames.append(vg1)
        # user3.videogames.append(vg3)

        # db.commit()

        # -------------------------
        # Crear reviews de ejemplo
        # -------------------------
        review1 = ReviewORM(rating=8.6, comment="Muy divertido", user_id=user1.id, videogame_id=vg1.id)
        review2 = ReviewORM(rating=9.0, comment="Me encantó", user_id=user1.id, videogame_id=vg2.id)
        review3 = ReviewORM(rating=7.5, comment="Buen juego", user_id=user2.id, videogame_id=vg2.id)
        review4 = ReviewORM(rating=9.2, comment="Excelente RPG", user_id=user2.id, videogame_id=vg3.id)
        review5 = ReviewORM(rating=8.0, comment="Entretenido", user_id=user3.id, videogame_id=vg1.id)
        review6 = ReviewORM(rating=9.5, comment="Me fascinó", user_id=user3.id, videogame_id=vg3.id)

        db.add_all([review1, review2, review3, review4, review5, review6])
        db.commit()

    finally:
        db.close()
