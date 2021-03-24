# highload_server

# Запуск тестов
```
git clone https://github.com/init/http-test-suite.git
cd http-test-suite

docker build -t kolganov-httpd https://github.com/Moxxx1e/highload_server.git
docker run -p 80:80 -v /etc/httpd.conf:/etc/httpd.conf:ro -v /var/www/html:/var/www/html:ro --name kolganov-httpd -t kolganov-httpd

./httptest.py
```

# Результаты нагрузочного тестирования

Сервер, без докера:


![изображение](https://user-images.githubusercontent.com/57684112/112342883-ae963600-8cd3-11eb-985e-56b5c14ea010.png)


Nginx, без докера:


![изображение](https://user-images.githubusercontent.com/57684112/112343048-d1c0e580-8cd3-11eb-981e-0ac7e42fede3.png)
