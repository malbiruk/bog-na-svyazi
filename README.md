# [bog-na-svyazi.ru](bog-na-svyazi.ru/)

Веб-приложение, оказывающее психологическую и духовную помощь пользователю, подбирая цитату из Евангелия под его запрос.

Бэкенд на Python использует библиотеку [sentence-transformers]([url](https://huggingface.co/sentence-transformers)) и дистиллированную модель глубокого обучения [Rubert-tiny2](https://huggingface.co/cointegrated/rubert-tiny2) для семантического поиска стихов из Евангелия, фронтенд написан на JavaScript, CSS и HTML.

Фидбэк пользователей (пальцы вверх и вниз) используются для дообучения (fine-tuning) модели при помощи [ContrastiveLoss]([url](https://www.sbert.net/docs/package_reference/losses.html#contrastiveloss)).
