# [bog-na-svyazi.ru](bog-na-svyazi.ru/)

Проект был представлен на христианском хакатоне [IT FOR CHRIST](https://www.it4christ.by/) 11-12 мая 2024, и был удостоин приза зрительских симпатий. 

Веб-приложение, оказывающее психологическую и духовную помощь пользователю, подбирая цитату из Евангелия под его запрос.

Бэкенд на Python использует библиотеку [sentence-transformers](https://huggingface.co/sentence-transformers) и дистиллированную модель глубокого обучения [Rubert-tiny2](https://huggingface.co/cointegrated/rubert-tiny2) для семантического поиска стихов из [Евангелия](https://royallib.com/book/avtor_neizvesten/bibliya__noviy_zavet.html), фронтенд написан на JavaScript, CSS и HTML.

Фидбэк пользователей (пальцы вверх и вниз) используются для дообучения (fine-tuning) модели при помощи [ContrastiveLoss](https://www.sbert.net/docs/package_reference/losses.html#contrastiveloss).

---
Код в этом репозитории защищен лицензией [MIT](https://opensource.org/license/mit), изображения -- [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Подробнее [тут](LICENSE.md).
