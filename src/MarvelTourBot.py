import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8054957126:AAHSictwPVUx-TdtZHkxPjqJaFWpEZQ6fMM"  # Замените на ваш токен

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Данные с картинками
data = {
    "movies": {
    "avengers_endgame": {
        "title": "Мстители: Финал",
        "year": 2019,
        "description": "Оставшиеся герои пытаются исправить последствия щелчка Таноса. Фильм содержит путешествия во времени, возвращение погибших персонажей и эпическую битву против Таноса. Завершает 22-фильмовую Сагу Бесконечности, принося жертвы (Железный человек, Чёрная вдова) и устанавливая новый статус-кво. Содержит множество отсылок к предыдущим фильмам франшизы.",
        "image_url": "https://avatars.mds.yandex.net/i?id=e729dcf1495aa58ad91fc470f8937945_l-4338066-images-thumbs&n=13",
        "required_viewing": "Все фильмы Саги Бесконечности, особенно 'Мстители: Война бесконечности'"
    } ,
    "avengers_infwar": {
            "title": "Мстители: Война бесконечности",
            "year": 2018,
            "description": "Танос начинает охоту за Камнями Бесконечности, чтобы осуществить свой план уничтожения половины вселенной. Мстители и Стражи Галактики объединяются, но терпят поражение - Танос добивается цели. Фильм объединяет 18 предыдущих картин и заканчивается самым шокирующим клиффхэнгером в истории MCU. Особое внимание уделено развитию характера Таноса.",
        "image_url": "https://pic.uma.media/cwebp/pic/cardimage/5c/6e/5c6e9a3aec4385a86a1790295a9c9f9c.jpg?size=1920&quality=90",
        "required_viewing": "Практически все предыдущие фильмы MCU, особенно 'Стражи Галактики', 'Тор: Рагнарёк', 'Чёрная пантера'."
    } ,
    "spiderman": {
            "title": "Человек-паук: Нет пути домой",
            "year": 2021,
            "description": "После раскрытия личности Питера Паркера он обращается к Доктору Стрэнджу за помощью, но заклинание идёт не так, открывая мультивселенную. В результате появляются злодеи из предыдущих киновселенных Человека-паука. Фильм соединяет трилогии Сэма Рэйми, Марка Уэбба и MCU, давая ностальгические моменты и завершая некоторые арки. Также представляет концепцию мультивселенной для следующих фаз Marvel.",
        "image_url": "https://static.okko.tv/images/v4/de944446-e627-4a7c-9e35-29a5e5ab721a",
        "required_viewing": "Трилогию о Человеке-пауке от Marvel, 'Доктора Стрэнджа', для полного понимания - предыдущие фильмы о Человеке-пауке с Тоби Магуайром и Эндрю Гарфилдом."
    } ,
    "ironman": {
            "title": "Железный человек",
            "year": 2008,
            "description": "Фильм, с которого началась вселенная Marvel. Гениальный изобретатель и миллиардер Тони Старк попадает в плен к террористам и создаёт первый прототип бронированного костюма, чтобы спастись. Вернувшись домой, он совершенствует технологию и становится Железным человеком, одновременно раскрывая заговор внутри своей собственной компании. Фильм заложил основы MCU и представил Ника Фьюри в после-титровой сцене.",
        "image_url": "https://images.kinorium.com/movie/poster/290389/w1500_50294407.jpg",
        "required_viewing": "Это первый фильм кинематографической вселенной Marvel, можно начинать без подготовки."
    } ,
    "firstavenger": {
            "title": "Первый мститель",
            "year": 2011,
            "description": "Действие происходит во время Второй мировой войны. Худой и болезненный, но добросердечный Стив Роджерс получает шанс служить родине, участвуя в эксперименте по созданию суперсолдата. После превращения в Капитана Америку он противостоит нацистской организации ГИДРА и её лидеру Красному Черепу. Фильм сочетает военную драму с элементами фантастики и заканчивается замораживанием Роджерса во льдах.",
        "image_url": "https://i.pinimg.com/originals/f2/f3/dd/f2f3dd2595f1c26521fddd61ee9e82e0.jpg",
        "required_viewing": "Лучше посмотреть до 'Мстителей', но строгой необходимости нет."
    } ,
    "avengers": {
            "title": "Мстители",
            "year": 2012,
            "description": "Первая сборка легендарной команды под руководством Ника Фьюри. Локи с помощью Тессеракта открывает портал для армии Читаури, угрожая Нью-Йорку. Железный человек, Капитан Америка, Тор, Халк, Чёрная Вдова и Соколиный глаз объединяются, чтобы остановить вторжение. Фильм установил стандарт для кроссоверов супергероев и показал, как разные характеры могут работать вместе.",
        "image_url": "https://static.okko.tv/images/v4/47b53187-0dcd-4d48-9a1a-2747087150e2",
        "required_viewing": "'Железный человек 1-2', 'Тор', 'Невероятный Халк', 'Первый мститель'."
    } ,
    "guardians": {
            "title": "Стражи Галактики",
            "year": 2014,
            "description": "Космическая авантюра о группе неудачников, ставших неожиданными героями. Питер Квилл (Звёздный Лорд), Грут, Ракета, Гамора и Дракс объединяются, чтобы защитить Камень Бесконечности от фанатичного Ронана. Фильм расширил границы MCU за пределы Земли, представил коллекционера и показал важность Камней Бесконечности. Запоминающийся саундтрек стал визитной карточкой фильма.",
        "image_url": "http://smotreshka.server-img.lfstrm.tv/image/aHR0cHM6Ly9jbXMuc21vdHJlc2hrYS50di9hcmNoaXZlLWltZy9zdGF0aWMvbWVkaWEvMDUvNDkvMDU0OTBkYmRmMjQ2ZjhlN2M1Y2U4NTFmMTJmMmZiYWQuanBn",
        "required_viewing": "Можно смотреть отдельно, но лучше после 'Мстителей' для понимания контекста Камней."
    } ,
    "avengersaa": {
            "title": "Мстители: Эра Альтрона",
            "year": 2015,
            "description": "Мстители атакуют базу ГИДРЫ, где находят скипетр Локи. Тони Старк и Брюс Баннер используют содержащийся в нём ИИ для создания системы защиты Альтрон, которая выходит из-под контроля. Появляются новые герои: Вижн, Ртуть и Алая Ведьма. Фильм исследует тему искусственного интеллекта и содержит важные сюжетные точки для будущих фильмов.",
        "image_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/4716873/760eac99-e941-4bc1-b90b-7abd19b8c6aa/1920x",
        "required_viewing": "'Мстители', 'Железный человек 3','Первый мститель: Другая война'."
    } ,
    "steverog": {
            "title": "Капитан Америка: Противостояние",
            "year": 2018,
            "description": "Описание: После событий в Соковии мировые правительства требуют контроля над Мстителями. Это приводит к расколу: Тони Старк поддерживает Соковианские соглашения, а Стив Роджерс выступает против. Фильм представляет Чёрную Пантеру и нового Человека-паука, а также содержит важные сюжетные повороты, связанные с Баки Барнсом. По сути, это третий фильм о Мстителях под видом сольника Капитана Америки.",
        "image_url": "https://avatars.mds.yandex.net/get-kinopoisk-image/1900788/ad7fbef8-01a5-4133-9185-75fffe044773/orig",
        "required_viewing": "'Первый мститель: Другая война', 'Мстители: Эра Альтрона'."
    } ,
    "blackpanter": {
            "title": "Чёрная пантера",
            "year": 2018,
            "description": "После смерти отца Т'Чалла возвращается в скрытую технологически развитую африканскую страну Ваканда, чтобы занять трон. Его правление оспаривает Эрик Киллмонгер, раскрывающий тёмные секреты прошлого. Фильм отличается уникальной культурной эстетикой, поднимает важные социальные вопросы и представляет вибраниум - самый прочный материал во вселенной.",
        "image_url": "http://images-s.kinorium.com/movie/poster/566968/w1500_45947143.jpg",
        "required_viewing": "'Капитан Америка: Гражданская война' (первое появление Т'Чаллы)."
    } ,
    },
    "characters": {
    "iron_man": {
        "name": "Железный человек (Тони Старк)",
        "description": "Гениальный изобретатель-миллиардер, создавший высокотехнологичный костюм. Основатель Мстителей.",
        "films": [
            "Железный человек (2008)",
            "Железный человек 2 (2010)",
            "Мстители (2012)",
            "Железный человек 3 (2013)",
            "Мстители: Эра Альтрона (2015)",
            "Первый мститель: Противостояние (2016)",
            "Человек-паук: Возвращение домой (2017, камео)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)"
        ],
        "image_url": "https://www.nashe.ru/storage/62731/conversions/zGdBGpsXCq-social.jpg"
    },
    "captain_america": {
        "name": "Капитан Америка (Стив Роджерс)",
        "description": "Суперсолдат из 1940-х, олицетворение чести и справедливости.",
        "films": [
            "Первый мститель (2011)",
            "Мстители (2012)",
            "Первый мститель: Зимний солдат (2014)",
            "Мстители: Эра Альтрона (2015)",
            "Первый мститель: Противостояние (2016)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)"
        ],
        "image_url": "https://m.media-amazon.com/images/M/MV5BMTg2NzQ5OTg2NV5BMl5BanBnXkFtZTgwMjAwMDM0MTE@._V1_FMjpg_UX1000_.jpg"
    },
    "thor": {
        "name": "Тор",
        "description": "Бог грома из Асгарда, наследник престола с молотом Мьёльнир.",
        "films": [
            "Тор (2011)",
            "Мстители (2012)",
            "Тор 2: Царство тьмы (2013)",
            "Мстители: Эра Альтрона (2015)",
            "Тор: Рагнарёк (2017)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)",
            "Тор: Любовь и гром (2022)"
        ],
        "image_url": "hhttps://vkplay.ru/hotbox/content_files/news/2022/05/24/366249d855654da2ac6c47f0babb4be6.jpg"
    },
    "black_widow": {
        "name": "Чёрная вдова (Наташа Романофф)",
        "description": "Бывший русский шпион, эксперт по рукопашному бою.",
        "films": [
            "Железный человек 2 (2010)",
            "Мстители (2012)",
            "Первый мститель: Зимний солдат (2014)",
            "Мстители: Эра Альтрона (2015)",
            "Первый мститель: Противостояние (2016)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)",
            "Чёрная вдова (2021)"
        ],
        "image_url": "https://cdn.shazoo.ru/365718_cw8Dl3CjmI_black_widow_civil_war3.jpg"
    },
    "hulk": {
        "name": "Халк (Брюс Беннер)",
        "description": "Учёный, превращающийся в зелёного монстра при гневе.",
        "films": [
            "Невероятный Халк (2008)",
            "Мстители (2012)",
            "Мстители: Эра Альтрона (2015)",
            "Тор: Рагнарёк (2017)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)",
            "Шан-Чи и легенда десяти колец (2021, камео)"
        ],
        "image_url": "https://avatars.mds.yandex.net/i?id=9d3aa31bc285024b51d19e4806ceda71_l-5865914-images-thumbs&n=13"
    },
    "black_panther": {
        "name": "Чёрная пантера (Т'Чалла)",
        "description": "Король Ваканды с усиленными способностями и продвинутыми технологиями.",
        "films": [
            "Первый мститель: Противостояние (2016)",
            "Чёрная пантера (2018)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)",
            "Чёрная пантера: Ваканда навеки (2022)"
        ],
        "image_url": "https://img.championat.com/s/1350x900/news/big/h/r/sikvel-chyornoj-pantery-proval_1668289921258081471.jpg"
    },
    "doctor_strange": {
        "name": "Доктор Стрэндж",
        "description": "Верховный маг, защищающий Землю от мистических угроз.",
        "films": [
            "Доктор Стрэндж (2016)",
            "Тор: Рагнарёк (2017, камео)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)",
            "Доктор Стрэндж: В мультивселенной безумия (2022)"
        ],
        "image_url": "https://avatars.mds.yandex.net/i?id=c44690b7616a69b331909137b9b7f66a_l-5910330-images-thumbs&n=13"
    },
    "spiderman": {
        "name": "Человек-паук (Питер Паркер)",
        "description": "Подросток с паучьими способностями, балансирующий между учёбой и геройством.",
        "films": [
            "Первый мститель: Противостояние (2016)",
            "Человек-паук: Возвращение домой (2017)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)",
            "Человек-паук: Вдали от дома (2019)",
            "Человек-паук: Нет пути домой (2021)"
        ],
        "image_url": "https://i.playground.ru/e/YnmPw-Ah3lRPnX-GIMrBmw.jpeg"
    },
    "star_lord": {
        "name": "Звёздный Лорд (Питер Квилл)",
        "description": "Лидер Стражей Галактики, наполовину человек, наполовину небожитель.",
        "films": [
            "Стражи Галактики (2014)",
            "Стражи Галактики. Часть 2 (2017)",
            "Мстители: Война бесконечности (2018)",
            "Мстители: Финал (2019)",
            "Тор: Любовь и гром (2022, камео)",
            "Стражи Галактики. Часть 3 (2023)"
        ],
        "image_url": "https://i.playground.ru/p/17Y4B27Tz_5dbKkmJb7ddg.jpeg"
    },
    "loki": {
        "name": "Локи",
        "description": "Бог обмана, брат Тора, антигерой с комплексом неполноценности.",
        "films": [
            "Тор (2011)",
            "Мстители (2012)",
            "Тор 2: Царство тьмы (2013)",
            "Тор: Рагнарёк (2017)",
            "Мстители: Война бесконечности (2018)",
            "Локи (сериал, 2021)",
            "Доктор Стрэндж: В мультивселенной безумия (2022, альтернативная версия)"
        ],
        "image_url": "https://img.championat.com/s/1350x900/news/big/s/b/startovali-syomki-vtorogo-sezona-seriala-loki-s-tomom-hiddlstonom_16545839271434379306.jpg"
    }
    },
    "comics": {
    "infinity_gauntlet": {
        "title": "Перчатка Бесконечности (1991)",
        "description": "Культовая арка, где Танос собирает все Камни Бесконечности, становясь богом. Мстители и космические существа объединяются, чтобы остановить его.",
        "characters": ["Танос", "Мстители", "Серебряный Сёрфер"],
        "events": "Сага Бесконечности",
        "image_url": "https://static.wikia.nocookie.net/marvel/images/e/e1/Infinity_Gauntlet_Vol_1_1.jpg/revision/latest/scale-to-width-down/1200?cb=20200910120209&path-prefix=ru"
    },
    "civil_war": {
        "title": "Гражданская война (2006-2007)",
        "description": "Раскол среди супергероев из-за Акта о регистрации. Железный человек и Капитан Америка возглавляют противоборствующие стороны.",
        "characters": ["Железный человек", "Капитан Америка", "Человек-паук"],
        "events": "Civil War",
        "image_url": "https://avatars.mds.yandex.net/i?id=54207675f78377392d7cd1fe57c828c8_l-4236668-images-thumbs&n=13"
    },
    "secret_wars": {
        "title": "Секретные войны (2015)",
        "description": "Вселенная разрушена, а её обломки собраны в единую планету Бattleworld. Герои из разных реальностей вынуждены сражаться.",
        "characters": ["Мистер Фантастик", "Доктор Дум", "Человек-паук"],
        "events": "Secret Wars",
        "image_url": "https://img.championat.com/i/e/v/1724670547834157046.jpg"
    },
    "dark_phoenix": {
        "title": "Тёмный Феникс (1980)",
        "description": "Джин Грей под влиянием космической силы Феникс становится угрозой для вселенной. Люди Икс сталкиваются с трудным выбором.",
        "characters": ["Джин Грей", "Профессор Икс", "Циклоп"],
        "events": "Dark Phoenix Saga",
        "image_url": "https://cdn.vox-cdn.com/thumbor/SR91utYyNL4YVsTwUuSQGegTMkE=/0x0:2563x1294/1200x0/filters:focal(0x0:2563x1294):no_upscale()/cdn.vox-cdn.com/uploads/chorus_asset/file/16320420/IMG_7FC59DC0D11D_1.jpeg"
    },
    "kravens_last_hunt": {
        "title": "Последняя охота Крейвена (1987)",
        "description": "Крейвен-охотник одержим идеей доказать своё превосходство над Человеком-пауком, доведя свою месть до крайности.",
        "characters": ["Человек-паук", "Крейвен-охотник"],
        "events": "Kraven's Last Hunt",
        "image_url": "https://avatars.mds.yandex.net/i?id=be7db66217a568bb4a2a29d6da721c94_l-5870227-images-thumbs&n=13"
    },
    "house_of_m": {
        "title": "Дом М (2005)",
        "description": "Алая Ведьма изменяет реальность, создавая мир, где мутанты правят человечеством. Люди Икс получают всё, о чём мечтали... но какой ценой?",
        "characters": ["Алая Ведьма", "Магнето", "Люди Икс"],
        "events": "House of M",
        "image_url": "https://static.wikia.nocookie.net/marveldatabase/images/0/09/House_of_M_Vol_1_5_McKone_Variant.jpg/revision/latest/scale-to-width-down/653?cb=20120702223429"
    },
    "age_of_apocalypse": {
        "title": "Эра Апокалипсиса (1995-1996)",
        "description": "Альтернативная реальность, где Профессор Икс был убит, а Магнето возглавил Людей Икс в борьбе против Апокалипсиса.",
        "characters": ["Апокалипсис", "Магнето", "Росомаха"],
        "events": "Age of Apocalypse",
        "image_url": "https://i.pinimg.com/originals/e1/2d/52/e12d52cf8741d15329c0063a60bdc7b7.jpg"
    },
    "planet_hulk": {
        "title": "Планета Халк (2006-2007)",
        "description": "Халк изгнан с Земли и попадает на планету Сакаар, где становится гладиатором и возглавляет революцию.",
        "characters": ["Халк", "Корг", "Мик"],
        "events": "Planet Hulk",
        "image_url": "https://i.pinimg.com/736x/cd/06/fe/cd06fef9b7a86ba8420e2ba6b60a4833.jpg"
    },
    "death_of_wolverine": {
        "title": "Смерть Росомахи (2014)",
        "description": "Росомаха теряет способность к исцелению и отправляется в последнюю миссию, сталкиваясь с врагами прошлого.",
        "characters": ["Росомаха", "Мистер Икс", "Сабилтут"],
        "events": "Death of Wolverine",
        "image_url": "https://avatars.mds.yandex.net/i?id=c664c090edc5431f3e2d544d271d77ac_l-4430658-images-thumbs&n=13"
    },
    "secret_invasion": {
        "title": "Тайное вторжение (2008)",
        "description": "Скруллы годами заменяли ключевых героев и политиков, готовя масштабное вторжение на Землю. Никому нельзя доверять.",
        "characters": ["Капитан Марвел", "Железный человек", "Человек-паук"],
        "events": "Secret Invasion",
        "image_url": "https://cdn.marvel.com/u/prod/marvel/i/mg/2/f0/511c078aa9163/standard_incredible.jpg"
    }
}
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Главное меню"""
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    keyboard = [
        [InlineKeyboardButton("🎬 Фильмы", callback_data='show_movies')],
        [InlineKeyboardButton("🦸 Персонажи", callback_data='show_characters')],
        [InlineKeyboardButton("📚 Комиксы", callback_data='show_comics')],
    ]
    await message.reply_text(
        'Добро пожаловать в энциклопедию Marvel! Выберите категорию:',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик кнопок"""
    query = update.callback_query
    await query.answer()

    try:
        if query.data == 'back':
            await start(update, context)
        elif query.data == 'show_movies':
            await query.message.reply_text("Вы выбрали категорию: 🎬 Фильмы")
            await show_category(query, "movies", "Фильмы")
        elif query.data == 'show_characters':
            await query.message.reply_text("Вы выбрали категорию: 🦸 Персонажи")
            await show_category(query, "characters", "Персонажи")
        elif query.data == 'show_comics':
            await query.message.reply_text("Вы выбрали категорию: 📚 Комиксы")
            await show_category(query, "comics", "Комиксы")
        elif query.data.startswith('movie_'):
            await show_item(query, "movies", query.data[6:])
        elif query.data.startswith('character_'):
            await show_item(query, "characters", query.data[10:])
        elif query.data.startswith('comic_'):
            await show_item(query, "comics", query.data[6:])
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await query.message.reply_text("Произошла ошибка. Попробуйте еще раз.")


async def show_category(query, category, title):
    """Показать меню категории"""
    items = data[category]
    keyboard = []

    for item_id in items:
        item = items[item_id]
        btn_text = item.get('name', item.get('title'))
        callback_data = f"{category[:-1]}_{item_id}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=callback_data)])

    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data='back')])

    await query.message.reply_text(
        text=f"Выберите {title.lower()}:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_item(query, category, item_id):
    """Показать информацию о выбранном элементе с картинкой"""
    item = data[category][item_id]
    text = f"<b>{item.get('name', item.get('title'))}</b>"

    if 'year' in item:
        text += f" ({item['year']})"

    text += f"\n\n{item['description']}"

    # Добавляем список фильмов для персонажей
    if category == 'characters' and 'films' in item and item['films']:
        text += "\n\n<b>Появляется в фильмах:</b>\n"
        text += "\n".join(f"• {film}" for film in item['films'])

    # Добавляем рекомендации для фильмов
    if category == 'movies' and 'required_viewing' in item:
        text += f"\n\n<u>Что посмотреть перед просмотром:</u>\n{item['required_viewing']}"

    # Добавляем информацию о персонажах и событиях для комиксов
    if category == 'comics':
        if 'characters' in item and item['characters']:
            text += f"\n\n<b>Ключевые персонажи:</b>\n{', '.join(item['characters'])}"
        if 'events' in item:
            text += f"\n\n<b>События:</b> {item['events']}"

    # Отправляем картинку с описанием
    await query.message.reply_photo(
        photo=item['image_url'],
        caption=text,
        parse_mode='HTML'
    )

    # Кнопка назад
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data=f'show_{category}')]]
    await query.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def main():
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CallbackQueryHandler(handle_button))

        logger.info("Бот запускается...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")


if __name__ == '__main__':
    main()