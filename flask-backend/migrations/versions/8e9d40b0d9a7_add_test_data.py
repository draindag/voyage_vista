"""add test data

Revision ID: 8e9d40b0d9a7
Revises: 7d8d9a2b788f
Create Date: 2024-12-09 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8e9d40b0d9a7'
down_revision = '7d8d9a2b788f'
branch_labels = None
depends_on = None

def upgrade():
    # Включение расширения uuid-ossp
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    op.execute("""
            INSERT INTO public.categories (category_id, category_title, category_description)
            VALUES
            ('e1f966a2-3f45-4a8d-a066-d82f1ea01bca', 'Зимний отдых', 'Горнолыжные курорты, снежные активности, северное сияние'),
            ('b2e679aa-4b5b-42c7-883c-7c5278460056', 'Жаркие страны', 'Пляжный отдых, тропики, островные туры'),
            ('bb22e87c-b7f1-4209-91ef-90a821028284', 'Семейные туры', 'Безопасные и удобные для детей маршруты');
        """)

    op.execute("""
            INSERT INTO public.countries (country_id, country_name, country_description)
            VALUES
            ('4c8f36a6-3c16-4cff-861e-c70a687437cb', 'Кипр', 'Остров с великолепными пляжами и историческими достопримечательностями'),
            ('4b0b9284-b53f-4cd3-ac6b-0731480be76f', 'Турция', 'Страна, известная своей богатой культурой и природными красотами'),
            ('293f2144-d2bc-428b-995b-12e3b9f46262', 'Чехия', 'Сердце Европы с прекрасной архитектурой и историей');
        """)

    op.execute("""
            INSERT INTO public.users (user_id, login, email, password, role)
            VALUES
            ('00394f7c-4634-4ecb-b39f-5e7517322db2', 'user', 'user@example.com', 'scrypt:32768:8:1$XwCqQ6ti6EakAoAn$3aab4d5589ec1c9f9dc05fc3d302643ca99d3bea540c0c3402f247e135b85845c74190d559c78cfa39156e39239a4eabfcf76f9fd858a5e99a4f233008899e9a', 'visitor'), 
            ('9774fb28-69e1-44cb-a71f-9d91a86aefcd', 'moderator', 'moderator@example.com', 'scrypt:32768:8:1$rlchu1Sp4R9N1fYA$3421264b3cdbb6381570d853bb67f32c8eb7ff24ace03b33ccbcf762a5add39d5692105b4ba022415b1db1fb903fb329b7065cefbdcd164d63a8a81e0ad4cd55', 'moderator');
        """)

    op.execute("""
            INSERT INTO public.tours (tour_id, tour_title, tour_description, tour_text, tour_price, tour_start_date, tour_end_date, category_id, country_id)
            VALUES
            -- Семейные туры
            ('e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be', 'Семейный отдых на Кипре', 'Пляжный отдых для всей семьи', 'Насладитесь великолепными пляжами Кипра в этом семейном туре. В программе – игры на пляже, экскурсии и многое другое.', 350.00, '2024-06-01', '2024-06-14', 'bb22e87c-b7f1-4209-91ef-90a821028284', '4c8f36a6-3c16-4cff-861e-c70a687437cb'),
            ('555ba1c3-eb88-40c2-93f4-65b0d20bad4d', 'Семейный тур в Турции', 'Отдых для всей семьи на красивых пляжах', 'Откройте для себя лучшие курорты Турции в этом семейном туре.', 400.00, '2024-07-01', '2024-07-14', 'bb22e87c-b7f1-4209-91ef-90a821028284', '4b0b9284-b53f-4cd3-ac6b-0731480be76f'),
            ('d0972ada-12bb-4f58-88f0-20a0a09bf755', 'Семейные приключения в Чехии', 'Увлекательные экскурсии для детей', 'Исследуйте сказочные замки и природу Чехии с детьми!', 300.00, '2024-08-01', '2024-08-10', 'bb22e87c-b7f1-4209-91ef-90a821028284', '293f2144-d2bc-428b-995b-12e3b9f46262'),

            -- Зимние туры
            ('c3f124f6-7c69-4e25-b021-f77f2881ec59', 'Горнолыжный тур в Чехии', 'Экстрим на снежных склонах', 'Прокатитесь на лучших горнолыжных курортах Чехии с профессиональными инструкторами.', 800.00, '2024-12-10', '2024-12-20', 'e1f966a2-3f45-4a8d-a066-d82f1ea01bca', '293f2144-d2bc-428b-995b-12e3b9f46262'),
            ('0d2b7241-fb36-4154-8fd8-729438486411', 'Горнолыжный отдых в Альпах', 'Снежные приключения в Альпах', 'Лучшие горнолыжные курорты Европы ждут вас!', 950.00, '2025-01-05', '2025-01-12', 'e1f966a2-3f45-4a8d-a066-d82f1ea01bca', '293f2144-d2bc-428b-995b-12e3b9f46262'),
            ('ec71c7a4-e3e5-4c75-8e4f-8b6492aa86ac', 'Зимний тур в Чехии', 'Отдых среди живописных пейзажей', 'Исследуйте очаровательные города и природные красоты Чехии в уютной зимней атмосфере.', 900.00, '2025-02-01', '2025-02-08', 'e1f966a2-3f45-4a8d-a066-d82f1ea01bca', '293f2144-d2bc-428b-995b-12e3b9f46262'),

            -- Жаркие страны
            ('ad6a2380-5af9-415b-b07a-6c88c6421ec1', 'Летний отдых в Турции', 'Отдых на солнечном берегу', 'Отправьтесь на отдых в Турцию, где вас ждут прекрасные пляжи и анимация для всей семьи.', 500.00, '2024-07-01', '2024-07-15', 'b2e679aa-4b5b-42c7-883c-7c5278460056', '4b0b9284-b53f-4cd3-ac6b-0731480be76f'),
            ('af512a04-d437-46f8-90fc-93a6e5c6cfe0', 'Отдых на Кипре', 'Рай для любителей солнца', 'Насладитесь солнцем и морем на Кипре с дружной компанией.', 600.00, '2024-06-15', '2024-06-30', 'b2e679aa-4b5b-42c7-883c-7c5278460056', '4c8f36a6-3c16-4cff-861e-c70a687437cb'),
            ('1c4f3ea9-906d-497a-82b3-2a1ca497c83f', 'Пляжный отдых в Анталии', 'Крутые пляжи и идеальная атмосфера', 'Проведите незабываемый отпуск на южном побережье Турции.', 700.00, '2024-08-01', '2024-08-15', 'b2e679aa-4b5b-42c7-883c-7c5278460056', '4b0b9284-b53f-4cd3-ac6b-0731480be76f');
        """)

    op.execute("""
            INSERT INTO public.fav_tours (tour_id, user_id)
            VALUES
            ('e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be', '00394f7c-4634-4ecb-b39f-5e7517322db2'),
            ('0d2b7241-fb36-4154-8fd8-729438486411', '00394f7c-4634-4ecb-b39f-5e7517322db2'),
            ('1c4f3ea9-906d-497a-82b3-2a1ca497c83f', '00394f7c-4634-4ecb-b39f-5e7517322db2');
        """)

    op.execute("""
            INSERT INTO public.special_offers (offer_id, offer_title, discount_size, end_date)
            VALUES
            ('34255d75-8ff1-467c-8f45-20a4281d4b9a', 'Скидка на летний отдых', 20.0, '2024-05-31'),
            ('de8c0c92-28ff-4669-8975-296c0608f531', 'Горнолыжный отпуск - 15% скидка', 15.0, '2024-12-15'),
            ('1f9fea75-2f23-4570-9bf8-0577cee37567', 'Семейные туры со скидкой', 10.0, '2024-08-31');
        """)

    op.execute("""
                INSERT INTO public.offers_tours (tour_id, offer_id)
                VALUES
                ('ad6a2380-5af9-415b-b07a-6c88c6421ec1', '34255d75-8ff1-467c-8f45-20a4281d4b9a'),  -- Летний отдых в Турции
                ('c3f124f6-7c69-4e25-b021-f77f2881ec59', 'de8c0c92-28ff-4669-8975-296c0608f531'),  -- Горнолыжный тур в Чехии
                ('e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be', '1f9fea75-2f23-4570-9bf8-0577cee37567');  -- Семейный отдых на Кипре
            """)

    op.execute("""
            INSERT INTO public.reviews (review_id, review_text, review_value, author_id, tour_id)
            VALUES
            -- Отзывы для "Семейный отдых на Кипре"
            (uuid_generate_v4(), 'Прекрасный семейный отдых! Много развлечений для детей.', 5, '00394f7c-4634-4ecb-b39f-5e7517322db2', 'e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be'),
            (uuid_generate_v4(), 'Отличный сервис, но цены завышены.', 3, '00394f7c-4634-4ecb-b39f-5e7517322db2', 'e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be'),

            -- Отзывы для "Горнолыжный тур в Чехии"
            (uuid_generate_v4(), 'Лучший опыт лыжного отдыха, рекомендую всем!', 5, '00394f7c-4634-4ecb-b39f-5e7517322db2', 'c3f124f6-7c69-4e25-b021-f77f2881ec59'),
            (uuid_generate_v4(), 'Курорт отличный, но были проблемы с транспортом.', 4, '00394f7c-4634-4ecb-b39f-5e7517322db2', 'c3f124f6-7c69-4e25-b021-f77f2881ec59'),

            -- Отзывы для "Летний отдых в Турции"
            (uuid_generate_v4(), 'Отличный пляж, дети были в восторге!', 4, '00394f7c-4634-4ecb-b39f-5e7517322db2', 'ad6a2380-5af9-415b-b07a-6c88c6421ec1'),
            (uuid_generate_v4(), 'Все было хорошо, но еда могла бы быть лучше.', 3, '00394f7c-4634-4ecb-b39f-5e7517322db2', 'ad6a2380-5af9-415b-b07a-6c88c6421ec1');
        """)

    op.execute("""
                INSERT INTO public.transactions (tour_id, user_id)
                VALUES
                ('ad6a2380-5af9-415b-b07a-6c88c6421ec1', '00394f7c-4634-4ecb-b39f-5e7517322db2'),
                ('c3f124f6-7c69-4e25-b021-f77f2881ec59', '00394f7c-4634-4ecb-b39f-5e7517322db2'),
                ('e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be', '00394f7c-4634-4ecb-b39f-5e7517322db2');
                """)

    op.execute("""
            INSERT INTO public.replies (reply_id, reply_text, author_id, tour_id, parent_reply_id)
            VALUES
            -- Вопросы и ответы для "Семейный отдых на Кипре"
            ('42283e12-f2e8-4a50-b3ec-ccb3b7d754f9', 'Какой пляж лучше для детей?', '00394f7c-4634-4ecb-b39f-5e7517322db2', 'e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be', NULL),
            ('074c8c3b-b252-4122-939b-1f0c68795d0c', 'Лучше всего подходит пляж Fig Tree Bay, он очень безопасный и чистый.', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', 'e3c1e48f-91fa-4c45-9ab5-09cbd2a0c1be', '42283e12-f2e8-4a50-b3ec-ccb3b7d754f9'),

            -- Вопросы и ответы для "Горнолыжный тур в Чехии"
            ('664f9f03-83be-44b3-9068-06d0eaa11241', 'Есть ли вещи, которые стоит взять с собой на горнолыжный курорт?', '00394f7c-4634-4ecb-b39f-5e7517322db2', 'c3f124f6-7c69-4e25-b021-f77f2881ec59', NULL),
            ('1ab632eb-1bd2-4672-a847-a1f9281a4192', 'Не забудьте теплую одежду, шапку и солнцезащитные очки! Это очень важно.', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', 'c3f124f6-7c69-4e25-b021-f77f2881ec59', '664f9f03-83be-44b3-9068-06d0eaa11241'),

            -- Вопросы и ответы для "Летний отдых в Турции"
            ('f79c01c7-5161-4a07-8149-ebe9beee5824', 'Какой отель лучше выбрать для отдыха с детьми?', '00394f7c-4634-4ecb-b39f-5e7517322db2', 'ad6a2380-5af9-415b-b07a-6c88c6421ec1', NULL),
            ('e12ca850-ca94-4967-bca0-88d53d20ce04', 'Попробуйте отель Sungate Port Royal, они отлично справляются с детьми!', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', 'ad6a2380-5af9-415b-b07a-6c88c6421ec1', 'f79c01c7-5161-4a07-8149-ebe9beee5824'),
            
            -- Вопросы и ответы для "Семейный тур в Турции"
            ('88c8f12b-e19f-4e07-ac30-44432b56f821', 'Есть ли в отелях программы для детей?', '00394f7c-4634-4ecb-b39f-5e7517322db2', '555ba1c3-eb88-40c2-93f4-65b0d20bad4d', NULL),
            ('4d4f5024-632c-49f8-856e-5016f070f318', 'Да, многие отели предлагают детские клубы и анимацию!', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', '555ba1c3-eb88-40c2-93f4-65b0d20bad4d', '88c8f12b-e19f-4e07-ac30-44432b56f821'),

            -- Вопросы и ответы для "Семейные приключения в Чехии"
            ('a3f32b3a-fa1e-4d49-bd74-58d8b941b4b0', 'Какие замки можно посетить?', '00394f7c-4634-4ecb-b39f-5e7517322db2', 'd0972ada-12bb-4f58-88f0-20a0a09bf755', NULL),
            ('f66e27d0-ec0a-439f-a1ef-17c38c8e5ded', 'Рекомендую посетить замки Чески Крумлов и Карлштейн! Они очень красивые.', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', 'd0972ada-12bb-4f58-88f0-20a0a09bf755', 'a3f32b3a-fa1e-4d49-bd74-58d8b941b4b0'),

            -- Вопросы и ответы для "Горнолыжный отдых в Альпах"
            ('b5105e1c-bb2e-49eb-8e01-e6db4e7cc367', 'Подходит ли этот тур для начинающих?','00394f7c-4634-4ecb-b39f-5e7517322db2', '0d2b7241-fb36-4154-8fd8-729438486411', NULL),
            ('ce2eca98-259d-4fd9-abf4-db39c7b1d1d9', 'Да, на курортах есть трассы для начинающих и обучение с инструкторами!', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', '0d2b7241-fb36-4154-8fd8-729438486411', 'b5105e1c-bb2e-49eb-8e01-e6db4e7cc367'),

            -- Вопросы и ответы для "Зимний тур в Чехии"
            ('14d7f7e1-03c9-42d5-bb30-b2b5e214d7a3', 'Что можно посмотреть в зимней Чехии?', '00394f7c-4634-4ecb-b39f-5e7517322db2', 'ec71c7a4-e3e5-4c75-8e4f-8b6492aa86ac', NULL),
            ('aa5e2fd1-99ff-4ea8-8b72-5372c23b951b', 'Не пропустите Прагу, её новогодние рынки и ледяные скульптуры!', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', 'ec71c7a4-e3e5-4c75-8e4f-8b6492aa86ac', '14d7f7e1-03c9-42d5-bb30-b2b5e214d7a3'),

            -- Вопросы и ответы для "Отдых на Кипре"
            ('bfc1ca68-6f9d-4fad-b5c7-7c5ed2df8c82', 'Какие экскурсии popular на Кипре?', '00394f7c-4634-4ecb-b39f-5e7517322db2', 'af512a04-d437-46f8-90fc-93a6e5c6cfe0', NULL),
            ('ed17b5d8-cf82-4364-9030-d83aca3fbebb', 'Попробуйте экскурсии на древние руины или винодельни Кипра!', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', 'af512a04-d437-46f8-90fc-93a6e5c6cfe0', 'bfc1ca68-6f9d-4fad-b5c7-7c5ed2df8c82'),

            -- Вопросы и ответы для "Пляжный отдых в Анталье"
            ('73a303e0-70c5-4a70-b8e5-e8e001858535', 'Какие пляжи самые лучшие?', '00394f7c-4634-4ecb-b39f-5e7517322db2', '1c4f3ea9-906d-497a-82b3-2a1ca497c83f', NULL),
            ('7f469cb0-d4f2-4554-89f3-8aada5cb3827', 'Пляжи Клеопатры и Лара считаются одними из лучших в Анталье!', '9774fb28-69e1-44cb-a71f-9d91a86aefcd', '1c4f3ea9-906d-497a-82b3-2a1ca497c83f', '73a303e0-70c5-4a70-b8e5-e8e001858535');
        """)

def downgrade():
    op.execute("TRUNCATE TABLE public.tours RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.countries RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.categories RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.fav_tours RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.special_offers RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.offers_tours RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.reviews RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.transactions RESTART IDENTITY CASCADE;")
    op.execute("TRUNCATE TABLE public.replies RESTART IDENTITY CASCADE;")
    op.execute("DELETE FROM public.users WHERE login IN ('user', 'moderator');")

    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\";")