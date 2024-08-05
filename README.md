# [bog-na-svyazi.ru](https://bog-na-svyazi.ru/)

Проект был представлен на христианском хакатоне [IT FOR CHRIST](https://www.it4christ.by/) 11-12 мая 2024, и был удостоин приза зрительских симпатий. 

Веб-приложение, оказывающее психологическую и духовную помощь пользователю, подбирая цитату из Евангелия под его запрос.

Бэкенд на Python использует библиотеку [sentence-transformers](https://huggingface.co/sentence-transformers) и дистиллированную модель глубокого обучения [Rubert-tiny2](https://huggingface.co/cointegrated/rubert-tiny2) для семантического поиска стихов из [Евангелия](https://royallib.com/book/avtor_neizvesten/bibliya__noviy_zavet.html), фронтенд написан на JavaScript, CSS и HTML.

Все изображения, анимация и дизайн были созданы моим коллегой Дмитрием Медведевым, а я занимался технической реализацией, включая создание анимаций на JavaScript и создание разметок на CSS.

Фидбэк пользователей (пальцы вверх и вниз) используются для дообучения (fine-tuning) модели при помощи [ContrastiveLoss](https://www.sbert.net/docs/package_reference/losses.html#contrastiveloss).

---

The project was presented at the Christian hackathon [IT FOR CHRIST](https://www.it4christ.by/) on May 11-12, 2024, and was awarded the audience prize. 

A web application that provides psychological and spiritual help to the user by matching a Bible quote to their request.

The Python backend uses the [sentence-transformers](https://huggingface.co/sentence-transformers) library and a distilled deep learning model [Rubert-tiny2](https://huggingface.co/cointegrated/rubert-tiny2) to semantically search for verses from the [Bible](https://royallib.com/book/avtor_neizvesten/bibliya__noviy_zavet.html), the frontend is written in JavaScript, CSS, and HTML.

All images, animations, and design were created by my colleague Dmitry Medvedev, while I handled the technical implementation, including making animations in JavaScript and creating layouts via CSS.

User feedback (thumbs up and thumbs down) is used to fine-tune the model using [ContrastiveLoss](https://www.sbert.net/docs/package_reference/losses.html#contrastiveloss).

---
Код в этом репозитории защищен лицензией [MIT](https://opensource.org/license/mit), изображения -- [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Подробнее [тут](LICENSE.md).

The code in this repository is protected under the [MIT](https://opensource.org/license/mit) license, images -- [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Read more [here](LICENSE.md).
